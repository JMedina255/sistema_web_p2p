/**
 * Servicio de Reservas Transaccionales de Cupos de Mentoría (T-23 / Sprint 05 Fase 1).
 * Módulo MOD-05: Quórum, Confirmación y Cancelaciones.
 * Trazabilidad: CUS04, CUS17, CUS24, RF12, RF13, RF14, RN-05, RN-08, RN-09, RN-10, RNF07.
 */

import { getApiBaseUrl } from './apiClient';
import { authService } from './authService';

/**
 * Estados canónicos del ciclo de vida de una reserva de mentoría (CUS04 / MOD-05 / SAD).
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
 * Payload opcional para registrar el desistimiento voluntario de una reserva (RF14 / CUS17 / RN-10).
 */
export interface BookingCancelPayload {
  /** Motivo justificado o descripción del desistimiento voluntario */
  motivo?: string;
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
 * Detalle ampliado de una reserva de cupo con metadatos de la sesión (CUS04 / RF12 / RF13 / RF14).
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
  asistio?: boolean | null;
  asistencia_confirmada?: boolean | null;
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
  | 'UNKNOWN_ERROR'
  | 'RESERVATION_NOT_FOUND'
  | 'INVALID_STATUS_TRANSITION'
  | 'ALREADY_CANCELLED'
  | 'ENDPOINT_NOT_IMPLEMENTED'
  | 'OPERATION_NOT_AVAILABLE';

/**
 * Excepción especializada para fallos de reserva de cupos (T-23 / RF12 / RF13 / RF14).
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

/**
 * Resuelve de forma segura el correo institucional del estudiante a partir del token JWT activo.
 * Previene la suplantación o manipulación de reservas ajenas (Auditoría B.2 / RN-01).
 */
function getAuthenticatedStudentEmail(): string | null {
  const token = authService.getToken();
  if (!token) return null;
  try {
    const parts = token.split('.');
    if (parts.length === 3) {
      const payloadJson = atob(parts[1].replace(/-/g, '+').replace(/_/g, '/'));
      const payload = JSON.parse(payloadJson);
      if (typeof payload.sub === 'string' && payload.sub.includes('@')) {
        return payload.sub.trim().toLowerCase();
      }
      if (typeof payload.email === 'string') {
        return payload.email.trim().toLowerCase();
      }
    }
  } catch {
    // Si el token no es decodificable en el entorno
  }
  return null;
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
   * Ratifica la asistencia a una reserva de cupo (RF13 / CUS24 / RN-08).
   * Contrato previsto: POST /api/v1/bookings/{id_reserva}/confirm (T-26).
   */
  public async confirmAttendance(id_reserva: number): Promise<BookingDetailResponse> {
    if (!id_reserva || !Number.isInteger(id_reserva) || id_reserva < 1) {
      throw new BookingException(
        'VALIDATION_ERROR',
        'El identificador de reserva debe ser un número entero positivo válido.',
        400
      );
    }

    const token = authService.getToken();
    if (!token) {
      throw new BookingException(
        'UNAUTHORIZED',
        'Se requiere autenticación institucional válida para ratificar la asistencia.',
        401
      );
    }

    const url = `${this.baseUrl}/api/v1/bookings/${id_reserva}/confirm`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': `Bearer ${token}`,
    };

    let response: Response;
    try {
      response = await fetch(url, {
        method: 'POST',
        headers,
      });
    } catch (err: unknown) {
      throw new BookingException(
        'NETWORK_ERROR',
        'No fue posible comunicar con el servidor para ratificar la reserva.',
        undefined,
        err
      );
    }

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      // Detección explícita de endpoint pendiente de backend (T-26 por Renzo)
      if (
        response.status === 501 ||
        (response.status === 404 &&
          (!data?.detail ||
            data.detail === 'Not Found' ||
            (typeof data.detail === 'string' && !data.detail.includes('RESERVATION_NOT_FOUND'))))
      ) {
        throw new BookingException(
          'ENDPOINT_NOT_IMPLEMENTED',
          'El endpoint de ratificación de asistencia (T-26: POST /api/v1/bookings/{id_reserva}/confirm) se encuentra actualmente en desarrollo en el backend por Renzo.',
          response.status,
          data
        );
      }
      this.handleHttpError(response.status, data);
    }

