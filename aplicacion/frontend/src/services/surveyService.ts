/**
 * Servicio de Encuestas de Calidad y Satisfacción Post-Mentoría (T-38 / T-39 / CUS05 / RF18 / RN-12 / RN-13)
 */

import { authService } from './authService';

export interface SurveyPayload {
  calificacion_general: number;
  dominio_tema: number;
  claridad_explicacion: number;
  puntualidad: number;
  comentarios?: string;
}

export interface SurveyResponse {
  id_encuesta: number;
  id_sesion: number;
  estudiante_email: string;
  calificacion_general: number;
  dominio_tema: number;
  claridad_explicacion: number;
  puntualidad: number;
  comentarios?: string;
  created_at: string;
  mensaje: string;
}

export interface SurveyStatus {
  id_sesion: number;
  eligible: boolean;
  has_surveyed: boolean;
  window_open: boolean;
  deadline?: string;
  mensaje?: string;
}

class ApiSurveyAdapter {
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

  public async submitSurvey(
    sessionId: string | number,
    payload: SurveyPayload
  ): Promise<SurveyResponse> {
    const url = `${this.getBaseUrl()}/api/v1/sessions/${sessionId}/survey`;
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

  public async getSurveyStatus(sessionId: string | number): Promise<SurveyStatus> {
    const url = `${this.getBaseUrl()}/api/v1/sessions/${sessionId}/survey`;
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

class MockSurveyAdapter {
  private surveys: Record<string, SurveyResponse> = {};

  public async submitSurvey(
    sessionId: string | number,
    payload: SurveyPayload
  ): Promise<SurveyResponse> {
    const sId = Number(sessionId) || 1;
    const user = authService.getCurrentUser();
    const studentEmail = user?.email || 'estudiante@upt.pe';

    if (
      payload.calificacion_general < 1 ||
      payload.calificacion_general > 5 ||
      payload.dominio_tema < 1 ||
      payload.dominio_tema > 5 ||
      payload.claridad_explicacion < 1 ||
      payload.claridad_explicacion > 5 ||
      payload.puntualidad < 1 ||
      payload.puntualidad > 5
    ) {
      throw new Error('Todas las dimensiones deben ser evaluadas entre 1 y 5 estrellas.');
    }

    if (payload.comentarios && payload.comentarios.trim().length > 0 && payload.comentarios.trim().length < 20) {
      throw new Error(
        'SURVEY_FEEDBACK_TOO_SHORT: Las observaciones cualitativas deben contener al menos 20 caracteres descriptivos.'
      );
    }

    const key = `${sId}:${studentEmail}`;
    if (this.surveys[key]) {
      throw new Error('DUPLICATE_SURVEY_SUBMISSION: Ya has registrado tu evaluación para esta sesión de mentoría.');
    }

    const resp: SurveyResponse = {
      id_encuesta: Object.keys(this.surveys).length + 1,
      id_sesion: sId,
      estudiante_email: studentEmail,
      calificacion_general: payload.calificacion_general,
      dominio_tema: payload.dominio_tema,
      claridad_explicacion: payload.claridad_explicacion,
      puntualidad: payload.puntualidad,
      comentarios: payload.comentarios?.trim(),
      created_at: new Date().toISOString(),
      mensaje: 'Evaluación de calidad post-mentoría registrada con éxito.',
    };
    this.surveys[key] = resp;
    return resp;
  }

  public async getSurveyStatus(sessionId: string | number): Promise<SurveyStatus> {
    const sId = Number(sessionId) || 1;
    const user = authService.getCurrentUser();
    const studentEmail = user?.email || 'estudiante@upt.pe';
    const key = `${sId}:${studentEmail}`;
    const hasSurveyed = Boolean(this.surveys[key]);

    return {
      id_sesion: sId,
      eligible: true,
      has_surveyed: hasSurveyed,
      window_open: true,
      deadline: new Date(Date.now() + 86400000).toISOString(),
      mensaje: 'Consulta de elegibilidad completada.',
    };
  }
}

const apiAdapter = new ApiSurveyAdapter();
const mockAdapter = new MockSurveyAdapter();

function resolveServiceMode(): 'mock' | 'api' {
  if (import.meta.env.PROD) return 'api';
  if (import.meta.env.VITE_SERVICE_MODE === 'mock' || import.meta.env.MODE === 'test') {
    return 'mock';
  }
  return 'api';
}

let currentMode: 'mock' | 'api' = resolveServiceMode();

export const surveyService = {
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

  async submitSurvey(
    sessionId: string | number,
    payload: SurveyPayload
  ): Promise<SurveyResponse> {
    if (currentMode === 'api') {
      return apiAdapter.submitSurvey(sessionId, payload);
    }
    return mockAdapter.submitSurvey(sessionId, payload);
  },

  async getSurveyStatus(sessionId: string | number): Promise<SurveyStatus> {
    if (currentMode === 'api') {
      return apiAdapter.getSurveyStatus(sessionId);
    }
    return mockAdapter.getSurveyStatus(sessionId);
  },
};
