import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import {
  bookingService,
  ApiBookingAdapter,
  MockBookingAdapter,
  BookingException,
  type BookingCreatePayload,
  type BookingResponse,
  type BookingDetailResponse,
} from '../bookingService';
import { authService } from '../authService';

describe('bookingService (T-23 / Sprint 05 Fase 1 - RF12 / RF13 / RF14 / RN-08 / RN-10)', () => {
  const mockBaseUrl = 'http://127.0.0.1:8000';
  let apiAdapter: ApiBookingAdapter;
  let mockAdapter: MockBookingAdapter;

  beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.clear();
    bookingService.setMode('mock');
    bookingService.resetToDefaults();
    apiAdapter = new ApiBookingAdapter(mockBaseUrl);
    mockAdapter = new MockBookingAdapter();
  });

  afterEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  // ==========================================================================
  // 1. Validaciones preventivas de contrato en cliente
  // ==========================================================================
  describe('1. Validaciones preventivas de contrato en cliente (Escenarios 1 y 2)', () => {
    it('rechaza id_sesion no entero, menor a 1 o indefinido en reserveSeat', async () => {
      const invalidPayloads: BookingCreatePayload[] = [
        { id_sesion: 0, estudiante_email: '2022074255@upt.pe' },
        { id_sesion: -5, estudiante_email: '2022074255@upt.pe' },
        { id_sesion: 3.14, estudiante_email: '2022074255@upt.pe' },
        { id_sesion: NaN, estudiante_email: '2022074255@upt.pe' },
      ];

      for (const payload of invalidPayloads) {
        await expect(apiAdapter.reserveSeat(payload)).rejects.toThrow(BookingException);
        await expect(mockAdapter.reserveSeat(payload)).rejects.toThrow(BookingException);
      }
    });

    it('rechaza correos que no pertenezcan al dominio institucional @upt.pe (RN-01)', async () => {
      const payload: BookingCreatePayload = {
        id_sesion: 10,
        estudiante_email: 'estudiante@gmail.com',
      };

      await expect(apiAdapter.reserveSeat(payload)).rejects.toThrow(
        /dominio institucional.*@upt\.pe/i
      );
      await expect(mockAdapter.reserveSeat(payload)).rejects.toThrow(
        /dominio institucional.*@upt\.pe/i
      );
    });

    it('rechaza id_reserva no entero, menor a 1 o inválido en confirmAttendance (Escenario 2)', async () => {
      authService.saveToken('token-valido');
      const invalidIds = [0, -1, 3.14, NaN];

      for (const id of invalidIds) {
        await expect(apiAdapter.confirmAttendance(id)).rejects.toMatchObject({
          code: 'VALIDATION_ERROR',
          status: 400,
        });
        await expect(mockAdapter.confirmAttendance(id)).rejects.toMatchObject({
          code: 'VALIDATION_ERROR',
          status: 400,
        });
      }
    });

    it('rechaza id_reserva no entero, menor a 1 o inválido en cancelReservation (Escenario 2)', async () => {
      authService.saveToken('token-valido');
      const invalidIds = [0, -99, 4.5, NaN];

      for (const id of invalidIds) {
        await expect(apiAdapter.cancelReservation(id)).rejects.toMatchObject({
          code: 'VALIDATION_ERROR',
          status: 400,
        });
        await expect(mockAdapter.cancelReservation(id)).rejects.toMatchObject({
          code: 'VALIDATION_ERROR',
          status: 400,
        });
      }
    });
  });

  // ==========================================================================
  // 2. Adaptador de API REST Real (ApiBookingAdapter)
  // ==========================================================================
  describe('2. Adaptador de API REST Real (ApiBookingAdapter)', () => {
    it('construye la petición POST a /api/v1/bookings/reserve con Bearer token e interpreta HTTP 201', async () => {
      authService.saveToken('fake-jwt-token-12345');

      const mockResponse: BookingResponse = {
        id_reserva: 101,
        codigo_reserva: 'RES-2026-0101',
        id_sesion: 14,
        estudiante_email: '2022074255@upt.pe',
        estado: 'PENDIENTE_CONFIRMACION',
        fecha_reserva: '2026-11-05T10:00:00Z',
        fecha_limite_confirmacion: '2026-11-04T10:00:00Z',
        mensaje: 'Reserva provisional registrada. Recuerde ratificar su asistencia antes de T-24h.',
        ticket_hash: 'hash-abc-123',
      };

      const fetchMock = vi.fn().mockResolvedValue({
        ok: true,
        status: 201,
        json: async () => mockResponse,
      });
      globalThis.fetch = fetchMock;

      const result = await apiAdapter.reserveSeat({
        id_sesion: 14,
        estudiante_email: '2022074255@upt.pe',
      });

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [calledUrl, calledInit] = fetchMock.mock.calls[0];

      expect(calledUrl).toBe(`${mockBaseUrl}/api/v1/bookings/reserve`);
      expect(calledInit.method).toBe('POST');
      expect(calledInit.headers['Authorization']).toBe('Bearer fake-jwt-token-12345');
      expect(calledInit.headers['Content-Type']).toBe('application/json');
      expect(JSON.parse(calledInit.body)).toEqual({
        id_sesion: 14,
        estudiante_email: '2022074255@upt.pe',
      });

      expect(result.codigo_reserva).toBe('RES-2026-0101');
      expect(result.estado).toBe('PENDIENTE_CONFIRMACION');
    });

    it('no incluye cabecera Authorization si no existe token en sesión', async () => {
      authService.clearToken();

      const fetchMock = vi.fn().mockResolvedValue({
        ok: true,
        status: 201,
        json: async () => ({
          id_reserva: 102,
          codigo_reserva: 'RES-2026-0102',
          id_sesion: 15,
          estudiante_email: '2022074255@upt.pe',
          estado: 'PENDIENTE_CONFIRMACION',
          fecha_reserva: '2026-11-05T10:00:00Z',
          mensaje: 'Reserva registrada.',
        }),
      });
      globalThis.fetch = fetchMock;

      await apiAdapter.reserveSeat({
        id_sesion: 15,
        estudiante_email: '2022074255@upt.pe',
      });

      const [, calledInit] = fetchMock.mock.calls[0];
      expect(calledInit.headers['Authorization']).toBeUndefined();
    });

    it('exige autenticación en cliente para confirmAttendance (401 UNAUTHORIZED si no hay token)', async () => {
      authService.clearToken();

      await expect(apiAdapter.confirmAttendance(101)).rejects.toMatchObject({
        code: 'UNAUTHORIZED',
        status: 401,
      });
    });

    it('exige autenticación en cliente para cancelReservation (401 UNAUTHORIZED si no hay token)', async () => {
      authService.clearToken();

      await expect(apiAdapter.cancelReservation(101, 'Motivo de prueba')).rejects.toMatchObject({
        code: 'UNAUTHORIZED',
        status: 401,
      });
    });

    it('construye la petición POST a /api/v1/bookings/{id}/confirm con Bearer token', async () => {
      authService.saveToken('jwt-token-ratify');

      const mockConfirmed: BookingDetailResponse = {
        id_reserva: 205,
        codigo_reserva: 'RES-2026-0205',
        id_sesion: 12,
        estudiante_email: '2022074255@upt.pe',
        estado: 'CONFIRMADA',
        fecha_reserva: '2026-11-01T10:00:00Z',
        fecha_ratificacion: '2026-11-02T10:00:00Z',
      };

      const fetchMock = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => mockConfirmed,
      });
      globalThis.fetch = fetchMock;

      const result = await apiAdapter.confirmAttendance(205);

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [calledUrl, calledInit] = fetchMock.mock.calls[0];
      expect(calledUrl).toBe(`${mockBaseUrl}/api/v1/bookings/205/confirm`);
      expect(calledInit.method).toBe('POST');
      expect(calledInit.headers['Authorization']).toBe('Bearer jwt-token-ratify');
      expect(result.estado).toBe('CONFIRMADA');
      expect(result.fecha_ratificacion).toBeDefined();
    });

    it('construye la petición POST a /api/v1/bookings/{id}/cancel con Bearer token y payload motivo', async () => {
      authService.saveToken('jwt-token-cancel');

      const mockCancelled: BookingDetailResponse = {
        id_reserva: 206,
        codigo_reserva: 'RES-2026-0206',
        id_sesion: 12,
        estudiante_email: '2022074255@upt.pe',
        estado: 'CANCELADA_USUARIO',
        fecha_reserva: '2026-11-01T10:00:00Z',
        motivo_cancelacion: 'Cruce con evaluación formativa',
      };

      const fetchMock = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => mockCancelled,
      });
      globalThis.fetch = fetchMock;

      const result = await apiAdapter.cancelReservation(206, 'Cruce con evaluación formativa');

      expect(fetchMock).toHaveBeenCalledTimes(1);
      const [calledUrl, calledInit] = fetchMock.mock.calls[0];
      expect(calledUrl).toBe(`${mockBaseUrl}/api/v1/bookings/206/cancel`);
      expect(calledInit.method).toBe('POST');
      expect(calledInit.headers['Authorization']).toBe('Bearer jwt-token-cancel');
      expect(JSON.parse(calledInit.body)).toEqual({
        motivo: 'Cruce con evaluación formativa',
      });
      expect(result.estado).toBe('CANCELADA_USUARIO');
    });

    it('eleva ENDPOINT_NOT_IMPLEMENTED ante 404 Not Found o 501 en confirmAttendance (Escenario 12)', async () => {
      authService.saveToken('jwt-token-test');

      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 404,
        json: async () => ({ detail: 'Not Found' }),
      });

      await expect(apiAdapter.confirmAttendance(301)).rejects.toMatchObject({
        code: 'ENDPOINT_NOT_IMPLEMENTED',
      });
    });

    it('eleva ENDPOINT_NOT_IMPLEMENTED ante 404 Not Found o 501 en cancelReservation (Escenario 12)', async () => {
      authService.saveToken('jwt-token-test');

      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 501,
        json: async () => ({ detail: 'Not Implemented' }),
      });

      await expect(apiAdapter.cancelReservation(301, 'Motivo')).rejects.toMatchObject({
        code: 'ENDPOINT_NOT_IMPLEMENTED',
      });
    });

    it('no inventa comprobantes exitosos ni conmuta a mock cuando la API real falla (Escenario 15)', async () => {
      authService.saveToken('jwt-token-test');

      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 500,
        json: async () => ({ detail: 'Internal Server Error' }),
      });

      await expect(apiAdapter.confirmAttendance(301)).rejects.toThrow(BookingException);
      await expect(apiAdapter.cancelReservation(301, 'Motivo')).rejects.toThrow(BookingException);
    });

    it('interpreta error 400 WINDOW_CLOSED_T24H correctamente', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 400,
        json: async () => ({
          detail: 'WINDOW_CLOSED_T24H: Las reservas cierran 24 horas antes del inicio de la sesión.',
        }),
      });

      await expect(
        apiAdapter.reserveSeat({ id_sesion: 10, estudiante_email: '2022074255@upt.pe' })
      ).rejects.toMatchObject({
        code: 'WINDOW_CLOSED_T24H',
        status: 400,
      });
    });

    it('interpreta error 400 MENTOR_CANNOT_BOOK correctamente', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 400,
        json: async () => ({
          detail: 'MENTOR_CANNOT_BOOK: Como mentor titular no puedes reservar una vacante en tu clase.',
        }),
      });

      await expect(
        apiAdapter.reserveSeat({ id_sesion: 10, estudiante_email: 'renzo.mentor@upt.pe' })
      ).rejects.toMatchObject({
        code: 'MENTOR_CANNOT_BOOK',
        status: 400,
      });
    });

    it('interpreta error 400 DUPLICATE_BOOKING correctamente', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 400,
        json: async () => ({
          detail: 'DUPLICATE_BOOKING: Ya cuentas con una reserva registrada para esta clase.',
        }),
      });

      await expect(
        apiAdapter.reserveSeat({ id_sesion: 10, estudiante_email: '2022074255@upt.pe' })
      ).rejects.toMatchObject({
        code: 'DUPLICATE_BOOKING',
        status: 400,
      });
    });

    it('interpreta error 403 CONSENT_REQUIRED correctamente', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 403,
        json: async () => ({
          detail:
            'CONSENT_REQUIRED: Debes aceptar los términos de tratamiento de datos personales conforme a la Ley Nº 29733 (RN-02).',
        }),
      });

      await expect(
        apiAdapter.reserveSeat({ id_sesion: 10, estudiante_email: 'sin_consentimiento@upt.pe' })
      ).rejects.toMatchObject({
        code: 'CONSENT_REQUIRED',
        status: 403,
      });
    });

    it('interpreta error 409 CAPACITY_EXCEEDED (aforo agotado por concurrencia RNF07)', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 409,
        json: async () => ({
          detail: 'CAPACITY_EXCEEDED: Aforo completo. No quedan vacantes disponibles en esta sesión.',
        }),
      });

      await expect(
        apiAdapter.reserveSeat({ id_sesion: 10, estudiante_email: '2022074255@upt.pe' })
      ).rejects.toMatchObject({
        code: 'CAPACITY_EXCEEDED',
        status: 409,
      });
    });

    it('interpreta error 503 DATABASE_BUSY y no ejecuta reintentos ciegos (Escenario 11)', async () => {
      const fetchMock = vi.fn().mockResolvedValue({
        ok: false,
        status: 503,
        json: async () => ({
          detail:
            'DATABASE_BUSY: El servicio de reservas se encuentra temporalmente sobrecargado. Por favor, reintente en unos momentos.',
        }),
      });
      globalThis.fetch = fetchMock;

      await expect(
        apiAdapter.reserveSeat({ id_sesion: 10, estudiante_email: '2022074255@upt.pe' })
      ).rejects.toMatchObject({
        code: 'DATABASE_BUSY',
        status: 503,
      });

      // Exactamente 1 llamada efectuada: sin retry automático destructivo
      expect(fetchMock).toHaveBeenCalledTimes(1);
    });

    it('captura fallos de red y genera NETWORK_ERROR (Escenario 10)', async () => {
      globalThis.fetch = vi.fn().mockRejectedValue(new TypeError('Failed to fetch'));

      await expect(
        apiAdapter.reserveSeat({ id_sesion: 10, estudiante_email: '2022074255@upt.pe' })
      ).rejects.toMatchObject({
        code: 'NETWORK_ERROR',
      });

      authService.saveToken('jwt-valido');
      await expect(apiAdapter.confirmAttendance(10)).rejects.toMatchObject({
        code: 'NETWORK_ERROR',
      });
      await expect(apiAdapter.cancelReservation(10, 'Motivo')).rejects.toMatchObject({
        code: 'NETWORK_ERROR',
      });
    });

    it('interpreta errores con objeto detail estructurado { code, message }', async () => {
      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: false,
        status: 400,
        json: async () => ({
          detail: {
            code: 'SESSION_NOT_OPEN',
            message: 'La sesión no se encuentra en estado PUBLICADA.',
          },
        }),
      });

      await expect(
        apiAdapter.reserveSeat({ id_sesion: 10, estudiante_email: '2022074255@upt.pe' })
      ).rejects.toMatchObject({
        code: 'SESSION_NOT_OPEN',
        status: 400,
      });
    });

    it('consulta mis reservas con getMyReservations (Escenario 1)', async () => {
      const mockList: BookingDetailResponse[] = [
        {
          id_reserva: 1,
          codigo_reserva: 'RES-001',
          id_sesion: 10,
          estudiante_email: '2022074255@upt.pe',
          estado: 'PENDIENTE_CONFIRMACION',
          fecha_reserva: '2026-11-01T10:00:00Z',
        },
      ];

      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => mockList,
      });

      const res = await apiAdapter.getMyReservations('PENDIENTE_CONFIRMACION', '2022074255@upt.pe');
      expect(res.length).toBe(1);
      expect(res[0].codigo_reserva).toBe('RES-001');
    });
  });

  // ==========================================================================
  // 3. Adaptador MOCK en Memoria (MockBookingAdapter)
  // ==========================================================================
  describe('3. Adaptador MOCK en Memoria (MockBookingAdapter)', () => {
    it('crea exitosamente una reserva provisional con código incremental', async () => {
      const b1 = await mockAdapter.reserveSeat({
        id_sesion: 101,
        estudiante_email: '2022074255@upt.pe',
      });

      expect(b1.id_reserva).toBe(501);
      expect(b1.codigo_reserva).toBe('RES-2026-0501');
      expect(b1.estado).toBe('PENDIENTE_CONFIRMACION');
      expect(b1.fecha_limite_confirmacion).toBeDefined();

      const b2 = await mockAdapter.reserveSeat({
        id_sesion: 102,
        estudiante_email: '2022074255@upt.pe',
      });
      expect(b2.id_reserva).toBe(502);
    });

    it('bloquea reservas duplicadas para la misma sesión y estudiante', async () => {
      await mockAdapter.reserveSeat({
        id_sesion: 101,
        estudiante_email: '2022074255@upt.pe',
      });

      await expect(
        mockAdapter.reserveSeat({
          id_sesion: 101,
          estudiante_email: '2022074255@upt.pe',
        })
      ).rejects.toMatchObject({
        code: 'DUPLICATE_BOOKING',
      });
    });

    it('simula casos de frontera por identificador o correo especial', async () => {
      // Falta de consentimiento
      await expect(
        mockAdapter.reserveSeat({
          id_sesion: 101,
          estudiante_email: 'sin_consentimiento@upt.pe',
        })
      ).rejects.toMatchObject({ code: 'CONSENT_REQUIRED' });

      // Sesión no encontrada
      await expect(
        mockAdapter.reserveSeat({
          id_sesion: 999,
          estudiante_email: '2022074255@upt.pe',
        })
      ).rejects.toMatchObject({ code: 'SESSION_NOT_FOUND' });

      // Aforo agotado
      await expect(
        mockAdapter.reserveSeat({
          id_sesion: 998,
          estudiante_email: '2022074255@upt.pe',
        })
      ).rejects.toMatchObject({ code: 'CAPACITY_EXCEEDED' });

      // Ventana T-24h cerrada
      await expect(
        mockAdapter.reserveSeat({
          id_sesion: 997,
          estudiante_email: '2022074255@upt.pe',
        })
      ).rejects.toMatchObject({ code: 'WINDOW_CLOSED_T24H' });
    });

    it('permite consultar las reservas simuladas registradas (Escenario 1)', async () => {
      await mockAdapter.reserveSeat({
        id_sesion: 101,
        estudiante_email: '2022074255@upt.pe',
      });

      const list = await mockAdapter.getMyReservations(undefined, '2022074255@upt.pe');
      expect(list.length).toBe(1);
      expect(list[0].id_sesion).toBe(101);
    });

    it('ratifica asistencia válidamente cambiando a CONFIRMADA con fecha_ratificacion (Escenario 3)', async () => {
      const booking = await mockAdapter.reserveSeat({
        id_sesion: 101,
        estudiante_email: '2022074255@upt.pe',
      });

      const confirmed = await mockAdapter.confirmAttendance(
        booking.id_reserva,
        '2022074255@upt.pe'
      );

      expect(confirmed.estado).toBe('CONFIRMADA');
      expect(confirmed.fecha_ratificacion).toBeDefined();
      expect(typeof confirmed.fecha_ratificacion).toBe('string');
      // Fecha en formato ISO 8601 UTC
      expect(new Date(confirmed.fecha_ratificacion!).toISOString()).toBe(
        confirmed.fecha_ratificacion
      );
    });

    it('rechaza ratificación después del corte T-24h con WINDOW_CLOSED_T24H (Escenario 4)', async () => {
      const now = new Date('2026-11-05T10:00:00Z').getTime();
      mockAdapter.setCurrentTime(now);

      // Sesión que inicia en 12 horas (< 24h, ventana cerrada)
      mockAdapter.seedBooking({
        id_reserva: 601,
        codigo_reserva: 'RES-2026-0601',
        id_sesion: 88,
        estudiante_email: '2022074255@upt.pe',
        estado: 'PENDIENTE_CONFIRMACION',
        fecha_reserva: '2026-11-01T10:00:00Z',
        fecha_inicio: new Date(now + 12 * 3600 * 1000).toISOString(),
      });

      await expect(
        mockAdapter.confirmAttendance(601, '2022074255@upt.pe')
      ).rejects.toMatchObject({
        code: 'WINDOW_CLOSED_T24H',
        status: 400,
      });
    });

    it('rechaza ratificación de reserva en estado incompatible (Escenario 5)', async () => {
      // Caso 5.1: Reserva ya confirmada
      mockAdapter.seedBooking({
        id_reserva: 602,
        codigo_reserva: 'RES-2026-0602',
        id_sesion: 89,
        estudiante_email: '2022074255@upt.pe',
        estado: 'CONFIRMADA',
        fecha_reserva: '2026-11-01T10:00:00Z',
        fecha_inicio: '2026-11-10T10:00:00Z',
      });

      await expect(
        mockAdapter.confirmAttendance(602, '2022074255@upt.pe')
      ).rejects.toMatchObject({
        code: 'INVALID_STATUS_TRANSITION',
        status: 400,
      });

      // Caso 5.2: Reserva cancelada por usuario
      mockAdapter.seedBooking({
        id_reserva: 603,
        codigo_reserva: 'RES-2026-0603',
        id_sesion: 90,
        estudiante_email: '2022074255@upt.pe',
        estado: 'CANCELADA_USUARIO',
        fecha_reserva: '2026-11-01T10:00:00Z',
        fecha_inicio: '2026-11-10T10:00:00Z',
      });

      await expect(
        mockAdapter.confirmAttendance(603, '2022074255@upt.pe')
      ).rejects.toMatchObject({
        code: 'INVALID_STATUS_TRANSITION',
        status: 400,
      });
    });

    it('desiste válidamente en modo mock pasando a CANCELADA_USUARIO y guardando motivo (Escenario 6)', async () => {
      const booking = await mockAdapter.reserveSeat({
        id_sesion: 101,
        estudiante_email: '2022074255@upt.pe',
      });

      const cancelled = await mockAdapter.cancelReservation(
        booking.id_reserva,
        'Cruce horario imprevisto con taller de titulación',
        '2022074255@upt.pe'
      );

      expect(cancelled.estado).toBe('CANCELADA_USUARIO');
      expect(cancelled.motivo_cancelacion).toBe(
        'Cruce horario imprevisto con taller de titulación'
      );
    });

    it('rechaza desistimiento fuera de plazo T-24h con WINDOW_CLOSED_T24H (Escenario 7)', async () => {
      const now = new Date('2026-11-05T10:00:00Z').getTime();
      mockAdapter.setCurrentTime(now);

      // Sesión en 8 horas (corte T-24h cerrado para desistimiento sin penalización RN-10)
      mockAdapter.seedBooking({
        id_reserva: 701,
        codigo_reserva: 'RES-2026-0701',
        id_sesion: 91,
        estudiante_email: '2022074255@upt.pe',
        estado: 'PENDIENTE_CONFIRMACION',
        fecha_reserva: '2026-11-01T10:00:00Z',
        fecha_inicio: new Date(now + 8 * 3600 * 1000).toISOString(),
      });

      await expect(
        mockAdapter.cancelReservation(701, 'Motivo tardío', '2022074255@upt.pe')
      ).rejects.toMatchObject({
        code: 'WINDOW_CLOSED_T24H',
        status: 400,
      });
    });

    it('rechaza doble desistimiento con ALREADY_CANCELLED (Escenario 8)', async () => {
      mockAdapter.seedBooking({
        id_reserva: 702,
        codigo_reserva: 'RES-2026-0702',
        id_sesion: 92,
        estudiante_email: '2022074255@upt.pe',
        estado: 'CANCELADA_USUARIO',
        fecha_reserva: '2026-11-01T10:00:00Z',
        fecha_inicio: '2026-11-20T10:00:00Z',
        motivo_cancelacion: 'Cancelación previa',
      });

      await expect(
        mockAdapter.cancelReservation(702, 'Segundo intento', '2022074255@upt.pe')
      ).rejects.toMatchObject({
        code: 'ALREADY_CANCELLED',
        status: 400,
      });
    });

    it('previene operaciones sobre reservas de otros estudiantes (FORBIDDEN) (Escenario 9)', async () => {
      mockAdapter.seedBooking({
        id_reserva: 703,
        codigo_reserva: 'RES-2026-0703',
        id_sesion: 93,
        estudiante_email: '2022074255@upt.pe',
        estado: 'PENDIENTE_CONFIRMACION',
        fecha_reserva: '2026-11-01T10:00:00Z',
        fecha_inicio: '2026-11-25T10:00:00Z',
      });

      // Intento de ratificar reserva ajena
      await expect(
        mockAdapter.confirmAttendance(703, 'otro.estudiante@upt.pe')
      ).rejects.toMatchObject({
        code: 'FORBIDDEN',
        status: 403,
      });

      // Intento de desistir de reserva ajena
      await expect(
        mockAdapter.cancelReservation(703, 'Intento ajeno', 'otro.estudiante@upt.pe')
      ).rejects.toMatchObject({
        code: 'FORBIDDEN',
        status: 403,
      });
    });

    it('controla con precisión el reloj simulado mediante setCurrentTime (Escenario 13)', async () => {
      const fixedTime = new Date('2026-11-01T08:00:00.000Z').getTime();
      mockAdapter.setCurrentTime(fixedTime);
      expect(mockAdapter.getCurrentTime()).toBe(fixedTime);

      const booking = await mockAdapter.reserveSeat({
        id_sesion: 101,
        estudiante_email: '2022074255@upt.pe',
      });
      expect(booking.fecha_reserva).toBe('2026-11-01T08:00:00.000Z');

      // Avanzar reloj simulado a 30 horas antes de la sesión (aún en ventana válida)
      // La sesión se agenda por defecto en fixedTime + 72h
      const advancedValid = fixedTime + 40 * 3600 * 1000;
      mockAdapter.setCurrentTime(advancedValid);

      const confirmed = await mockAdapter.confirmAttendance(
        booking.id_reserva,
        '2022074255@upt.pe'
      );
      expect(confirmed.estado).toBe('CONFIRMADA');

      // Restablecer reloj al valor real del sistema
      mockAdapter.setCurrentTime(null);
      expect(Math.abs(mockAdapter.getCurrentTime() - Date.now())).toBeLessThan(1000);
    });

    it('maneja estandarización de UTC e interoperabilidad con America/Lima (-05:00) (Escenario 14)', async () => {
      // Timestamp con zona horaria local peruana (America/Lima UTC-5)
      const limaTimeStr = '2026-11-10T14:00:00-05:00';
      const equivalentUtc = new Date(limaTimeStr).getTime();

      // Fijar el tiempo simulado a 48 horas antes de la sesión
      mockAdapter.setCurrentTime(equivalentUtc - 48 * 3600 * 1000);

      mockAdapter.seedBooking({
        id_reserva: 801,
        codigo_reserva: 'RES-2026-0801',
        id_sesion: 105,
        estudiante_email: '2022074255@upt.pe',
        estado: 'PENDIENTE_CONFIRMACION',
        fecha_reserva: new Date(equivalentUtc - 72 * 3600 * 1000).toISOString(),
        fecha_inicio: limaTimeStr,
      });

      const confirmed = await mockAdapter.confirmAttendance(801, '2022074255@upt.pe');
      expect(confirmed.estado).toBe('CONFIRMADA');
      // La fecha de ratificación se genera siempre en formato ISO UTC estándar
      expect(confirmed.fecha_ratificacion).toContain('Z');
    });

    it('rechaza desistimiento en estados ya ejecutados o terminales (ASISTIDA, INASISTENCIA)', async () => {
      mockAdapter.seedBooking({
        id_reserva: 802,
        codigo_reserva: 'RES-2026-0802',
        id_sesion: 106,
        estudiante_email: '2022074255@upt.pe',
        estado: 'ASISTIDA',
        fecha_reserva: '2026-11-01T10:00:00Z',
        fecha_inicio: '2026-11-02T10:00:00Z',
      });

      await expect(
        mockAdapter.cancelReservation(802, 'Desistir post-sesión', '2022074255@upt.pe')
      ).rejects.toMatchObject({
        code: 'INVALID_STATUS_TRANSITION',
      });
    });

    it('eleva RESERVATION_NOT_FOUND al buscar una reserva inexistente', async () => {
      await expect(mockAdapter.confirmAttendance(99999)).rejects.toMatchObject({
        code: 'RESERVATION_NOT_FOUND',
        status: 404,
      });

      await expect(mockAdapter.cancelReservation(99999, 'Motivo')).rejects.toMatchObject({
        code: 'RESERVATION_NOT_FOUND',
        status: 404,
      });
    });
  });

  // ==========================================================================
  // 4. Fachada bookingService (Modos mock y api)
  // ==========================================================================
  describe('4. Fachada bookingService (Modos mock y api)', () => {
    it('conmuta correctamente entre adaptador mock y api', async () => {
      bookingService.setMode('mock');
      expect(bookingService.getMode()).toBe('mock');

      const mockRes = await bookingService.reserveSeat({
        id_sesion: 201,
        estudiante_email: '2022074255@upt.pe',
      });
      expect(mockRes.id_reserva).toBe(501);

      bookingService.setMode('api');
      expect(bookingService.getMode()).toBe('api');

      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 201,
        json: async () => ({
          id_reserva: 9999,
          codigo_reserva: 'RES-API-9999',
          id_sesion: 201,
          estudiante_email: '2022074255@upt.pe',
          estado: 'PENDIENTE_CONFIRMACION',
          fecha_reserva: '2026-11-05T12:00:00Z',
          mensaje: 'Reserva vía API real.',
        }),
      });

      const apiRes = await bookingService.reserveSeat({
        id_sesion: 201,
        estudiante_email: '2022074255@upt.pe',
      });
      expect(apiRes.codigo_reserva).toBe('RES-API-9999');
    });

    it('ejecuta confirmAttendance y cancelReservation mediante la fachada en modo mock', async () => {
      bookingService.setMode('mock');

      const b = await bookingService.reserveSeat({
        id_sesion: 301,
        estudiante_email: '2022074255@upt.pe',
      });

      const confirmed = await bookingService.confirmAttendance(
        b.id_reserva,
        '2022074255@upt.pe'
      );
      expect(confirmed.estado).toBe('CONFIRMADA');

      // Semillar una nueva para probar cancelReservation
      bookingService.seedBooking({
        id_reserva: 888,
        codigo_reserva: 'RES-2026-0888',
        id_sesion: 302,
        estudiante_email: '2022074255@upt.pe',
        estado: 'PENDIENTE_CONFIRMACION',
        fecha_reserva: '2026-11-01T10:00:00Z',
        fecha_inicio: '2026-11-20T10:00:00Z',
      });

      const cancelled = await bookingService.cancelReservation(
        888,
        'Desistimiento formal',
        '2022074255@upt.pe'
      );
      expect(cancelled.estado).toBe('CANCELADA_USUARIO');
      expect(cancelled.motivo_cancelacion).toBe('Desistimiento formal');
    });

    it('ejecuta confirmAttendance y cancelReservation mediante la fachada en modo api', async () => {
      bookingService.setMode('api');
      authService.saveToken('token-api-test');

      globalThis.fetch = vi.fn().mockResolvedValue({
        ok: true,
        status: 200,
        json: async () => ({
          id_reserva: 999,
          codigo_reserva: 'RES-999',
          id_sesion: 305,
          estudiante_email: '2022074255@upt.pe',
          estado: 'CONFIRMADA',
          fecha_reserva: '2026-11-01T10:00:00Z',
          fecha_ratificacion: '2026-11-02T10:00:00Z',
        }),
      });

      const res = await bookingService.confirmAttendance(999);
      expect(res.estado).toBe('CONFIRMADA');
    });

    it('actualiza y retorna la URL base de la API', () => {
      bookingService.setBaseUrl('http://servidor-upt:9000/');
      expect(bookingService.getBaseUrl()).toBe('http://servidor-upt:9000');
    });

    it('impide activar modo mock en compilaciones de producción (Auditoría B.1)', () => {
      vi.stubEnv('PROD', true);
      try {
        bookingService.setMode('api');
        expect(bookingService.getMode()).toBe('api');

        // Intento de conmutar a mock debe ser rechazado
        bookingService.setMode('mock');
        expect(bookingService.getMode()).toBe('api');
      } finally {
        vi.unstubAllEnvs();
        bookingService.setMode('mock');
      }
    });
  });
});
