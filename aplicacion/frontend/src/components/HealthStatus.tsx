import React, { useEffect, useState, useCallback } from 'react';
import { fetchHealth, getApiBaseUrl } from '../services/apiClient';
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
      setState({ status: 'success', data, latencyMs });
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
        maxWidth: '680px',
        margin: '0 auto',
      }}
    >
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
        <div>
          <h2 style={{ fontSize: '1.25rem', fontWeight: 700, color: '#1C2A59', margin: 0 }}>
            🛰️ Comunicación React ↔ FastAPI (Hito 1 · T-01)
          </h2>
          <p style={{ margin: '0.25rem 0 0 0', fontSize: '0.85rem', color: '#64748B' }}>
            Endpoint: <code style={{ background: '#F1F5F9', padding: '0.15rem 0.4rem', borderRadius: '4px' }}>{apiBaseUrl}/api/v1/health</code>
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
          <p style={{ margin: 0, fontWeight: 500 }}>Consultando estado de salud del backend FastAPI...</p>
        </div>
      )}

      {state.status === 'success' && (
        <div
          style={{
            background: '#F0FDF4',
            border: '1px solid #BBF7D0',
            borderRadius: '8px',
            padding: '1.25rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
            <span style={{ fontSize: '1.5rem' }}>✅</span>
            <div>
              <strong style={{ color: '#166534', fontSize: '1rem', display: 'block' }}>
                Conexión establecida con éxito (HTTP 200)
              </strong>
              <span style={{ fontSize: '0.8rem', color: '#15803D' }}>
                Latencia de respuesta: {state.latencyMs} ms
              </span>
            </div>
          </div>

          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
              gap: '0.75rem',
              marginTop: '1rem',
              background: '#FFFFFF',
              padding: '0.85rem',
              borderRadius: '6px',
              border: '1px solid #DCFCE7',
              fontSize: '0.82rem',
            }}
          >
            <div>
              <span style={{ color: '#64748B', display: 'block' }}>Estado API:</span>
              <strong style={{ color: '#166534' }}>{state.data.status}</strong>
            </div>
            <div>
              <span style={{ color: '#64748B', display: 'block' }}>Servicio:</span>
              <strong style={{ color: '#1C2A59' }}>{state.data.service}</strong>
            </div>
            <div>
              <span style={{ color: '#64748B', display: 'block' }}>Entorno:</span>
              <strong style={{ color: '#B99451' }}>{state.data.environment}</strong>
            </div>
            <div>
              <span style={{ color: '#64748B', display: 'block' }}>Proyecto:</span>
              <strong style={{ color: '#334155' }}>{state.data.project}</strong>
            </div>
          </div>
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
              <li>Comando para iniciar backend: <code>uvicorn app.main:app --reload --port 8000</code> dentro de <code>aplicacion/backend</code>.</li>
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
