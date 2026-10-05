import React, { useState } from 'react';
import {
  CRITICAL_SUBJECTS,
  MOCK_MENTORS,
  INITIAL_DEMAND_REQUESTS
} from '../data/mockData';
import type { Mentor, SessionBooking, DemandRequest } from '../data/mockData';

interface MenteeFlowViewProps {
  bookings: SessionBooking[];
  onRatifyAttendance: (sessionId: string) => void;
  onOpenConsentModal: () => void;
  hasAcceptedConsent: boolean;
  onSelectMentorForBooking: (mentor: Mentor, topic: string) => void;
}

export const MenteeFlowView: React.FC<MenteeFlowViewProps> = ({
  bookings,
  onRatifyAttendance,
  onOpenConsentModal,
  hasAcceptedConsent,
  onSelectMentorForBooking
}) => {
  const [activeTab, setActiveTab] = useState<'recommendation' | 'my_bookings' | 'demand_request' | 'survey'>('recommendation');

  // Estado para Recomendación Top-k (CUS02 / RF07)
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>(CRITICAL_SUBJECTS[0].id);
  const [selectedTopic, setSelectedTopic] = useState<string>(CRITICAL_SUBJECTS[0].topics[0]);
  const [isCalculating, setIsCalculating] = useState<boolean>(false);

  // Estado para Solicitud de Demanda Temática (CUS03 / RF04)
  const [demands, setDemands] = useState<DemandRequest[]>(INITIAL_DEMAND_REQUESTS);
  const [demandSubject, setDemandSubject] = useState<string>('Programación Orientada a Objetos');
  const [demandTopic, setDemandTopic] = useState<string>('');
  const [demandDesc, setDemandDesc] = useState<string>('');
  const [demandModality, setDemandModality] = useState<string>('Virtual (Meet)');
  const [demandSuccessMessage, setDemandSuccessMessage] = useState<string | null>(null);

  // Estado para Ticket QR Modal (CUS11)
  const [selectedTicketSession, setSelectedTicketSession] = useState<SessionBooking | null>(null);

  // Estado para Encuesta de Calidad CSAT (CUS05 / RF11)
  const [surveyRating, setSurveyRating] = useState<number>(5);
  const [surveyComment, setSurveyComment] = useState<string>('');
  const [surveySuccessMessage, setSurveySuccessMessage] = useState<string | null>(null);

  const activeSubject = CRITICAL_SUBJECTS.find(s => s.id === selectedSubjectId) || CRITICAL_SUBJECTS[0];

  const handleSubjectChange = (id: string) => {
    setSelectedSubjectId(id);
    const sub = CRITICAL_SUBJECTS.find(s => s.id === id);
    if (sub && sub.topics.length > 0) {
      setSelectedTopic(sub.topics[0]);
    }
  };

  const handleRunMatching = () => {
    setIsCalculating(true);
    setTimeout(() => {
      setIsCalculating(false);
    }, 600);
  };

  // Calcular ranking Top-k con afinidad
  const rankedMentors = MOCK_MENTORS.map((m, index) => {
    const hasSpec = m.subjectSpecialties.includes(activeSubject.name);
    let affinity = hasSpec ? 92 + (m.rating * 1.5) - (index * 4) : 74 - (index * 6);
    if (affinity > 99) affinity = 99;
    return {
      ...m,
      affinityPercentage: Math.round(affinity)
    };
  }).sort((a, b) => (b.affinityPercentage || 0) - (a.affinityPercentage || 0));

  // Registrar nueva demanda (CUS03)
  const handleCreateDemand = (e: React.FormEvent) => {
    e.preventDefault();
    if (!demandTopic.trim()) return;

    const newDemand: DemandRequest = {
      id: `req-${Date.now()}`,
      studentName: 'Renzo Antayhua M',
      studentCode: '2025018341',
      cycle: 'II Ciclo EPIS',
      subjectName: demandSubject,
      topicNeeded: demandTopic,
      description: demandDesc,
      preferredModality: demandModality,
      dateCreated: 'Hoy',
      status: 'ABIERTA'
    };

    setDemands([newDemand, ...demands]);
    setDemandSuccessMessage('¡Solicitud por demanda publicada en la bolsa académica de la EPIS!');
    setDemandTopic('');
    setDemandDesc('');
    setTimeout(() => setDemandSuccessMessage(null), 3500);
  };

  // Enviar encuesta CSAT (CUS05)
  const handleSubmitSurvey = (e: React.FormEvent) => {
    e.preventDefault();
    if (!surveyComment.trim()) return;
    setSurveySuccessMessage('¡Encuesta enviada con éxito! Tus datos han sido disociados conforme a la Ley N° 29733 (RN-13).');
    setSurveyComment('');
    setTimeout(() => setSurveySuccessMessage(null), 3500);
  };

  return (
    <div className="fade-in">
      {/* Cabecera del Mentoreado */}
      <div style={{ marginBottom: '1.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
            <span className="badge badge-navy">📚 Estudiante Mentoreado</span>
            <span className="badge badge-gold">Ciclos Formativos (I - IV)</span>
          </div>
          <h2 style={{ fontSize: '1.65rem', color: 'var(--primary-navy)' }}>
            Portal del Mentoreado: Renzo Antayhua M (II Ciclo)
          </h2>
          <p style={{ color: 'var(--text-body)', fontSize: '0.9rem', maxWidth: '750px' }}>
            Encuentra apoyo en asignaturas filtro mediante el algoritmo Top-k (CUS02), ratifica tus asistencias antes de T-24h (CUS24) y evalúa la calidad de la sesión (CUS05).
          </p>
        </div>

        {/* Pestañas del Mentoreado */}
        <div style={{ display: 'flex', gap: '0.5rem', background: '#FFFFFF', padding: '0.3rem', borderRadius: '12px', border: '1px solid var(--border-color)', flexWrap: 'wrap' }}>
          <button
            onClick={() => setActiveTab('recommendation')}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeTab === 'recommendation' ? 'var(--primary-navy)' : 'transparent',
              color: activeTab === 'recommendation' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            🎯 Recomendador Top-k (CUS02)
          </button>
          <button
            onClick={() => setActiveTab('my_bookings')}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeTab === 'my_bookings' ? 'var(--primary-navy)' : 'transparent',
              color: activeTab === 'my_bookings' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            📅 Mis Reservas & Pase QR (CUS24)
          </button>
          <button
            onClick={() => setActiveTab('demand_request')}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeTab === 'demand_request' ? 'var(--primary-navy)' : 'transparent',
              color: activeTab === 'demand_request' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            ➕ Pedir Tema por Demanda (CUS03)
          </button>
          <button
            onClick={() => setActiveTab('survey')}
            style={{
              padding: '0.45rem 0.85rem',
              borderRadius: '8px',
              border: 'none',
              fontSize: '0.8rem',
              fontWeight: 700,
              cursor: 'pointer',
              backgroundColor: activeTab === 'survey' ? 'var(--primary-navy)' : 'transparent',
              color: activeTab === 'survey' ? '#FFFFFF' : 'var(--text-body)'
            }}
          >
            ⭐ Evaluar Mentor CSAT (CUS05)
          </button>
        </div>
      </div>

      {/* Estado del Consentimiento Informado (RF01 / Ley N° 29733) */}
      {!hasAcceptedConsent && (
        <div
          style={{
            backgroundColor: '#FEF7E0',
            border: '1.5px solid #FEEFC3',
            borderRadius: '12px',
            padding: '0.85rem 1.25rem',
            marginBottom: '1.5rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            gap: '1rem',
            flexWrap: 'wrap'
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
            <span style={{ fontSize: '1.3rem' }}>⚖️</span>
            <div>
              <strong style={{ fontSize: '0.88rem', color: '#B06000', display: 'block' }}>
                Consentimiento Académico Pendiente (Ley N° 29733)
              </strong>
              <span style={{ fontSize: '0.78rem', color: '#7A4100' }}>
                Debes autorizar el uso de tu historial académico para que el recomendador optimice el emparejamiento con mentores de ciclos superiores.
              </span>
            </div>
          </div>
          <button
            onClick={onOpenConsentModal}
            className="btn-gold"
            style={{ fontSize: '0.78rem', padding: '0.4rem 1rem' }}
          >
            Firmar Consentimiento Digital
          </button>
        </div>
      )}

      {/* 1. RECOMENDADOR TOP-K Y EMPAREJAMIENTO INTELIGENTE (CUS02 / RF05 / RF07) */}
      {activeTab === 'recommendation' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1.75rem', marginBottom: '2.5rem' }}>
          {/* Panel Izquierdo: Formulario de Selección Temática */}
          <div className="upt-card" style={{ height: 'fit-content' }}>
            <h3 style={{ fontSize: '0.98rem', color: 'var(--primary-navy)', marginBottom: '1rem' }}>
              ¿En qué tema necesitas apoyo?
            </h3>

            <div style={{ marginBottom: '1.15rem' }}>
              <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.35rem' }}>
                Asignatura Crítica:
              </label>
              <select
                value={selectedSubjectId}
                onChange={(e) => handleSubjectChange(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.55rem 0.75rem',
                  borderRadius: '8px',
                  border: '1.5px solid var(--border-color)',
                  fontFamily: 'inherit',
                  fontSize: '0.88rem',
                  backgroundColor: 'var(--bg-page)',
                  color: 'var(--text-heading)',
                  outline: 'none'
                }}
              >
                {CRITICAL_SUBJECTS.map((sub) => (
                  <option key={sub.id} value={sub.id}>
                    {sub.name} ({sub.cycle})
                  </option>
                ))}
              </select>
            </div>

            <div style={{ marginBottom: '1.15rem' }}>
              <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.35rem' }}>
                Tópico Específico:
              </label>
              <select
                value={selectedTopic}
                onChange={(e) => setSelectedTopic(e.target.value)}
                style={{
                  width: '100%',
                  padding: '0.55rem 0.75rem',
                  borderRadius: '8px',
                  border: '1.5px solid var(--border-color)',
                  fontFamily: 'inherit',
                  fontSize: '0.88rem',
                  backgroundColor: 'var(--bg-page)',
                  color: 'var(--text-heading)',
                  outline: 'none'
                }}
              >
                {activeSubject.topics.map((t) => (
                  <option key={t} value={t}>
                    {t}
                  </option>
                ))}
              </select>
            </div>

            <div style={{ backgroundColor: 'var(--bg-page)', padding: '0.75rem', borderRadius: '8px', border: '1px solid var(--border-color)', marginBottom: '1.25rem', fontSize: '0.78rem' }}>
              <span style={{ color: 'var(--accent-gold-dark)', fontWeight: 700 }}>Bonificación Institucional RN-11:</span>
              <p style={{ margin: '0.2rem 0 0 0', color: 'var(--text-body)' }}>
                Esta materia cuenta con factor prioritario <code>α = 1.35</code> para destacar a mentores de alto rendimiento.
              </p>
            </div>

            <button
              className="btn-gold"
              onClick={handleRunMatching}
              style={{ width: '100%', padding: '0.7rem' }}
            >
              {isCalculating ? 'Ejecutando Similitud Coseno...' : 'Calcular Recomendación Top-k →'}
            </button>
          </div>

          {/* Panel Derecho: Ranking Top-k Ordenado */}
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 style={{ fontSize: '1rem', color: 'var(--primary-navy)', margin: 0 }}>
                Mentores Recomendados (Top-{rankedMentors.length})
              </h3>
              <span style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                Ordenado por Afinidad Temática y Calificación
              </span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {rankedMentors.map((mentor, index) => (
                <div
                  key={mentor.id}
                  style={{
                    backgroundColor: '#FFFFFF',
                    borderRadius: '16px',
                    padding: '1.25rem',
                    border: index === 0 ? '2px solid var(--accent-gold)' : '1px solid var(--border-color)',
                    boxShadow: index === 0 ? '0 8px 24px rgba(185, 148, 81, 0.12)' : '0 2px 8px rgba(0,0,0,0.03)',
                    display: 'flex',
                    flexDirection: 'column',
                    gap: '0.85rem'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                    <div style={{ display: 'flex', gap: '1rem' }}>
                      <img
                        src={mentor.avatar}
                        alt={mentor.name}
                        style={{ width: '60px', height: '60px', borderRadius: '50%', border: '2.5px solid var(--accent-gold)', objectFit: 'cover' }}
                      />
                      <div>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          <h4 style={{ margin: 0, fontSize: '1.05rem', color: 'var(--primary-navy)' }}>
                            {mentor.name}
                          </h4>
                          {index === 0 && (
                            <span className="badge badge-gold" style={{ fontSize: '0.68rem' }}>
                              👑 #1 Más Recomendado
                            </span>
                          )}
                        </div>
                        <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                          {mentor.cycle} • Código: {mentor.code}
                        </span>
                        <div style={{ display: 'flex', gap: '0.35rem', marginTop: '0.35rem' }}>
                          {mentor.badges.map(b => (
                            <span key={b} className="badge badge-navy" style={{ fontSize: '0.65rem' }}>
                              {b}
                            </span>
                          ))}
                        </div>
                      </div>
                    </div>

                    {/* Porcentaje de Afinidad */}
                    <div style={{ textAlign: 'right' }}>
                      <div style={{ fontSize: '1.4rem', fontWeight: 800, color: 'var(--accent-gold-dark)' }}>
                        {mentor.affinityPercentage}%
                      </div>
                      <span style={{ fontSize: '0.68rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700 }}>
                        Afinidad Algorítmica
                      </span>
                    </div>
                  </div>

                  {/* Horarios disponibles y botón */}
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', borderTop: '1px dashed var(--border-color)', paddingTop: '0.75rem', flexWrap: 'wrap', gap: '0.5rem' }}>
                    <div style={{ fontSize: '0.78rem', color: 'var(--text-body)' }}>
                      <strong>Próximo horario: </strong>
                      {mentor.availabilitySlots[0]?.day} ({mentor.availabilitySlots[0]?.time})
                    </div>

                    <button
                      className="btn-gold"
                      onClick={() => onSelectMentorForBooking(mentor, selectedTopic)}
                      style={{ fontSize: '0.8rem', padding: '0.45rem 1rem' }}
                    >
                      Reservar Sesión con {mentor.name.split(' ')[0]} →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 2. MIS RESERVAS Y RATIFICACIÓN T-24H (CUS04 / CUS24 / CUS11 / RN-08) */}
      {activeTab === 'my_bookings' && (
        <div>
          <div className="upt-card" style={{ marginBottom: '1.5rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <div>
                <h3 style={{ margin: 0, fontSize: '1.1rem', color: 'var(--primary-navy)' }}>
                  Mis Reservas y Pases de Ingreso
                </h3>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  Recuerda ratificar tu asistencia antes de las 24h de inicio para evitar anulación automática (RN-08).
                </span>
              </div>
              <span className="badge badge-navy">{bookings.length} Reservas</span>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              {bookings.map((booking) => (
                <div
                  key={booking.id}
                  style={{
                    border: '1px solid var(--border-color)',
                    borderRadius: '14px',
                    padding: '1.25rem',
                    backgroundColor: '#FFFFFF',
                    boxShadow: '0 2px 8px rgba(0,0,0,0.03)'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.5rem' }}>
                    <div>
                      <span className="badge badge-navy" style={{ fontSize: '0.7rem', marginBottom: '0.25rem' }}>
                        {booking.subjectName}
                      </span>
                      <h4 style={{ fontSize: '1.05rem', color: 'var(--primary-navy)', margin: '0.2rem 0' }}>
                        {booking.topic}
                      </h4>
                    </div>

                    <span className="badge badge-gold" style={{ fontSize: '0.75rem' }}>
                      ● {booking.status}
                    </span>
                  </div>

                  <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '0.75rem', fontSize: '0.8rem', backgroundColor: 'var(--bg-page)', padding: '0.75rem', borderRadius: '8px', border: '1px solid var(--border-color)', margin: '0.5rem 0' }}>
                    <div>
                      <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.68rem' }}>Mentor Responsable:</span>
                      <strong>{booking.mentorName}</strong>
                    </div>
                    <div>
                      <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.68rem' }}>Horario Programado:</span>
                      <strong>{booking.dateFormatted}</strong>
                    </div>
                    <div>
                      <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.68rem' }}>Estado de Ratificación:</span>
                      <strong style={{ color: booking.ratifiedT24 ? '#137333' : '#B06000' }}>
                        {booking.ratifiedT24 ? '✓ Ratificado' : '⏳ Pendiente de Ratificar (T-24h)'}
                      </strong>
                    </div>
                  </div>

                  <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '0.75rem', borderTop: '1px dashed var(--border-color)', paddingTop: '0.75rem' }}>
                    {/* Botón Ratificar Asistencia (CUS24) */}
                    {!booking.ratifiedT24 && (
                      <button
                        onClick={() => onRatifyAttendance(booking.id)}
                        className="btn-gold"
                        style={{ fontSize: '0.78rem', padding: '0.4rem 1rem' }}
                      >
                        ✓ Ratificar Mi Asistencia Obligatoria (T-24h)
                      </button>
                    )}

                    {/* Botón Ver Ticket QR (CUS11) */}
                    <button
                      onClick={() => setSelectedTicketSession(booking)}
                      className="btn-pill-navy"
                      style={{ fontSize: '0.78rem', padding: '0.4rem 1rem' }}
                    >
                      📱 Ver Mi Pase Digital / QR
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Modal de Ticket con Código QR */}
          {selectedTicketSession && (
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
              onClick={() => setSelectedTicketSession(null)}
            >
              <div
                className="upt-card"
                style={{ maxWidth: '420px', width: '100%', textAlign: 'center', padding: '2rem' }}
                onClick={(e) => e.stopPropagation()}
              >
                <span className="badge badge-gold" style={{ marginBottom: '0.5rem' }}>
                  Pase Digital EPIS UPT (CUS11)
                </span>
                <h3 style={{ fontSize: '1.2rem', color: 'var(--primary-navy)', margin: '0.25rem 0' }}>
                  {selectedTicketSession.subjectName}
                </h3>
                <p style={{ fontSize: '0.82rem', color: 'var(--text-body)', margin: '0 0 1.25rem 0' }}>
                  {selectedTicketSession.topic} • Con {selectedTicketSession.mentorName}
                </p>

                {/* Código QR Simulado */}
                <div
                  style={{
                    width: '180px',
                    height: '180px',
                    backgroundColor: 'var(--primary-navy)',
                    color: '#FFFFFF',
                    borderRadius: '16px',
                    margin: '0 auto 1.25rem',
                    display: 'flex',
                    flexDirection: 'column',
                    alignItems: 'center',
                    justifyContent: 'center',
                    padding: '1rem',
                    boxShadow: '0 8px 20px rgba(28, 42, 89, 0.2)'
                  }}
                >
                  <div style={{ fontSize: '4.5rem', lineHeight: 1 }}>▦</div>
                  <span style={{ fontSize: '0.65rem', marginTop: '0.5rem', color: 'var(--accent-gold-light)', letterSpacing: '0.05em' }}>
                    TOKEN CRIPTOGRÁFICO EFÍMERO
                  </span>
                </div>

                <div style={{ backgroundColor: 'var(--bg-page)', padding: '0.6rem', borderRadius: '8px', border: '1px solid var(--border-color)', fontSize: '0.75rem', marginBottom: '1.25rem' }}>
                  <span style={{ color: 'var(--text-muted)', display: 'block' }}>Código de Acceso:</span>
                  <code style={{ color: 'var(--primary-blue)', fontWeight: 700, wordBreak: 'break-all' }}>
                    {selectedTicketSession.qrToken || 'QR-P2P-SI301-2025018341-998'}
                  </code>
                </div>

                <button
                  onClick={() => setSelectedTicketSession(null)}
                  className="btn-gold"
                  style={{ width: '100%', padding: '0.65rem' }}
                >
                  Cerrar Pase
                </button>
              </div>
            </div>
          )}
        </div>
      )}

      {/* 3. SOLICITUD TEMÁTICA POR DEMANDA (CUS03 / RF04) */}
      {activeTab === 'demand_request' && (
        <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1fr', gap: '1.75rem' }}>
          <div className="upt-card">
            <h3 style={{ fontSize: '1.15rem', color: 'var(--primary-navy)', marginBottom: '0.3rem' }}>
              Registrar Solicitud Temática por Demanda (CUS03)
            </h3>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-body)', marginBottom: '1.25rem' }}>
              Si no encuentras una mentoría abierta para tu dificultad, regístrala aquí. Los mentores la verán en su feed de necesidades no cubiertas.
            </p>

            {demandSuccessMessage && (
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
                {demandSuccessMessage}
              </div>
            )}

            <form onSubmit={handleCreateDemand}>
              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>
                  Asignatura Crítica:
                </label>
                <select
                  value={demandSubject}
                  onChange={(e) => setDemandSubject(e.target.value)}
                  style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
                >
                  {CRITICAL_SUBJECTS.map((s) => (
                    <option key={s.id} value={s.name}>
                      {s.name} ({s.cycle})
                    </option>
                  ))}
                </select>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>
                  Tema o Vacío Conceptual:
                </label>
                <input
                  type="text"
                  value={demandTopic}
                  onChange={(e) => setDemandTopic(e.target.value)}
                  placeholder="ej: Patrón Observer o resolución de matrices inversas"
                  style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>
                  Descripción de la dificultad:
                </label>
                <textarea
                  value={demandDesc}
                  onChange={(e) => setDemandDesc(e.target.value)}
                  placeholder="Explica qué ejercicios o conceptos del sílabo te causan dudas..."
                  rows={3}
                  style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.85rem', fontFamily: 'inherit' }}
                  required
                />
              </div>

              <div style={{ marginBottom: '1.25rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, marginBottom: '0.3rem' }}>
                  Preferencia de Modalidad:
                </label>
                <select
                  value={demandModality}
                  onChange={(e) => setDemandModality(e.target.value)}
                  style={{ width: '100%', padding: '0.6rem', borderRadius: '8px', border: '1.5px solid var(--border-color)', fontSize: '0.88rem', fontFamily: 'inherit' }}
                >
                  <option value="Virtual (Meet)">Virtual (Google Meet)</option>
                  <option value="Presencial (Lab EPIS)">Presencial (Laboratorio EPIS)</option>
                </select>
              </div>

              <button
                type="submit"
                className="btn-gold"
                style={{ width: '100%', padding: '0.75rem', fontSize: '0.9rem' }}
              >
                Publicar Solicitud de Demanda →
              </button>
            </form>
          </div>

          {/* Solicitudes Abiertas */}
          <div className="upt-card">
            <h3 style={{ fontSize: '1.05rem', color: 'var(--primary-navy)', marginBottom: '1rem' }}>
              Bolsa de Demandas Abiertas (EPIS)
            </h3>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {demands.map((d) => (
                <div key={d.id} style={{ padding: '0.85rem', backgroundColor: 'var(--bg-page)', borderRadius: '10px', border: '1px solid var(--border-color)' }}>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.25rem' }}>
                    <span className="badge badge-navy" style={{ fontSize: '0.68rem' }}>{d.subjectName}</span>
                    <span className="badge badge-gold" style={{ fontSize: '0.65rem' }}>{d.status}</span>
                  </div>
                  <strong style={{ fontSize: '0.88rem', color: 'var(--primary-navy)', display: 'block' }}>{d.topicNeeded}</strong>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-body)', margin: '0.25rem 0' }}>{d.description}</p>
                  <span style={{ fontSize: '0.72rem', color: 'var(--text-muted)' }}>Publicado por {d.studentName} ({d.cycle}) • {d.preferredModality}</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}

      {/* 4. ENCUESTA DE CALIDAD CSAT (CUS05 / RF11 / RN-13) */}
      {activeTab === 'survey' && (
        <div className="upt-card" style={{ maxWidth: '640px', margin: '0 auto' }}>
          <div style={{ textAlign: 'center', marginBottom: '1.5rem' }}>
            <span style={{ fontSize: '2.5rem' }}>⭐</span>
            <h3 style={{ fontSize: '1.25rem', color: 'var(--primary-navy)', margin: '0.35rem 0' }}>
              Evaluación de Calidad CSAT Post-Mentoría (CUS05)
            </h3>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-body)' }}>
              Tus respuestas son <strong>estrictamente anónimas y disociadas mediante SHA-256 (RN-13)</strong>. Ayudan a retroalimentar la reputación de los mentores en el recomendador.
            </p>
          </div>

          {surveySuccessMessage && (
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
              {surveySuccessMessage}
            </div>
          )}

          <form onSubmit={handleSubmitSurvey}>
            <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
              <label style={{ display: 'block', fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.6rem' }}>
                ¿Cómo calificarías la claridad pedagógica del mentor?
              </label>
              <div style={{ display: 'flex', justifyContent: 'center', gap: '0.75rem' }}>
                {[1, 2, 3, 4, 5].map((star) => (
                  <button
                    key={star}
                    type="button"
                    onClick={() => setSurveyRating(star)}
                    style={{
                      background: 'none',
                      border: 'none',
                      fontSize: '2rem',
                      cursor: 'pointer',
                      color: star <= surveyRating ? '#FFB800' : '#E2E8F0',
                      transition: 'transform 0.15s ease'
                    }}
                  >
                    ★
                  </button>
                ))}
              </div>
              <span style={{ fontSize: '0.8rem', color: 'var(--accent-gold-dark)', fontWeight: 700 }}>
                {surveyRating} de 5 Estrellas
              </span>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.35rem' }}>
                Comentarios y retroalimentación pedagógica (Anónimo):
              </label>
              <textarea
                value={surveyComment}
                onChange={(e) => setSurveyComment(e.target.value)}
                placeholder="¿Qué te pareció el ritmo de la explicación, ejercicios resueltos o recomendaciones para futuras sesiones?..."
                rows={4}
                style={{
                  width: '100%',
                  padding: '0.75rem',
                  borderRadius: '10px',
                  border: '1.5px solid var(--border-color)',
                  fontSize: '0.88rem',
                  fontFamily: 'inherit',
                  outline: 'none'
                }}
                required
              />
            </div>

            <button
              type="submit"
              className="btn-gold"
              style={{ width: '100%', padding: '0.8rem', fontSize: '0.92rem' }}
            >
              Enviar Evaluación Anónima CSAT →
            </button>
          </form>
        </div>
      )}
    </div>
  );
};
