import React, { useEffect, useState, useCallback } from 'react';
import { fetchHealth, fetchDbHealth, getApiBaseUrl } from '../services/apiClient';
import type { HealthState } from '../data/types';

export const HealthStatus: React.FC = () => {
  const [state, setState] = useState<HealthState>({ status: 'idle' });
  const [lastChecked, setLastChecked] = useState<Date | null>(null);

  const checkHealth = useCallback(async () => {
    setState({ status: 'loading' });
    const startTime = performance.now();
    try {
      const data = await fetchHealth();
      const latencyMs = Math.round(performance.now() - startTime);
      const dbData = await fetchDbHealth();
      setState({ status: 'success', data, latencyMs, dbData: dbData || undefined });
      setLastChecked(new Date());
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : 'Error desconocido al conectar con el backend';
      setState({ status: 'error', message });
      setLastChecked(new Date());
    }
  }, []);

  useEffect(() => {
    checkHealth();
  }, [checkHealth]);

  const apiBaseUrl = getApiBaseUrl();

  return (
    <div
      style={{
        background: '#FFFFFF',
        borderRadius: '12px',
        padding: '1.75rem',
        boxShadow: '0 4px 16px rgba(0, 0, 0, 0.06)',
        border: '1px solid #E2E8F0',
        maxWidth: '720px',
        margin: '0 auto',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1C2A59', margin: 0 }}>
            🛰️ Monitor de Servicios (Hito 2 · T-01)
          </h2>
          <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.85rem', color: '#64748B' }}>
            Base URL: <code style={{ background: '#F1F5F9', padding: '0.15rem 0.4rem', borderRadius: '4px' }}>{apiBaseUrl}</code>
          </p>
        </div>
        <button
          onClick={checkHealth}
          disabled={state.status === 'loading'}
          style={{
            background: '#1C2A59',
            color: '#FFFFFF',
            border: 'none',
            borderRadius: '6px',
            padding: '0.5rem 1rem',
            fontSize: '0.85rem',
            fontWeight: 600,
            cursor: state.status === 'loading' ? 'not-allowed' : 'pointer',
            opacity: state.status === 'loading' ? 0.7 : 1,
            transition: 'background 0.2s',
          }}
        >
          {state.status === 'loading' ? '⏳ Comprobando...' : '🔄 Reintentar'}
        </button>
      </div>

      {state.status === 'loading' && (
        <div style={{ padding: '2rem', textAlign: 'center', color: '#64748B' }}>
          <div style={{ fontSize: '2rem', marginBottom: '0.5rem' }}>⚙️</div>
          <p style={{ margin: 0, fontWeight: 500 }}>Consultando estado de salud de FastAPI y Supabase...</p>
        </div>
      )}

      {state.status === 'success' && (
        <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
          {/* Tarjeta de Backend FastAPI */}
          <div
            style={{
              background: '#F0FDF4',
              border: '1px solid #BBF7D0',
              borderRadius: '8px',
              padding: '1rem 1.25rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
              <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                <span style={{ fontSize: '1.25rem' }}>✅</span>
                <strong style={{ color: '#166534', fontSize: '0.95rem' }}>
                  Backend FastAPI: Operativo (HTTP 200)
                </strong>
              </div>
              <span style={{ fontSize: '0.8rem', color: '#15803D', fontWeight: 600 }}>
                {state.latencyMs} ms
              </span>
            </div>

            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(140px, 1fr))',
                gap: '0.5rem',
                fontSize: '0.8rem',
                color: '#334155',
                marginTop: '0.5rem',
              }}
            >
              <div><span style={{ color: '#64748B' }}>Servicio:</span> <strong>{state.data.service}</strong></div>
              <div><span style={{ color: '#64748B' }}>Entorno:</span> <strong>{state.data.environment}</strong></div>
              <div><span style={{ color: '#64748B' }}>Proyecto:</span> <strong>{state.data.project}</strong></div>
            </div>
          </div>

          {/* Tarjeta de Base de Datos PostgreSQL / Supabase */}
          {state.dbData && (
            <div
              style={{
                background: state.dbData.status === 'ok' ? '#F0F9FF' : '#FFFBEB',
                border: `1px solid ${state.dbData.status === 'ok' ? '#BAE6FD' : '#FDE68A'}`,
                borderRadius: '8px',
                padding: '1rem 1.25rem',
              }}
            >
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem' }}>
                  <span style={{ fontSize: '1.25rem' }}>{state.dbData.status === 'ok' ? '🐘' : '⚠️'}</span>
                  <strong style={{ color: state.dbData.status === 'ok' ? '#0369A1' : '#B45309', fontSize: '0.95rem' }}>
                    PostgreSQL (Supabase - p2p-epis-dev): {state.dbData.status === 'ok' ? 'Conectado' : 'No disponible'}
                  </strong>
                </div>
                {state.dbData.latency_ms && (
                  <span style={{ fontSize: '0.8rem', color: '#0284C7', fontWeight: 600 }}>
                    {state.dbData.latency_ms} ms
                  </span>
                )}
              </div>

              <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.82rem', color: '#475569' }}>
                {state.dbData.detail}
              </p>
            </div>
          )}
        </div>
      )}

      {state.status === 'error' && (
        <div
          style={{
            background: '#FEF2F2',
            border: '1px solid #FECACA',
            borderRadius: '8px',
            padding: '1.25rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
            <span style={{ fontSize: '1.5rem' }}>❌</span>
            <div>
              <strong style={{ color: '#991B1B', fontSize: '1rem', display: 'block' }}>
                Fallo de conexión con el backend
              </strong>
              <span style={{ fontSize: '0.82rem', color: '#B91C1C' }}>{state.message}</span>
            </div>
          </div>

          <div style={{ fontSize: '0.82rem', color: '#7F1D1D', marginTop: '0.75rem', lineHeight: 1.5 }}>
            <p style={{ margin: '0 0 0.35rem 0', fontWeight: 600 }}>Diagnóstico sugerido:</p>
            <ul style={{ margin: 0, paddingLeft: '1.2rem' }}>
              <li>Verifica que el backend esté ejecutándose en <code>http://localhost:8000</code>.</li>
              <li>Asegúrate de que la variable <code>VITE_API_BASE_URL</code> apunte al origen correcto.</li>
            </ul>
          </div>
        </div>
      )}

      {lastChecked && (
        <div style={{ textAlign: 'right', marginTop: '0.75rem', fontSize: '0.75rem', color: '#94A3B8' }}>
          Última comprobación: {lastChecked.toLocaleTimeString()}
        </div>
      )}
    </div>
  );
};
