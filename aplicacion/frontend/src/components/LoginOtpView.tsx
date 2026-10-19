import React, { useState, useEffect } from 'react';
import { authService, AuthException } from '../services/authService';
import type { RequestOtpResponse, VerifyOtpResponse } from '../services/authService';

export const LoginOtpView: React.FC = () => {
  // Estados del flujo
  const [step, setStep] = useState<'email' | 'otp' | 'success'>('email');
  const [email, setEmail] = useState<string>('');
  const [otp, setOtp] = useState<string>('');
  const [challenge, setChallenge] = useState<RequestOtpResponse | null>(null);
  const [verifyResult, setVerifyResult] = useState<VerifyOtpResponse | null>(null);

  // Estados de control y feedback
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

    if (!cleanEmail.toLowerCase().endsWith('@upt.pe')) {
      setErrorMessage('Acceso restringido: Solo se permiten correos institucionales con dominio @upt.pe (CUS01 / RF01).');
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

  // Helper de escenarios de prueba para Joan
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
      {/* Banner de Modo de Acceso en Desarrollo */}
      <div
        style={{
          backgroundColor: '#FFFBEB',
          borderBottom: '1px solid #FDE68A',
          padding: '0.6rem 1.25rem',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'space-between',
          fontSize: '0.78rem',
          color: '#B45309',
          fontWeight: 600,
        }}
      >
        <span>🧪 Acceso de prueba — Simulación (Hito 3 · T-02)</span>
        <span
          style={{
            background: '#FDE68A',
            padding: '0.15rem 0.45rem',
            borderRadius: '4px',
            fontSize: '0.7rem',
          }}
        >
          Dev Mock
        </span>
      </div>

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
            Acceso seguro con 2FA mediante código OTP temporal (CUS01 / RNF01)
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

        {/* PASO 1: Ingreso de Correo Institucional */}
        {step === 'email' && (
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
                Correo Electrónico Institucional (@upt.pe)
              </label>
              <input
                id="institutional-email"
                type="email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                placeholder="ejemplo@upt.pe"
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
                Solo se admiten direcciones con dominio corporativo oficial <strong>@upt.pe</strong>.
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
                <span style={{ color: '#64748B' }}>Modo de verificación:</span>{' '}
                <strong style={{ color: '#B99451' }}>
                  {verifyResult.mode === 'mock' ? 'Acceso de prueba — Simulación (T-02)' : 'API Backend Real'}
                </strong>
              </div>
              <div style={{ marginBottom: '0.35rem' }}>
                <span style={{ color: '#64748B' }}>Marca de tiempo:</span>{' '}
                <span>{new Date(verifyResult.verifiedAt).toLocaleTimeString()}</span>
              </div>
              <div style={{ fontSize: '0.75rem', color: '#64748B', marginTop: '0.5rem', borderTop: '1px solid #E2E8F0', paddingTop: '0.4rem' }}>
                📌 <em>Alcance delimitado:</em> El consentimiento legal informado (Ley 29733, T-04/T-05) y la emisión definitiva de tokens JWT institucionales se incorporan en los siguientes sprints.
              </div>
            </div>

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
              Probar Otro Acceso / Reiniciar
            </button>
          </div>
        )}
      </div>

      {/* Panel Auxiliar de Escenarios de Prueba (Solo visible en Modo Mock / Dev) */}
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
          🛠️ Escenarios de Prueba Reproducibles (Joan - T-02):
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
            Joan (2022074255@upt.pe)
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
            Renzo (2022073504@upt.pe)
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
    </div>
  );
};
