import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { fetchHealth, fetchDbHealth, getApiBaseUrl } from '../apiClient';

describe('apiClient (T-01 / RNF09)', () => {
  const originalFetch = globalThis.fetch;

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    globalThis.fetch = originalFetch;
  });

  it('getApiBaseUrl retorna una URL base válida', () => {
    const url = getApiBaseUrl();
    expect(url).toMatch(/^https?:\/\//);
  });

  it('fetchHealth devuelve datos cuando la API responde HTTP 200', async () => {
    const mockData = {
      status: 'ok',
      service: 'backend',
      project: 'Sistema Web P2P - EPIS UPT',
      environment: 'development',
    };

    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => mockData,
    } as unknown as Response);

    const res = await fetchHealth();
    expect(res).toEqual(mockData);
  });

  it('fetchHealth lanza Error cuando la respuesta no es ok', async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 500,
      statusText: 'Internal Server Error',
    } as unknown as Response);

    await expect(fetchHealth()).rejects.toThrow(/Error HTTP 500/);
  });

  it('fetchDbHealth devuelve datos cuando responde 200', async () => {
    const mockDbData = {
      status: 'ok',
      database: 'connected',
      detail: 'Conexión a PostgreSQL (Supabase) verificada con éxito',
      latency_ms: 15.2,
      environment: 'development',
    };

    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: true,
      status: 200,
      json: async () => mockDbData,
    } as unknown as Response);

    const res = await fetchDbHealth();
    expect(res).toEqual(mockDbData);
  });

  it('fetchDbHealth retorna null cuando responde 404 (fuera de dev)', async () => {
    globalThis.fetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 404,
    } as unknown as Response);

    const res = await fetchDbHealth();
    expect(res).toBeNull();
  });

  it('fetchDbHealth maneja excepciones de red retornando null sin colapsar', async () => {
    globalThis.fetch = vi.fn().mockRejectedValue(new Error('Network offline'));

    const res = await fetchDbHealth();
    expect(res).toBeNull();
  });
});
