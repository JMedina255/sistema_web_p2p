/**
 * Servicio de Reservas Transaccionales de Cupos de Mentoría (T-23).
 * Módulo MOD-05: Quórum, Confirmación y Cancelaciones.
 * Trazabilidad: CUS04, RF12, RN-05, RN-08, RNF07.
 */

import { getApiBaseUrl } from './apiClient';
import { authService } from './authService';

/**
 * Estados canónicos del ciclo de vida de una reserva de mentoría (CUS04 / MOD-05).
 */
export type BookingStatus =
  | 'PENDIENTE_CONFIRMACION'
  | 'CONFIRMADA'
  | 'CANCELADA_USUARIO'
  | 'NO_CONFIRMADA'
  | 'CANCELADA_SISTEMA'
  | 'ASISTIDA'
  | 'INASISTENCIA';

/**
 * Payload para formalizar de manera atómica una reserva de cupo (CUS04 / RF12 / RN-05).
 */
export interface BookingCreatePayload {
  /** Identificador unívoco entero de la sesión de mentoría (id_sesion >= 1) */
  id_sesion: number;
  /** Correo institucional @upt.pe del estudiante mentoreado */
  estudiante_email: string;
}

/**
 * Respuesta canónica de confirmación de reserva provisional (HTTP 201 Created).
 */
export interface BookingResponse {
  id_reserva: number;
  codigo_reserva: string;
  id_sesion: number;
  estudiante_email: string;
  estado: BookingStatus;
  fecha_reserva: string; // ISO 8601
  fecha_limite_confirmacion?: string | null; // ISO 8601
  mensaje: string;
  ticket_hash?: string | null;
}

/**
 * Detalle ampliado de una reserva de cupo con metadatos de la sesión (CUS04 / RF12).
 */
export interface BookingDetailResponse {
  id_reserva: number;
  codigo_reserva: string;
  id_sesion: number;
  codigo_sesion?: string | null;
  estudiante_email: string;
  estado: BookingStatus | string;
  fecha_reserva: string;
  fecha_ratificacion?: string | null;
  motivo_cancelacion?: string | null;
  ticket_hash?: string | null;
  nombre_asignatura?: string | null;
  nombre_tema?: string | null;
  fecha_inicio?: string | null;
  duracion_minutos?: number | null;
  modalidad?: string | null;
  espacio_asignado?: string | null;
  mentor_email?: string | null;
}

/**
 * Códigos de error estructurados del servicio de reservas.
 */
export type BookingErrorCode =
  | 'WINDOW_CLOSED_T24H'
  | 'MENTOR_CANNOT_BOOK'
  | 'DUPLICATE_BOOKING'
  | 'CAPACITY_EXCEEDED'
  | 'CONSENT_REQUIRED'
  | 'SESSION_NOT_FOUND'
  | 'SESSION_NOT_OPEN'
  | 'DATABASE_BUSY'
  | 'UNAUTHORIZED'
  | 'FORBIDDEN'
  | 'VALIDATION_ERROR'
  | 'NETWORK_ERROR'
  | 'UNKNOWN_ERROR';

/**
 * Excepción especializada para fallos de reserva de cupos (T-23 / RF12).
 */
export class BookingException extends Error {
  public code: BookingErrorCode;
  public status?: number;
  public details?: unknown;

  constructor(code: BookingErrorCode, message: string, status?: number, details?: unknown) {
    super(message);
    this.name = 'BookingException';
    this.code = code;
    this.status = status;
    this.details = details;
  }
}

// ============================================================================
// Adaptador de API REST Real (FastAPI Backend)
// ============================================================================

