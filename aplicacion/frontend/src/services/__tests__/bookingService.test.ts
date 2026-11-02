import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import {
  bookingService,
  ApiBookingAdapter,
  MockBookingAdapter,
  BookingException,
  type BookingCreatePayload,
  type BookingResponse,
} from '../bookingService';
import { authService } from '../authService';

describe('bookingService (T-23 / CUS04 / RF12 / RN-05 / RN-08 / RNF07)', () => {
  const mockBaseUrl = 'http://127.0.0.1:8000';
  let apiAdapter: ApiBookingAdapter;
  let mockAdapter: MockBookingAdapter;

  beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.clear();
    bookingService.setMode('mock');
    bookingService.getMockAdapter().resetToDefaults();
    apiAdapter = new ApiBookingAdapter(mockBaseUrl);
    mockAdapter = new MockBookingAdapter();
  });

  afterEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  describe('1. Validaciones preventivas de contrato en cliente', () => {
    it('rechaza id_sesion no entero, menor a 1 o indefinido', async () => {
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
        /dominio institucional @upt.pe/i
      );
      await expect(mockAdapter.reserveSeat(payload)).rejects.toThrow(
        /dominio institucional @upt.pe/i
      );
    });
  });

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

    it('interpreta error 503 DATABASE_BUSY y no ejecuta reintentos ciegos', async () => {
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

      // Solo 1 llamada efectuada: sin retry automático
      expect(fetchMock).toHaveBeenCalledTimes(1);
    });

    it('captura fallos de red y genera NETWORK_ERROR', async () => {
      globalThis.fetch = vi.fn().mockRejectedValue(new TypeError('Failed to fetch'));

      await expect(
        apiAdapter.reserveSeat({ id_sesion: 10, estudiante_email: '2022074255@upt.pe' })
      ).rejects.toMatchObject({
        code: 'NETWORK_ERROR',
      });
    });

    it('interpreta errores con objeto detail { code, message }', async () => {
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

    it('consulta mis reservas con getMyReservations', async () => {
      const mockList = [
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

    it('permite consultar las reservas simuladas registradas', async () => {
      await mockAdapter.reserveSeat({
        id_sesion: 101,
        estudiante_email: '2022074255@upt.pe',
      });

      const list = await mockAdapter.getMyReservations(undefined, '2022074255@upt.pe');
      expect(list.length).toBe(1);
      expect(list[0].id_sesion).toBe(101);
    });
  });

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

    it('actualiza y retorna la URL base de la API', () => {
      bookingService.setBaseUrl('http://servidor-upt:9000/');
      expect(bookingService.getBaseUrl()).toBe('http://servidor-upt:9000');
    });
  });
});
