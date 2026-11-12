/**
 * Servicio de Bitácora Pedagógica, Acreditación de Horas y Auditoría Administrativa (T-34 / T-35 / T-40 / T-41 / RF17 / RF26 / RN-12 / RN-14)
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

export interface BitacoraVisadoResponse {
  id_bitacora: number;
  id_sesion: number;
  id_mentor: string;
  horas_declaradas: number;
  visado_administrador: boolean;
  estado_sesion: string;
  auditor_email: string;
  visado_at: string;
  mensaje: string;
}

export interface BitacoraObservacionResponse {
  id_bitacora: number;
  id_sesion: number;
  id_mentor: string;
  estado_sesion: string;
  motivo_observacion: string;
  auditor_email: string;
  observado_at: string;
  mensaje: string;
}

export interface BitacoraItem {
  id_bitacora: number;
  id_sesion: number;
  codigo_sesion?: string;
  id_mentor: string;
  temas_cubiertos: string[];
  observaciones: string;
  nivel_dificultad: string;
  hash_firma: string;
  horas_declaradas: number;
  visado_administrador: boolean;
  estado_sesion: string;
  fecha_inicio?: string;
  created_at: string;
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

  public async getBitacoras(filtro?: string): Promise<BitacoraItem[]> {
    const q = filtro ? `?estado=${encodeURIComponent(filtro)}` : '';
    const url = `${this.getBaseUrl()}/api/v1/bitacoras${q}`;
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

  public async visarBitacora(bitacoraId: string | number): Promise<BitacoraVisadoResponse> {
    const url = `${this.getBaseUrl()}/api/v1/bitacoras/${bitacoraId}/visar`;
    const res = await fetch(url, {
      method: 'POST',
      headers: this.getAuthHeaders(),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => null);
      throw new Error(err?.detail || `Error HTTP ${res.status}: ${res.statusText}`);
    }
    return res.json();
  }

  public async observarBitacora(
    bitacoraId: string | number,
    motivo: string
  ): Promise<BitacoraObservacionResponse> {
    const url = `${this.getBaseUrl()}/api/v1/bitacoras/${bitacoraId}/observar`;
    const res = await fetch(url, {
      method: 'POST',
      headers: this.getAuthHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ motivo }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => null);
      throw new Error(err?.detail || `Error HTTP ${res.status}: ${res.statusText}`);
    }
    return res.json();
  }
}

class MockBitacoraAdapter {
  private bitacoras: Record<number, BitacoraItem> = {
    1: {
      id_bitacora: 1,
      id_sesion: 1,
      codigo_sesion: 'SES-CC-001',
      id_mentor: 'mentor.sistemas@upt.pe',
      temas_cubiertos: ['Punteros y Gestión Dinámica de Memoria'],
      observaciones:
        'Se desarrollaron ejemplos prácticos de punteros dobles y asignación dinámica con malloc y free en C++.',
      nivel_dificultad: 'Medio',
      hash_firma: 'sha256-mock-hash-1-c89a0b12',
      horas_declaradas: 2.0,
      visado_administrador: false,
      estado_sesion: 'BITACORA_REGISTRADA',
      fecha_inicio: new Date(Date.now() - 3600000 * 5).toISOString(),
      created_at: new Date(Date.now() - 3600000 * 4).toISOString(),
    },
    2: {
      id_bitacora: 2,
      id_sesion: 2,
      codigo_sesion: 'SES-CC-002',
      id_mentor: 'mentor.redes@upt.pe',
      temas_cubiertos: ['Subnetting IPv4 y VLSM'],
      observaciones:
        'Resolución guiada de ejercicios de direccionamiento con máscaras de subred de longitud variable.',
      nivel_dificultad: 'Alto',
      hash_firma: 'sha256-mock-hash-2-e91b3fa4',
      horas_declaradas: 1.5,
      visado_administrador: true,
      estado_sesion: 'HORAS_VISADAS',
      fecha_inicio: new Date(Date.now() - 3600000 * 20).toISOString(),
      created_at: new Date(Date.now() - 3600000 * 18).toISOString(),
    },
    3: {
      id_bitacora: 3,
      id_sesion: 3,
      codigo_sesion: 'SES-CC-003',
      id_mentor: 'mentor.bd@upt.pe',
      temas_cubiertos: ['Normalización hasta Tercera Forma Normal (3FN)'],
      observaciones:
        'Presentación teórica y aplicación a modelo relacional de matrícula universitaria con alta participación.',
      nivel_dificultad: 'Medio',
      hash_firma: 'sha256-mock-hash-3-a72c1d98',
      horas_declaradas: 1.0,
      visado_administrador: false,
      estado_sesion: 'OBSERVADA',
      fecha_inicio: new Date(Date.now() - 3600000 * 10).toISOString(),
      created_at: new Date(Date.now() - 3600000 * 8).toISOString(),
    },
  };

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

    const item: BitacoraItem = {
      id_bitacora: sId,
      id_sesion: sId,
      codigo_sesion: `SES-MOCK-${sId}`,
      id_mentor: mentorEmail,
      temas_cubiertos: payload.temas_cubiertos,
      observaciones: payload.observaciones,
      nivel_dificultad: payload.nivel_dificultad,
      hash_firma: mockHash,
      horas_declaradas: 1.0,
      visado_administrador: false,
      estado_sesion: 'BITACORA_REGISTRADA',
      created_at: new Date().toISOString(),
    };
    this.bitacoras[sId] = item;

    return {
      id_bitacora: sId,
      id_sesion: sId,
      id_mentor: mentorEmail,
      temas_cubiertos: payload.temas_cubiertos,
      observaciones: payload.observaciones,
      nivel_dificultad: payload.nivel_dificultad,
      hash_firma: mockHash,
      horas_declaradas: 1.0,
      visado_administrador: false,
      created_at: item.created_at,
      mensaje: 'Bitácora pedagógica registrada y sellada criptográficamente con éxito.',
    };
  }

  public async getBitacora(sessionId: string | number): Promise<BitacoraResponse> {
    const sId = Number(sessionId) || 1;
    if (!this.bitacoras[sId]) {
      throw new Error('NOT_FOUND: No existe bitácora para esta sesión.');
    }
    const b = this.bitacoras[sId];
    return {
      id_bitacora: b.id_bitacora,
      id_sesion: b.id_sesion,
      id_mentor: b.id_mentor,
      temas_cubiertos: b.temas_cubiertos,
      observaciones: b.observaciones,
      nivel_dificultad: b.nivel_dificultad,
      hash_firma: b.hash_firma,
      horas_declaradas: b.horas_declaradas,
      visado_administrador: b.visado_administrador,
      created_at: b.created_at,
      mensaje: 'Bitácora pedagógica recuperada con éxito.',
    };
  }

  public async getBitacoras(filtro?: string): Promise<BitacoraItem[]> {
    const all = Object.values(this.bitacoras);
    if (!filtro || filtro === 'TODAS') return all;
    if (filtro === 'PENDIENTES' || filtro === 'BITACORA_REGISTRADA') {
      return all.filter((b) => !b.visado_administrador && b.estado_sesion === 'BITACORA_REGISTRADA');
    }
    if (filtro === 'VISADAS' || filtro === 'HORAS_VISADAS') {
      return all.filter((b) => b.visado_administrador || b.estado_sesion === 'HORAS_VISADAS');
    }
    if (filtro === 'OBSERVADA') {
      return all.filter((b) => b.estado_sesion === 'OBSERVADA');
    }
    return all;
  }

  public async visarBitacora(bitacoraId: string | number): Promise<BitacoraVisadoResponse> {
    const id = Number(bitacoraId) || 1;
    const b = this.bitacoras[id];
    if (!b) {
      throw new Error('NOT_FOUND: La bitácora pedagógica no existe.');
    }
    b.visado_administrador = true;
    b.estado_sesion = 'HORAS_VISADAS';

    return {
      id_bitacora: b.id_bitacora,
      id_sesion: b.id_sesion,
      id_mentor: b.id_mentor,
      horas_declaradas: b.horas_declaradas,
      visado_administrador: true,
      estado_sesion: 'HORAS_VISADAS',
      auditor_email: authService.getCurrentUser()?.email || 'admin.epis@upt.pe',
      visado_at: new Date().toISOString(),
      mensaje: `Bitácora pedagógica visada institucionalmente con éxito. ${b.horas_declaradas} horas formativas acreditadas para certificación.`,
    };
  }

  public async observarBitacora(
    bitacoraId: string | number,
    motivo: string
  ): Promise<BitacoraObservacionResponse> {
    const id = Number(bitacoraId) || 1;
    const cleanMotivo = motivo ? motivo.trim() : '';
    if (cleanMotivo.length < 15) {
      throw new Error(
        'OBSERVATION_REASON_REQUIRED: Debe ingresar obligatoriamente una justificación para la observación técnica (mínimo 15 caracteres).'
      );
    }
    const b = this.bitacoras[id];
    if (!b) {
      throw new Error('NOT_FOUND: La bitácora pedagógica no existe.');
    }
    b.visado_administrador = false;
    b.estado_sesion = 'OBSERVADA';

    return {
      id_bitacora: b.id_bitacora,
      id_sesion: b.id_sesion,
      id_mentor: b.id_mentor,
      estado_sesion: 'OBSERVADA',
      motivo_observacion: cleanMotivo,
      auditor_email: authService.getCurrentUser()?.email || 'admin.epis@upt.pe',
      observado_at: new Date().toISOString(),
      mensaje: 'Bitácora observada para corrección técnica por el Administrador.',
    };
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

  async getBitacoras(filtro?: string): Promise<BitacoraItem[]> {
    if (currentMode === 'api') {
      return apiAdapter.getBitacoras(filtro);
    }
    return mockAdapter.getBitacoras(filtro);
  },

  async visarBitacora(bitacoraId: string | number): Promise<BitacoraVisadoResponse> {
    if (currentMode === 'api') {
      return apiAdapter.visarBitacora(bitacoraId);
    }
    return mockAdapter.visarBitacora(bitacoraId);
  },

  // Alias compatible con tests y Cuadro 3.1
  async visar(bitacoraId: string | number): Promise<BitacoraVisadoResponse> {
    return this.visarBitacora(bitacoraId);
  },

  async observarBitacora(
    bitacoraId: string | number,
    motivo: string
  ): Promise<BitacoraObservacionResponse> {
    if (currentMode === 'api') {
      return apiAdapter.observarBitacora(bitacoraId, motivo);
    }
    return mockAdapter.observarBitacora(bitacoraId, motivo);
  },

  // Alias compatible con tests
  async observar(
    bitacoraId: string | number,
    motivo: string
  ): Promise<BitacoraObservacionResponse> {
    return this.observarBitacora(bitacoraId, motivo);
  },
};
