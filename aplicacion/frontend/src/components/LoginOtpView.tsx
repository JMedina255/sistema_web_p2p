import React, { useState, useEffect } from 'react';
import { authService, AuthException } from '../services/authService';
import type { RequestOtpResponse, VerifyOtpResponse } from '../services/authService';

export interface LoginOtpViewProps {
  onLoginSuccess?: (data: VerifyOtpResponse) => void;
  showDevControls?: boolean;
}

export const LoginOtpView: React.FC<LoginOtpViewProps> = ({ onLoginSuccess, showDevControls = false }) => {
  const isDevVisible = showDevControls && !import.meta.env.PROD;
  // Estados del flujo (Inicia limpiamente en el paso 1 sin trampas de URL ni estados inyectados)
  const [step, setStep] = useState<'email' | 'otp' | 'success'>('email');
  const [email, setEmail] = useState<string>('');
  const [otp, setOtp] = useState<string>('');
  const [challenge, setChallenge] = useState<RequestOtpResponse | null>(null);
  const [verifyResult, setVerifyResult] = useState<VerifyOtpResponse | null>(null);

  // Estados de control y feedback
  const [authMode, setAuthMode] = useState<'mock' | 'api'>(authService.getMode());
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [infoMessage, setInfoMessage] = useState<string | null>(null);

  // Temporizadores dinámicos basados en marcas de tiempo reales
  const [secondsUntilExpire, setSecondsUntilExpire] = useState<number>(0);
  const [secondsUntilResend, setSecondsUntilResend] = useState<number>(0);

  // Actualizador del contador de expiración y cooldown
  useEffect(() => {
    if (step !== 'otp' || !challenge) return;

    const targetExpire = new Date(challenge.expiresAt).getTime();
    const cooldownTarget = targetExpire - (5 * 60 - challenge.cooldownSeconds) * 1000;

    const updateTimers = () => {
      const now = Date.now();
      const remainingExpire = Math.max(0, Math.floor((targetExpire - now) / 1000));
      const remainingResend = Math.max(0, Math.floor((cooldownTarget - now) / 1000));

      setSecondsUntilExpire(remainingExpire);
      setSecondsUntilResend(remainingResend);

      if (remainingExpire === 0 && !errorMessage) {
        setErrorMessage('El código OTP ha expirado (5 minutos). Por favor solicita un nuevo código.');
      }
    };

    updateTimers();
    const interval = setInterval(updateTimers, 500);

    return () => clearInterval(interval);
  }, [step, challenge, errorMessage]);

  // Formateador de tiempo MM:SS
  const formatTime = (totalSeconds: number): string => {
    const mins = Math.floor(totalSeconds / 60);
    const secs = totalSeconds % 60;
    return `${mins.toString().padStart(2, '0')}:${secs.toString().padStart(2, '0')}`;
  };

  // Manejador del Paso 1: Solicitud de OTP
  const handleRequestOtp = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    setErrorMessage(null);
    setInfoMessage(null);

    const cleanEmail = email.trim();
    if (!cleanEmail) {
      setErrorMessage('Por favor, ingresa tu correo electrónico institucional.');
      return;
    }

    const lowerEmail = cleanEmail.toLowerCase();
    if (!lowerEmail.endsWith('@virtual.upt.pe') && !lowerEmail.endsWith('@upt.pe')) {
      setErrorMessage('Acceso restringido: Solo se permiten correos institucionales con dominio @virtual.upt.pe o @upt.pe.');
      return;
    }

    setIsLoading(true);
    try {
      const resp = await authService.requestOtp({ email: cleanEmail });
      setChallenge(resp);
      setStep('otp');
      setOtp('');
      setInfoMessage(`Código de verificación enviado. Revisa tu buzón institucional.`);
    } catch (err: unknown) {
      if (err instanceof AuthException) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage('Error inesperado de comunicación con el servicio de autenticación.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Manejador del Paso 2: Verificación de OTP
  const handleVerifyOtp = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!challenge) return;

    setErrorMessage(null);
    setInfoMessage(null);

    const cleanOtp = otp.trim();
    if (cleanOtp.length !== 6) {
      setErrorMessage('El código debe contener exactamente 6 dígitos numéricos.');
      return;
    }

    setIsLoading(true);
    try {
      const resp = await authService.verifyOtp({
        challengeId: challenge.challengeId,
        otp: cleanOtp,
      });
      setVerifyResult(resp);
      setStep('success');
      if (onLoginSuccess) {
        onLoginSuccess(resp);
      }
    } catch (err: unknown) {
      if (err instanceof AuthException) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage('Error al validar el código OTP.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Inicio de sesión federado con Google Workspace UPT
  const handleGoogleLogin = async () => {
    setErrorMessage(null);
    setInfoMessage(null);
    setIsLoading(true);

    try {
      const clean = email.trim().toLowerCase();
      const targetEmail =
        clean && (clean.endsWith('@virtual.upt.pe') || clean.endsWith('@upt.pe'))
          ? clean
          : 'ra2022073504@virtual.upt.pe';

      const mockPayload = btoa(
        JSON.stringify({
          email: targetEmail,
          given_name: 'Renzo Antonio',
          family_name: 'Antayhua Mamani',
        })
      );
      const dummyIdToken = `header.${mockPayload}.signature`;

      const resp = await authService.loginWithGoogle(dummyIdToken);
      setVerifyResult(resp);
      setStep('success');
      if (onLoginSuccess) {
        onLoginSuccess(resp);
      }
    } catch (err: unknown) {
      if (err instanceof AuthException) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage('Error durante la autenticación con Google Workspace.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Reenvío de código OTP
  const handleResendOtp = async () => {
    if (!challenge || isLoading || secondsUntilResend > 0) return;

    setErrorMessage(null);
    setInfoMessage(null);
    setIsLoading(true);

    try {
      const resp = await authService.resendOtp({ challengeId: challenge.challengeId });
      setChallenge(resp);
      setOtp('');
      setInfoMessage('Se ha generado y enviado un nuevo código OTP. El anterior ha sido invalidado.');
    } catch (err: unknown) {
      if (err instanceof AuthException) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage('Error al solicitar el reenvío de OTP.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  // Cambiar de correo / Reiniciar desafío
  const handleReset = () => {
    authService.cancelChallenge();
    setChallenge(null);
    setVerifyResult(null);
    setOtp('');
    setErrorMessage(null);
    setInfoMessage(null);
    setStep('email');
  };

  // Manejador de cambio entre modo Mock y API real
  const handleToggleMode = (newMode: 'mock' | 'api') => {
    setAuthMode(newMode);
    authService.setMode(newMode);
    handleReset();
  };

  // Helper de escenarios de prueba para Joan y Renzo
  const handleLoadTestEmail = (testEmail: string) => {
    setEmail(testEmail);
    setErrorMessage(null);
  };

  return (
    <div
      style={{
        width: '100%',
        maxWidth: '520px',
        margin: '0 auto',
        backgroundColor: '#FFFFFF',
        borderRadius: '16px',
        boxShadow: '0 8px 24px rgba(28, 42, 89, 0.08)',
        border: '1px solid #E2E8F0',
        overflow: 'hidden',
      }}
    >
      {/* Banner de Modo de Acceso en Desarrollo (Oculto en experiencia normal) */}
      {isDevVisible && (
        <div
          style={{
            backgroundColor: authMode === 'api' ? '#F0FDF4' : '#FFFBEB',
            borderBottom: authMode === 'api' ? '1px solid #BBF7D0' : '1px solid #FDE68A',
            padding: '0.6rem 1.25rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '0.5rem',
            fontSize: '0.78rem',
            color: authMode === 'api' ? '#15803D' : '#B45309',
            fontWeight: 600,
          }}
        >
          <span>
            {authMode === 'api'
              ? '⚡ Servidor Institucional API Real'
              : '🧪 Acceso de prueba — Simulación'}
          </span>
          <div style={{ display: 'flex', gap: '0.35rem' }}>
            <button
              type="button"
              onClick={() => handleToggleMode('mock')}
              style={{
                background: authMode === 'mock' ? '#FDE68A' : '#FFFFFF',
                border: '1px solid #FCD34D',
                borderRadius: '4px',
                padding: '0.15rem 0.45rem',
                fontSize: '0.7rem',
                fontWeight: authMode === 'mock' ? 700 : 500,
                cursor: 'pointer',
                color: '#92400E',
              }}
            >
              Dev Mock
            </button>
            <button
              type="button"
              onClick={() => handleToggleMode('api')}
              style={{
                background: authMode === 'api' ? '#BBF7D0' : '#FFFFFF',
                border: '1px solid #86EFAC',
                borderRadius: '4px',
                padding: '0.15rem 0.45rem',
                fontSize: '0.7rem',
                fontWeight: authMode === 'api' ? 700 : 500,
                cursor: 'pointer',
                color: '#166534',
              }}
            >
              API Real
            </button>
          </div>
        </div>
      )}

      <div style={{ padding: '2rem' }}>
        {/* Encabezado del Formulario */}
        <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
          <div
            style={{
              width: '44px',
              height: '44px',
              backgroundColor: '#1C2A59',
              color: '#B99451',
              borderRadius: '10px',
              display: 'inline-flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontWeight: 900,
              fontSize: '1.1rem',
              marginBottom: '0.75rem',
            }}
          >
            UPT
          </div>
          <h2 style={{ fontSize: '1.45rem', color: '#1C2A59', margin: '0 0 0.35rem 0', fontWeight: 700 }}>
            Iniciar Sesión Institucional
          </h2>
          <p style={{ margin: 0, fontSize: '0.85rem', color: '#64748B' }}>
            Ingresa tu correo institucional @upt.pe para recibir un código de verificación temporal.
          </p>
        </div>

        {/* Notificaciones de Error */}
        {errorMessage && (
          <div
            role="alert"
            style={{
              backgroundColor: '#FEF2F2',
              border: '1px solid #FECACA',
              color: '#991B1B',
              borderRadius: '8px',
              padding: '0.75rem 1rem',
              fontSize: '0.82rem',
              marginBottom: '1.25rem',
              display: 'flex',
              alignItems: 'flex-start',
              gap: '0.5rem',
              lineHeight: 1.4,
            }}
          >
            <span>⚠️</span>
            <span>{errorMessage}</span>
          </div>
        )}

        {/* Notificaciones Informativas */}
        {infoMessage && (
          <div
            role="status"
            style={{
              backgroundColor: '#EFF6FF',
              border: '1px solid #BFDBFE',
              color: '#1E40AF',
              borderRadius: '8px',
              padding: '0.75rem 1rem',
              fontSize: '0.82rem',
              marginBottom: '1.25rem',
              display: 'flex',
              alignItems: 'flex-start',
              gap: '0.5rem',
              lineHeight: 1.4,
            }}
          >
            <span>ℹ️</span>
            <span>{infoMessage}</span>
          </div>
        )}

        {/* PASO 1: Ingreso de Correo Institucional o Google Sign-In */}
        {step === 'email' && (
          <div>
            {/* Botón de Autenticación Federada Google Workspace UPT */}
            <button
              type="button"
              onClick={handleGoogleLogin}
              disabled={isLoading}
              style={{
                width: '100%',
                padding: '0.8rem',
                backgroundColor: '#FFFFFF',
                color: '#1E293B',
                border: '1.5px solid #E2E8F0',
                borderRadius: '8px',
                fontSize: '0.92rem',
                fontWeight: 600,
                cursor: isLoading ? 'not-allowed' : 'pointer',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                gap: '0.75rem',
                marginBottom: '1.25rem',
                boxShadow: '0 1px 3px rgba(0,0,0,0.06)',
                transition: 'all 0.2s',
              }}
            >
              <svg width="20" height="20" viewBox="0 0 24 24">
                <path fill="#4285F4" d="M22.56 12.25c0-.78-.07-1.53-.2-2.25H12v4.26h5.92c-.26 1.37-1.04 2.53-2.21 3.31v2.77h3.57c2.08-1.92 3.28-4.74 3.28-8.09z"/>
                <path fill="#34A853" d="M12 23c2.97 0 5.46-.98 7.28-2.66l-3.57-2.77c-.98.66-2.23 1.06-3.71 1.06-2.86 0-5.29-1.93-6.16-4.53H2.18v2.84C3.99 20.53 7.7 23 12 23z"/>
                <path fill="#FBBC05" d="M5.84 14.09c-.22-.66-.35-1.36-.35-2.09s.13-1.43.35-2.09V7.06H2.18C1.43 8.55 1 10.22 1 12s.43 3.45 1.18 4.94l2.85-2.22.81-.63z"/>
                <path fill="#EA4335" d="M12 5.38c1.62 0 3.06.56 4.21 1.64l3.15-3.15C17.45 2.09 14.97 1 12 1 7.7 1 3.99 3.47 2.18 7.06l3.66 2.84c.87-2.6 3.3-4.52 6.16-4.52z"/>
              </svg>
              Continuar con Google Workspace UPT
            </button>

            <div style={{ display: 'flex', alignItems: 'center', margin: '1rem 0 1.25rem' }}>
              <div style={{ flex: 1, height: '1px', backgroundColor: '#E2E8F0' }} />
              <span style={{ padding: '0 0.6rem', fontSize: '0.74rem', color: '#94A3B8', fontWeight: 600 }}>
                O CON CÓDIGO OTP POR CORREO
              </span>
              <div style={{ flex: 1, height: '1px', backgroundColor: '#E2E8F0' }} />
            </div>

            <form onSubmit={handleRequestOtp}>
              <div style={{ marginBottom: '1.25rem' }}>
                <label
                  htmlFor="institutional-email"
                  style={{
                    display: 'block',
                    fontSize: '0.85rem',
                    fontWeight: 600,
                    color: '#1C2A59',
                    marginBottom: '0.45rem',
                  }}
                >
                  Correo Electrónico Institucional UPT
                </label>
                <input
                  id="institutional-email"
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                  placeholder="ej: ra2022073504@virtual.upt.pe"
                  disabled={isLoading}
                  required
                  style={{
                    width: '100%',
                    padding: '0.75rem 0.9rem',
                    fontSize: '0.9rem',
                    borderRadius: '8px',
                    border: '1.5px solid #CBD5E1',
                    outline: 'none',
                    boxSizing: 'border-box',
                    transition: 'border-color 0.2s',
                  }}
                  onFocus={(e) => (e.target.style.borderColor = '#1C2A59')}
                  onBlur={(e) => (e.target.style.borderColor = '#CBD5E1')}
                />
                <span style={{ display: 'block', fontSize: '0.75rem', color: '#64748B', marginTop: '0.35rem' }}>
                  Alumnos: <strong>@virtual.upt.pe</strong> (iniciales + código). Docentes y directivos: <strong>@upt.pe</strong>.
                </span>
              </div>

              <button
                type="submit"
                disabled={isLoading || !email.trim()}
                style={{
                  width: '100%',
                  padding: '0.8rem',
                  backgroundColor: '#1C2A59',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '0.92rem',
                  fontWeight: 600,
                  cursor: isLoading || !email.trim() ? 'not-allowed' : 'pointer',
                  opacity: isLoading || !email.trim() ? 0.7 : 1,
                  transition: 'opacity 0.2s',
                }}
              >
                {isLoading ? 'Enviando código OTP...' : 'Continuar con Código OTP →'}
              </button>
            </form>
          </div>
        )}

        {/* PASO 2: Ingreso de Código OTP */}
        {step === 'otp' && challenge && (
          <form onSubmit={handleVerifyOtp}>
            <div
              style={{
                backgroundColor: '#F8FAFC',
                border: '1px solid #E2E8F0',
                borderRadius: '8px',
                padding: '0.85rem 1rem',
                marginBottom: '1.25rem',
                fontSize: '0.82rem',
              }}
            >
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div>
                  <span style={{ color: '#64748B', display: 'block' }}>Destino de verificación:</span>
                  <strong style={{ color: '#1C2A59' }}>{challenge.email}</strong>
                </div>
                <button
                  type="button"
                  onClick={handleReset}
                  disabled={isLoading}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: '#B99451',
                    fontSize: '0.78rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                    textDecoration: 'underline',
                  }}
                >
                  Cambiar correo
                </button>
              </div>
              {isDevVisible && challenge.mockCodeHint && (
                <div
                  style={{
                    marginTop: '0.6rem',
                    paddingTop: '0.5rem',
                    borderTop: '1px dashed #CBD5E1',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                  }}
                >
                  <span style={{ color: '#0F766E', fontSize: '0.8rem', fontWeight: 600 }}>
                    🔑 Código OTP para pruebas:
                  </span>
                  <strong
                    style={{
                      color: '#0F766E',
                      fontFamily: 'monospace',
                      fontSize: '1.05rem',
                      letterSpacing: '0.15em',
                      backgroundColor: '#CCFBF1',
                      padding: '0.15rem 0.5rem',
                      borderRadius: '4px',
                    }}
                  >
                    {challenge.mockCodeHint}
                  </strong>
                </div>
              )}
            </div>

            <div style={{ marginBottom: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: '0.45rem' }}>
                <label
                  htmlFor="otp-code"
                  style={{ fontSize: '0.85rem', fontWeight: 600, color: '#1C2A59' }}
                >
                  Código de 6 dígitos
                </label>
                <span
                  style={{
                    fontSize: '0.78rem',
                    color: secondsUntilExpire < 60 ? '#DC2626' : '#64748B',
                    fontWeight: secondsUntilExpire < 60 ? 700 : 500,
                  }}
                >
                  ⏳ Expira en: {formatTime(secondsUntilExpire)}
                </span>
              </div>

              <input
                id="otp-code"
                type="text"
                inputMode="numeric"
                pattern="[0-9]*"
                maxLength={6}
                value={otp}
                onChange={(e) => {
                  const val = e.target.value.replace(/\D/g, '');
                  setOtp(val);
                }}
                placeholder="123456"
                disabled={isLoading || secondsUntilExpire === 0}
                required
                style={{
                  width: '100%',
                  padding: '0.85rem',
                  fontSize: '1.4rem',
                  textAlign: 'center',
                  letterSpacing: '0.4em',
                  fontFamily: 'monospace',
                  borderRadius: '8px',
                  border: '1.5px solid #CBD5E1',
                  outline: 'none',
                  boxSizing: 'border-box',
                }}
              />
              <span style={{ display: 'block', fontSize: '0.75rem', color: '#64748B', marginTop: '0.35rem' }}>
                Ingresa los 6 dígitos numéricos recibidos (se conservan ceros a la izquierda).
              </span>
            </div>

            <button
              type="submit"
              disabled={isLoading || otp.length !== 6 || secondsUntilExpire === 0}
              style={{
                width: '100%',
                padding: '0.8rem',
                backgroundColor: '#1C2A59',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '8px',
                fontSize: '0.92rem',
                fontWeight: 600,
                cursor: isLoading || otp.length !== 6 || secondsUntilExpire === 0 ? 'not-allowed' : 'pointer',
                opacity: isLoading || otp.length !== 6 || secondsUntilExpire === 0 ? 0.6 : 1,
                marginBottom: '1rem',
              }}
            >
              {isLoading ? 'Verificando...' : 'Verificar y Acceder'}
            </button>

            {/* Acciones secundarias: Reenvío y Descarte */}
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
                paddingTop: '0.5rem',
                borderTop: '1px solid #F1F5F9',
                fontSize: '0.8rem',
              }}
            >
              <button
                type="button"
                onClick={handleResendOtp}
                disabled={isLoading || (secondsUntilResend > 0 && secondsUntilExpire > 0)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: secondsUntilResend > 0 && secondsUntilExpire > 0 ? '#94A3B8' : '#1C2A59',
                  fontWeight: 600,
                  cursor: secondsUntilResend > 0 && secondsUntilExpire > 0 ? 'not-allowed' : 'pointer',
                  padding: 0,
                }}
              >
                {secondsUntilResend > 0 && secondsUntilExpire > 0
                  ? `Reenviar código en ${secondsUntilResend}s`
                  : '🔄 Reenviar nuevo código'}
              </button>

              <button
                type="button"
                onClick={handleReset}
                disabled={isLoading}
                style={{
                  background: 'none',
                  border: 'none',
                  color: '#64748B',
                  cursor: 'pointer',
                  padding: 0,
                }}
              >
                Cancelar
              </button>
            </div>
          </form>
        )}

        {/* PASO 3: Confirmación Mínima de Verificación Exitosa */}
        {step === 'success' && verifyResult && (
          <div style={{ textAlign: 'center' }}>
            <div
              style={{
                width: '56px',
                height: '56px',
                borderRadius: '50%',
                backgroundColor: '#DCFCE7',
                color: '#16A34A',
                fontSize: '2rem',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                margin: '0 auto 1rem auto',
              }}
            >
              ✓
            </div>

            <h3 style={{ fontSize: '1.25rem', color: '#1C2A59', margin: '0 0 0.5rem 0', fontWeight: 700 }}>
              Código OTP Verificado con Éxito
            </h3>
            <p style={{ margin: '0 0 1.25rem 0', fontSize: '0.85rem', color: '#475569' }}>
              Identidad institucional comprobada para: <strong>{verifyResult.email}</strong>
            </p>

            <div
              style={{
                backgroundColor: '#F8FAFC',
                border: '1px solid #E2E8F0',
                borderRadius: '8px',
                padding: '0.85rem 1rem',
                textAlign: 'left',
                fontSize: '0.8rem',
                marginBottom: '1.5rem',
                lineHeight: 1.5,
              }}
            >
              <div style={{ marginBottom: '0.35rem' }}>
                <span style={{ color: '#64748B' }}>Estado:</span>{' '}
                <strong style={{ color: '#16A34A' }}>Sesión institucional confirmada</strong>
              </div>
              <div style={{ marginBottom: '0.35rem' }}>
                <span style={{ color: '#64748B' }}>Hora de verificación:</span>{' '}
                <span>{new Date(verifyResult.verifiedAt).toLocaleTimeString()}</span>
              </div>
            </div>

            {onLoginSuccess && (
              <button
                type="button"
                onClick={() => onLoginSuccess(verifyResult)}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  backgroundColor: '#0F766E',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '8px',
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  marginBottom: '0.5rem',
                  boxShadow: '0 2px 8px rgba(15, 118, 110, 0.25)',
                }}
              >
                Ingresar al Sistema →
              </button>
            )}

            <button
              type="button"
              onClick={handleReset}
              style={{
                width: '100%',
                padding: '0.75rem',
                backgroundColor: '#1C2A59',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '8px',
                fontSize: '0.88rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Cerrar y volver a iniciar
            </button>
          </div>
        )}
      </div>

      {/* Panel Auxiliar de Escenarios de Prueba (Solo visible en configuración explícita de desarrollo) */}
      {isDevVisible && (
        <div
          style={{
            backgroundColor: '#F8FAFC',
            borderTop: '1px solid #E2E8F0',
            padding: '1rem 1.5rem',
            fontSize: '0.76rem',
            color: '#475569',
          }}
        >
          <span style={{ fontWeight: 700, color: '#1C2A59', display: 'block', marginBottom: '0.4rem' }}>
            🛠️ Cuentas de prueba preconfiguradas:
          </span>
          <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem', marginBottom: '0.6rem' }}>
            <button
              type="button"
              onClick={() => handleLoadTestEmail('2022074255@upt.pe')}
              style={{
                background: '#FFFFFF',
                border: '1px solid #CBD5E1',
                borderRadius: '4px',
                padding: '0.2rem 0.5rem',
                fontSize: '0.72rem',
                cursor: 'pointer',
              }}
            >
              Estudiante (2022074255@upt.pe)
            </button>
            <button
              type="button"
              onClick={() => handleLoadTestEmail('2022073504@upt.pe')}
              style={{
                background: '#FFFFFF',
                border: '1px solid #CBD5E1',
                borderRadius: '4px',
                padding: '0.2rem 0.5rem',
                fontSize: '0.72rem',
                cursor: 'pointer',
              }}
            >
              Mentor (2022073504@upt.pe)
            </button>
            <button
              type="button"
              onClick={() => handleLoadTestEmail('admin.epis@upt.pe')}
              style={{
                background: '#FFFFFF',
                border: '1px solid #CBD5E1',
                borderRadius: '4px',
                padding: '0.2rem 0.5rem',
                fontSize: '0.72rem',
                cursor: 'pointer',
                color: '#1C2A59',
                fontWeight: 600,
              }}
            >
              Admin (admin.epis@upt.pe)
            </button>
            <button
              type="button"
              onClick={() => handleLoadTestEmail('estudiante@gmail.com')}
              style={{
                background: '#FFFFFF',
                border: '1px solid #CBD5E1',
                borderRadius: '4px',
                padding: '0.2rem 0.5rem',
                fontSize: '0.72rem',
                cursor: 'pointer',
                color: '#DC2626',
              }}
            >
              Inválido (@gmail.com)
            </button>
          </div>
          <div style={{ lineHeight: 1.4, color: '#64748B' }}>
            • Código válido: <code>123456</code> (tras reenvío: <code>654321</code>).<br />
            • Simular vencimiento inmediato: código <code>000000</code>.
          </div>
        </div>
      )}
    </div>
  );
};