    return data as BookingDetailResponse;
  }

  /**
   * Desiste voluntariamente de una reserva de cupo (RF14 / CUS17 / RN-08 / RN-10).
   * Contrato previsto: POST /api/v1/bookings/{id_reserva}/cancel (T-28).
   */
  public async cancelReservation(
    id_reserva: number,
    motivo?: string
  ): Promise<BookingDetailResponse> {
    if (!id_reserva || !Number.isInteger(id_reserva) || id_reserva < 1) {
      throw new BookingException(
        'VALIDATION_ERROR',
        'El identificador de reserva debe ser un número entero positivo válido.',
        400
      );
    }

    const token = authService.getToken();
    if (!token) {
      throw new BookingException(
        'UNAUTHORIZED',
        'Se requiere autenticación institucional válida para desistir de la reserva.',
        401
      );
    }

    const url = `${this.baseUrl}/api/v1/bookings/${id_reserva}/cancel`;
    const headers: Record<string, string> = {
      'Content-Type': 'application/json',
      'Accept': 'application/json',
      'Authorization': `Bearer ${token}`,
    };

    let response: Response;
    try {
      response = await fetch(url, {
        method: 'POST',
        headers,
        body: JSON.stringify({
          motivo: motivo?.trim() || 'Desistimiento voluntario del estudiante',
        }),
      });
    } catch (err: unknown) {
      throw new BookingException(
        'NETWORK_ERROR',
        'No fue posible comunicar con el servidor para desistir de la reserva.',
        undefined,
        err
      );
    }

    const data = await response.json().catch(() => null);

    if (!response.ok) {
      // Detección explícita de endpoint pendiente de backend (T-28 por Renzo)
      if (
        response.status === 501 ||
        (response.status === 404 &&
          (!data?.detail ||
            data.detail === 'Not Found' ||
            (typeof data.detail === 'string' && !data.detail.includes('RESERVATION_NOT_FOUND'))))
      ) {
        throw new BookingException(
          'ENDPOINT_NOT_IMPLEMENTED',
          'El endpoint de desistimiento voluntario (T-28: POST /api/v1/bookings/{id_reserva}/cancel) se encuentra actualmente en desarrollo en el backend por Renzo.',
          response.status,
          data
        );
      }
      this.handleHttpError(response.status, data);
    }

    return data as BookingDetailResponse;
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
      } else if (detail.includes('RESERVATION_NOT_FOUND')) {
        code = 'RESERVATION_NOT_FOUND';
      } else if (detail.includes('SESSION_NOT_FOUND')) {
        code = 'SESSION_NOT_FOUND';
      } else if (detail.includes('SESSION_NOT_OPEN')) {
        code = 'SESSION_NOT_OPEN';
      } else if (detail.includes('INVALID_STATUS_TRANSITION')) {
        code = 'INVALID_STATUS_TRANSITION';
      } else if (detail.includes('ALREADY_CANCELLED')) {
        code = 'ALREADY_CANCELLED';
      } else if (detail.includes('ENDPOINT_NOT_IMPLEMENTED')) {
        code = 'ENDPOINT_NOT_IMPLEMENTED';
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
          code = 'RESERVATION_NOT_FOUND';
          message = message || 'La reserva seleccionada no existe o fue retirada.';
          break;
        case 409:
          code = 'CAPACITY_EXCEEDED';
          message = 'Aforo completo o colisión con otra reserva concurrente.';
          break;
        case 501:
          code = 'ENDPOINT_NOT_IMPLEMENTED';
          message = 'Operación aún no disponible en el servidor.';
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
  private bookings: BookingDetailResponse[] = [];
  private nextBookingId = 501;
  private simulatedTime: number | null = null;

  constructor() {
    this.resetToDefaults();
  }

  public resetToDefaults(): void {
    this.bookings = [];
    this.nextBookingId = 501;
    this.simulatedTime = null;
  }

  /**
   * Permite fijar un timestamp simulado para evaluar con precisión las ventanas RN-08 (corte T-24h).
   */
  public setCurrentTime(timestamp: number | null): void {
    this.simulatedTime = timestamp;
  }

  /**
   * Retorna el timestamp simulado actual o Date.now() por defecto.
   */
  public getCurrentTime(): number {
    return this.simulatedTime ?? Date.now();
  }

  /**
   * Semilla una reserva preconfigurada para pruebas de casos de uso y estados específicos.
   */
  public seedBooking(booking: BookingDetailResponse): void {
    const idx = this.bookings.findIndex((b) => b.id_reserva === booking.id_reserva);
    if (idx >= 0) {
      this.bookings[idx] = { ...booking };
    } else {
      this.bookings.push({ ...booking });
    }
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

    // Verificar duplicidad (excluyendo canceladas)
    const exists = this.bookings.some(
      (b) =>
        b.id_sesion === payload.id_sesion &&
        b.estudiante_email === cleanEmail &&
        b.estado !== 'CANCELADA_USUARIO' &&
        b.estado !== 'CANCELADA_SISTEMA'
    );
    if (exists) {
      throw new BookingException(
        'DUPLICATE_BOOKING',
        'DUPLICATE_BOOKING: Ya cuentas con una reserva registrada para esta clase.',
        400
      );
    }

    const id = this.nextBookingId++;
    const now = new Date(this.getCurrentTime());
    // Sesión proyectada para 72 horas después de la reserva por defecto
    const sessionDate = new Date(now.getTime() + 72 * 3600 * 1000);
    const cutoff = new Date(sessionDate.getTime() - 24 * 3600 * 1000).toISOString();

    const detail: BookingDetailResponse = {
      id_reserva: id,
      codigo_reserva: `RES-2026-${String(id).padStart(4, '0')}`,
      id_sesion: payload.id_sesion,
      codigo_sesion: `SES-${String(payload.id_sesion).padStart(4, '0')}`,
      estudiante_email: cleanEmail,
      estado: 'PENDIENTE_CONFIRMACION',
      fecha_reserva: now.toISOString(),
      fecha_ratificacion: null,
      motivo_cancelacion: null,
      ticket_hash: `mock-ticket-hash-${id}`,
      nombre_asignatura: 'Asignatura Institucional',
      nombre_tema: 'Tema Silábico',
      fecha_inicio: sessionDate.toISOString(),
      duracion_minutos: 90,
      modalidad: 'presencial',
      espacio_asignado: 'Laboratorio L-01',
      mentor_email: 'renzo.mentor@upt.pe',
    };

    this.bookings.push(detail);

    return {
      id_reserva: id,
      codigo_reserva: detail.codigo_reserva,
      id_sesion: detail.id_sesion,
      estudiante_email: cleanEmail,
      estado: 'PENDIENTE_CONFIRMACION',
      fecha_reserva: detail.fecha_reserva,
      fecha_limite_confirmacion: cutoff,
      mensaje:
        'Reserva provisional registrada. Recuerde ratificar su asistencia antes de T-24h conforme a la regla institucional RN-08.',
      ticket_hash: detail.ticket_hash,
    };
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

    return filtered.map((b) => ({ ...b }));
  }

  /**
   * Ratifica la asistencia de una reserva en memoria (RF13 / CUS24 / RN-08).
   */
  public async confirmAttendance(
    id_reserva: number,
    callerEmail?: string
  ): Promise<BookingDetailResponse> {
    if (!id_reserva || !Number.isInteger(id_reserva) || id_reserva < 1) {
      throw new BookingException(
        'VALIDATION_ERROR',
        'El identificador de reserva debe ser un número entero positivo válido.',
        400
      );
    }

    const booking = this.bookings.find((b) => b.id_reserva === id_reserva);
    if (!booking) {
      throw new BookingException(
        'RESERVATION_NOT_FOUND',
        `RESERVATION_NOT_FOUND: No se encontró la reserva con ID ${id_reserva}.`,
        404
      );
    }

    // Prevención de operaciones sobre reservas ajenas (RN-01 / Seguridad B.2)
    const effectiveEmail = callerEmail || getAuthenticatedStudentEmail();
    if (
      effectiveEmail &&
      effectiveEmail.trim().toLowerCase() !== booking.estudiante_email.trim().toLowerCase()
    ) {
      throw new BookingException(
        'FORBIDDEN',
        'FORBIDDEN: No tiene permisos para ratificar una reserva que no le pertenece.',
        403
      );
    }

    // Transiciones de estado permitidas (solo desde PENDIENTE_CONFIRMACION)
    if (booking.estado === 'CONFIRMADA') {
      throw new BookingException(
        'INVALID_STATUS_TRANSITION',
        'INVALID_STATUS_TRANSITION: La reserva ya se encuentra ratificada y confirmada.',
        400
      );
    }

    if (
      booking.estado === 'CANCELADA_USUARIO' ||
      booking.estado === 'CANCELADA_SISTEMA' ||
      booking.estado === 'NO_CONFIRMADA'
    ) {
      throw new BookingException(
        'INVALID_STATUS_TRANSITION',
        `INVALID_STATUS_TRANSITION: No se puede ratificar una reserva en estado ${booking.estado}.`,
        400
      );
    }

    if (booking.estado !== 'PENDIENTE_CONFIRMACION') {
      throw new BookingException(
        'INVALID_STATUS_TRANSITION',
        `INVALID_STATUS_TRANSITION: Transición no permitida desde el estado ${booking.estado}.`,
        400
      );
    }

    // Verificación de la ventana temporal RN-08 (corte T-24h)
    const now = this.getCurrentTime();
    if (booking.fecha_inicio) {
      const startTime = new Date(booking.fecha_inicio).getTime();
      const diffMs = startTime - now;
      if (diffMs <= 24 * 3600 * 1000) {
        throw new BookingException(
          'WINDOW_CLOSED_T24H',
          'WINDOW_CLOSED_T24H: La ratificación de asistencia debe realizarse como mínimo 24 horas antes del inicio de la sesión (RN-08).',
          400
        );
      }
    }

    // Aplicar ratificación
    booking.estado = 'CONFIRMADA';
    booking.fecha_ratificacion = new Date(now).toISOString();

    return { ...booking };
  }

  /**
   * Desiste voluntariamente de una reserva en memoria (RF14 / CUS17 / RN-08 / RN-10).
   */
  public async cancelReservation(
    id_reserva: number,
    motivo?: string,
    callerEmail?: string
  ): Promise<BookingDetailResponse> {
    if (!id_reserva || !Number.isInteger(id_reserva) || id_reserva < 1) {
      throw new BookingException(
        'VALIDATION_ERROR',
        'El identificador de reserva debe ser un número entero positivo válido.',
        400
      );
    }

    const booking = this.bookings.find((b) => b.id_reserva === id_reserva);
    if (!booking) {
      throw new BookingException(
        'RESERVATION_NOT_FOUND',
        `RESERVATION_NOT_FOUND: No se encontró la reserva con ID ${id_reserva}.`,
        404
      );
    }

    // Prevención de operaciones sobre reservas ajenas (RN-01 / Seguridad B.2)
    const effectiveEmail = callerEmail || getAuthenticatedStudentEmail();
    if (
      effectiveEmail &&
      effectiveEmail.trim().toLowerCase() !== booking.estudiante_email.trim().toLowerCase()
    ) {
      throw new BookingException(
        'FORBIDDEN',
        'FORBIDDEN: No tiene permisos para desistir de una reserva que no le pertenece.',
        403
      );
    }

    // Doble desistimiento o estado cancelado previo
    if (
      booking.estado === 'CANCELADA_USUARIO' ||
      booking.estado === 'CANCELADA_SISTEMA'
    ) {
      throw new BookingException(
        'ALREADY_CANCELLED',
        'ALREADY_CANCELLED: La reserva ya se encuentra cancelada.',
        400
      );
    }

    // Estados no cancelables por ser terminales, ejecutados o expirados (solo PENDIENTE_CONFIRMACION o CONFIRMADA)
    if (
      booking.estado !== 'PENDIENTE_CONFIRMACION' &&
      booking.estado !== 'CONFIRMADA'
    ) {
      throw new BookingException(
        'INVALID_STATUS_TRANSITION',
        `INVALID_STATUS_TRANSITION: No se puede desistir de una reserva en estado ${booking.estado}.`,
        400
      );
    }

    // Verificación de la ventana temporal RN-08 / RN-10 (corte T-24h para desistimiento)
    const now = this.getCurrentTime();
    if (booking.fecha_inicio) {
      const startTime = new Date(booking.fecha_inicio).getTime();
      const diffMs = startTime - now;
      if (diffMs <= 24 * 3600 * 1000) {
        throw new BookingException(
          'WINDOW_CLOSED_T24H',
          'WINDOW_CLOSED_T24H: El desistimiento voluntario debe realizarse con más de 24 horas de anticipación al inicio de la sesión (RN-08 / RN-10).',
          400
        );
      }
    }

    // Aplicar desistimiento
    booking.estado = 'CANCELADA_USUARIO';
    booking.motivo_cancelacion = motivo?.trim() || 'Desistimiento voluntario del estudiante';

    return { ...booking };
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
   * Fija un reloj simulado en el adaptador mock para pruebas deterministas temporales.
   */
  setCurrentTime(timestamp: number | null): void {
    mockAdapterInstance.setCurrentTime(timestamp);
  },

  /**
   * Semilla una reserva en el adaptador mock para pruebas de integración o unitarias.
   */
  seedBooking(booking: BookingDetailResponse): void {
    mockAdapterInstance.seedBooking(booking);
  },

  /**
   * Restablece el estado del adaptador mock a sus valores limpios iniciales.
   */
  resetToDefaults(): void {
    mockAdapterInstance.resetToDefaults();
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

  /**
   * Ratifica la asistencia de una reserva provisional (RF13 / CUS24 / RN-08).
   */
  async confirmAttendance(
    id_reserva: number,
    studentEmail?: string
  ): Promise<BookingDetailResponse> {
    if (currentServiceMode === 'mock') {
      return mockAdapterInstance.confirmAttendance(id_reserva, studentEmail);
    }
    return apiAdapterInstance.confirmAttendance(id_reserva);
  },

  /**
   * Desiste voluntariamente de una reserva de cupo (RF14 / CUS17 / RN-08 / RN-10).
   */
  async cancelReservation(
    id_reserva: number,
    motivo?: string,
    studentEmail?: string
  ): Promise<BookingDetailResponse> {
    if (currentServiceMode === 'mock') {
      return mockAdapterInstance.cancelReservation(id_reserva, motivo, studentEmail);
    }
    return apiAdapterInstance.cancelReservation(id_reserva, motivo);
  },
};
