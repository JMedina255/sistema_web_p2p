import type { HealthResponse } from '../data/types';

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

export function getApiBaseUrl(): string {
  return API_BASE_URL;
}
