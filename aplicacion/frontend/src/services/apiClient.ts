import type { HealthResponse, DbHealthResponse } from '../data/types';

const API_BASE_URL: string =
  (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';

export async function fetchHealth(): Promise<HealthResponse> {
  const url = `${API_BASE_URL}/api/v1/health`;
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Error HTTP ${response.status}: ${response.statusText}`);
  }

  const data: HealthResponse = await response.json();
  return data;
}

export async function fetchDbHealth(): Promise<DbHealthResponse | null> {
  const url = `${API_BASE_URL}/api/v1/health/db`;
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });

    if (response.status === 404) {
      // Endpoint no expuesto fuera de desarrollo
      return null;
    }

    const data = await response.json();
    return data as DbHealthResponse;
  } catch (err) {
    console.warn('No fue posible consultar /health/db:', err);
    return null;
  }
}

export function getApiBaseUrl(): string {
  return API_BASE_URL;
}