export class ApiBookingAdapter {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    this.baseUrl = (baseUrl || getApiBaseUrl()).replace(/\/+$/, '');
  }

  public getBaseUrl(): string {
    return this.baseUrl;
  }

  public setBaseUrl(url: string): void {
    this.baseUrl = url.replace(/\/+$/, '');
  }

  /**
   * Formaliza una reserva provisional consumiendo POST /api/v1/bookings/reserve.
   */
  public async reserveSeat(payload: BookingCreatePayload): Promise<BookingResponse> {
    // 1. Validaciones preventivas de contrato en cliente
    if (!payload.id_sesion || !Number.isInteger(payload.id_sesion) || payload.id_sesion < 1) {
      throw new BookingException(
        'VALIDATION_ERROR',
        'El identificador de sesión debe ser un número entero positivo válido.',
        400
      );
    }

    const cleanEmail = (payload.estudiante_email || '').trim().toLowerCase();
    if (!cleanEmail.endsWith('@upt.pe')) {
      throw new BookingException(
        'VALIDATION_ERROR',
        'El correo del estudiante debe pertenecer obligatoriamente al dominio institucional @upt.pe.',
        400
      );
    }

    const url = `${this.baseUrl}/api/v1/bookings/reserve`;
    const token = authService.getToken();

    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    let response: Response;
    try {
      response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          id_sesion: payload.id_sesion,
          estudiante_email: cleanEmail,
        }),
      });
    } catch (err: unknown) {
      // Regla de seguridad: no transformar fallos de red en reintentos ciegos
      throw new BookingException(
        'NETWORK_ERROR',
        'No fue posible comunicar con el servidor de reservas. Verifique su conectividad a la red institucional.',
        undefined,
        err
      );
    }

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      this.handleHttpError(response.status, data);
    }

    return data as BookingResponse;
  }

  /**
   * Consulta las reservas personales del estudiante (GET /api/v1/bookings/my-reservations).
   */
  public async getMyReservations(
    estado?: string,
    studentEmail?: string
  ): Promise<BookingDetailResponse[]> {
    const params = new URLSearchParams();
    if (estado) params.append('estado', estado);
    if (studentEmail) params.append('student_email', studentEmail);

    const qs = params.toString() ? `?${params.toString()}` : '';
    const url = `${this.baseUrl}/api/v1/bookings/my-reservations${qs}`;
    const token = authService.getToken();

    const headers: Record<string, string> = {
      Accept: 'application/json',
    };

    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    let response: Response;
    try {
      response = await fetch(url, { method: 'GET', headers });
    } catch (err: unknown) {
      throw new BookingException(
        'NETWORK_ERROR',
        'Error de red al consultar el historial de reservas.',
        undefined,
        err
      );
    }

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      this.handleHttpError(response.status, data);
    }

    return (Array.isArray(data) ? data : []) as BookingDetailResponse[];
  }

  /**
   * Interpreta las respuestas de error estructuradas de FastAPI y eleva BookingException.
   */
  private handleHttpError(status: number, data: unknown): never {
    let code: BookingErrorCode = 'UNKNOWN_ERROR';
    let message = `Error al procesar la reserva (HTTP ${status}).`;

    const detail = (data as { detail?: unknown })?.detail;

    if (typeof detail === 'string') {
      message = detail;
      if (detail.includes('WINDOW_CLOSED_T24H')) {
        code = 'WINDOW_CLOSED_T24H';
      } else if (detail.includes('MENTOR_CANNOT_BOOK')) {
        code = 'MENTOR_CANNOT_BOOK';
      } else if (detail.includes('DUPLICATE_BOOKING')) {
        code = 'DUPLICATE_BOOKING';
      } else if (detail.includes('CAPACITY_EXCEEDED')) {
        code = 'CAPACITY_EXCEEDED';
      } else if (detail.includes('CONSENT_REQUIRED')) {
        code = 'CONSENT_REQUIRED';
      } else if (detail.includes('DATABASE_BUSY')) {
        code = 'DATABASE_BUSY';
      } else if (detail.includes('SESSION_NOT_FOUND')) {
        code = 'SESSION_NOT_FOUND';
      } else if (detail.includes('SESSION_NOT_OPEN')) {
        code = 'SESSION_NOT_OPEN';
      }
    } else if (typeof detail === 'object' && detail !== null) {
      const errObj = detail as { code?: string; message?: string };
      if (errObj.code && typeof errObj.code === 'string') {
        code = errObj.code as BookingErrorCode;
      }
      if (errObj.message && typeof errObj.message === 'string') {
        message = errObj.message;
      }
    }

    if (code === 'UNKNOWN_ERROR') {
      switch (status) {
        case 400:
          code = 'VALIDATION_ERROR';
          break;
        case 401:
          code = 'UNAUTHORIZED';
          message = message || 'Se requiere autenticación institucional válida.';
          break;
        case 403:
          code = 'FORBIDDEN';
          message = message || 'Acceso restringido a los recursos de reserva.';
          break;
        case 404:
          code = 'SESSION_NOT_FOUND';
          message = message || 'La sesión de mentoría seleccionada no existe o fue retirada.';
          break;
        case 409:
          code = 'CAPACITY_EXCEEDED';
          message = 'Aforo completo. No quedan vacantes disponibles en esta sesión.';
          break;
        case 503:
          code = 'DATABASE_BUSY';
          message =
            'El servicio de reservas se encuentra temporalmente sobrecargado. Reintente en unos momentos.';
          break;
      }
    }

    throw new BookingException(code, message, status, data);
  }
}

