import React from 'react';
import type { DigitalCertificate } from '../data/mockData';

interface CertificateModalProps {
  certificate: DigitalCertificate | null;
  isOpen: boolean;
  onClose: () => void;
}

export const CertificateModal: React.FC<CertificateModalProps> = ({ certificate, isOpen, onClose }) => {
  if (!isOpen || !certificate) return null;

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(23, 35, 73, 0.75)',
        backdropFilter: 'blur(5px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        padding: '1rem'
      }}
      onClick={onClose}
    >
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '16px',
          maxWidth: '780px',
          width: '100%',
          overflow: 'hidden',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
          border: '1.5px solid #D9BF7D'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        {/* Cabecera del Certificado */}
        <div
          style={{
            background: 'linear-gradient(135deg, #1C2A59 0%, #172349 100%)',
            color: '#FFFFFF',
            padding: '1.25rem 2rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            borderBottom: '3px solid #B99451'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
            <span style={{ fontSize: '1.5rem' }}>📜</span>
            <div>
              <h3 style={{ margin: 0, fontSize: '1.1rem', color: '#FFFFFF' }}>
                Constancia Oficial de Horas Extracurriculares
              </h3>
              <span style={{ fontSize: '0.75rem', color: 'var(--accent-gold-light)' }}>
                Folio Oficial: {certificate.folio} • Validez Institucional Sunedu / EPIS
              </span>
            </div>
          </div>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              color: '#FFFFFF',
              fontSize: '1.5rem',
              cursor: 'pointer',
              lineHeight: 1
            }}
          >
            ×
          </button>
        </div>

        {/* Cuerpo del Certificado (Diseño Diploma) */}
        <div style={{ padding: '2.5rem', backgroundColor: '#FDFCF7', border: '12px solid #FAF6EB', margin: '1rem', borderRadius: '12px' }}>
          <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
            <div style={{ fontSize: '0.85rem', fontWeight: 800, letterSpacing: '0.1em', color: '#1C2A59', textTransform: 'uppercase' }}>
              Universidad Privada de Tacna
            </div>
            <div style={{ fontSize: '0.75rem', fontWeight: 600, color: '#A6823F', textTransform: 'uppercase' }}>
              Facultad de Ingeniería • Escuela Profesional de Ingeniería de Sistemas
            </div>
            <div style={{ width: '80px', height: '2px', backgroundColor: '#B99451', margin: '0.6rem auto' }} />
            <h2 style={{ fontSize: '1.75rem', fontFamily: 'serif', color: '#1C2A59', margin: '0.5rem 0' }}>
              CERTIFICADO DE MENTORÍA ACADÉMICA
            </h2>
            <span style={{ fontSize: '0.82rem', color: '#5A6578' }}>
              Conforme al Reglamento de Horas Formativas y Mentorías P2P
            </span>
          </div>

          <div style={{ textAlign: 'center', margin: '1.8rem 0', color: '#2D3748', lineHeight: 1.8 }}>
            <p style={{ fontSize: '0.95rem' }}>
              El Comité de Tutoría y la Dirección de la EPIS-UPT certifican que:
            </p>
            <div style={{ fontSize: '1.5rem', fontWeight: 800, color: '#1C2A59', margin: '0.4rem 0', borderBottom: '1px solid #D9BF7D', display: 'inline-block', paddingBottom: '0.2rem' }}>
              {certificate.mentorName}
            </div>
            <div style={{ fontSize: '0.85rem', color: '#718096' }}>
              Código Universitario: <strong>{certificate.mentorCode}</strong>
            </div>
            <p style={{ fontSize: '0.92rem', marginTop: '1rem', maxWidth: '580px', margin: '1rem auto 0' }}>
              Ha completado satisfactoriamente <strong>{certificate.hoursValidated} horas cronológicas</strong> de asesoría y mentoría académica entre pares en asignaturas críticas durante el <strong>{certificate.semester}</strong>, habiendo superado el proceso de auditoría y visado pedagógico reglamentario.
            </p>
          </div>

          {/* Bloque de Fe Pública y QR Criptográfico */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: '120px 1fr 180px',
              gap: '1.5rem',
              alignItems: 'center',
              backgroundColor: '#FFFFFF',
              padding: '1rem',
              borderRadius: '8px',
              border: '1px dashed #CBD5E0',
              marginTop: '1.5rem'
            }}
          >
            {/* Código QR Simulado */}
            <div style={{ textAlign: 'center' }}>
              <div
                style={{
                  width: '90px',
                  height: '90px',
                  backgroundColor: '#1C2A59',
                  color: '#FFFFFF',
                  display: 'flex',
                  flexDirection: 'column',
                  alignItems: 'center',
                  justifyContent: 'center',
                  borderRadius: '6px',
                  margin: '0 auto',
                  fontSize: '0.65rem',
                  padding: '4px'
                }}
              >
                <div style={{ fontSize: '1.8rem', lineHeight: 1 }}>▦</div>
                <span>QR VERIFICABLE</span>
              </div>
            </div>

            {/* Metadatos Criptográficos */}
            <div style={{ fontSize: '0.72rem', color: '#4A5568' }}>
              <div style={{ fontWeight: 700, color: '#1C2A59', marginBottom: '0.2rem' }}>
                Custodia Digital & Trazabilidad (RNF09):
              </div>
              <div><strong>Fecha de emisión:</strong> {certificate.issueDate}</div>
              <div><strong>Folio institucional:</strong> {certificate.folio}</div>
              <div style={{ marginTop: '0.3rem', wordBreak: 'break-all' }}>
                <strong>Hash SHA-256:</strong> <code style={{ color: '#2B6CB0' }}>{certificate.hashSha256}</code>
              </div>
            </div>

            {/* Firma Institucional */}
            <div style={{ textAlign: 'center', borderTop: '1px solid #A0AEC0', paddingTop: '0.5rem' }}>
              <div style={{ fontSize: '0.8rem', fontWeight: 700, color: '#1C2A59' }}>
                {certificate.signedBy}
              </div>
              <div style={{ fontSize: '0.68rem', color: '#718096' }}>
                Dirección de Escuela EPIS-UPT
              </div>
            </div>
          </div>
        </div>

        {/* Acciones del Modal */}
        <div
          style={{
            backgroundColor: '#F7FAFC',
            padding: '1rem 2rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            borderTop: '1px solid #E2E8F0'
          }}
        >
          <span style={{ fontSize: '0.75rem', color: '#718096' }}>
            🔒 Documento autenticado mediante token digital de fe pública EPIS
          </span>
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <button
              onClick={() => window.print()}
              className="btn-gold"
              style={{ fontSize: '0.85rem', padding: '0.5rem 1.25rem' }}
            >
              🖨️ Imprimir / Guardar PDF
            </button>
            <button
              onClick={onClose}
              style={{
                backgroundColor: 'transparent',
                border: '1.5px solid #CBD5E0',
                borderRadius: '9999px',
                padding: '0.5rem 1.25rem',
                fontSize: '0.85rem',
                fontWeight: 600,
                color: '#4A5568',
                cursor: 'pointer'
              }}
            >
              Cerrar
            </button>
          </div>
        </div>
      </div>
    </div>
  );
};
