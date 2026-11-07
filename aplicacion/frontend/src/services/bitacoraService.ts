/**
 * Servicio de Bitácora Pedagógica y Acreditación de Horas (T-34 / T-35 / CUS13 / RF17 / RN-12)
 */

import { authService } from './authService';

export interface BitacoraPayload {
  temas_cubiertos: string[];
  observaciones: string;
  nivel_dificultad: 'Bajo' | 'Medio' | 'Alto';
}

export interface BitacoraResponse {
  id_bitacora: number;
  id_sesion: number;
  id_mentor: string;
  temas_cubiertos: string[];
  observaciones: string;
  nivel_dificultad: string;
  hash_firma: string;
  horas_declaradas: number;
  visado_administrador: boolean;
  created_at: string;
  mensaje: string;
}

class ApiBitacoraAdapter {
  private getBaseUrl(): string {
    return (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
  }

  private getAuthHeaders(custom: Record<string, string> = {}): Record<string, string> {
    const headers: Record<string, string> = {
      Accept: 'application/json',
      ...custom,
    };
    const token = authService.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  public async submitBitacora(
    sessionId: string | number,
    payload: BitacoraPayload
  ): Promise<BitacoraResponse> {
    const url = `${this.getBaseUrl()}/api/v1/sessions/${sessionId}/bitacora`;
    const res = await fetch(url, {
      method: 'POST',
      headers: this.getAuthHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify(payload),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => null);
      throw new Error(err?.detail || `Error HTTP ${res.status}: ${res.statusText}`);
    }
    return res.json();
  }

  public async getBitacora(sessionId: string | number): Promise<BitacoraResponse> {
    const url = `${this.getBaseUrl()}/api/v1/sessions/${sessionId}/bitacora`;
    const res = await fetch(url, {
      method: 'GET',
      headers: this.getAuthHeaders(),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => null);
      throw new Error(err?.detail || `Error HTTP ${res.status}: ${res.statusText}`);
    }
    return res.json();
  }
}

class MockBitacoraAdapter {
  private bitacoras: Record<number, BitacoraResponse> = {};

  public async submitBitacora(
    sessionId: string | number,
    payload: BitacoraPayload
  ): Promise<BitacoraResponse> {
    const sId = Number(sessionId) || 1;
    if (payload.observaciones.trim().length < 50) {
      throw new Error('VALIDATION_ERROR: Las observaciones deben tener al menos 50 caracteres.');
    }
    const mockHash = `sha256-mock-${sId}-${Date.now()}`;
    const mentorEmail = authService.getCurrentUser()?.email || 'mentor@upt.pe';

    const resp: BitacoraResponse = {
      id_bitacora: sId,
      id_sesion: sId,
      id_mentor: mentorEmail,
      temas_cubiertos: payload.temas_cubiertos,
      observaciones: payload.observaciones,
      nivel_dificultad: payload.nivel_dificultad,
      hash_firma: mockHash,
      horas_declaradas: 1.0,
      visado_administrador: false,
      created_at: new Date().toISOString(),
      mensaje: 'Bitácora pedagógica registrada y sellada criptográficamente con éxito.',
    };
    this.bitacoras[sId] = resp;
    return resp;
  }

  public async getBitacora(sessionId: string | number): Promise<BitacoraResponse> {
    const sId = Number(sessionId) || 1;
    if (!this.bitacoras[sId]) {
      throw new Error('NOT_FOUND: No existe bitácora para esta sesión.');
    }
    return this.bitacoras[sId];
  }
}

const apiAdapter = new ApiBitacoraAdapter();
const mockAdapter = new MockBitacoraAdapter();

function resolveServiceMode(): 'mock' | 'api' {
  if (import.meta.env.PROD) return 'api';
  if (import.meta.env.VITE_SERVICE_MODE === 'api') return 'api';
  return 'mock';
}

const currentMode = resolveServiceMode();

export const bitacoraService = {
  async submitBitacora(
    sessionId: string | number,
    payload: BitacoraPayload
  ): Promise<BitacoraResponse> {
    if (currentMode === 'api') {
      return apiAdapter.submitBitacora(sessionId, payload);
    }
    return mockAdapter.submitBitacora(sessionId, payload);
  },

  async getBitacora(sessionId: string | number): Promise<BitacoraResponse> {
    if (currentMode === 'api') {
      return apiAdapter.getBitacora(sessionId);
    }
    return mockAdapter.getBitacora(sessionId);
  },
};
