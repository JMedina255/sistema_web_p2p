import React, { useState } from 'react';
import {
  INITIAL_LOGS,
  INITIAL_CERTIFICATES,
  INITIAL_SUBJECT_PRIORITIES,
  MOCK_MENTORS
} from '../data/mockData';
import type { PedagogicalLog, DigitalCertificate, SubjectPriority } from '../data/mockData';
import { CertificateModal } from './CertificateModal';

interface AdminViewProps {
  certificates?: DigitalCertificate[];
  onAddCertificate?: (cert: DigitalCertificate) => void;
}

export const AdminView: React.FC<AdminViewProps> = ({
  certificates: propCertificates,
  onAddCertificate
}) => {
  const [activeAdminSubTab, setActiveAdminSubTab] = useState<'analytics' | 'audit' | 'certificates' | 'curriculum'>('analytics');
  
  // Estado de Bitácoras para Auditoría
  const [logs, setLogs] = useState<PedagogicalLog[]>(INITIAL_LOGS);
  const [selectedLogForReview, setSelectedLogForReview] = useState<PedagogicalLog | null>(null);
  const [observationInput, setObservationInput] = useState<string>('');
  const [notification, setNotification] = useState<{ message: string; type: 'success' | 'warning' } | null>(null);

  // Estado de Certificados
  const [localCertificates, setLocalCertificates] = useState<DigitalCertificate[]>(INITIAL_CERTIFICATES);
  const certificates = propCertificates || localCertificates;
  const [viewingCertificate, setViewingCertificate] = useState<DigitalCertificate | null>(null);
  const [selectedMentorForNewCert, setSelectedMentorForNewCert] = useState<string>(MOCK_MENTORS[1].name);

  // Estado de Prioridades Curriculares (CUS12 / RN-11)
  const [subjectPriorities, setSubjectPriorities] = useState<SubjectPriority[]>(INITIAL_SUBJECT_PRIORITIES);

  const showNotification = (message: string, type: 'success' | 'warning' = 'success') => {
    setNotification({ message, type });
    setTimeout(() => setNotification(null), 3500);
  };

  // Visar bitácora (CUS22 / RN-14)
  const handleApproveLog = (logId: string) => {
    const updated = logs.map(l => {
      if (l.id === logId) {
        const randomHash = Array.from({ length: 64 }, () => Math.floor(Math.random() * 16).toString(16)).join('');
        return {
          ...l,
          status: 'VISADA' as const,
          auditFeedback: 'Horas y trazabilidad pedagógica auditadas y aprobadas por Comité de Tutoría.',
          auditDate: new Date().toLocaleDateString('es-PE', { day: '2-digit', month: 'short', year: 'numeric' }),
          hashSha256: randomHash
        };
      }
      return l;
    });
    setLogs(updated);
    showNotification('✓ Bitácora visada exitosamente. Las horas han sido promovidas a Oficiales para convalidación.');
  };

  // Observar bitácora
  const handleObserveLog = (logId: string) => {
    if (!observationInput.trim()) return;
    const updated = logs.map(l => {
      if (l.id === logId) {
        return {
          ...l,
          status: 'OBSERVADA' as const,
          auditFeedback: observationInput.trim(),
          auditDate: new Date().toLocaleDateString('es-PE', { day: '2-digit', month: 'short', year: 'numeric' })
        };
      }
      return l;
    });
    setLogs(updated);
    setObservationInput('');
    setSelectedLogForReview(null);
    showNotification('⚠️ Bitácora observada. Se notificó al mentor para subsanar evidencias en 48 horas.', 'warning');
  };

  // Emitir nuevo certificado (CUS13)
  const handleIssueCertificate = () => {
    const mentor = MOCK_MENTORS.find(m => m.name === selectedMentorForNewCert) || MOCK_MENTORS[1];
    const folioNum = String(certificates.length + 90).padStart(3, '0');
    const newCert: DigitalCertificate = {
      folio: `CERT-EPIS-2026-${folioNum}`,
      mentorName: mentor.name,
      mentorCode: mentor.code,
      hoursValidated: mentor.totalHours,
      issueDate: new Date().toLocaleDateString('es-PE', { day: '2-digit', month: 'long', year: 'numeric' }),
      semester: 'Semestre Académico 2026-II',
      hashSha256: Array.from({ length: 64 }, () => Math.floor(Math.random() * 16).toString(16)).join('',),
      qrVerificationUrl: `https://epis.upt.edu.pe/verificar/CERT-EPIS-2026-${folioNum}`,
      signedBy: 'Ing. Liliana Vega Bernal — Comité de Tutoría EPIS'
    };
    if (onAddCertificate) {
      onAddCertificate(newCert);
    } else {
      setLocalCertificates([newCert, ...localCertificates]);
    }
    showNotification(`✓ Certificado oficial ${newCert.folio} emitido con hash criptográfico SHA-256.`);
  };

  // Modificar factor de bonificación (CUS12 / RN-11)
  const handleUpdateAlpha = (subId: string, newAlpha: number) => {
    setSubjectPriorities(subjectPriorities.map(sp => {
      if (sp.id === subId) {
        return { ...sp, criticalFactorAlpha: newAlpha };
      }
      return sp;
    }));
    showNotification(`Factor α actualizado para la asignatura. El algoritmo Top-k bonificará el ranking.`);
  };

  const handleTogglePriority = (subId: string) => {
    setSubjectPriorities(subjectPriorities.map(sp => {
      if (sp.id === subId) {
        return { ...sp, isPriorityBoosted: !sp.isPriorityBoosted };
      }
      return sp;
    }));
  };

  return (
    <div className="fade-in">
      {/* Cabecera del Panel Administrador */}
      <div style={{ marginBottom: '1.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
            <span className="badge badge-gold">🛡️ Comité de Tutoría y Calidad</span>
            <span className="badge badge-navy">EPIS-UPT 2026</span>
          </div>
          <h2 style={{ fontSize: '1.65rem', color: 'var(--primary-navy)' }}>
            Panel de Supervisión y Gobernanza Institucional
          </h2>
          <p style={{ color: 'var(--text-body)', fontSize: '0.9rem', maxWidth: '750px' }}>
            Control directivo de analíticas académicas (CUS14), auditoría y visado de horas (CUS22), emisión de constancias SHA-256 (CUS13) y calibración algorítmica (CUS12).
          </p>
        </div>

        {/* Pestañas Secundarias de Navegación del Administrador */}
        <div style={{ display: 'flex', gap: '0.5rem', background: '#FFFFFF', padding: '0.3rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <button
            onClick={() => setActiveAdminSubTab('analytics')}
            style={{
              padding: '0.45rem 0.9rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeAdminSubTab === 'analytics' ? 'var(--primary-navy)' : 'transparent',
              color: activeAdminSubTab === 'analytics' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            📊 Analíticas (CUS14)
          </button>
          <button
            onClick={() => setActiveAdminSubTab('audit')}
            style={{
              padding: '0.45rem 0.9rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeAdminSubTab === 'audit' ? 'var(--primary-navy)' : 'transparent',
              color: activeAdminSubTab === 'audit' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            ⚖️ Auditoría Horas (CUS22)
          </button>
          <button
            onClick={() => setActiveAdminSubTab('certificates')}
            style={{
              padding: '0.45rem 0.9rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeAdminSubTab === 'certificates' ? 'var(--primary-navy)' : 'transparent',
              color: activeAdminSubTab === 'certificates' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            📜 Certificados (CUS13)
          </button>
          <button
            onClick={() => setActiveAdminSubTab('curriculum')}
            style={{
              padding: '0.45rem 0.9rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeAdminSubTab === 'curriculum' ? 'var(--primary-navy)' : 'transparent',
              color: activeAdminSubTab === 'curriculum' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            ⚡ Bonificación α (CUS12)
          </button>
        </div>
      </div>

      {/* Alerta de notificación flotante */}
      {notification && (
        <div
          style={{
            padding: '0.85rem 1.25rem',
            borderRadius: '12px',
            marginBottom: '1.25rem',
            backgroundColor: notification.type === 'success' ? '#E6F4EA' : '#FEF7E0',
            color: notification.type === 'success' ? '#137333' : '#B06000',
            border: `1px solid ${notification.type === 'success' ? '#CEEAD6' : '#FEEFC3'}`,
            fontSize: '0.88rem',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '0.5rem'
          }}
        >
          <span>{notification.type === 'success' ? '🛡️' : '⚠️'}</span>
          <span>{notification.message}</span>
        </div>
      )}

      {/* 1. SUB-TAB: ANALÍTICAS INSTITUCIONALES (CUS14 / RF14) */}
      {activeAdminSubTab === 'analytics' && (
        <div>
          {/* Tarjetas de Métricas Clave (KPIs) */}
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1.25rem', marginBottom: '2rem' }}>
            <div className="upt-card" style={{ padding: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 700 }}>SESIONES EJECUTADAS</span>
                <span style={{ fontSize: '1.2rem' }}>📅</span>
              </div>
              <div style={{ fontSize: '1.85rem', fontWeight: 800, color: 'var(--primary-navy)' }}>
                48
              </div>
              <div style={{ fontSize: '0.75rem', color: '#137333', fontWeight: 600, marginTop: '0.25rem' }}>
                ↑ 18% vs ciclo anterior
              </div>
            </div>

            <div className="upt-card" style={{ padding: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 700 }}>HORAS VISADAS OFICIALES</span>
                <span style={{ fontSize: '1.2rem' }}>⏱️</span>
              </div>
              <div style={{ fontSize: '1.85rem', fontWeight: 800, color: 'var(--accent-gold)' }}>
                96.5 hrs
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-body)', marginTop: '0.25rem' }}>
                Convalidables en Dirección
              </div>
            </div>

            <div className="upt-card" style={{ padding: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 700 }}>SATISFACCIÓN CSAT</span>
                <span style={{ fontSize: '1.2rem' }}>⭐</span>
              </div>
              <div style={{ fontSize: '1.85rem', fontWeight: 800, color: 'var(--primary-navy)' }}>
                4.88 / 5.0
              </div>
              <div style={{ fontSize: '0.75rem', color: '#137333', fontWeight: 600, marginTop: '0.25rem' }}>
                98% valoraciones positivas
              </div>
            </div>

            <div className="upt-card" style={{ padding: '1.25rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.5rem' }}>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)', fontWeight: 700 }}>ASISTENCIA QR EFECTIVA</span>
                <span style={{ fontSize: '1.2rem' }}>📱</span>
              </div>
              <div style={{ fontSize: '1.85rem', fontWeight: 800, color: '#1B873F' }}>
                94.2%
              </div>
              <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
                Tokens efímeros validados en aula
              </div>
            </div>
          </div>

          {/* Gráfica de Demanda y Riesgo por Asignatura */}
          <div style={{ display: 'grid', gridTemplateColumns: '1.5fr 1fr', gap: '1.5rem', marginBottom: '2rem' }}>
            <div className="upt-card">
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
                <div>
                  <h3 style={{ margin: 0, fontSize: '1.05rem', color: 'var(--primary-navy)' }}>
                    Materias Filtro con Mayor Demanda de Refuerzo
                  </h3>
                  <span style={{ fontSize: '0.76rem', color: 'var(--text-muted)' }}>
                    Indicador de impacto en deserción y reprobación semestral
                  </span>
                </div>
                <button
                  onClick={() => showNotification('Descargando dataset estadístico disociado (Ley N° 29733)...')}
                  style={{
                    background: 'none',
                    border: '1px solid var(--border-color)',
                    padding: '0.35rem 0.75rem',
                    borderRadius: '8px',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    cursor: 'pointer'
                  }}
                >
                  📥 Exportar CSV Anónimo
                </button>
              </div>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
                {[
                  { name: 'Cálculo I (CB-101)', demand: 88, sessions: 18, color: '#D9381E', failRate: '46% reprobación' },
                  { name: 'Algoritmos y Estructura de Datos (SI-301)', demand: 82, sessions: 15, color: '#E65100', failRate: '41% reprobación' },
                  { name: 'Cálculo II (CB-201)', demand: 76, sessions: 11, color: '#F57C00', failRate: '44% reprobación' },
                  { name: 'Programación Orientada a Objetos (SI-202)', demand: 64, sessions: 9, color: '#1C2A59', failRate: '32% reprobación' },
                  { name: 'Base de Datos I (SI-402)', demand: 52, sessions: 7, color: '#B99451', failRate: '28% reprobación' }
                ].map((item) => (
                  <div key={item.name}>
                    <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.25rem' }}>
                      <strong style={{ color: 'var(--primary-navy)' }}>{item.name}</strong>
                      <span style={{ color: 'var(--text-muted)' }}>
                        {item.sessions} sesiones • <span style={{ color: item.color, fontWeight: 700 }}>{item.failRate}</span>
                      </span>
                    </div>
                    <div style={{ height: '10px', backgroundColor: '#EDF2F7', borderRadius: '9999px', overflow: 'hidden' }}>
                      <div
                        style={{
                          height: '100%',
                          width: `${item.demand}%`,
                          backgroundColor: item.color,
                          borderRadius: '9999px',
                          transition: 'width 0.5s ease'
                        }}
                      />
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Modalidad y Gobernanza de Quórum */}
            <div className="upt-card">
              <h3 style={{ margin: 0, fontSize: '1.05rem', color: 'var(--primary-navy)', marginBottom: '0.25rem' }}>
                Control de Quórum y Logística
              </h3>
              <span style={{ fontSize: '0.76rem', color: 'var(--text-muted)', display: 'block', marginBottom: '1.25rem' }}>
                Monitoreo del corte perentorio en T-24h (RN-08/RN-09)
              </span>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
                <div style={{ padding: '0.85rem', backgroundColor: 'var(--bg-page)', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--primary-navy)' }}>Salas Virtuales Google Meet</span>
                    <span className="badge badge-navy" style={{ fontSize: '0.72rem' }}>62% del total</span>
                  </div>
                  <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Aforo máx: 25 participantes (RN-05)</span>
                </div>

                <div style={{ padding: '0.85rem', backgroundColor: 'var(--bg-page)', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--primary-navy)' }}>Laboratorios Físicos EPIS 1 y 2</span>
                    <span className="badge badge-gold" style={{ fontSize: '0.72rem' }}>38% del total</span>
                  </div>
                  <span style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>Aforo máx: 15 participantes presenciales</span>
                </div>

                <div style={{ padding: '0.85rem', backgroundColor: '#FEF7E0', borderRadius: '10px', border: '1px solid #FEEFC3' }}>
                  <strong style={{ fontSize: '0.8rem', color: '#B06000', display: 'block', marginBottom: '0.2rem' }}>
                    ⚠️ Sesiones en Contingencia (Quórum &lt; 50%)
                  </strong>
                  <p style={{ fontSize: '0.74rem', color: '#7A4100', margin: 0 }}>
                    1 sesión actual en evaluación en T-24h. Los mentores pueden ejercer dictado excepcional o cancelación solidaria sin penalización (RN-10).
                  </p>
                </div>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* 2. SUB-TAB: AUDITORÍA DE BITÁCORAS DOCENTES (CUS22 / RN-12 / RN-14) */}
      {activeAdminSubTab === 'audit' && (
        <div>
          <div className="upt-card" style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--primary-navy)' }}>
                  Bandeja de Bitácoras Docentes Pendientes de Visado
                </h3>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  Las horas permanecen provisionales hasta su aprobación por este Comité (RN-14).
                </span>
              </div>
              <span className="badge badge-navy">{logs.length} Bitácoras Registradas</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {logs.map((log) => {
                const isPending = log.status === 'REGISTRADA';
                const isApproved = log.status === 'VISADA';
                const isObserved = log.status === 'OBSERVADA';

                return (
                  <div
                    key={log.id}
                    style={{
                      border: `1.5px solid ${isApproved ? '#CEEAD6' : isObserved ? '#F8B4B4' : 'var(--accent-gold)'}`,
                      borderRadius: '14px',
                      padding: '1.25rem',
                      backgroundColor: isApproved ? '#FFFFFF' : isObserved ? '#FFF5F5' : '#FFFCF5',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.03)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.6rem' }}>
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                          <span className="badge badge-navy" style={{ fontSize: '0.7rem' }}>{log.subjectName}</span>
                          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>Fecha: {log.date}</span>
                        </div>
                        <h4 style={{ fontSize: '1.05rem', color: 'var(--primary-navy)', margin: '0.3rem 0' }}>
                          {log.topic}
                        </h4>
                      </div>

                      <span
                        className="badge"
                        style={{
                          backgroundColor: isApproved ? '#E6F4EA' : isObserved ? '#FDE8E8' : '#FEF7E0',
                          color: isApproved ? '#137333' : isObserved ? '#9B1C1C' : '#B06000',
                          fontWeight: 700,
                          fontSize: '0.75rem',
                          border: `1px solid ${isApproved ? '#CEEAD6' : isObserved ? '#F8B4B4' : '#FEEFC3'}`
                        }}
                      >
                        ● Estado: {log.status}
                      </span>
                    </div>

                    {/* Metadatos del Dictado */}
                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.75rem', fontSize: '0.8rem', backgroundColor: '#FFFFFF', padding: '0.75rem', borderRadius: '8px', border: '1px solid var(--border-color)', marginBottom: '0.75rem' }}>
                      <div>
                        <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.7rem' }}>Mentor Responsable:</span>
                        <strong>{log.mentorName}</strong> ({log.mentorCode})
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.7rem' }}>Horas Cronológicas:</span>
                        <strong style={{ color: 'var(--accent-gold-dark)' }}>{log.durationHours} horas</strong>
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.7rem' }}>Estudiantes con Asistencia QR:</span>
                        <span>{log.studentsAttended.join(', ')}</span>
                      </div>
                    </div>

                    <div style={{ fontSize: '0.84rem', color: 'var(--text-body)', marginBottom: '0.6rem' }}>
                      <strong style={{ color: 'var(--text-heading)' }}>Resumen Pedagógico: </strong>
                      {log.summary}
                    </div>

                    {log.observations && (
                      <div style={{ fontSize: '0.8rem', color: 'var(--text-muted)', fontStyle: 'italic', marginBottom: '0.6rem' }}>
                        Nota adicional: {log.observations}
                      </div>
                    )}

                    {log.auditFeedback && (
                      <div
                        style={{
                          fontSize: '0.8rem',
                          backgroundColor: isApproved ? '#F0FBF3' : '#FDF2F2',
                          color: isApproved ? '#137333' : '#9B1C1C',
                          padding: '0.5rem 0.75rem',
                          borderRadius: '8px',
                          marginBottom: '0.75rem',
                          borderLeft: `3px solid ${isApproved ? '#137333' : '#9B1C1C'}`
                        }}
                      >
                        <strong>Dictamen del Comité ({log.auditDate}): </strong>
                        {log.auditFeedback}
                        {log.hashSha256 && (
                          <div style={{ marginTop: '0.25rem', fontSize: '0.72rem', wordBreak: 'break-all' }}>
                            Hash de Validez: <code>{log.hashSha256}</code>
                          </div>
                        )}
                      </div>
                    )}

                    {/* Acciones de Auditoría */}
                    {isPending && (
                      <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'flex-end', borderTop: '1px dashed var(--border-color)', paddingTop: '0.75rem' }}>
                        <button
                          onClick={() => setSelectedLogForReview(log)}
                          style={{
                            backgroundColor: 'transparent',
                            border: '1.5px solid #F8B4B4',
                            color: '#9B1C1C',
                            padding: '0.45rem 1rem',
                            borderRadius: '9999px',
                            fontSize: '0.78rem',
                            fontWeight: 700,
                            cursor: 'pointer'
                          }}
                        >
                          ⚠️ Observar Bitácora
                        </button>

                        <button
                          className="btn-gold"
                          onClick={() => handleApproveLog(log.id)}
                          style={{
                            fontSize: '0.8rem',
                            padding: '0.45rem 1.2rem',
                            boxShadow: '0 2px 8px rgba(185, 148, 81, 0.25)'
                          }}
                        >
                          ✓ Visar Horas (Aprobar Oficialmente)
                        </button>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>

          {/* Modal de Observación */}
          {selectedLogForReview && (
            <div
              style={{
                position: 'fixed',
                top: 0,
                left: 0,
                right: 0,
                bottom: 0,
                backgroundColor: 'rgba(23, 35, 73, 0.6)',
                backdropFilter: 'blur(4px)',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                zIndex: 1000,
                padding: '1rem'
              }}
            >
              <div className="upt-card" style={{ maxWidth: '540px', width: '100%', padding: '1.75rem' }}>
                <h3 style={{ fontSize: '1.15rem', color: '#9B1C1C', marginBottom: '0.4rem' }}>
                  Emitir Pliego de Observaciones Pedagógicas
                </h3>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-body)', marginBottom: '1rem' }}>
                  Especifica los puntos a subsanar por el mentor <strong>{selectedLogForReview.mentorName}</strong> para la sesión <em>"{selectedLogForReview.topic}"</em> (Plazo reglamentario: 48h).
                </p>

                <textarea
                  value={observationInput}
                  onChange={(e) => setObservationInput(e.target.value)}
                  placeholder="Detalla las evidencias faltantes (ej: adjuntar ejercicios resueltos en GitHub, captura de nómina QR)..."
                  rows={4}
                  style={{
                    width: '100%',
                    padding: '0.75rem',
                    borderRadius: '8px',
                    border: '1.5px solid var(--border-color)',
                    fontFamily: 'inherit',
                    fontSize: '0.85rem',
                    marginBottom: '1rem',
                    outline: 'none'
                  }}
                />

                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
                  <button
                    onClick={() => setSelectedLogForReview(null)}
                    style={{
                      background: 'none',
                      border: '1px solid var(--border-color)',
                      padding: '0.45rem 1rem',
                      borderRadius: '9999px',
                      fontSize: '0.82rem',
                      cursor: 'pointer'
                    }}
                  >
                    Cancelar
                  </button>
                  <button
                    onClick={() => handleObserveLog(selectedLogForReview.id)}
                    style={{
                      backgroundColor: '#9B1C1C',
                      color: '#FFFFFF',
                      border: 'none',
                      padding: '0.45rem 1.2rem',
                      borderRadius: '9999px',
                      fontSize: '0.82rem',
                      fontWeight: 700,
                      cursor: 'pointer'
                    }}
                  >
                    Notificar Observación
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>
      )}

      {/* 3. SUB-TAB: EMISIÓN DE CERTIFICADOS CON HASH SHA-256 (CUS13 / RN-14) */}
      {activeAdminSubTab === 'certificates' && (
        <div>
          {/* Panel de Emisión de Nueva Constancia */}
          <div className="upt-card" style={{ marginBottom: '2rem', border: '1.5px solid var(--accent-gold)' }}>
            <h3 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--primary-navy)', marginBottom: '0.35rem' }}>
              Emitir Nueva Constancia Oficial Foliada (CUS13)
            </h3>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-body)', marginBottom: '1.25rem' }}>
              Solo mentores con horas previamente auditadas y en estado <code>VISADA</code> son elegibles para certificación oficial.
            </p>

            <div style={{ display: 'flex', gap: '1rem', alignItems: 'flex-end', flexWrap: 'wrap' }}>
              <div style={{ flex: 1, minWidth: '260px' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.35rem', color: 'var(--text-heading)' }}>
                  Seleccionar Mentor Elegible:
                </label>
                <select
                  value={selectedMentorForNewCert}
                  onChange={(e) => setSelectedMentorForNewCert(e.target.value)}
                  style={{
                    width: '100%',
                    padding: '0.6rem 0.8rem',
                    borderRadius: '8px',
                    border: '1.5px solid var(--border-color)',
                    fontSize: '0.88rem',
                    fontFamily: 'inherit',
                    backgroundColor: 'var(--bg-page)'
                  }}
                >
                  {MOCK_MENTORS.map((m) => (
                    <option key={m.id} value={m.name}>
                      {m.name} ({m.code}) — {m.totalHours} hrs acumuladas
                    </option>
                  ))}
                </select>
              </div>

              <button
                className="btn-gold"
                onClick={handleIssueCertificate}
                style={{ padding: '0.65rem 1.4rem', fontSize: '0.85rem' }}
              >
                📜 Emitir Certificado con Hash SHA-256
              </button>
            </div>
          </div>

          {/* Listado de Certificados Emitidos */}
          <div className="upt-card">
            <h3 style={{ margin: 0, fontSize: '1.05rem', color: 'var(--primary-navy)', marginBottom: '1rem' }}>
              Registro de Certificados Emitidos con Fe Pública
            </h3>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {certificates.map((cert) => (
                <div
                  key={cert.folio}
                  style={{
                    border: '1px solid var(--border-color)',
                    borderRadius: '12px',
                    padding: '1.25rem',
                    backgroundColor: '#FFFFFF',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    flexWrap: 'wrap',
                    gap: '1rem'
                  }}
                >
                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', marginBottom: '0.25rem' }}>
                      <span className="badge badge-gold" style={{ fontSize: '0.72rem' }}>{cert.folio}</span>
                      <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>Emitido el {cert.issueDate}</span>
                    </div>
                    <h4 style={{ fontSize: '1rem', color: 'var(--primary-navy)', margin: '0.2rem 0' }}>
                      {cert.mentorName} (Cód: {cert.mentorCode})
                    </h4>
                    <span style={{ fontSize: '0.82rem', color: 'var(--accent-gold-dark)', fontWeight: 700 }}>
                      {cert.hoursValidated} Horas Académicas Convalidadas • {cert.semester}
                    </span>
                    <div style={{ fontSize: '0.72rem', color: 'var(--text-muted)', marginTop: '0.35rem' }}>
                      Hash: <code style={{ color: 'var(--primary-blue)' }}>{cert.hashSha256.substring(0, 36)}...</code>
                    </div>
                  </div>

                  <button
                    className="btn-pill-navy"
                    onClick={() => setViewingCertificate(cert)}
                    style={{ fontSize: '0.82rem', padding: '0.5rem 1.2rem' }}
                  >
                    👁️ Ver Documento Oficial →
                  </button>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 4. SUB-TAB: BONIFICACIÓN CURRICULAR DIRECTIVA (CUS12 / RN-11) */}
      {activeAdminSubTab === 'curriculum' && (
        <div className="upt-card">
          <div style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.3rem' }}>
              <span className="badge badge-gold">Directiva Académica RN-11</span>
              <span className="badge badge-navy">Motor de Recomendación</span>
            </div>
            <h3 style={{ fontSize: '1.15rem', color: 'var(--primary-navy)', margin: '0.2rem 0' }}>
              Ponderación Algorítmica de Materias Filtro (Factor α)
            </h3>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-body)', maxWidth: '750px' }}>
              La Dirección EPIS puede ajustar el factor multiplicador <code>α ∈ [1.05, 1.50]</code> para bonificar la visibilidad de los mentores en los cursos con más alta tasa de reprobación. Al actualizar, se invalida la caché Redis del recomendador.
            </p>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
            {subjectPriorities.map((item) => (
              <div
                key={item.id}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '1.25rem',
                  borderRadius: '12px',
                  backgroundColor: item.isPriorityBoosted ? 'rgba(185, 148, 81, 0.08)' : 'var(--bg-page)',
                  border: `1.5px solid ${item.isPriorityBoosted ? 'var(--accent-gold)' : 'var(--border-color)'}`,
                  flexWrap: 'wrap',
                  gap: '1rem'
                }}
              >
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <h4 style={{ fontSize: '0.98rem', color: 'var(--primary-navy)', margin: 0 }}>
                      {item.subjectName}
                    </h4>
                    {item.isPriorityBoosted && (
                      <span className="badge badge-gold" style={{ fontSize: '0.65rem' }}>
                        ★ Prioridad Activa
                      </span>
                    )}
                  </div>
                  <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                    Reprobación histórica estimada: <strong>{item.failRateEstimated}%</strong>
                  </span>
                </div>

                <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
                  <div>
                    <label style={{ display: 'block', fontSize: '0.7rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '0.2rem' }}>
                      Factor de Bonificación (α):
                    </label>
                    <select
                      value={item.criticalFactorAlpha}
                      onChange={(e) => handleUpdateAlpha(item.id, parseFloat(e.target.value))}
                      style={{
                        padding: '0.35rem 0.6rem',
                        borderRadius: '6px',
                        border: '1px solid var(--border-color)',
                        fontWeight: 700,
                        color: 'var(--primary-navy)',
                        backgroundColor: '#FFFFFF'
                      }}
                    >
                      <option value="1.05">α = 1.05 (+5%)</option>
                      <option value="1.15">α = 1.15 (+15%)</option>
                      <option value="1.25">α = 1.25 (+25%)</option>
                      <option value="1.35">α = 1.35 (+35%)</option>
                      <option value="1.50">α = 1.50 (+50% Máx)</option>
                    </select>
                  </div>

                  <button
                    onClick={() => handleTogglePriority(item.id)}
                    style={{
                      padding: '0.45rem 0.9rem',
                      borderRadius: '9999px',
                      border: 'none',
                      fontSize: '0.78rem',
                      fontWeight: 700,
                      cursor: 'pointer',
                      backgroundColor: item.isPriorityBoosted ? 'var(--primary-navy)' : 'var(--border-color)',
                      color: item.isPriorityBoosted ? '#FFFFFF' : 'var(--text-body)'
                    }}
                  >
                    {item.isPriorityBoosted ? 'Desactivar Bonificación' : 'Activar Bonificación'}
                  </button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Modal del Certificado Oficial */}
      <CertificateModal
        certificate={viewingCertificate}
        isOpen={Boolean(viewingCertificate)}
        onClose={() => setViewingCertificate(null)}
      />
    </div>
  );
};
