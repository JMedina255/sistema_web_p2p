/**
 * Vista de Consulta y Descarga de Constancias Oficiales de Mentoría DEMO
 * T-43 / RF22 / RF23 / CUS18 / RN-14 / WCAG 2.1 AA
 * Sistema Web P2P de Mentorías Académicas — EPIS UPT
 */

import React, { useState, useEffect, useCallback, useId } from 'react';
import {
  certificateService,
  type HoursSummaryResponse,
  type CertificateMetaResponse,
  type CertificateVerifyResponse,
} from '../services/certificateService';

export interface CertificateDownloadViewProps {
  mentorEmail?: string;
  onNavigateToSessions?: () => void;
}

export const CertificateDownloadView: React.FC<CertificateDownloadViewProps> = ({
  mentorEmail,
  onNavigateToSessions,
}) => {
  const [summary, setSummary] = useState<HoursSummaryResponse | null>(null);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isGenerating, setIsGenerating] = useState<boolean>(false);
  const [isDownloading, setIsDownloading] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successMessage, setSuccessMessage] = useState<string | null>(null);

  // Estado del modal de verificación institucional QR
  const [isVerifyModalOpen, setIsVerifyModalOpen] = useState<boolean>(false);
  const [verifyData, setVerifyData] = useState<CertificateVerifyResponse | null>(null);
  const [isVerifying, setIsVerifying] = useState<boolean>(false);

  const headingId = useId();
  const verifyModalId = useId();

  const loadSummary = useCallback(async () => {
    try {
      setIsLoading(true);
      setErrorMessage(null);
      const data = await certificateService.getHoursSummary({ mentorEmail });
      setSummary(data);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage('Error al consultar el resumen de horas del estudiante mentor.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [mentorEmail]);

  useEffect(() => {
    loadSummary();
  }, [loadSummary]);

  // Manejar emisión de constancia
  const handleGenerateCertificate = async () => {
    try {
      setIsGenerating(true);
      setErrorMessage(null);
      setSuccessMessage(null);

      let cert: CertificateMetaResponse;
      try {
        cert = await certificateService.generateCertificate({
          mentorEmail: summary?.mentor_email || mentorEmail,
          academicPeriod: '2026-II',
        });
      } catch (genErr: unknown) {
        if (genErr instanceof Error) {
          setErrorMessage(genErr.message);
        } else {
          setErrorMessage('Error al emitir la constancia institucional de mentoría.');
        }
        return;
      }

      setSuccessMessage(
        `¡Constancia oficial emitida exitosamente! Folio asignado: ${cert.codigo_folio}. Ya puedes descargar tu documento en PDF.`
      );

      // Actualizar resumen local con el certificado emitido
      if (summary) {
        setSummary({
          ...summary,
          certificado_emitido: cert,
        });
      }

      // Descarga inmediata del PDF compilado (en bloque aislado para no opacar el éxito de la emisión)
      try {
        await certificateService.downloadPdf(cert.id_certificado, cert.codigo_folio);
      } catch {
        // En caso el navegador restrinja la descarga automática, el certificado ya está emitido y disponible para descarga manual
      }
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage('Error inesperado durante la emisión de la constancia.');
      }
    } finally {
      setIsGenerating(false);
    }
  };

  // Manejar descarga directa de PDF existente
  const handleDownloadExistingPdf = async (cert: CertificateMetaResponse) => {
    try {
      setIsDownloading(true);
      setErrorMessage(null);
      await certificateService.downloadPdf(cert.id_certificado, cert.codigo_folio);
      setSuccessMessage(`Documento descargado con éxito: Constancia_Mentoria_EPIS_2026_II_${cert.codigo_folio}.pdf`);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage('Error al descargar el archivo binario PDF.');
      }
    } finally {
      setIsDownloading(false);
    }
  };

  // Manejar apertura de modal de verificación por QR
  const handleOpenVerifyModal = async (folio: string) => {
    try {
      setIsVerifying(true);
      setIsVerifyModalOpen(true);
      const v = await certificateService.verifyCertificate(folio);
      setVerifyData(v);
    } catch (err: unknown) {
      if (err instanceof Error) {
        setErrorMessage(err.message);
      }
      setIsVerifyModalOpen(false);
    } finally {
      setIsVerifying(false);
    }
  };

  // Cerrojo de foco y Escape para accesibilidad WCAG 2.1 AA
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isVerifyModalOpen) {
        setIsVerifyModalOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isVerifyModalOpen]);

  if (isLoading) {
    return (
      <div
        role="status"
        aria-live="polite"
        style={{
          padding: '3rem',
          textAlign: 'center',
          color: '#475569',
          fontSize: '1rem',
        }}
      >
        <div style={{ display: 'inline-block', marginBottom: '1rem', fontSize: '2rem' }}>📜</div>
        <p>Consultando cómputo de horas formativas en la Escuela Profesional de Ingeniería de Sistemas...</p>
      </div>
    );
  }

  const horasVisadas = summary?.horas_visadas ?? 0;
  const horasPendientes = summary?.horas_pendientes ?? 0;
  const umbral = summary?.umbral_requerido ?? 20.0;
  const progreso = summary?.porcentaje_progreso ?? 0;
  const esElegible = summary?.es_elegible ?? false;
  const horasFaltantes = summary?.horas_faltantes ?? 20.0;
  const certEmitido = summary?.certificado_emitido;

  return (
    <div
      style={{
        maxWidth: '920px',
        margin: '0 auto',
        padding: '1.5rem',
        fontFamily: 'Inter, system-ui, -apple-system, sans-serif',
      }}
    >
      {/* Encabezado Institucional */}
      <div
        style={{
          borderBottom: '2px solid #E2E8F0',
          paddingBottom: '1.25rem',
          marginBottom: '2rem',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: '1rem',
        }}
      >
        <div>
          <span
            style={{
              display: 'inline-block',
              backgroundColor: '#EFF6FF',
              color: '#1C2A59',
              padding: '0.25rem 0.75rem',
              borderRadius: '9999px',
              fontSize: '0.75rem',
              fontWeight: 700,
              textTransform: 'uppercase',
              letterSpacing: '0.05em',
              marginBottom: '0.5rem',
            }}
          >
            Acreditación de Mentoría (RF22 / RF23 / RN-14)
          </span>
          <h1
            id={headingId}
            style={{
              fontSize: '1.65rem',
              fontWeight: 800,
              color: '#1C2A59',
              margin: '0 0 0.25rem 0',
            }}
          >
            Acreditación y Constancias Oficiales de Mentoría
          </h1>
          <p style={{ margin: 0, color: '#64748B', fontSize: '0.9rem' }}>
            Universidad Privada de Tacna — Facultad de Ingeniería (EPIS) • Semestre 2026-II
          </p>
        </div>

        {onNavigateToSessions && (
          <button
            type="button"
            onClick={onNavigateToSessions}
            style={{
              padding: '0.5rem 1rem',
              backgroundColor: '#F1F5F9',
              color: '#334155',
              border: '1px solid #CBD5E1',
              borderRadius: '8px',
              fontSize: '0.85rem',
              fontWeight: 600,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            ← Volver a Mis Sesiones
          </button>
        )}
      </div>

      {/* Alertas Accesibles */}
      {errorMessage && (
        <div
          role="alert"
          style={{
            padding: '1rem 1.25rem',
            backgroundColor: '#FEF2F2',
            border: '1px solid #F87171',
            borderRadius: '8px',
            color: '#991B1B',
            fontSize: '0.9rem',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '0.75rem',
          }}
        >
          <span style={{ fontSize: '1.25rem', lineHeight: 1 }}>⚠️</span>
          <div>
            <strong style={{ display: 'block', marginBottom: '0.25rem' }}>Aviso de Validación</strong>
            {errorMessage}
          </div>
        </div>
      )}

      {successMessage && (
        <div
          role="status"
          aria-live="polite"
          style={{
            padding: '1rem 1.25rem',
            backgroundColor: '#F0FDF4',
            border: '1px solid #4ADE80',
            borderRadius: '8px',
            color: '#166534',
            fontSize: '0.9rem',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '0.75rem',
          }}
        >
          <span style={{ fontSize: '1.25rem', lineHeight: 1 }}>✅</span>
          <div>
            <strong style={{ display: 'block', marginBottom: '0.25rem' }}>Operación Exitosa</strong>
            {successMessage}
          </div>
        </div>
      )}

      {/* Tarjeta de Progreso Formativo hacia el Umbral Reglamentario */}
      <section
        aria-labelledby="progress-card-title"
        style={{
          backgroundColor: '#FFFFFF',
          border: '1px solid #E2E8F0',
          borderRadius: '12px',
          padding: '1.75rem',
          boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
          marginBottom: '2rem',
        }}
      >
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            justifyContent: 'space-between',
            alignItems: 'baseline',
            marginBottom: '1rem',
          }}
        >
          <h2
            id="progress-card-title"
            style={{
              fontSize: '1.2rem',
              fontWeight: 700,
              color: '#1E293B',
              margin: 0,
            }}
          >
            Avance hacia el Umbral de Acreditación (Regla RN-14)
          </h2>
          <span
            style={{
              fontSize: '1.1rem',
              fontWeight: 800,
              color: esElegible ? '#16A34A' : '#D97706',
            }}
          >
            {horasVisadas.toFixed(1)} / {umbral.toFixed(1)} horas ({progreso}%)
          </span>
        </div>

        {/* Barra de Progreso Accesible WAI-ARIA */}
        <div
          role="progressbar"
          aria-valuenow={horasVisadas}
          aria-valuemin={0}
          aria-valuemax={umbral}
          aria-label="Progreso de horas formativas visadas para certificación"
          style={{
            width: '100%',
            height: '18px',
            backgroundColor: '#E2E8F0',
            borderRadius: '9999px',
            overflow: 'hidden',
            marginBottom: '1.25rem',
          }}
        >
          <div
            style={{
              width: `${progreso}%`,
              height: '100%',
              backgroundColor: esElegible ? '#16A34A' : '#1C2A59',
              transition: 'width 0.6s cubic-bezier(0.4, 0, 0.2, 1)',
              borderRadius: '9999px',
            }}
          />
        </div>

        {/* Desglose de Horas y Estado Formativo */}
        <div
          style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '1rem',
            paddingTop: '0.75rem',
            borderTop: '1px solid #F1F5F9',
          }}
        >
          <div style={{ padding: '0.5rem 0' }}>
            <span style={{ fontSize: '0.78rem', color: '#64748B', display: 'block' }}>
              Horas Acreditadas (Visadas por Dirección)
            </span>
            <strong style={{ fontSize: '1.25rem', color: '#1E293B' }}>{horasVisadas.toFixed(1)} h</strong>
          </div>

          <div style={{ padding: '0.5rem 0' }}>
            <span style={{ fontSize: '0.78rem', color: '#64748B', display: 'block' }}>
              Horas en Revisión Provisional
            </span>
            <strong style={{ fontSize: '1.25rem', color: '#D97706' }}>{horasPendientes.toFixed(1)} h</strong>
          </div>

          <div style={{ padding: '0.5rem 0' }}>
            <span style={{ fontSize: '0.78rem', color: '#64748B', display: 'block' }}>
              Condición Reglamentaria RN-14
            </span>
            <span
              style={{
                display: 'inline-block',
                marginTop: '0.2rem',
                padding: '0.2rem 0.6rem',
                borderRadius: '6px',
                fontSize: '0.8rem',
                fontWeight: 700,
                backgroundColor: esElegible ? '#DCFCE7' : '#FEF3C7',
                color: esElegible ? '#166534' : '#92400E',
              }}
            >
              {esElegible ? '✓ ELEGIBLE PARA CERTIFICACIÓN' : `FALTAN ${horasFaltantes.toFixed(1)} HORAS VISADAS`}
            </span>
          </div>
        </div>

        {/* Aviso Pedagógico si Horas < 20.0 */}
        {!esElegible && (
          <div
            style={{
              marginTop: '1.25rem',
              padding: '0.9rem 1rem',
              backgroundColor: '#FFFBEB',
              border: '1px solid #FDE68A',
              borderRadius: '8px',
              color: '#92400E',
              fontSize: '0.88rem',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            <span>ℹ️</span>
            <span>
              <strong>Aviso Pedagógico RN-14:</strong> Te faltan {horasFaltantes.toFixed(1)} horas visadas para solicitar tu
              constancia oficial de mentoría. Recuerda registrar tus bitácoras pedagógicas oportunamente dentro de las 48
              horas de finalizada cada sesión para su visado por Dirección.
            </span>
          </div>
        )}
      </section>

      {/* Panel de Emisión y Descarga */}
      <section
        aria-labelledby="cert-panel-title"
        style={{
          backgroundColor: '#FFFFFF',
          border: '1px solid #E2E8F0',
          borderRadius: '12px',
          padding: '1.75rem',
          boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
        }}
      >
        <h2
          id="cert-panel-title"
          style={{
            fontSize: '1.2rem',
            fontWeight: 700,
            color: '#1E293B',
            margin: '0 0 1rem 0',
          }}
        >
          Emisión de Constancia Digital Oficial (DEMO)
        </h2>

        {certEmitido ? (
          // Caso A: Ya cuenta con constancia emitida en el semestre
          <div
            style={{
              border: '2px solid #BAE6FD',
              backgroundColor: '#F0F9FF',
              borderRadius: '10px',
              padding: '1.5rem',
            }}
          >
            <div
              style={{
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'flex-start',
                flexWrap: 'wrap',
                gap: '1rem',
                marginBottom: '1rem',
              }}
            >
              <div>
                <span
                  style={{
                    backgroundColor: '#0284C7',
                    color: '#FFFFFF',
                    padding: '0.2rem 0.6rem',
                    borderRadius: '4px',
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    letterSpacing: '0.05em',
                  }}
                >
                  CONSTANCIA EMITIDA • {certEmitido.estado}
                </span>
                <h3
                  style={{
                    fontSize: '1.3rem',
                    fontWeight: 800,
                    color: '#1C2A59',
                    margin: '0.5rem 0 0.25rem 0',
                  }}
                >
                  Folio: {certEmitido.codigo_folio}
                </h3>
                <p style={{ margin: 0, fontSize: '0.85rem', color: '#475569' }}>
                  Acreditación de {certEmitido.horas_acreditadas.toFixed(1)} horas académicas en el periodo lectivo{' '}
                  {certEmitido.periodo_academico}.
                </p>
              </div>

              <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                <button
                  type="button"
                  onClick={() => handleDownloadExistingPdf(certEmitido)}
                  disabled={isDownloading}
                  aria-label="Descargar Constancia en PDF"
                  style={{
                    padding: '0.65rem 1.25rem',
                    backgroundColor: '#1C2A59',
                    color: '#FFFFFF',
                    border: 'none',
                    borderRadius: '8px',
                    fontSize: '0.9rem',
                    fontWeight: 700,
                    cursor: isDownloading ? 'wait' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                    boxShadow: '0 2px 4px rgba(28, 42, 89, 0.2)',
                  }}
                >
                  📥 {isDownloading ? 'Descargando...' : 'Descargar Constancia en PDF'}
                </button>

                <button
                  type="button"
                  onClick={() => handleOpenVerifyModal(certEmitido.codigo_folio)}
                  aria-label="Verificar QR Institucional"
                  style={{
                    padding: '0.65rem 1rem',
                    backgroundColor: '#FFFFFF',
                    color: '#1C2A59',
                    border: '1px solid #CBD5E1',
                    borderRadius: '8px',
                    fontSize: '0.9rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.5rem',
                  }}
                >
                  🔍 Verificar QR
                </button>
              </div>
            </div>

            {/* Metadatos de Integridad y Seguridad */}
            <div
              style={{
                backgroundColor: '#FFFFFF',
                borderRadius: '8px',
                padding: '1rem',
                border: '1px solid #E0F2FE',
                fontSize: '0.8rem',
                color: '#334155',
              }}
            >
              <div style={{ marginBottom: '0.35rem' }}>
                <strong>Marca de Agua:</strong> &quot;DEMO - FINES ACADÉMICOS&quot; (Diagonal de seguridad 45°)
              </div>
              <div style={{ marginBottom: '0.35rem' }}>
                <strong>Fecha de Expedición:</strong> {new Date(certEmitido.created_at).toLocaleString('es-PE')}
              </div>
              <div style={{ wordBreak: 'break-all', fontFamily: 'monospace', fontSize: '0.75rem' }}>
                <strong>Firma Criptográfica SHA-256:</strong> {certEmitido.hash_firma}
              </div>
            </div>
          </div>
        ) : (
          // Caso B: Aún no ha emitido constancia
          <div>
            <p style={{ color: '#475569', fontSize: '0.9rem', lineHeight: 1.6, marginBottom: '1.5rem' }}>
              La constancia institucional certifica formalmente tu cumplimiento de las horas formativas como estudiante
              mentor ante la cátedra de Construcción de Software I y la Escuela Profesional de Ingeniería de Sistemas. El
              documento emitido incorpora marca de agua diagonal de seguridad, sello criptográfico SHA-256 y código QR
              conducente a la auditoría oficial.
            </p>

            <button
              type="button"
              disabled={!esElegible || isGenerating}
              onClick={handleGenerateCertificate}
              aria-label={
                esElegible
                  ? 'Emitir Constancia Oficial'
                  : `Emitir Constancia Oficial (Bloqueada: Faltan ${horasFaltantes.toFixed(1)} horas visadas)`
              }
              style={{
                padding: '0.85rem 1.75rem',
                backgroundColor: esElegible ? '#1C2A59' : '#94A3B8',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '8px',
                fontSize: '1rem',
                fontWeight: 700,
                cursor: esElegible && !isGenerating ? 'pointer' : 'not-allowed',
                display: 'flex',
                alignItems: 'center',
                gap: '0.6rem',
                transition: 'all 0.2s ease',
                boxShadow: esElegible ? '0 4px 6px rgba(28, 42, 89, 0.25)' : 'none',
              }}
            >
              📜 {isGenerating ? 'Generando PDF Oficial y QR...' : 'Emitir Constancia Oficial'}
            </button>
          </div>
        )}
      </section>

      {/* Modal Accesible de Verificación Institucional QR (CUS09) */}
      {isVerifyModalOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby={verifyModalId}
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(15, 23, 42, 0.7)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '1.5rem',
            zIndex: 9999,
          }}
          onClick={(e) => {
            if (e.target === e.currentTarget) setIsVerifyModalOpen(false);
          }}
        >
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              maxWidth: '520px',
              width: '100%',
              padding: '2rem',
              boxShadow: '0 20px 25px -5px rgba(0,0,0,0.1)',
            }}
          >
            <h3
              id={verifyModalId}
              style={{
                margin: '0 0 1rem 0',
                fontSize: '1.3rem',
                fontWeight: 800,
                color: '#1C2A59',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
              }}
            >
              🏛️ Verificación de Autenticidad Institucional
            </h3>

            {isVerifying ? (
              <p style={{ color: '#64748B' }}>Auditando folio en el validador oficial EPIS-UPT...</p>
            ) : verifyData ? (
              <div>
                <div
                  style={{
                    padding: '0.75rem',
                    backgroundColor: '#DCFCE7',
                    border: '1px solid #86EFAC',
                    borderRadius: '8px',
                    color: '#166534',
                    fontSize: '0.85rem',
                    fontWeight: 600,
                    marginBottom: '1rem',
                  }}
                >
                  ✓ Constancia oficial auténtica, vigente y acreditada por la EPIS-UPT.
                </div>

                <div style={{ fontSize: '0.85rem', color: '#334155', lineHeight: 1.6 }}>
                  <p>
                    <strong>Folio:</strong> {verifyData.codigo_folio}
                  </p>
                  <p>
                    <strong>Mentor Titular:</strong> {verifyData.id_mentor}
                  </p>
                  <p>
                    <strong>Horas Acreditadas:</strong> {verifyData.horas_acreditadas} horas
                  </p>
                  <p>
                    <strong>Período Lectivo:</strong> {verifyData.periodo_academico}
                  </p>
                  <p>
                    <strong>Estado Documental:</strong> {verifyData.estado}
                  </p>
                  <p style={{ wordBreak: 'break-all', fontFamily: 'monospace', fontSize: '0.75rem' }}>
                    <strong>Firma SHA-256:</strong> {verifyData.hash_firma}
                  </p>
                </div>
              </div>
            ) : (
              <p style={{ color: '#DC2626' }}>No fue posible resolver la verificación del folio.</p>
            )}

            <div style={{ marginTop: '1.5rem', textAlign: 'right' }}>
              <button
                type="button"
                onClick={() => setIsVerifyModalOpen(false)}
                style={{
                  padding: '0.5rem 1.25rem',
                  backgroundColor: '#1C2A59',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '6px',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                Cerrar
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
