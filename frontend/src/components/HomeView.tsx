import React, { useState, useMemo } from 'react';
import { ImageCarousel } from './ImageCarousel';
import { HERO_SLIDES, CRITICAL_SUBJECTS, AVAILABLE_MENTORSHIPS } from '../data/mockData';
import type { Mentor } from '../data/mockData';

interface HomeViewProps {
  onStartMatching: () => void;
  onOpenBookings: () => void;
  onSelectMentorForBooking: (mentor: Mentor, topic: string) => void;
}

export const HomeView: React.FC<HomeViewProps> = ({
  onStartMatching,
  onOpenBookings,
  onSelectMentorForBooking
}) => {
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [selectedSubjectId, setSelectedSubjectId] = useState<string>('all');

  const scrollToCatalog = () => {
    const el = document.getElementById('catalog-section');
    if (el) {
      el.scrollIntoView({ behavior: 'smooth' });
    }
  };

  // Filtrado reactivo en tiempo real según lo requiera el mentoreado
  const filteredMentorships = useMemo(() => {
    return AVAILABLE_MENTORSHIPS.filter((item) => {
      // 1. Filtro por selector de clase / asignatura
      if (selectedSubjectId !== 'all') {
        const currentSub = CRITICAL_SUBJECTS.find(s => s.id === selectedSubjectId);
        if (currentSub && item.subjectName !== currentSub.name && item.subjectCode !== currentSub.code) {
          return false;
        }
      }

      // 2. Filtro por escritura del mentoreado
      if (searchTerm.trim() !== '') {
        const query = searchTerm.toLowerCase().trim();
        const matchTopic = item.topic.toLowerCase().includes(query);
        const matchSubject = item.subjectName.toLowerCase().includes(query);
        const matchCode = item.subjectCode.toLowerCase().includes(query);
        const matchMentor = item.mentor.name.toLowerCase().includes(query);
        const matchModality = item.modality.toLowerCase().includes(query);
        const matchDay = item.scheduleDay.toLowerCase().includes(query);

        return matchTopic || matchSubject || matchCode || matchMentor || matchModality || matchDay;
      }

      return true;
    });
  }, [searchTerm, selectedSubjectId]);

  return (
    <div className="fade-in">
      {/* 1. Carrusel de Imágenes Institucional */}
      <ImageCarousel
        slides={HERO_SLIDES}
        onExploreClick={scrollToCatalog}
      />

      {/* 2. Sección Principal: Catálogo de Clases y Mentorías con Buscador por Escritura */}
      <section id="catalog-section" style={{ marginBottom: '3.5rem', scrollMarginTop: '20px' }}>
        <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
          <span className="badge badge-gold" style={{ marginBottom: '0.5rem' }}>
            Catálogo en Vivo • EPIS UPT
          </span>
          <h2 style={{ fontSize: '1.85rem', color: 'var(--primary-navy)', marginBottom: '0.4rem' }}>
            Clases y Mentorías Disponibles
          </h2>
          <p style={{ color: 'var(--text-body)', fontSize: '0.95rem', maxWidth: '600px', margin: '0 auto' }}>
            Escribe el tema o dificultad que necesitas resolver y encuentra las mentorías abiertas al instante.
          </p>
        </div>

        {/* Cuadro de Búsqueda por Escritura (Input en Tiempo Real) */}
        <div style={{ maxWidth: '720px', margin: '0 auto 1.5rem' }}>
          <div className="search-box-wrapper">
            <span style={{ fontSize: '1.2rem', color: 'var(--text-muted)' }}>🔍</span>
            <input
              type="text"
              className="search-input"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Escribe un tema, clase o dificultad (ej. Árboles binarios, Límites, SQL, Java, Joan)..."
            />
            {searchTerm && (
              <button
                onClick={() => setSearchTerm('')}
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'var(--text-muted)',
                  fontSize: '0.85rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  padding: '0.2rem 0.5rem',
                  borderRadius: '4px'
                }}
                title="Limpiar búsqueda"
              >
                ✕ Limpiar
              </button>
            )}
          </div>
        </div>

        {/* Filtros Rápidos por Clase (Chips Horizontales) */}
        <div className="course-chips-container" style={{ justifyContent: 'center', marginBottom: '1.5rem' }}>
          <button
            className={`course-chip ${selectedSubjectId === 'all' ? 'active' : ''}`}
            onClick={() => setSelectedSubjectId('all')}
          >
            Todas las Clases ({AVAILABLE_MENTORSHIPS.length})
          </button>
          {CRITICAL_SUBJECTS.map((sub) => {
            const countForSubject = AVAILABLE_MENTORSHIPS.filter(m => m.subjectCode === sub.code || m.subjectName === sub.name).length;
            return (
              <button
                key={sub.id}
                className={`course-chip ${selectedSubjectId === sub.id ? 'active' : ''}`}
                onClick={() => setSelectedSubjectId(selectedSubjectId === sub.id ? 'all' : sub.id)}
              >
                {sub.name} ({countForSubject})
              </button>
            );
          })}
        </div>

        {/* Barra Informativa de Resultados */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem', padding: '0 0.5rem', flexWrap: 'wrap', gap: '0.6rem' }}>
          <span style={{ fontSize: '0.88rem', color: 'var(--text-heading)', fontWeight: 600 }}>
            Mostrando <strong>{filteredMentorships.length}</strong> mentoría{filteredMentorships.length !== 1 ? 's' : ''} disponible{filteredMentorships.length !== 1 ? 's' : ''}
            {searchTerm && <span> para "{searchTerm}"</span>}
          </span>

          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <button
              className="btn-outline-navy btn-sm"
              onClick={onOpenBookings}
              style={{ fontSize: '0.78rem' }}
            >
              📅 Mis Sesiones
            </button>
            <button
              className="btn-gold btn-sm"
              onClick={onStartMatching}
              style={{ fontSize: '0.78rem' }}
            >
              Emparejamiento Top-k →
            </button>
          </div>
        </div>

        {/* Cuadrícula de Mentorías Filtradas */}
        {filteredMentorships.length > 0 ? (
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fill, minmax(340px, 1fr))', gap: '1.25rem' }}>
            {filteredMentorships.map((item) => (
              <div key={item.id} className="mentorship-card">
                {/* Cabecera de la Tarjeta */}
                <div>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: '0.6rem' }}>
                    <span className="badge badge-navy" style={{ fontSize: '0.7rem' }}>
                      {item.subjectCode} • {item.cycle}
                    </span>
                    <span
                      className="badge"
                      style={{
                        fontSize: '0.68rem',
                        backgroundColor: item.modality.includes('Virtual') ? 'rgba(0, 102, 204, 0.1)' : 'rgba(185, 148, 81, 0.15)',
                        color: item.modality.includes('Virtual') ? 'var(--primary-blue)' : 'var(--accent-gold-dark)',
                        fontWeight: 700
                      }}
                    >
                      {item.modality.includes('Virtual') ? '🌐 Virtual' : '🏛️ Presencial'}
                    </span>
                  </div>

                  <h3 style={{ fontSize: '1rem', color: 'var(--primary-navy)', marginBottom: '0.5rem', lineHeight: 1.35 }}>
                    {item.topic}
                  </h3>
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-muted)', marginBottom: '1rem' }}>
                    Asignatura: <strong style={{ color: 'var(--text-heading)' }}>{item.subjectName}</strong>
                  </div>

                  {/* Fila del Mentor */}
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', padding: '0.6rem 0.8rem', background: 'var(--bg-page)', borderRadius: '10px', marginBottom: '1rem' }}>
                    <img
                      src={item.mentor.avatar}
                      alt={item.mentor.name}
                      style={{ width: '42px', height: '42px', borderRadius: '50%', border: '2px solid var(--accent-gold)' }}
                    />
                    <div style={{ flex: 1, minWidth: 0 }}>
                      <div style={{ fontSize: '0.85rem', fontWeight: 700, color: 'var(--primary-navy)', whiteSpace: 'nowrap', overflow: 'hidden', textOverflow: 'ellipsis' }}>
                        {item.mentor.name}
                      </div>
                      <div style={{ fontSize: '0.74rem', color: 'var(--text-muted)' }}>
                        {item.mentor.cycle} • Nota: <strong>{item.mentor.gradeInSubject}/20</strong>
                      </div>
                    </div>
                    <div style={{ textAlign: 'right' }}>
                      <span style={{ color: 'var(--accent-gold-dark)', fontWeight: 800, fontSize: '0.85rem' }}>
                        ★ {item.mentor.rating}
                      </span>
                    </div>
                  </div>

                  {/* Horario y Lugar */}
                  <div style={{ fontSize: '0.78rem', color: 'var(--text-body)', display: 'flex', alignItems: 'center', gap: '0.4rem', marginBottom: '1rem' }}>
                    <span>📅</span>
                    <span><strong>{item.scheduleDay}:</strong> {item.scheduleTime}</span>
                  </div>
                </div>

                {/* Botón de Acción Directo */}
                <button
                  className="btn-gold btn-sm"
                  onClick={() => onSelectMentorForBooking(item.mentor, item.topic)}
                  style={{ width: '100%', padding: '0.6rem' }}
                >
                  Reservar Esta Mentoría →
                </button>
              </div>
            ))}
          </div>
        ) : (
          /* Estado Vacío cuando la búsqueda no coincide */
          <div className="upt-card" style={{ textAlign: 'center', padding: '3rem 1.5rem' }}>
            <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>🔍</div>
            <h3 style={{ color: 'var(--primary-navy)', fontSize: '1.15rem', marginBottom: '0.4rem' }}>
              No encontramos mentorías para "{searchTerm}"
            </h3>
            <p style={{ color: 'var(--text-muted)', fontSize: '0.88rem', maxWidth: '480px', margin: '0 auto 1.5rem' }}>
              Prueba con palabras clave más generales (ej. <em>Cálculo, Java, Punteros, SQL</em>) o restablece los filtros.
            </p>
            <div style={{ display: 'flex', gap: '0.75rem', justifyContent: 'center', flexWrap: 'wrap' }}>
              <button
                className="btn-gold btn-sm"
                onClick={() => { setSearchTerm(''); setSelectedSubjectId('all'); }}
              >
                Ver Todas las Mentorías
              </button>
              <button
                className="btn-outline-navy btn-sm"
                onClick={onStartMatching}
              >
                Buscar Mentor Personalizado (Top-k) →
              </button>
            </div>
          </div>
        )}
      </section>

      {/* 3. Métricas Clave Simplificadas */}
      <section style={{ marginBottom: '3.5rem' }}>
        <div className="grid-cols-4">
          <div className="upt-card" style={{ textAlign: 'center', padding: '1.25rem' }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--primary-navy)', marginBottom: '0.15rem' }}>
              Top-k
            </div>
            <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--accent-gold-dark)', textTransform: 'uppercase' }}>
              Recomendación Inteligente
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
              Afinidad por contenido y calificaciones.
            </p>
          </div>

          <div className="upt-card" style={{ textAlign: 'center', padding: '1.25rem' }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--primary-navy)', marginBottom: '0.15rem' }}>
              100%
            </div>
            <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--accent-gold-dark)', textTransform: 'uppercase' }}>
              Horas Convalidables
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
              Acreditación oficial ante Dirección EPIS.
            </p>
          </div>

          <div className="upt-card" style={{ textAlign: 'center', padding: '1.25rem' }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--primary-navy)', marginBottom: '0.15rem' }}>
              5
            </div>
            <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--accent-gold-dark)', textTransform: 'uppercase' }}>
              Clases Críticas
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
              Cálculo, Algoritmos, POO y Bases de Datos.
            </p>
          </div>

          <div className="upt-card" style={{ textAlign: 'center', padding: '1.25rem' }}>
            <div style={{ fontSize: '1.8rem', fontWeight: 800, color: 'var(--primary-navy)', marginBottom: '0.15rem' }}>
              Ley 29733
            </div>
            <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--accent-gold-dark)', textTransform: 'uppercase' }}>
              Privacidad Segura
            </div>
            <p style={{ fontSize: '0.75rem', color: 'var(--text-muted)', marginTop: '0.25rem' }}>
              Consentimiento digital y políticas RLS.
            </p>
          </div>
        </div>
      </section>

      {/* 4. ¿Cómo Funciona? (3 Pasos Directos) */}
      <section className="upt-card" style={{ background: '#FFFFFF', padding: '2rem', marginBottom: '2rem' }}>
        <h2 style={{ fontSize: '1.3rem', color: 'var(--primary-navy)', marginBottom: '1.5rem', textAlign: 'center' }}>
          ¿Cómo Funciona la Mentoría entre Pares?
        </h2>

        <div className="grid-cols-3">
          <div style={{ textAlign: 'center', padding: '0.75rem' }}>
            <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'rgba(28, 42, 89, 0.08)', color: 'var(--primary-navy)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 0.75rem', fontSize: '1.25rem', fontWeight: 800 }}>
              1
            </div>
            <h4 style={{ fontSize: '0.95rem', color: 'var(--primary-navy)', marginBottom: '0.3rem' }}>
              Busca tu Tema o Duda
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-body)' }}>
              Escribe el concepto específico en el buscador o selecciona tu asignatura.
            </p>
          </div>

          <div style={{ textAlign: 'center', padding: '0.75rem' }}>
            <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'rgba(185, 148, 81, 0.15)', color: 'var(--accent-gold-dark)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 0.75rem', fontSize: '1.25rem', fontWeight: 800 }}>
              2
            </div>
            <h4 style={{ fontSize: '0.95rem', color: 'var(--primary-navy)', marginBottom: '0.3rem' }}>
              Elige Horario y Modalidad
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-body)' }}>
              Revisa la disponibilidad del estudiante mentor, su calificación y lugar de sesión.
            </p>
          </div>

          <div style={{ textAlign: 'center', padding: '0.75rem' }}>
            <div style={{ width: '48px', height: '48px', borderRadius: '50%', background: 'rgba(0, 102, 204, 0.1)', color: 'var(--primary-blue)', display: 'flex', alignItems: 'center', justifyContent: 'center', margin: '0 auto 0.75rem', fontSize: '1.25rem', fontWeight: 800 }}>
              3
            </div>
            <h4 style={{ fontSize: '0.95rem', color: 'var(--primary-navy)', marginBottom: '0.3rem' }}>
              Aprende y Convalida
            </h4>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-body)' }}>
              Participa en la mentoría, califica la experiencia y acredita horas oficiales.
            </p>
          </div>
        </div>
      </section>
    </div>
  );
};