// ============================================================================
// Adaptador MOCK en Memoria (Para Desarrollo Local y Pruebas Unitarias Aisladas)
// ============================================================================

export class MockBookingAdapter {
  private bookings: BookingResponse[] = [];
  private nextBookingId = 501;

  constructor() {
    this.resetToDefaults();
  }

  public resetToDefaults(): void {
    this.bookings = [];
    this.nextBookingId = 501;
  }

  public async reserveSeat(payload: BookingCreatePayload): Promise<BookingResponse> {
    if (
      !payload.id_sesion ||
      !Number.isInteger(payload.id_sesion) ||
      payload.id_sesion < 1
    ) {
      throw new BookingException(
        'VALIDATION_ERROR',
        'El identificador de sesión debe ser un entero positivo válido.',
        400
      );
    }

    const cleanEmail = (payload.estudiante_email || '').trim().toLowerCase();
    if (!cleanEmail.endsWith('@upt.pe')) {
      throw new BookingException(
        'VALIDATION_ERROR',
        'El correo del estudiante debe pertenecer al dominio institucional @upt.pe.',
        400
      );
    }

    // Casos simulados para pruebas de frontera
    if (cleanEmail.startsWith('sin_consentimiento') || cleanEmail.startsWith('revocado')) {
      throw new BookingException(
        'CONSENT_REQUIRED',
        'CONSENT_REQUIRED: Debes aceptar los términos de tratamiento de datos personales conforme a la Ley Nº 29733 (RN-02).',
        403
      );
    }

    if (payload.id_sesion === 999) {
      throw new BookingException(
        'SESSION_NOT_FOUND',
        'SESSION_NOT_FOUND: La clase de mentoría seleccionada no existe o fue retirada.',
        404
      );
    }

    if (payload.id_sesion === 998) {
      throw new BookingException(
        'CAPACITY_EXCEEDED',
        'CAPACITY_EXCEEDED: Aforo completo. No quedan vacantes disponibles en esta sesión.',
        409
      );
    }

    if (payload.id_sesion === 997) {
      throw new BookingException(
        'WINDOW_CLOSED_T24H',
        'WINDOW_CLOSED_T24H: Las reservas cierran 24 horas antes del inicio de la sesión.',
        400
      );
    }

    // Verificar duplicidad
    const exists = this.bookings.some(
      (b) => b.id_sesion === payload.id_sesion && b.estudiante_email === cleanEmail
    );
    if (exists) {
      throw new BookingException(
        'DUPLICATE_BOOKING',
        'DUPLICATE_BOOKING: Ya cuentas con una reserva registrada para esta clase.',
        400
      );
    }

    const id = this.nextBookingId++;
    const now = new Date();
    const cutoff = new Date(now.getTime() + 48 * 3600 * 1000).toISOString();

    const newBooking: BookingResponse = {
      id_reserva: id,
      codigo_reserva: `RES-2026-${String(id).padStart(4, '0')}`,
      id_sesion: payload.id_sesion,
      estudiante_email: cleanEmail,
      estado: 'PENDIENTE_CONFIRMACION',
      fecha_reserva: now.toISOString(),
      fecha_limite_confirmacion: cutoff,
      mensaje:
        'Reserva provisional registrada. Recuerde ratificar su asistencia antes de T-24h conforme a la regla institucional RN-08.',
      ticket_hash: `mock-ticket-hash-${id}`,
    };

    this.bookings.push(newBooking);
    return newBooking;
  }

