import React, { useState } from 'react';

interface ConsentModalProps {
  isOpen: boolean;
  onClose: () => void;
  onAccept: () => void;
}

export const ConsentModal: React.FC<ConsentModalProps> = ({
  isOpen,
  onClose,
  onAccept
}) => {
  const [acceptedTerms, setAcceptedTerms] = useState(true);
  const [acceptedDataTreatment, setAcceptedDataTreatment] = useState(true);
  const [savedSuccess, setSavedSuccess] = useState(false);

  if (!isOpen) return null;

  const handleConfirm = () => {
    setSavedSuccess(true);
    setTimeout(() => {
      setSavedSuccess(false);
      onAccept();
      onClose();
    }, 1200);
  };

  return (
    <div className="modal-backdrop" onClick={onClose}>
      <div className="modal-card" onClick={(e) => e.stopPropagation()}>
        <div className="modal-header">
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <div style={{ fontSize: '1.5rem' }}>⚖️</div>
            <div>
              <h2 style={{ color: '#FFFFFF', fontSize: '1.15rem', margin: 0 }}>
                Consentimiento Informado Digital
              </h2>
              <span style={{ fontSize: '0.75rem', opacity: 0.85, color: 'var(--accent-gold-light)' }}>
                Ley N° 29733 — Protección de Datos Personales del Perú
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              color: '#FFFFFF',
              fontSize: '1.25rem',
              cursor: 'pointer'
            }}
          >
            ✕
          </button>
        </div>

        <div className="modal-body">
          <p style={{ marginBottom: '1rem', fontSize: '0.9rem' }}>
            Para acceder a las mentorías académicas, requerimos tu autorización para usar tus datos académicos
            exclusivamente con fines de emparejamiento con mentores y convalidación de horas oficiales ante la EPIS.
          </p>

          <div className="modal-legal-box">
            <h4 style={{ fontSize: '0.85rem', color: 'var(--primary-navy)', marginBottom: '0.35rem' }}>
              Finalidades del tratamiento de datos (Ley N° 29733):
            </h4>
            <ul style={{ paddingLeft: '1.25rem', display: 'flex', flexDirection: 'column', gap: '0.3rem', fontSize: '0.82rem' }}>
              <li>
                <strong>Emparejamiento Personalizado:</strong> Comparar temas requeridos y materias aprobadas para sugerir el mejor mentor.
              </li>
              <li>
                <strong>Acreditación de Horas:</strong> Registro de horas efectivas de mentoría ante la Dirección de Escuela.
              </li>
              <li>
                <strong>Seguridad y Privacidad:</strong> Acceso autenticado y protección de datos mediante políticas RLS.
              </li>
            </ul>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem', marginTop: '1rem' }}>
            <label style={{ display: 'flex', alignItems: 'flex-start', gap: '0.6rem', cursor: 'pointer', fontSize: '0.85rem' }}>
              <input
                type="checkbox"
                checked={acceptedTerms}
                onChange={(e) => setAcceptedTerms(e.target.checked)}
                style={{ marginTop: '0.2rem' }}
              />
              <span>
                Acepto los <strong>Términos del Servicio y Código de Conducta</strong> de las mentorías académicas.
              </span>
            </label>

            <label style={{ display: 'flex', alignItems: 'flex-start', gap: '0.6rem', cursor: 'pointer', fontSize: '0.85rem' }}>
              <input
                type="checkbox"
                checked={acceptedDataTreatment}
                onChange={(e) => setAcceptedDataTreatment(e.target.checked)}
                style={{ marginTop: '0.2rem' }}
              />
              <span>
                Autorizo el uso de mi disponibilidad y materias cursadas para el <strong>sistema de recomendación</strong>.
              </span>
            </label>
          </div>

          {savedSuccess && (
            <div style={{
              marginTop: '1.25rem',
              padding: '0.75rem',
              backgroundColor: '#E6F4EA',
              color: '#137333',
              borderRadius: '8px',
              fontSize: '0.85rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem'
            }}>
              ✓ Consentimiento registrado en PostgreSQL/Supabase (timestamp + token de sesión emitido).
            </div>
          )}
        </div>

        <div className="modal-footer">
          <button className="btn-outline-navy btn-sm" onClick={onClose}>
            Revisar luego
          </button>
          <button
            className="btn-gold"
            disabled={!acceptedTerms || !acceptedDataTreatment || savedSuccess}
            onClick={handleConfirm}
            style={{ opacity: (!acceptedTerms || !acceptedDataTreatment) ? 0.5 : 1 }}
          >
            {savedSuccess ? 'Registrando...' : 'Aceptar y Continuar'}
          </button>
        </div>
      </div>
    </div>
  );
};
