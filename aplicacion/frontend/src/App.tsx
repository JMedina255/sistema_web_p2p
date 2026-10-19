import React, { useState } from 'react';
import { HealthStatus } from './components/HealthStatus';
import { LoginOtpView } from './components/LoginOtpView';

export const App: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'auth' | 'services'>('auth');

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
              Sprint 1 · Hito 3 (T-02)
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

      {/* Selector de Vistas / Pestañas de Sprint 1 */}
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
            gap: '0.75rem',
          }}
        >
          <button
            onClick={() => setActiveTab('auth')}
            style={{
              background: activeTab === 'auth' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'auth' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1.1rem',
              fontSize: '0.84rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            🔐 Acceso & OTP de Prueba (T-02)
          </button>
          <button
            onClick={() => setActiveTab('services')}
            style={{
              background: activeTab === 'services' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'services' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1.1rem',
              fontSize: '0.84rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            🛰️ Monitor de Servicios & BD (T-01)
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
          padding: '2.5rem 1.5rem',
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
            Sprint 1 · Construcción de Software I (2026-II)
          </span>
          <h2 style={{ fontSize: '1.8rem', color: '#1C2A59', margin: '0 0 0.5rem 0', fontWeight: 800 }}>
            {activeTab === 'auth'
              ? 'Interfaz de Acceso Institucional y Desafío OTP'
              : 'Infraestructura Base: React + FastAPI + Supabase'}
          </h2>
          <p style={{ margin: '0 auto', maxWidth: '640px', fontSize: '0.92rem', color: '#64748B', lineHeight: 1.6 }}>
            {activeTab === 'auth'
              ? 'Validación del flujo de dos pasos: comprobación de dominio @upt.pe y desafío OTP temporal de 6 dígitos con vigencia de 5 minutos (RF01 / CUS01 / RNF01).'
              : 'Monitoreo de comunicación asíncrona entre la SPA cliente (React 19 / TypeScript / Vite), el backend RESTful (FastAPI) y PostgreSQL (Supabase).'
            }
          </p>
        </div>

        {/* Renderizado condicional según pestaña */}
        {activeTab === 'auth' ? <LoginOtpView /> : <HealthStatus />}

        {/* Bloque informativo de especificaciones del sprint */}
        <div
          style={{
            maxWidth: '720px',
            margin: '2.5rem auto 0 auto',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(210px, 1fr))',
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
              🎯 Trazabilidad CUS01
            </strong>
            <span style={{ color: '#64748B' }}>
              Dominio exclusivo @upt.pe, OTP numérico de 6 dígitos con soporte de ceros iniciales.
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
              ⏱️ Gobernanza Temporal
            </strong>
            <span style={{ color: '#64748B' }}>
              Vigencia estricta de 5 min (RNF01) calculada desde expires_at y cooldown de reenvío de 60s.
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
              🔌 Adaptador Mock Dev
            </strong>
            <span style={{ color: '#64748B' }}>
              Simulación explícita para pruebas de Joan; pendiente de integración con API T-03 de Renzo.
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
