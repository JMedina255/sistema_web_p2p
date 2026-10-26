import React, { useState, useEffect } from 'react';
import { consentService } from '../services/consentService';
import type { ConsentStatus } from '../services/consentService';

export interface ConsentModalViewProps {
  userEmail?: string;
  onConsentAccepted?: (consentedAt: string) => void;
  onConsentRejected?: () => void;
  isModal?: boolean;
}

export const ConsentModalView: React.FC<ConsentModalViewProps> = ({
  userEmail = '2022074255@upt.pe',
  onConsentAccepted,
  onConsentRejected,
  isModal = false,
}) => {
  const [email, setEmail] = useState<string>(userEmail);
  const [status, setStatus] = useState<ConsentStatus | null>(null);
  const [isChecked, setIsChecked] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);
  const [message, setMessage] = useState<{ text: string; type: 'success' | 'error' | 'info' } | null>(null);

  useEffect(() => {
    setEmail(userEmail);
  }, [userEmail]);

  useEffect(() => {
    let isMounted = true;
    const checkStatus = async () => {
      setIsLoading(true);
      try {
        const s = await consentService.getConsentStatus(email);
        if (isMounted) {
          setStatus(s);
          if (s.hasConsented) {
            setIsChecked(true);
          }
        }
      } catch {
        // Fallback silencioso
      } finally {
        if (isMounted) setIsLoading(false);
      }
    };
    if (email) {
      checkStatus();
    }
    return () => {
      isMounted = false;
    };
  }, [email]);

  const handleAccept = async () => {
    if (!isChecked) {
      setMessage({
        text: 'Debe marcar la casilla de conformidad expresa para continuar (Ley N° 29733).',
        type: 'error',
      });
      return;
    }

    setIsLoading(true);
    setMessage(null);
    try {
      const res = await consentService.acceptConsent(email);
      const s = await consentService.getConsentStatus(email);
      setStatus(s);
      setMessage({
        text: 'Consentimiento registrado exitosamente. Tu acceso ha sido formalizado.',
        type: 'success',
      });
      if (onConsentAccepted) {
        onConsentAccepted(res.consentedAt);
      }
    } catch (err: unknown) {
      setMessage({
        text: err instanceof Error ? err.message : 'Error al registrar consentimiento digital.',
        type: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  const handleReject = async () => {
    setIsLoading(true);
    setMessage(null);
    try {
      await consentService.revokeConsent(email);
      const s = await consentService.getConsentStatus(email);
      setStatus(s);
      setIsChecked(false);
      setMessage({
        text: 'Has rechazado el tratamiento de datos. El acceso a la plataforma ha sido bloqueado preventivamente (RN-02).',
        type: 'info',
      });
      if (onConsentRejected) {
        onConsentRejected();
      }
    } catch (err: unknown) {
      setMessage({
        text: err instanceof Error ? err.message : 'Error al revocar consentimiento.',
        type: 'error',
      });
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div
      style={{
        width: '100%',
        maxWidth: isModal ? '640px' : '760px',
        margin: '0 auto',
        backgroundColor: '#FFFFFF',
        borderRadius: '16px',
        boxShadow: isModal
          ? '0 20px 25px -5px rgba(0, 0, 0, 0.2), 0 10px 10px -5px rgba(0, 0, 0, 0.1)'
          : '0 8px 24px rgba(28, 42, 89, 0.08)',
        border: '1px solid #E2E8F0',
        overflow: 'hidden',
      }}
    >
      {/* Cabecera Institucional */}
      <div
        style={{
          backgroundColor: '#1C2A59',
          color: '#FFFFFF',
          padding: '1.25rem 1.75rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '0.75rem',
          borderBottom: '3px solid #B99451',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          <div
            style={{
              backgroundColor: '#B99451',
              color: '#FFFFFF',
              fontWeight: 900,
              fontSize: '1rem',
              padding: '0.35rem 0.65rem',
              borderRadius: '8px',
            }}
          >
            ⚖️
          </div>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.15rem', fontWeight: 800 }}>
              Consentimiento Informado Digital
            </h2>
            <p style={{ margin: 0, fontSize: '0.75rem', color: '#CBD5E1' }}>
              Protección de Datos Personales · Ley N° 29733 (RF02 / CUS01 / RN-02)
            </p>
          </div>
        </div>

        <span
          style={{
            backgroundColor: status?.hasConsented ? '#10B981' : '#F59E0B',
            color: '#FFFFFF',
            fontSize: '0.72rem',
            fontWeight: 700,
            padding: '0.25rem 0.65rem',
            borderRadius: '9999px',
          }}
        >
          {status?.hasConsented ? '✓ VIGENTE / CONFORME' : '⚠️ PENDIENTE DE FIRMA'}
        </span>
      </div>

      <div style={{ padding: '1.75rem' }}>
        {/* Selector de correo para simulación en dev */}
        <div
          style={{
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            marginBottom: '1.25rem',
            padding: '0.65rem 1rem',
            backgroundColor: '#F8FAFC',
            borderRadius: '8px',
            border: '1px solid #E2E8F0',
            fontSize: '0.82rem',
          }}
        >
          <div>
            <span style={{ color: '#64748B' }}>Usuario evaluado: </span>
            <strong style={{ color: '#1C2A59' }}>{email}</strong>
          </div>
          <div style={{ display: 'flex', gap: '0.35rem' }}>
            <button
              type="button"
              onClick={() => setEmail('2022074255@upt.pe')}
              style={{
                fontSize: '0.7rem',
                padding: '0.2rem 0.5rem',
                borderRadius: '4px',
                border: '1px solid #CBD5E1',
                background: email === '2022074255@upt.pe' ? '#1C2A59' : '#FFFFFF',
                color: email === '2022074255@upt.pe' ? '#FFFFFF' : '#334155',
                cursor: 'pointer',
              }}
            >
              Joan (2022074255)
            </button>
            <button
              type="button"
              onClick={() => setEmail('2022073504@upt.pe')}
              style={{
                fontSize: '0.7rem',
                padding: '0.2rem 0.5rem',
                borderRadius: '4px',
                border: '1px solid #CBD5E1',
                background: email === '2022073504@upt.pe' ? '#1C2A59' : '#FFFFFF',
                color: email === '2022073504@upt.pe' ? '#FFFFFF' : '#334155',
                cursor: 'pointer',
              }}
            >
              Renzo (2022073504)
            </button>
          </div>
        </div>

        {/* Texto normativo institucional de la Ley 29733 */}
        <div
          tabIndex={0}
          role="region"
          aria-label="Términos y condiciones del consentimiento legal"
          style={{
            maxHeight: '220px',
            overflowY: 'auto',
            padding: '1rem',
            backgroundColor: '#F1F5F9',
            borderRadius: '8px',
            border: '1px solid #CBD5E1',
            fontSize: '0.8rem',
            lineHeight: 1.6,
            color: '#334155',
            marginBottom: '1.25rem',
          }}
        >
          <h4 style={{ margin: '0 0 0.5rem 0', color: '#1C2A59', fontSize: '0.88rem' }}>
            POLÍTICA DE PRIVACIDAD Y TRATAMIENTO DE DATOS PERSONALES (EPIS - UPT)
          </h4>
          <p style={{ margin: '0 0 0.6rem 0' }}>
            En concordancia con la <strong>Ley N° 29733 (Ley de Protección de Datos Personales de la República del Perú)</strong> y su Reglamento aprobado mediante D.S. N° 003-2013-JUS, la Universidad Privada de Tacna (Facultad de Ingeniería - EPIS) informa al estudiante que sus datos personales y académicos serán incorporados al banco de datos institucional con las siguientes finalidades exclusivas:
          </p>
          <ol style={{ paddingLeft: '1.25rem', margin: '0 0 0.6rem 0' }}>
            <li>
              <strong>Emparejamiento Académico P2P:</strong> Utilizar las materias filtro matriculadas, calificaciones de cursos aprobados y temas silábicos declarados para alimentar el <em>algoritmo de recomendación Top-k</em>.
            </li>
            <li>
              <strong>Gestión de Disponibilidad:</strong> Almacenar y cruzar los bloques horarios semanales para coordinar sesiones de mentoría presenciales o virtuales con estudiantes de ciclos avanzados.
            </li>
            <li>
              <strong>Acreditación y Auditoría Horaria:</strong> Computar la asistencia a mentorías para el visado institucional de horas extracurriculares y proyección social.
            </li>
            <li>
              <strong>Gobernanza y No Transferencia:</strong> Se prohíbe taxativamente la transferencia o comercialización de datos a entidades externas o terceros ajenos a la UPT.
            </li>
          </ol>
          <p style={{ margin: 0 }}>
            El titular podrá ejercer sus derechos de Acceso, Rectificación, Cancelación y Oposición (Derechos ARCO) dirigiendo una solicitud formal ante la Dirección de la EPIS o al correo institucional de tutoría académica.
          </p>
        </div>

        {/* Checkbox de Conformidad Expresa */}
        <label
          style={{
            display: 'flex',
            alignItems: 'flex-start',
            gap: '0.75rem',
            cursor: 'pointer',
            padding: '0.85rem',
            backgroundColor: isChecked ? '#EFF6FF' : '#F8FAFC',
            border: `1px solid ${isChecked ? '#93C5FD' : '#E2E8F0'}`,
            borderRadius: '8px',
            marginBottom: '1.25rem',
            transition: 'all 0.2s',
          }}
        >
          <input
            type="checkbox"
            checked={isChecked}
            onChange={(e) => setIsChecked(e.target.checked)}
            style={{
              width: '18px',
              height: '18px',
              accentColor: '#1C2A59',
              marginTop: '0.15rem',
              cursor: 'pointer',
            }}
          />
          <span style={{ fontSize: '0.82rem', color: '#1E293B', lineHeight: 1.5 }}>
            <strong>Otorgo mi consentimiento expreso, previo, libre e informado</strong> para que mis datos académicos de cursos filtro y disponibilidad horaria sean tratados por el Sistema Web P2P conforme a la Ley N° 29733 (Versión: {consentService.getTermsVersion()}).
          </span>
        </label>

        {/* Mensajes de Estado */}
        {message && (
          <div
            role="alert"
            style={{
              padding: '0.75rem 1rem',
              borderRadius: '8px',
              marginBottom: '1.25rem',
              fontSize: '0.82rem',
              backgroundColor:
                message.type === 'success' ? '#F0FDF4' : message.type === 'error' ? '#FEF2F2' : '#FFFBEB',
              color:
                message.type === 'success' ? '#166534' : message.type === 'error' ? '#991B1B' : '#92400E',
              border: `1px solid ${
                message.type === 'success' ? '#BBF7D0' : message.type === 'error' ? '#FECACA' : '#FDE68A'
              }`,
            }}
          >
            {message.text}
          </div>
        )}

        {/* Información de estado previo si ya consintió */}
        {status?.hasConsented && status.consentedAt && (
          <div
            style={{
              marginBottom: '1.25rem',
              padding: '0.65rem 1rem',
              backgroundColor: '#F0FDF4',
              borderRadius: '8px',
              border: '1px solid #DCFCE7',
              fontSize: '0.78rem',
              color: '#166534',
            }}
          >
            🕒 <strong>Consentimiento activo registrado el:</strong>{' '}
            {new Date(status.consentedAt).toLocaleString()} ({status.termsVersion})
          </div>
        )}

        {/* Botones de Acción */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'flex-end',
            gap: '0.75rem',
            flexWrap: 'wrap',
          }}
        >
          <button
            type="button"
            onClick={handleReject}
            disabled={isLoading}
            style={{
              backgroundColor: '#FFFFFF',
              color: '#DC2626',
              border: '1px solid #FECACA',
              borderRadius: '8px',
              padding: '0.65rem 1.25rem',
              fontSize: '0.84rem',
              fontWeight: 600,
              cursor: isLoading ? 'not-allowed' : 'pointer',
              transition: 'background 0.2s',
            }}
          >
            🚫 Rechazar y Salir (RN-02)
          </button>

          <button
            type="button"
            onClick={handleAccept}
            disabled={isLoading || !isChecked}
            style={{
              backgroundColor: isChecked && !isLoading ? '#1C2A59' : '#94A3B8',
              color: '#FFFFFF',
              border: 'none',
              borderRadius: '8px',
              padding: '0.65rem 1.5rem',
              fontSize: '0.84rem',
              fontWeight: 700,
              cursor: isChecked && !isLoading ? 'pointer' : 'not-allowed',
              boxShadow: isChecked ? '0 4px 12px rgba(28, 42, 89, 0.2)' : 'none',
              transition: 'all 0.2s',
            }}
          >
            {isLoading ? 'Registrando...' : '✓ Aceptar y Continuar'}
          </button>
        </div>
      </div>
    </div>
  );
};
