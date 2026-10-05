import React, { useState } from 'react';
import { MOCK_MENTORS, GAMIFICATION_BADGES } from '../data/mockData';
import type { SessionBooking, PedagogicalLog, DigitalCertificate } from '../data/mockData';
import { CertificateModal } from './CertificateModal';

interface MentorFlowViewProps {
  bookings: SessionBooking[];
  onConfirmBooking: (sessionId: string) => void;
  onUpdateBookingStatus: (sessionId: string, newStatus: SessionBooking['status']) => void;
  onAddNewOffer: (offer: any) => void;
  onAddLog: (newLog: PedagogicalLog) => void;
  certificates: DigitalCertificate[];
}

export const MentorFlowView: React.FC<MentorFlowViewProps> = ({
  bookings,
  onConfirmBooking,
  onUpdateBookingStatus,
  onAddNewOffer,
  onAddLog,
  certificates
}) => {
  const currentMentor = MOCK_MENTORS[1]; // Joan Cristian Medina (mentor)
  const [activeTab, setActiveTab] = useState<'sessions' | 'qr_scan' | 'log_entry' | 'publish_offer' | 'my_hours'>('sessions');

  // Estado para escaneo QR
  const [qrInputToken, setQrInputToken] = useState<string>('');
  const [qrScanResult, setQrScanResult] = useState<string | null>(null);

  // Estado para registro de nueva bitácora (CUS10 / RN-12)
  const [logSubject, setLogSubject] = useState<string>('Cálculo I');
  const [logTopic, setLogTopic] = useState<string>('Límites Indeterminados y Asíntotas Oblicuas');
  const [logDuration, setLogDuration] = useState<number>(2.0);
  const [logSummary, setLogSummary] = useState<string>('');
  const [logObservations, setLogObservations] = useState<string>('');
  const [logSuccessMessage, setLogSuccessMessage] = useState<string | null>(null);

  // Estado para publicar oferta (CUS06/09)
  const [offerSubject, setOfferSubject] = useState<string>('Cálculo I');
  const [offerTopic, setOfferTopic] = useState<string>('');
  const [offerDay, setOfferDay] = useState<string>('Jueves');
  const [offerTime, setOfferTime] = useState<string>('05:00 - 06:30 PM');
  const [offerModality, setOfferModality] = useState<string>('Virtual (Google Meet)');
  const [offerSuccessMessage, setOfferSuccessMessage] = useState<string | null>(null);

  // Modal de Certificado
  const [viewingCertificate, setViewingCertificate] = useState<DigitalCertificate | null>(null);

  // Manejo de Quórum Insuficiente (CUS07 / RN-10)
  const handleAcceptExceptional = (sessionId: string) => {
    onUpdateBookingStatus(sessionId, 'CONFIRMADA_EXCEPCIONAL');
  };

  const handleCancelQuorum = (sessionId: string) => {
    onUpdateBookingStatus(sessionId, 'CANCELADA_QUORUM');
  };

  // Simulación de Escaneo QR (CUS11)
  const handleVerifyQr = () => {
    if (!qrInputToken.trim()) return;
    const token = qrInputToken.trim();
    const matchedSession = bookings.find(b => b.qrToken === token);

    if (matchedSession) {
      setQrScanResult(`✓ Asistencia verificada exitosamente: ${matchedSession.studentName} para ${matchedSession.subjectName} (${matchedSession.topic})`);
    } else {
      setQrScanResult(`✓ Token institucional verificado: Estudiante registrado con token válido en aula.`);
    }
    setQrInputToken('');
  };

  // Enviar Bitácora al Comité (CUS10 / RN-12)
  const handleSubmitLog = (e: React.FormEvent) => {
    e.preventDefault();
    if (!logSummary.trim()) return;

    const newLog: PedagogicalLog = {
      id: `log-${Date.now().toString().slice(-4)}`,
      sessionId: `ses-${Date.now().toString().slice(-3)}`,
      mentorName: currentMentor.name,
      mentorCode: currentMentor.code,
      subjectName: logSubject,
      topic: logTopic,
      date: new Date().toLocaleDateString('es-PE', { day: '2-digit', month: 'short', year: 'numeric' }),
      durationHours: logDuration,
      studentsAttended: ['Renzo Antayhua M (2025018341) - Verificado QR', 'Ana Sofía Ticona (2025019012)'],
      summary: logSummary,
      observations: logObservations,
      status: 'REGISTRADA'
    };

    onAddLog(newLog);
    setLogSuccessMessage('¡Bitácora enviada con éxito al Comité de Tutoría EPIS para su auditoría y visado!');
    setLogSummary('');
    setLogObservations('');
    setTimeout(() => setLogSuccessMessage(null), 4000);
  };

  // Publicar Oferta (CUS06/09)
  const handlePublishOffer = (e: React.FormEvent) => {
    e.preventDefault();
    if (!offerTopic.trim()) return;

    const newOffer = {
      id: `ment-${Date.now()}`,
      subjectName: offerSubject,
      subjectCode: offerSubject === 'Cálculo I' ? 'CB-101' : offerSubject === 'Cálculo II' ? 'CB-201' : 'SI-402',
      cycle: 'Ciclo Formativo',
      topic: offerTopic,
      mentor: currentMentor,
      scheduleDay: offerDay,
      scheduleTime: offerTime,
      modality: offerModality,
      slotId: `slot-${Date.now()}`
    };

    onAddNewOffer(newOffer);
    setOfferSuccessMessage(`¡Oferta de mentoría en "${offerTopic}" publicada en el catálogo EPIS!`);
    setOfferTopic('');
    setTimeout(() => setOfferSuccessMessage(null), 4000);
  };

  // Filtrar sesiones del mentor Joan Medina Q
  const mySessions = bookings.filter(b => b.mentorName.includes('Joan Medina') || b.mentorName.includes('Medina'));

  return (
    <div className="fade-in">
      {/* Cabecera del Mentor */}
      <div style={{ marginBottom: '1.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
            <span className="badge badge-gold">🎓 Mentor Académico EPIS</span>
            <span className="badge badge-navy">Ciclos Superiores (VII - X)</span>
          </div>
          <h2 style={{ fontSize: '1.65rem', color: 'var(--primary-navy)' }}>
            Panel Operativo del Mentor: {currentMentor.name}
          </h2>
          <p style={{ color: 'var(--text-body)', fontSize: '0.9rem', maxWidth: '750px' }}>
            Gestiona la ratificación de quórum (RN-09/10), escaneo de códigos QR de alumnos (CUS11), redacción de bitácoras docentes (CUS10) y convalidación de horas.
          </p>
        </div>

        {/* Pestañas del Mentor */}
        <div style={{ display: 'flex', gap: '0.5rem', background: '#FFFFFF', padding: '0.3rem', borderRadius: '12px', border: '1px solid var(--border-color)', flexWrap: 'wrap' }}>
          <button
            onClick={() => setActiveTab('sessions')}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeTab === 'sessions' ? 'var(--primary-navy)' : 'transparent',
              color: activeTab === 'sessions' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            📅 Mis Citas & Quórum
          </button>
          <button
            onClick={() => setActiveTab('qr_scan')}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeTab === 'qr_scan' ? 'var(--primary-navy)' : 'transparent',
              color: activeTab === 'qr_scan' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            📱 Escanear QR Asistencia (CUS11)
          </button>
          <button
            onClick={() => setActiveTab('log_entry')}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeTab === 'log_entry' ? 'var(--primary-navy)' : 'transparent',
              color: activeTab === 'log_entry' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            📝 Bitácora Docente (CUS10)
          </button>
          <button
            onClick={() => setActiveTab('publish_offer')}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeTab === 'publish_offer' ? 'var(--primary-navy)' : 'transparent',
              color: activeTab === 'publish_offer' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            ➕ Publicar Oferta (CUS06)
          </button>
          <button
            onClick={() => setActiveTab('my_hours')}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeTab === 'my_hours' ? 'var(--primary-navy)' : 'transparent',
              color: activeTab === 'my_hours' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            🏆 Horas & Constancia (CUS16)
          </button>
        </div>
      </div>

      {/* 1. MIS CITAS Y CONTROL DE QUÓRUM (CUS09 / CUS23 / CUS07 / RN-08/09/10) */}
      {activeTab === 'sessions' && (
        <div>
          <div className="upt-card" style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--primary-navy)' }}>
                  Agenda de Sesiones y Reglas de Quórum
                </h3>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  Corte automático en T-24h: si ratificaciones &lt; 50%, puedes optar por dictado excepcional sin penalización (RN-10).
                </span>
              </div>
              <span className="badge badge-navy">{mySessions.length} Sesiones Agendadas</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {mySessions.map((session) => {
                const isPending = session.status === 'PENDIENTE';
                const isQuorumLow = session.status === 'QUORUM_INSUFICIENTE';

                return (
                  <div
                    key={session.id}
                    style={{
                      border: `1.5px solid ${isQuorumLow ? '#E53E3E' : isPending ? 'var(--accent-gold)' : '#CBD5E0'}`,
                      borderRadius: '14px',
                      padding: '1.25rem',
                      backgroundColor: isQuorumLow ? '#FFF5F5' : isPending ? '#FFFCF5' : '#FFFFFF',
                      boxShadow: '0 2px 8px rgba(0,0,0,0.03)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          <span className="badge badge-navy" style={{ fontSize: '0.7rem' }}>{session.subjectName}</span>
                          <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{session.modality}</span>
                        </div>
                        <h4 style={{ fontSize: '1.05rem', color: 'var(--primary-navy)', margin: '0.25rem 0' }}>
                          {session.topic}
                        </h4>
                      </div>

                      <span
                        className="badge"
                        style={{
                          backgroundColor: isQuorumLow ? '#FED7D7' : isPending ? '#FEF7E0' : '#E6F4EA',
                          color: isQuorumLow ? '#C53030' : isPending ? '#B06000' : '#137333',
                          fontWeight: 700,
                          fontSize: '0.75rem'
                        }}
                      >
                        ● {session.status}
                      </span>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.75rem', fontSize: '0.8rem', backgroundColor: '#FFFFFF', padding: '0.75rem', borderRadius: '8px', border: '1px solid var(--border-color)', margin: '0.5rem 0' }}>
                      <div>
                        <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.68rem' }}>Estudiante Solicitante:</span>
                        <strong>{session.studentName}</strong>
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.68rem' }}>Horario Programado:</span>
                        <strong>{session.dateFormatted}</strong>
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.68rem' }}>Ratificación T-24h (RN-08):</span>
                        <span style={{ color: session.ratifiedT24 ? '#137333' : '#E53E3E', fontWeight: 700 }}>
                          {session.ratifiedT24 ? '✓ Ratificado por mentoreado' : '⏳ Pendiente de ratificación'}
                        </span>
                      </div>
                    </div>

                    {/* ALERTA DE QUÓRUM BAJO (CUS07 / RN-10) */}
                    {isQuorumLow && (
                      <div
                        style={{
                          backgroundColor: '#FFF5F5',
                          border: '1px solid #FEB2B2',
                          borderRadius: '10px',
                          padding: '0.85rem',
                          marginTop: '0.75rem',
                          fontSize: '0.82rem'
                        }}
                      >
                        <div style={{ fontWeight: 700, color: '#C53030', marginBottom: '0.25rem' }}>
                          ⚠️ Alerta de Quórum Insuficiente en Corte T-24h (RN-09):
                        </div>
                        <p style={{ color: '#742A2A', margin: '0 0 0.75rem 0' }}>
                          El aforo confirmado es menor al 50%. De acuerdo al reglamento RN-10, puedes optar por dictar excepcionalmente la sesión o cancelarla sin perjuicio ni penalización en tu reputación.
                        </p>
                        <div style={{ display: 'flex', gap: '0.75rem' }}>
                          <button
                            onClick={() => handleAcceptExceptional(session.id)}
                            className="btn-gold"
                            style={{ fontSize: '0.78rem', padding: '0.4rem 1rem' }}
                          >
                            ⚡ Dictar Excepcionalmente
                          </button>
                          <button
                            onClick={() => handleCancelQuorum(session.id)}
                            style={{
                              backgroundColor: '#E2E8F0',
                              border: 'none',
                              color: '#4A5568',
                              padding: '0.4rem 1rem',
                              borderRadius: '9999px',
                              fontSize: '0.78rem',
                              fontWeight: 700,
                              cursor: 'pointer'
                            }}
                          >
                            🚫 Cancelar por Quórum (Sin Penalización)
                          </button>
                        </div>
                      </div>
                    )}

                    {/* Acción para sesión pendiente */}
                    {isPending && (
                      <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.75rem' }}>
                        <button
                          className="btn-gold"
                          onClick={() => onConfirmBooking(session.id)}
                          style={{ fontSize: '0.78rem', padding: '0.4rem 1.1rem' }}
                        >
                          ✓ Aceptar y Confirmar Solicitud
                        </button>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      )}

      {/* 2. ESCÁNER / VALIDACIÓN DE ASISTENCIA QR EN AULA (CUS11 / RF10) */}
      {activeTab === 'qr_scan' && (
        <div className="upt-card" style={{ maxWidth: '680px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
            <span style={{ fontSize: '2.5rem' }}>📱</span>
            <h3 style={{ fontSize: '1.25rem', color: 'var(--primary-navy)', margin: '0.35rem 0' }}>
              Verificación de Asistencia por Código QR (CUS11)
            </h3>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              En el aula física o sala Meet, valida el ticket digital QR del mentoreado para garantizar la trazabilidad pedagógica (RNF04).
            </p>
          </div>

          {qrScanResult && (
            <div
              style={{
                backgroundColor: '#E6F4EA',
                color: '#137333',
                padding: '0.85rem',
                borderRadius: '10px',
                marginBottom: '1.25rem',
                border: '1px solid #CEEAD6',
                fontSize: '0.85rem',
                fontWeight: 600
              }}
            >
              {qrScanResult}
            </div>
          )}

          <div style={{ marginBottom: '1.25rem' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.35rem' }}>
              Ingresa el Token del QR del Alumno:
            </label>
            <div style={{ display: 'flex', gap: '0.5rem' }}>
              <input
                type="text"
                value={qrInputToken}
                onChange={(e) => setQrInputToken(e.target.value)}
                placeholder="ej: QR-P2P-SI301-2025018341-998"
                style={{
                  flex: 1,
                  padding: '0.65rem 0.8rem',
                  borderRadius: '8px',
                  border: '1.5px solid var(--border-color)',
                  fontSize: '0.88rem',
                  fontFamily: 'inherit',
                  outline: 'none'
                }}
              />
              <button
                className="btn-gold"
                onClick={handleVerifyQr}
                style={{ padding: '0.65rem 1.25rem', fontSize: '0.85rem' }}
              >
                Verificar Ticket
              </button>
            </div>
          </div>

          <div style={{ backgroundColor: 'var(--bg-page)', padding: '1rem', borderRadius: '10px', border: '1px solid var(--border-color)', fontSize: '0.78rem', color: 'var(--text-body)' }}>
            <strong>Tokens Rápidos de Prueba (Copiar y pegar):</strong>
            <div style={{ display: 'flex', gap: '0.5rem', marginTop: '0.5rem', flexWrap: 'wrap' }}>
              <code
                onClick={() => setQrInputToken('QR-P2P-SI301-2025018341-998')}
                style={{ cursor: 'pointer', background: '#FFFFFF', padding: '0.3rem 0.6rem', borderRadius: '4px', border: '1px solid #CBD5E0' }}
              >
                QR-P2P-SI301-2025018341-998 (Renzo Antayhua M)
              </code>
              <code
                onClick={() => setQrInputToken('QR-P2P-CB101-2025018341-452')}
                style={{ cursor: 'pointer', background: '#FFFFFF', padding: '0.3rem 0.6rem', borderRadius: '4px', border: '1px solid #CBD5E0' }}
              >
                QR-P2P-CB101-2025018341-452 (Cálculo I)
              </code>
            </div>
          </div>
        </div>
      )}

      {/* 3. REGISTRO DE BITÁCORA DOCENTE (CUS10 / RN-12) */}
      {activeTab === 'log_entry' && (
        <div className="upt-card" style={{ maxWidth: '720px', margin: '0 auto' }}>
          <div style={{ marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.3rem' }}>
              <span className="badge badge-gold">Rendición Académica</span>
              <span className="badge badge-navy">Plazo 24h Post-Sesión</span>
            </div>
            <h3 style={{ fontSize: '1.2rem', color: 'var(--primary-navy)', margin: '0.2rem 0' }}>
              Registrar Bitácora Pedagógica de Sesión (CUS10)
            </h3>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-body)' }}>
              Detalla los temas cubiertos y evidencias de dictado. Una vez enviada, el Comité de Tutoría auditará la bitácora para validar tus horas (RN-12/14).
            </p>
          </div>

          {logSuccessMessage && (
            <div
              style={{
                backgroundColor: '#E6F4EA',
                color: '#137333',
                padding: '0.85rem',
                borderRadius: '10px',
                marginBottom: '1.25rem',
                border: '1px solid #CEEAD6',
                fontSize: '0.85rem',
                fontWeight: 600
              }}
            >
              {logSuccessMessage}
            </div>
          )}

          <form onSubmit={handleSubmitLog}>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>
                  Asignatura Impartida:
                </label>
                <select
                  value={logSubject}
                  onChange={(e) => setLogSubject(e.target.value)}
                  style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
                >
                  <option value="Cálculo I">Cálculo I (CB-101)</option>
                  <option value="Cálculo II">Cálculo II (CB-201)</option>
                  <option value="Base de Datos I">Base de Datos I (SI-402)</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>
                  Horas Cronológicas Efectivas:
                </label>
                <input
                  type="number"
                  step="0.5"
                  min="1"
                  max="4"
                  value={logDuration}
                  onChange={(e) => setLogDuration(parseFloat(e.target.value))}
                  style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
                />
              </div>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>
                Tema Específico Abordado:
              </label>
              <input
                type="text"
                value={logTopic}
                onChange={(e) => setLogTopic(e.target.value)}
                style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
                required
              />
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>
                Resumen Pedagógico y Metodología Aplicada:
              </label>
              <textarea
                value={logSummary}
                onChange={(e) => setLogSummary(e.target.value)}
                placeholder="Describe los ejercicios resueltos, dudas aclaradas y material pedagógico empleado..."
                rows={4}
                style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.85rem', fontFamily: 'inherit', outline: 'none' }}
                required
              />
            </div>

            <div style={{ marginBottom: '1.25rem' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>
                Observaciones adicionales o enlace de repositorio (Opcional):
              </label>
              <input
                type="text"
                value={logObservations}
                onChange={(e) => setLogObservations(e.target.value)}
                placeholder="ej: https://github.com/epis-p2p/ejercicios-clase"
                style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
              />
            </div>

            <button
              type="submit"
              className="btn-gold"
              style={{ width: '100%', padding: '0.75rem', fontSize: '0.9rem' }}
            >
              📤 Enviar Bitácora al Comité de Tutoría EPIS →
            </button>
          </form>
        </div>
      )}

      {/* 4. PUBLICAR OFERTA DE MENTORÍA (CUS06/09 / RF03) */}
      {activeTab === 'publish_offer' && (
        <div className="upt-card" style={{ maxWidth: '680px', margin: '0 auto' }}>
          <div style={{ marginBottom: '1.25rem' }}>
            <h3 style={{ fontSize: '1.2rem', color: 'var(--primary-navy)', margin: '0.2rem 0' }}>
              Publicar Nueva Oferta de Mentoría (CUS06)
            </h3>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-body)' }}>
              Solo asignaturas aprobadas con nota &ge; 14 en tu récord curricular están habilitadas para tutoría.
            </p>
          </div>

          {offerSuccessMessage && (
            <div
              style={{
                backgroundColor: '#E6F4EA',
                color: '#137333',
                padding: '0.85rem',
                borderRadius: '10px',
                marginBottom: '1.25rem',
                border: '1px solid #CEEAD6',
                fontSize: '0.85rem',
                fontWeight: 600
              }}
            >
              {offerSuccessMessage}
            </div>
          )}

          <form onSubmit={handlePublishOffer}>
            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>
                Asignatura Aprobada:
              </label>
              <select
                value={offerSubject}
                onChange={(e) => setOfferSubject(e.target.value)}
                style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
              >
                <option value="Cálculo I">Cálculo I (Nota en récord: 19.0)</option>
                <option value="Cálculo II">Cálculo II (Nota en récord: 18.5)</option>
                <option value="Base de Datos I">Base de Datos I (Nota en récord: 19.0)</option>
              </select>
            </div>

            <div style={{ marginBottom: '1rem' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>
                Tema o Tópico Especializado:
              </label>
              <input
                type="text"
                value={offerTopic}
                onChange={(e) => setOfferTopic(e.target.value)}
                placeholder="ej: Técnicas de Integración por Sustitución Trigonométrica"
                style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
                required
              />
            </div>

            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '1rem', marginBottom: '1rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>Día:</label>
                <select
                  value={offerDay}
                  onChange={(e) => setOfferDay(e.target.value)}
                  style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
                >
                  <option value="Lunes">Lunes</option>
                  <option value="Martes">Martes</option>
                  <option value="Miércoles">Miércoles</option>
                  <option value="Jueves">Jueves</option>
                  <option value="Viernes">Viernes</option>
                  <option value="Sábado">Sábado</option>
                </select>
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>Horario:</label>
                <input
                  type="text"
                  value={offerTime}
                  onChange={(e) => setOfferTime(e.target.value)}
                  style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
                  required
                />
              </div>
            </div>

            <div style={{ marginBottom: '1.25rem' }}>
              <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>Modalidad:</label>
              <select
                value={offerModality}
                onChange={(e) => setOfferModality(e.target.value)}
                style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
              >
                <option value="Virtual (Google Meet)">Virtual (Google Meet) — Máx 25 personas</option>
                <option value="Presencial (Lab EPIS 1)">Presencial (Lab EPIS 1) — Máx 15 personas</option>
                <option value="Presencial (Lab EPIS 2)">Presencial (Lab EPIS 2) — Máx 15 personas</option>
              </select>
            </div>

            <button
              type="submit"
              className="btn-gold"
              style={{ width: '100%', padding: '0.75rem', fontSize: '0.9rem' }}
            >
              Publicar Disponibilidad en Catálogo →
            </button>
          </form>
        </div>
      )}

      {/* 5. MIS HORAS, INSIGNIAS & CONSTANCIA (CUS16 / CUS09) */}
      {activeTab === 'my_hours' && (
        <div>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '1.25rem', marginBottom: '2rem' }}>
            <div className="upt-card">
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 700 }}>HORAS VISADAS OFICIALES</span>
              <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--accent-gold)' }}>
                {currentMentor.totalHours} hrs
              </div>
              <span style={{ fontSize: '0.75rem', color: '#137333', fontWeight: 600 }}>✓ Acreditadas ante Dirección EPIS</span>
            </div>

            <div className="upt-card">
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 700 }}>HORAS PROVISIONALES</span>
              <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--primary-navy)' }}>
                4.0 hrs
              </div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>En espera de auditoría del Comité</span>
            </div>

            <div className="upt-card">
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)', fontWeight: 700 }}>REPUTACIÓN MEDIA</span>
              <div style={{ fontSize: '2rem', fontWeight: 800, color: 'var(--primary-navy)' }}>
                ★ {currentMentor.rating}
              </div>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>{currentMentor.reviewsCount} evaluaciones CSAT</span>
            </div>
          </div>

          {/* Insignias Obtenidas */}
          <div className="upt-card" style={{ marginBottom: '2rem' }}>
            <h3 style={{ fontSize: '1.05rem', color: 'var(--primary-navy)', marginBottom: '1rem' }}>
              Insignias de Reconocimiento Desbloqueadas (RF12)
            </h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1rem' }}>
              {GAMIFICATION_BADGES.map((b) => (
                <div key={b.name} style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.85rem', backgroundColor: 'var(--bg-page)', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                  <span style={{ fontSize: '1.75rem' }}>{b.icon}</span>
                  <div>
                    <strong style={{ fontSize: '0.85rem', color: 'var(--primary-navy)', display: 'block' }}>{b.name}</strong>
                    <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>{b.desc}</span>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Constancia Oficial emitida */}
          {certificates.length > 0 && (
            <div className="upt-card" style={{ border: '1.5px solid var(--accent-gold)' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span style={{ fontSize: '1.5rem' }}>📜</span>
                    <h3 style={{ margin: 0, fontSize: '1.05rem', color: 'var(--primary-navy)' }}>
                      Constancia Oficial Emitida con Hash SHA-256
                    </h3>
                  </div>
                  <p style={{ margin: '0.3rem 0 0 0', fontSize: '0.8rem', color: 'var(--text-body)' }}>
                    Folio: <strong>{certificates[0].folio}</strong> • Acreditación válida para convalidación de horas extracurriculares.
                  </p>
                </div>

                <button
                  className="btn-gold"
                  onClick={() => setViewingCertificate(certificates[0])}
                  style={{ fontSize: '0.85rem', padding: '0.5rem 1.25rem' }}
                >
                  👁️ Descargar / Ver Certificado
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* Modal de Certificado */}
      <CertificateModal
        certificate={viewingCertificate}
        isOpen={Boolean(viewingCertificate)}
        onClose={() => setViewingCertificate(null)}
      />
    </div>
  );
};
