import React from 'react';
import { HealthStatus } from './components/HealthStatus';

export const App: React.FC = () => {
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
              Sprint 1 · Hito 1 (T-01)
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
        <div style={{ textAlign: 'center', marginBottom: '2.5rem' }}>
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
            Fase de Construcción · Arquitectura Desacoplada (RNF09)
          </span>
          <h2 style={{ fontSize: '1.9rem', color: '#1C2A59', margin: '0 0 0.5rem 0', fontWeight: 800 }}>
            Infraestructura Base: React + FastAPI
          </h2>
          <p style={{ margin: '0 auto', maxWidth: '640px', fontSize: '0.95rem', color: '#64748B', lineHeight: 1.6 }}>
            Esta pantalla valida la comunicación asíncrona entre la SPA cliente (React 19 / TypeScript / Vite)
            y el backend RESTful (FastAPI / Uvicorn), sentando las bases operativas del <strong>Sprint 1</strong>.
          </p>
        </div>

        {/* Tarjeta de verificación de salud */}
        <HealthStatus />

        {/* Bloque informativo de especificaciones del hito */}
        <div
          style={{
            maxWidth: '680px',
            margin: '2rem auto 0 auto',
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
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
              ⚛️ Frontend SPA
            </strong>
            <span style={{ color: '#64748B' }}>
              React 19, TypeScript estricto, Vite, arquitectura modular orientada a servicios.
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
              🐍 Backend API
            </strong>
            <span style={{ color: '#64748B' }}>
              FastAPI con Uvicorn, contratos JSON fuertemente tipados con Pydantic, CORS configurado.
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
              📐 Trazabilidad SAD
            </strong>
            <span style={{ color: '#64748B' }}>
              Estructura canónica: app/api, app/core, app/services, app/models y app/db.
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