  public async getMyReservations(
    estado?: string,
    studentEmail?: string
  ): Promise<BookingDetailResponse[]> {
    let filtered = [...this.bookings];
    if (studentEmail) {
      const clean = studentEmail.trim().toLowerCase();
      filtered = filtered.filter((b) => b.estudiante_email === clean);
    }
    if (estado) {
      filtered = filtered.filter((b) => b.estado === estado);
    }

    return filtered.map((b) => ({
      id_reserva: b.id_reserva,
      codigo_reserva: b.codigo_reserva,
      id_sesion: b.id_sesion,
      codigo_sesion: `SES-${String(b.id_sesion).padStart(4, '0')}`,
      estudiante_email: b.estudiante_email,
      estado: b.estado,
      fecha_reserva: b.fecha_reserva,
      fecha_ratificacion: null,
      ticket_hash: b.ticket_hash,
      nombre_asignatura: 'Asignatura Institucional',
      nombre_tema: 'Tema Silábico',
      duracion_minutos: 90,
      modalidad: 'presencial',
      espacio_asignado: 'Laboratorio L-01',
    }));
  }
}

// ============================================================================
// Fachada Principal del Servicio de Reservas
// ============================================================================

/**
 * Determina el modo inicial del servicio garantizando seguridad en producción.
 * En producción (import.meta.env.PROD), NUNCA se permite operar en modo mock.
 */
function resolveInitialServiceMode(): 'mock' | 'api' {
  if (import.meta.env.PROD) {
    return 'api';
  }
  const envMode = import.meta.env.VITE_SERVICE_MODE;
  if (envMode === 'mock') {
    return 'mock';
  }
  if (envMode === 'api') {
    return 'api';
  }
  if (import.meta.env.MODE === 'test') {
    return 'mock';
  }
  return 'api';
}

const apiAdapterInstance = new ApiBookingAdapter();
const mockAdapterInstance = new MockBookingAdapter();
let currentServiceMode: 'mock' | 'api' = resolveInitialServiceMode();

export const bookingService = {
  setMode(mode: 'mock' | 'api'): void {
    if (import.meta.env.PROD && mode === 'mock') {
      console.error(
        'Violación de seguridad: El modo mock está estrictamente prohibido en compilaciones de producción.'
      );
      currentServiceMode = 'api';
      return;
    }
    currentServiceMode = mode;
  },

  getMode(): 'mock' | 'api' {
    return currentServiceMode;
  },

  setBaseUrl(url: string): void {
    apiAdapterInstance.setBaseUrl(url);
  },

  getBaseUrl(): string {
    return apiAdapterInstance.getBaseUrl();
  },

  getApiAdapter(): ApiBookingAdapter {
    return apiAdapterInstance;
  },

  getMockAdapter(): MockBookingAdapter {
    return mockAdapterInstance;
  },

  /**
   * Formaliza una reserva provisional con control transaccional de aforo (CUS04 / RF12).
   */
  async reserveSeat(payload: BookingCreatePayload): Promise<BookingResponse> {
    if (currentServiceMode === 'mock') {
      return mockAdapterInstance.reserveSeat(payload);
    }
    return apiAdapterInstance.reserveSeat(payload);
  },

  /**
   * Consulta las reservas del estudiante mentoreado autenticado.
   */
  async getMyReservations(
    estado?: string,
    studentEmail?: string
  ): Promise<BookingDetailResponse[]> {
    if (currentServiceMode === 'mock') {
      return mockAdapterInstance.getMyReservations(estado, studentEmail);
    }
    return apiAdapterInstance.getMyReservations(estado, studentEmail);
  },
};
