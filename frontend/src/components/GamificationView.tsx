import React, { useState } from 'react';
import { GAMIFICATION_BADGES, MOCK_MENTORS } from '../data/mockData';

export const GamificationView: React.FC = () => {
  const [selectedMentor, setSelectedMentor] = useState(MOCK_MENTORS[0]);
  const [mentorHours, setMentorHours] = useState(selectedMentor.totalHours);
  const [rating, setRating] = useState(5);
  const [reviewText, setReviewText] = useState('');
  const [recentReviews, setRecentReviews] = useState([
    {
      id: 'rev-1',
      student: 'Carlos Paredes (II Ciclo)',
      rating: 5,
      comment: 'Excelente explicación de punteros en C++ y memoria dinámica. Muy paciente y claro.',
      date: '03 Sep 2026',
      hoursAdded: 2
    },
    {
      id: 'rev-2',
      student: 'Elena Gómez (I Ciclo)',
      rating: 5,
      comment: 'Resolvimos ejercicios de límites indeterminados que venían en la práctica calificada.',
      date: '28 Ago 2026',
      hoursAdded: 1.5
    }
  ]);
  const [feedbackSent, setFeedbackSent] = useState(false);

  const handleSubmitReview = (e: React.FormEvent) => {
    e.preventDefault();
    if (!reviewText.trim()) return;

    const newReview = {
      id: `rev-${Date.now()}`,
      student: 'Estudiante Mentoreado (Tú)',
      rating,
      comment: reviewText,
      date: 'Hoy, ' + new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' }),
      hoursAdded: 2
    };

    setRecentReviews([newReview, ...recentReviews]);
    setMentorHours(prev => prev + 2);
    setReviewText('');
    setFeedbackSent(true);
    setTimeout(() => setFeedbackSent(false), 3000);
  };

  return (
    <div className="fade-in">
      <div style={{ marginBottom: '1.75rem', display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '1rem' }}>
        <div>
          <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
            <span className="badge badge-gold">Horas & Reputación EPIS</span>
            <span className="badge badge-navy">Acreditación Oficial</span>
          </div>
          <h2 style={{ fontSize: '1.65rem', color: 'var(--primary-navy)' }}>
            Acreditación de Horas e Insignias
          </h2>
          <p style={{ color: 'var(--text-body)', fontSize: '0.9rem', maxWidth: '750px' }}>
            Las sesiones evaluadas generan horas de servicio universitario ante la Dirección EPIS e insignias de prestigio.
          </p>
        </div>

        {/* Ver Perfil del Mentor */}
        <div style={{ background: '#FFFFFF', padding: '0.5rem 0.85rem', borderRadius: '12px', border: '1px solid var(--border-color)' }}>
          <label style={{ display: 'block', fontSize: '0.72rem', fontWeight: 700, color: 'var(--text-muted)', marginBottom: '0.2rem' }}>
            Ver perfil de mentor:
          </label>
          <select
            value={selectedMentor.id}
            onChange={(e) => {
              const m = MOCK_MENTORS.find(item => item.id === e.target.value);
              if (m) {
                setSelectedMentor(m);
                setMentorHours(m.totalHours);
              }
            }}
            style={{
              padding: '0.35rem 0.55rem',
              borderRadius: '8px',
              border: '1px solid var(--border-color)',
              fontSize: '0.82rem',
              color: 'var(--primary-navy)',
              fontWeight: 600,
              outline: 'none'
            }}
          >
            {MOCK_MENTORS.map(m => (
              <option key={m.id} value={m.id}>{m.name} ({m.totalHours} hrs)</option>
            ))}
          </select>
        </div>
      </div>

      {feedbackSent && (
        <div
          style={{
            backgroundColor: '#E6F4EA',
            color: '#137333',
            padding: '0.85rem 1.25rem',
            borderRadius: '12px',
            marginBottom: '1.5rem',
            border: '1px solid #CEEAD6',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            boxShadow: '0 2px 8px rgba(19, 115, 51, 0.08)'
          }}
        >
          <span>✓</span>
          <span>¡Calificación registrada! Se sumaron <strong>+2 horas convalidables</strong> al perfil del mentor.</span>
        </div>
      )}

      {/* Resumen del Perfil del Mentor */}
      <div className="upt-card" style={{ marginBottom: '2rem', padding: '1.5rem' }}>
        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', flexWrap: 'wrap', gap: '1.25rem' }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: '1.25rem' }}>
            <img
              src={selectedMentor.avatar}
              alt={selectedMentor.name}
              className="avatar-gold-border"
              style={{ width: '75px', height: '75px' }}
            />
            <div>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.2rem' }}>
                <h3 style={{ fontSize: '1.15rem', color: 'var(--primary-navy)', margin: 0 }}>
                  {selectedMentor.name}
                </h3>
                <span className="badge badge-gold" style={{ fontSize: '0.7rem' }}>⭐ Top Mentor</span>
              </div>
              <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)' }}>
                {selectedMentor.cycle} • Código: <code>{selectedMentor.code}</code>
              </p>
              <div style={{ display: 'flex', gap: '0.4rem', marginTop: '0.35rem', flexWrap: 'wrap' }}>
                {selectedMentor.subjectSpecialties.map((spec, i) => (
                  <span key={i} className="badge badge-navy" style={{ fontSize: '0.68rem' }}>
                    {spec}
                  </span>
                ))}
              </div>
            </div>
          </div>

          {/* Métricas de Horas y Calificación */}
          <div style={{ display: 'flex', gap: '0.75rem' }}>
            <div style={{ background: 'var(--bg-page)', border: '1px solid var(--border-color)', borderRadius: '12px', padding: '0.75rem 1.25rem', textAlign: 'center' }}>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--primary-navy)', lineHeight: 1.1 }}>
                {mentorHours} hrs
              </div>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700 }}>
                Horas Convalidadas
              </span>
            </div>

            <div style={{ background: 'rgba(185, 148, 81, 0.1)', border: '1px solid rgba(185, 148, 81, 0.3)', borderRadius: '12px', padding: '0.75rem 1.25rem', textAlign: 'center' }}>
              <div style={{ fontSize: '1.6rem', fontWeight: 800, color: 'var(--accent-gold-dark)', lineHeight: 1.1 }}>
                ★ {selectedMentor.rating}
              </div>
              <span style={{ fontSize: '0.7rem', color: 'var(--text-gold)', textTransform: 'uppercase', fontWeight: 700 }}>
                Reputación
              </span>
            </div>
          </div>
        </div>

        {/* Progreso hacia la Meta Oficial */}
        <div style={{ marginTop: '1.25rem', borderTop: '1px solid var(--border-color)', paddingTop: '1rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.8rem', marginBottom: '0.4rem' }}>
            <span style={{ fontWeight: 600, color: 'var(--primary-navy)' }}>
              Meta de convalidación extracurricular: 40 horas
            </span>
            <span style={{ fontWeight: 700, color: 'var(--accent-gold-dark)' }}>
              {Math.min(Math.round((mentorHours / 40) * 100), 100)}% ({mentorHours}/40 hrs)
            </span>
          </div>
          <div style={{ width: '100%', height: '8px', background: 'var(--bg-page)', borderRadius: '9999px', overflow: 'hidden' }}>
            <div
              style={{
                width: `${Math.min((mentorHours / 40) * 100, 100)}%`,
                height: '100%',
                background: 'linear-gradient(90deg, var(--accent-gold) 0%, var(--primary-blue) 100%)',
                borderRadius: '9999px',
                transition: 'width 0.4s ease'
              }}
            />
          </div>
        </div>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1.8fr', gap: '1.75rem' }}>
        {/* Insignias */}
        <div className="upt-card">
          <h3 style={{ fontSize: '0.98rem', color: 'var(--primary-navy)', marginBottom: '1rem' }}>
            Insignias Obtenidas
          </h3>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
            {GAMIFICATION_BADGES.map((badge, idx) => (
              <div
                key={idx}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.85rem',
                  padding: '0.75rem',
                  borderRadius: '10px',
                  background: 'var(--bg-page)',
                  border: '1px solid var(--border-color)'
                }}
              >
                <div style={{ fontSize: '1.5rem', background: '#FFFFFF', width: '42px', height: '42px', borderRadius: '50%', display: 'flex', alignItems: 'center', justifyContent: 'center', boxShadow: '0 2px 4px rgba(0,0,0,0.05)' }}>
                  {badge.icon}
                </div>
                <div>
                  <h4 style={{ fontSize: '0.88rem', color: 'var(--primary-navy)', margin: '0 0 0.15rem' }}>
                    {badge.name}
                  </h4>
                  <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    {badge.desc}
                  </p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* Simulador de Evaluación */}
        <div>
          <div className="upt-card" style={{ marginBottom: '1.25rem' }}>
            <h3 style={{ fontSize: '0.98rem', color: 'var(--primary-navy)', marginBottom: '0.6rem' }}>
              Calificar Sesión de Mentoría
            </h3>
            <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
              Evalúa la sesión para acreditar horas al mentor y actualizar su reputación.
            </p>

            <form onSubmit={handleSubmitReview}>
              <div style={{ marginBottom: '0.85rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.3rem' }}>
                  Calificación (Estrellas):
                </label>
                <div style={{ display: 'flex', gap: '0.4rem' }}>
                  {[1, 2, 3, 4, 5].map((star) => (
                    <button
                      type="button"
                      key={star}
                      onClick={() => setRating(star)}
                      style={{
                        background: 'none',
                        border: 'none',
                        fontSize: '1.6rem',
                        cursor: 'pointer',
                        color: star <= rating ? '#B99451' : '#D1D5DB',
                        transition: 'transform 0.1s'
                      }}
                    >
                      ★
                    </button>
                  ))}
                  <span style={{ alignSelf: 'center', fontSize: '0.85rem', fontWeight: 700, color: 'var(--text-gold)', marginLeft: '0.4rem' }}>
                    {rating} de 5
                  </span>
                </div>
              </div>

              <div style={{ marginBottom: '1rem' }}>
                <label style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.3rem' }}>
                  Comentario breve:
                </label>
                <textarea
                  rows={2}
                  value={reviewText}
                  onChange={(e) => setReviewText(e.target.value)}
                  placeholder="Explica qué tema reforzaron y cómo te ayudó el mentor..."
                  style={{
                    width: '100%',
                    padding: '0.55rem 0.75rem',
                    borderRadius: '8px',
                    border: '1.5px solid var(--border-color)',
                    fontFamily: 'inherit',
                    fontSize: '0.85rem',
                    backgroundColor: 'var(--bg-page)',
                    resize: 'none',
                    outline: 'none'
                  }}
                  required
                />
              </div>

              <button type="submit" className="btn-gold" style={{ width: '100%', padding: '0.65rem' }}>
                Enviar Calificación →
              </button>
            </form>
          </div>

          {/* Historial de Reseñas */}
          <div className="upt-card">
            <h4 style={{ fontSize: '0.92rem', color: 'var(--primary-navy)', marginBottom: '0.85rem' }}>
              Últimas Valoraciones
            </h4>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
              {recentReviews.map((rev) => (
                <div
                  key={rev.id}
                  style={{
                    borderBottom: '1px solid var(--border-color)',
                    paddingBottom: '0.6rem'
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.15rem' }}>
                    <strong style={{ fontSize: '0.82rem', color: 'var(--primary-navy)' }}>{rev.student}</strong>
                    <span style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{rev.date}</span>
                  </div>
                  <div style={{ color: 'var(--accent-gold)', fontSize: '0.8rem', marginBottom: '0.2rem' }}>
                    {'★'.repeat(rev.rating)}{'☆'.repeat(5 - rev.rating)}
                  </div>
                  <p style={{ fontSize: '0.78rem', color: 'var(--text-body)', fontStyle: 'italic' }}>
                    "{rev.comment}"
                  </p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
