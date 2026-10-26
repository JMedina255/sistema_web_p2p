import React, { useState } from 'react';
import { CurriculumCatalogView } from './components/CurriculumCatalogView';
import { HealthStatus } from './components/HealthStatus';
import { LoginOtpView } from './components/LoginOtpView';
import { ConsentModalView } from './components/ConsentModalView';
import { ProfileAvailabilityView } from './components/ProfileAvailabilityView';
import { OfferPublishView } from './components/OfferPublishView';

export const App: React.FC = () => {
  type NavTab = 'auth' | 'consent' | 'curriculum' | 'profile' | 'offers' | 'services';
  const [activeTab, setActiveTab] = useState<NavTab>(() => {
    if (typeof window !== 'undefined' && window.location) {
      const p = new URLSearchParams(window.location.search).get('tab');
      if (
        p === 'curriculum' ||
        p === 'services' ||
        p === 'auth' ||
        p === 'consent' ||
        p === 'profile' ||
        p === 'offers'
      ) {
        return p;
      }
    }
    return 'auth';
  });

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#F8FAFC',
        fontFamily: "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif",
        color: '#1E293B',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* Barra superior institucional */}
      <header
        style={{
          backgroundColor: '#1C2A59',
          color: '#FFFFFF',
          padding: '0.9rem 2rem',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
          borderBottom: '3px solid #B99451',
        }}
      >
        <div
          style={{
            maxWidth: '1100px',
            margin: '0 auto',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '1rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
            <div
              style={{
                background: '#B99451',
                color: '#FFFFFF',
                fontWeight: 900,
                fontSize: '1rem',
                padding: '0.35rem 0.65rem',
                borderRadius: '6px',
                letterSpacing: '0.05em',
              }}
            >
              UPT
            </div>
            <div>
              <h1 style={{ margin: 0, fontSize: '1.15rem', fontWeight: 700, letterSpacing: '-0.01em' }}>
                SISTEMA WEB P2P DE MENTORÍAS ACADÉMICAS
              </h1>
              <p style={{ margin: 0, fontSize: '0.75rem', opacity: 0.85 }}>
                Escuela Profesional de Ingeniería de Sistemas • Facultad de Ingeniería
              </p>
            </div>
          </div>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', fontSize: '0.8rem' }}>
            <span
              style={{
                background: 'rgba(255, 255, 255, 0.12)',
                padding: '0.3rem 0.75rem',
                borderRadius: '9999px',
                border: '1px solid rgba(255, 255, 255, 0.2)',
              }}
            >
              Sprint 3 · Publicación de Ofertas (T-14)
            </span>
            <a
              href="http://localhost:8000/docs"
              target="_blank"
              rel="noopener noreferrer"
              style={{
                color: '#F8FAFC',
                textDecoration: 'none',
                background: '#B99451',
                padding: '0.3rem 0.75rem',
                borderRadius: '9999px',
                fontWeight: 600,
              }}
            >
              Swagger /docs ↗
            </a>
          </div>
        </div>
      </header>

      {/* Selector de Vistas / Pestañas de Navegación */}
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderBottom: '1px solid #E2E8F0',
          padding: '0.6rem 2rem',
        }}
      >
        <div
          style={{
            maxWidth: '1100px',
            margin: '0 auto',
            display: 'flex',
            gap: '0.5rem',
            flexWrap: 'wrap',
          }}
        >
          <button
            type="button"
            onClick={() => setActiveTab('auth')}
            style={{
              background: activeTab === 'auth' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'auth' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            🔐 Acceso & OTP (T-02)
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('consent')}
            style={{
              background: activeTab === 'consent' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'consent' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            ⚖️ Consentimiento Ley 29733 (T-04)
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('curriculum')}
            style={{
              background: activeTab === 'curriculum' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'curriculum' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            📚 Catálogo Curricular (T-10)
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('profile')}
            style={{
              background: activeTab === 'profile' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'profile' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            👤 Perfil & Disponibilidad (T-11)
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('offers')}
            style={{
              background: activeTab === 'offers' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'offers' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            🏷️ Publicar Ofertas (T-14)
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('services')}
            style={{
              background: activeTab === 'services' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'services' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            🛰️ Monitor de Servicios (T-01)
          </button>
        </div>
      </div>

      {/* Contenido principal */}
      <main
        style={{
          flex: 1,
          maxWidth: '1100px',
          width: '100%',
          margin: '0 auto',
          padding: '2rem 1.5rem',
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <span
            style={{
              textTransform: 'uppercase',
              fontSize: '0.75rem',
              fontWeight: 700,
              letterSpacing: '0.1em',
              color: '#B99451',
              display: 'block',
              marginBottom: '0.5rem',
            }}
          >
            Sprint 3 · Construcción de Software I (2026-II)
          </span>
          <h2 style={{ fontSize: '1.75rem', color: '#1C2A59', margin: '0 0 0.5rem 0', fontWeight: 800 }}>
            {activeTab === 'auth'
              ? 'Interfaz de Acceso Institucional y Desafío OTP'
              : activeTab === 'consent'
              ? 'Consentimiento Informado Digital — Ley N° 29733 (T-04)'
              : activeTab === 'curriculum'
              ? 'Consulta Avanzada del Catálogo Curricular EPIS-UPT (T-10)'
              : activeTab === 'profile'
              ? 'Configuración de Perfil Formativo y Disponibilidad Horaria (T-11)'
              : activeTab === 'offers'
              ? 'Publicación y Parametrización de Ofertas de Mentoría (T-14)'
              : 'Infraestructura Base: React + FastAPI + Supabase'}
          </h2>
          <p style={{ margin: '0 auto', maxWidth: '680px', fontSize: '0.88rem', color: '#64748B', lineHeight: 1.6 }}>
            {activeTab === 'auth'
              ? 'Validación del flujo de dos pasos: comprobación de dominio @upt.pe y desafío OTP temporal de 6 dígitos con emisión de JWT.'
              : activeTab === 'consent'
              ? 'Formalización obligatoria de la política institucional de privacidad y tratamiento de datos personales conforme a la Ley N° 29733 (RF02 / CUS01 / RN-02).'
              : activeTab === 'curriculum'
              ? 'Búsqueda en tiempo real por materias filtro, código y temas silábicos para el motor de recomendación Top-k (RF05 / CUS21).'
              : activeTab === 'profile'
              ? 'Selección de intereses/fortalezas y agenda semanal en bloques de 1 hora con validación de mérito RN-03 (RF04 / CUS15).'
              : activeTab === 'offers'
              ? 'Programación de sesiones de mentoría con validación de antelación obligatoria RN-04 (>24h), aforos estándar inmutables RN-05 (10 presencial / 20 virtual) y asignación de infraestructura (RF08 / CUS06).'
              : 'Monitoreo de comunicación asíncrona entre la SPA cliente (React 19 / TypeScript / Vite), FastAPI y Supabase.'
            }
          </p>
        </div>

        {/* Renderizado condicional según pestaña */}
        {activeTab === 'auth' ? (
          <LoginOtpView />
        ) : activeTab === 'consent' ? (
          <ConsentModalView />
        ) : activeTab === 'curriculum' ? (
          <CurriculumCatalogView />
        ) : activeTab === 'profile' ? (
          <ProfileAvailabilityView />
        ) : activeTab === 'offers' ? (
          <OfferPublishView />
        ) : (
          <HealthStatus />
        )}

        {/* Bloque informativo de especificaciones */}
        <div
          style={{
            maxWidth: '920px',
            margin: '2.5rem auto 0 auto',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
            gap: '1rem',
          }}
        >
          <div
            style={{
              background: '#FFFFFF',
              border: '1px solid #E2E8F0',
              borderRadius: '8px',
              padding: '1rem',
              fontSize: '0.82rem',
            }}
          >
            <strong style={{ color: '#1C2A59', display: 'block', marginBottom: '0.25rem' }}>
              ⚖️ T-04: Ley N° 29733 (RF02 / RN-02)
            </strong>
            <span style={{ color: '#64748B' }}>
              Consentimiento legal previo, libre e informado. El rechazo bloquea preventivamente el acceso a la plataforma.
            </span>
          </div>

          <div
            style={{
              background: '#FFFFFF',
              border: '1px solid #E2E8F0',
              borderRadius: '8px',
              padding: '1rem',
              fontSize: '0.82rem',
            }}
          >
            <strong style={{ color: '#1C2A59', display: 'block', marginBottom: '0.25rem' }}>
              🔍 T-10: Catálogo Avanzado (RF05 / CUS21)
            </strong>
            <span style={{ color: '#64748B' }}>
              Buscador en tiempo real con filtrado profundo por código, nombre y unidades temáticas silábicas oficiales.
            </span>
          </div>

          <div
            style={{
              background: '#FFFFFF',
              border: '1px solid #E2E8F0',
              borderRadius: '8px',
              padding: '1rem',
              fontSize: '0.82rem',
            }}
          >
            <strong style={{ color: '#1C2A59', display: 'block', marginBottom: '0.25rem' }}>
              📅 T-11: Perfiles & Agenda (RF04 / CUS15)
            </strong>
            <span style={{ color: '#64748B' }}>
              Matriz interactiva semanal (L-S) y validación de mérito RN-03 (mentores en ciclos VII a X).
            </span>
          </div>

          <div
            style={{
              background: '#FFFFFF',
              border: '1px solid #E2E8F0',
              borderRadius: '8px',
              padding: '1rem',
              fontSize: '0.82rem',
            }}
          >
            <strong style={{ color: '#1C2A59', display: 'block', marginBottom: '0.25rem' }}>
              🏷️ T-14: Ofertas de Mentoría (RF08 / CUS06)
            </strong>
            <span style={{ color: '#64748B' }}>
              Publicación con antelación reglamentaria &gt; 24 h (RN-04) y aforos estándar inmutables de 10 (presencial) o 20 (virtual) cupos (RN-05).
            </span>
          </div>
        </div>
      </main>

      {/* Pie de página institucional */}
      <footer
        style={{
          background: '#FFFFFF',
          borderTop: '1px solid #E2E8F0',
          padding: '1.25rem 2rem',
          textAlign: 'center',
          fontSize: '0.8rem',
          color: '#64748B',
        }}
      >
        Sistema Web P2P de Mentorías Académicas · EPIS UPT (2026) · Construcción de Software I
      </footer>
    </div>
  );
};
