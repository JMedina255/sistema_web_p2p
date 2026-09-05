import React, { useState } from 'react';
import { CRITICAL_SUBJECTS, MOCK_MENTORS } from '../data/mockData';
import type { Mentor } from '../data/mockData';

interface RecommendationViewProps {
  onSelectMentorForBooking: (mentor: Mentor, topic: string) => void;
}

export const RecommendationView: React.FC<RecommendationViewProps> = ({ onSelectMentorForBooking }) => {
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>(CRITICAL_SUBJECTS[0].id);
  const [selectedTopic, setSelectedTopic] = useState<string>(CRITICAL_SUBJECTS[0].topics[0]);
  const [customNeed, setCustomNeed] = useState<string>('');
  const [isCalculating, setIsCalculating] = useState<boolean>(false);
  const [recommendationGenerated, setRecommendationGenerated] = useState<boolean>(false);

  const activeSubject = CRITICAL_SUBJECTS.find(s => s.id === selectedSubjectId) || CRITICAL_SUBJECTS[0];

  const handleSubjectChange = (id: string) => {
    setSelectedSubjectId(id);
    const sub = CRITICAL_SUBJECTS.find(s => s.id === id);
    if (sub && sub.topics.length > 0) {
      setSelectedTopic(sub.topics[0]);
    }
  };

  // Simulación del motor de recomendación híbrido
  const rankedMentors: Mentor[] = MOCK_MENTORS.map((mentor, index) => {
    const hasSpecialty = mentor.subjectSpecialties.includes(activeSubject.name);
    let score = hasSpecialty ? 88 + (mentor.rating * 2) - (index * 4) : 70 - (index * 5);
    if (score > 98) score = 98;
    return {
      ...mentor,
      affinityPercentage: Math.round(score)
    };
  }).sort((a, b) => (b.affinityPercentage || 0) - (a.affinityPercentage || 0));

  const runHybridRecommendation = () => {
    setIsCalculating(true);
    setRecommendationGenerated(false);
    setTimeout(() => {
      setIsCalculating(false);
      setRecommendationGenerated(true);
    }, 700);
  };

  return (
    <div className="fade-in">
      <div style={{ marginBottom: '1.75rem' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
          <span className="badge badge-gold">Emparejamiento Inteligente</span>
          <span className="badge badge-navy">Afinidad Top-k</span>
        </div>
        <h2 style={{ fontSize: '1.65rem', color: 'var(--primary-navy)' }}>
          Recomendación de Mentores
        </h2>
        <p style={{ color: 'var(--text-body)', fontSize: '0.9rem', maxWidth: '750px' }}>
          Selecciona la asignatura y el tema específico. El recomendador calculará la compatibilidad temática y valoraciones de los mentores.
        </p>
      </div>

      <div style={{ display: 'grid', gridTemplateColumns: '1fr 2fr', gap: '1.75rem', marginBottom: '2.5rem' }}>
        {/* Panel Izquierdo: Formulario de Solicitud */}
        <div className="upt-card" style={{ height: 'fit-content' }}>
          <h3 style={{ fontSize: '0.98rem', color: 'var(--primary-navy)', marginBottom: '1rem' }}>
            ¿Qué deseas reforzar?
          </h3>

          <div style={{ marginBottom: '1.15rem' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.35rem' }}>
              Asignatura:
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
              Tema o Concepto:
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
              {activeSubject.topics.map((top, idx) => (
                <option key={idx} value={top}>
                  {top}
                </option>
              ))}
            </select>
          </div>

          <div style={{ marginBottom: '1.25rem' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.35rem' }}>
              Detalle opcional de tu consulta:
            </label>
            <textarea
              rows={3}
              placeholder="Ej: Tengo dudas con árboles AVL y punteros en C++..."
              value={customNeed}
              onChange={(e) => setCustomNeed(e.target.value)}
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
            />
          </div>

          <button
            className="btn-gold"
            onClick={runHybridRecommendation}
            disabled={isCalculating}
            style={{ width: '100%', padding: '0.7rem' }}
          >
            {isCalculating ? 'Calculando afinidad...' : '⚡ Buscar Mentores Compatibles'}
          </button>
        </div>

        {/* Panel Derecho: Ranking Top-k */}
        <div>
          {/* Proceso simplificado */}
          <div
            style={{
              background: 'linear-gradient(135deg, #172349 0%, #1C2A59 100%)',
              color: '#FFFFFF',
              borderRadius: 'var(--radius-card)',
              padding: '1rem 1.25rem',
              marginBottom: '1.25rem',
              boxShadow: 'var(--shadow-card)'
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.4rem' }}>
              <span style={{ fontSize: '0.75rem', color: 'var(--accent-gold-light)', fontWeight: 700, textTransform: 'uppercase' }}>
                Criterios de Recomendación
              </span>
              <span className="badge badge-success" style={{ fontSize: '0.68rem' }}>Activo</span>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(4, 1fr)', gap: '0.5rem', fontSize: '0.75rem', textAlign: 'center' }}>
              <div style={{ background: 'rgba(255,255,255,0.06)', padding: '0.4rem', borderRadius: '8px' }}>
                <strong>1. Asignatura</strong>
                <p style={{ opacity: 0.8, fontSize: '0.7rem' }}>Aprobada con alta nota</p>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.06)', padding: '0.4rem', borderRadius: '8px' }}>
                <strong>2. Tema Afín</strong>
                <p style={{ opacity: 0.8, fontSize: '0.7rem' }}>Similitud de contenidos</p>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.06)', padding: '0.4rem', borderRadius: '8px' }}>
                <strong>3. Valoraciones</strong>
                <p style={{ opacity: 0.8, fontSize: '0.7rem' }}>Estrellas y reseñas</p>
              </div>
              <div style={{ background: 'rgba(255,255,255,0.06)', padding: '0.4rem', borderRadius: '8px' }}>
                <strong>4. Horarios</strong>
                <p style={{ opacity: 0.8, fontSize: '0.7rem' }}>Bloques libres</p>
              </div>
            </div>
          </div>

          {/* Estado de carga */}
          {isCalculating && (
            <div className="upt-card" style={{ textAlign: 'center', padding: '2.5rem' }}>
              <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>⚙️</div>
              <h4 style={{ color: 'var(--primary-navy)', marginBottom: '0.25rem' }}>Calculando compatibilidad...</h4>
              <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
                Buscando a los mentores mejor calificados para tu consulta.
              </p>
            </div>
          )}

          {/* Lista de Resultados Top-k */}
          {!isCalculating && (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <h3 style={{ fontSize: '0.98rem', color: 'var(--primary-navy)', margin: 0 }}>
                    Mentores Recomendados ({rankedMentors.length})
                  </h3>
                  {recommendationGenerated && (
                    <span className="badge badge-success" style={{ fontSize: '0.68rem' }}>
                      ✓ Actualizado
                    </span>
                  )}
                </div>
                <span style={{ fontSize: '0.78rem', color: 'var(--text-muted)' }}>
                  {activeSubject.name} • <em>{selectedTopic}</em>
                </span>
              </div>

              {rankedMentors.map((mentor, index) => (
                <div
                  key={mentor.id}
                  className="upt-card upt-card-hover"
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'auto 1fr auto',
                    gap: '1.25rem',
                    alignItems: 'center',
                    borderLeft: index === 0 ? '4px solid var(--accent-gold)' : '1px solid var(--border-color)',
                    padding: '1.25rem'
                  }}
                >
                  <div className="avatar-container">
                    <img
                      src={mentor.avatar}
                      alt={mentor.name}
                      className="avatar-gold-border"
                      style={{ width: '70px', height: '70px' }}
                    />
                    {index === 0 && (
                      <span
                        style={{
                          position: 'absolute',
                          top: '-6px',
                          right: '-6px',
                          background: 'var(--accent-gold)',
                          color: '#FFFFFF',
                          borderRadius: '50%',
                          width: '22px',
                          height: '22px',
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          fontSize: '0.72rem',
                          boxShadow: '0 2px 4px rgba(0,0,0,0.2)'
                        }}
                      >
                        #1
                      </span>
                    )}
                  </div>

                  <div>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.2rem' }}>
                      <h4 style={{ fontSize: '1.02rem', color: 'var(--primary-navy)', margin: 0 }}>
                        {mentor.name}
                      </h4>
                      <span className="badge badge-navy" style={{ fontSize: '0.68rem' }}>
                        {mentor.cycle}
                      </span>
                    </div>

                    <p style={{ fontSize: '0.8rem', color: 'var(--text-muted)', marginBottom: '0.4rem' }}>
                      Nota en materia: <strong>{mentor.gradeInSubject} / 20</strong> • 🕒 {mentor.totalHours} hrs acreditadas
                    </p>

                    <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.8rem' }}>
                      <span style={{ color: 'var(--text-gold)', fontWeight: 700 }}>
                        ★ {mentor.rating} ({mentor.reviewsCount} reseñas)
                      </span>
                    </div>
                  </div>

                  <div style={{ textAlign: 'right', display: 'flex', flexDirection: 'column', alignItems: 'flex-end', gap: '0.5rem' }}>
                    <div style={{ background: 'rgba(185, 148, 81, 0.1)', padding: '0.35rem 0.7rem', borderRadius: '8px', textAlign: 'center' }}>
                      <div style={{ fontSize: '1.25rem', fontWeight: 800, color: 'var(--accent-gold-dark)', lineHeight: 1 }}>
                        {mentor.affinityPercentage}%
                      </div>
                      <span style={{ fontSize: '0.65rem', color: 'var(--text-muted)', textTransform: 'uppercase', fontWeight: 700 }}>
                        Afinidad
                      </span>
                    </div>

                    <button
                      className="btn-gold btn-sm"
                      onClick={() => onSelectMentorForBooking(mentor, selectedTopic)}
                    >
                      Reservar →
                    </button>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
