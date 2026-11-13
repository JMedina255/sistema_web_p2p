/**
 * Servicio de Asistencia Digital con Código QR Dinámico TOTP (T-34 / T-36 / CUS12 / RF17 / RN-12)
 */

import { authService } from './authService';

export interface DynamicQrTokenResponse {
  session_id: number;
  token: string;
  totp_code: string;
  expires_in: number;
  expires_at: string;
}

export interface AttendanceCheckinPayload {
  qr_token?: string;
  numeric_code?: string;
  estudiante_email?: string;
}

export interface AttendanceCheckinResponse {
  id_asistencia: number;
  id_sesion: number;
  estudiante_email: string;
  asistio: boolean;
  fecha_checkin: string;
  mensaje: string;
}

export interface AttendanceItem {
  id_asistencia: number;
  id_sesion: number;
  estudiante_email: string;
  asistio: boolean;
  fecha_checkin: string | null;
}

class ApiAttendanceAdapter {
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

  public async getDynamicQrToken(sessionId: string | number): Promise<DynamicQrTokenResponse> {
    const url = `${this.getBaseUrl()}/api/v1/sessions/${sessionId}/attendance/token`;
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

  public async checkIn(
    sessionId: string | number,
    payload: AttendanceCheckinPayload
  ): Promise<AttendanceCheckinResponse> {
    const url = `${this.getBaseUrl()}/api/v1/sessions/${sessionId}/attendance/check-in`;
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

  public async getAttendanceList(sessionId: string | number): Promise<AttendanceItem[]> {
    const url = `${this.getBaseUrl()}/api/v1/sessions/${sessionId}/attendance`;
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

class MockAttendanceAdapter {
  private mockToken: DynamicQrTokenResponse | null = null;
  private roster: Record<number, AttendanceItem[]> = {};

  public async getDynamicQrToken(sessionId: string | number): Promise<DynamicQrTokenResponse> {
    const sId = Number(sessionId) || 1;
    const now = Date.now();
    const token = `mock-token-${sId}-${now}`;
    const totp_code = `${Math.floor(100000 + Math.random() * 900000)}`;
    const expires_at = new Date(now + 30000).toISOString();

    this.mockToken = {
      session_id: sId,
      token,
      totp_code,
      expires_in: 30,
      expires_at,
    };
    return this.mockToken;
  }

  public async checkIn(
    sessionId: string | number,
    payload: AttendanceCheckinPayload
  ): Promise<AttendanceCheckinResponse> {
    const sId = Number(sessionId) || 1;
    const email = payload.estudiante_email || authService.getCurrentUser()?.email || '2024071111@upt.pe';

    if (!this.roster[sId]) {
      this.roster[sId] = [];
    }

    const existing = this.roster[sId].find((r) => r.estudiante_email === email);
    if (existing) {
      existing.asistio = true;
      existing.fecha_checkin = new Date().toISOString();
    } else {
      this.roster[sId].push({
        id_asistencia: this.roster[sId].length + 1,
        id_sesion: sId,
        estudiante_email: email,
        asistio: true,
        fecha_checkin: new Date().toISOString(),
      });
    }

    return {
      id_asistencia: 1,
      id_sesion: sId,
      estudiante_email: email,
      asistio: true,
      fecha_checkin: new Date().toISOString(),
      mensaje: '¡Asistencia registrada exitosamente! Gracias por tu puntualidad.',
    };
  }

  public async getAttendanceList(sessionId: string | number): Promise<AttendanceItem[]> {
    const sId = Number(sessionId) || 1;
    return this.roster[sId] || [];
  }
}

const apiAdapter = new ApiAttendanceAdapter();
const mockAdapter = new MockAttendanceAdapter();

function resolveServiceMode(): 'mock' | 'api' {
  if (import.meta.env.PROD) return 'api';
  if (import.meta.env.VITE_SERVICE_MODE === 'mock' || import.meta.env.MODE === 'test') {
    return 'mock';
  }
  return 'api';
}

let currentMode: 'mock' | 'api' = resolveServiceMode();

export const attendanceService = {
  getMode(): 'mock' | 'api' {
    return currentMode;
  },

  setMode(mode: 'mock' | 'api'): void {
    if (import.meta.env.PROD && mode === 'mock') {
      console.warn('Violación de seguridad: El modo mock está desactivado en producción.');
      currentMode = 'api';
      return;
    }
    currentMode = mode;
  },

  async getDynamicQrToken(sessionId: string | number): Promise<DynamicQrTokenResponse> {
    if (currentMode === 'api') {
      return apiAdapter.getDynamicQrToken(sessionId);
    }
    return mockAdapter.getDynamicQrToken(sessionId);
  },

  async checkIn(
    sessionId: string | number,
    payload: AttendanceCheckinPayload
  ): Promise<AttendanceCheckinResponse> {
    if (currentMode === 'api') {
      return apiAdapter.checkIn(sessionId, payload);
    }
    return mockAdapter.checkIn(sessionId, payload);
  },

  async getAttendanceList(sessionId: string | number): Promise<AttendanceItem[]> {
    if (currentMode === 'api') {
      return apiAdapter.getAttendanceList(sessionId);
    }
    return mockAdapter.getAttendanceList(sessionId);
  },
};
