/**
 * Batería de Pruebas de Integración: Flujo Completo de Mis Reservas, Ratificación y Desistimiento
 * Sprint 05 — Fase 4 (T-25 / T-27 / RF13 / RF14 / CUS24 / CUS17 / RN-08 / RN-09 / RN-10 / PB-014 / PB-015)
 *
 * Verifica:
 * 1. Navegación hacia Mis Reservas desde pestañas y URL.
 * 2. Protección de acceso sin autenticación institucional.
 * 3. Consulta de reservas personales del estudiante y estado vacío pedagógico.
 * 4. Navegación desde una reserva provisional (botón en comprobante).
 * 5. Apertura del diálogo de ratificación pedagógica.
 * 6. Confirmación válida de asistencia (estado CONFIRMADA).
 * 7. Bloqueo preventivo por ventana temporal T-24h (RN-08).
 * 8. Apertura del diálogo de desistimiento voluntario.
 * 9. Desistimiento voluntario válido (estado CANCELADA_USUARIO).
 * 10. Bloqueo de acciones en estados terminales.
 * 11. Manejo de errores HTTP controlados.
 * 12. Manejo explícito de ENDPOINT_NOT_IMPLEMENTED (T-26 / T-28 en backend por Renzo).
 * 13. Prevención de dobles envíos y estados de carga.
 * 14. Actualización reactiva de nómina tras operaciones.
 * 15. Filtrado por estado de reservas en la interfaz.
 * 16. Accesibilidad modal y cierre con tecla Escape (WAI-ARIA RNF05).
 * 17. Diferenciación estricta entre mocks y API real (Seguridad B.1).
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { App } from '../App';
import {
  bookingService,
  BookingException,
  type BookingDetailResponse,
} from '../services/bookingService';
import { recommendationService } from '../services/recommendationService';
import { authService } from '../services/authService';

describe('StudentBookingsIntegration (Sprint 05 Fase 4 - T-25 / T-27 / RF13 / RF14)', () => {
  const studentEmail = '2022074255@upt.pe';
  const fixedNow = new Date('2026-11-02T10:00:00Z').getTime();

  // Reserva pendiente con 48h de antelación (válida para ratificar y desistir)
  const pendingBooking48h: BookingDetailResponse = {
    id_reserva: 101,
    codigo_reserva: 'RES-2026-0101',
    id_sesion: 12,
    codigo_sesion: 'SES-0012',
    nombre_asignatura: 'Algoritmos y Estructuras de Datos',
    nombre_tema: 'Árboles Balanceados AVL',
    estudiante_email: studentEmail,
    mentor_email: 'mentor.titular@upt.pe',
    estado: 'PENDIENTE_CONFIRMACION',
    fecha_reserva: new Date(fixedNow - 3600 * 1000).toISOString(),
    fecha_inicio: new Date(Date.now() + 48 * 3600 * 1000).toISOString(),
    duracion_minutos: 120,
    modalidad: 'presencial',
    espacio_asignado: 'Laboratorio L-03 EPIS',
    ticket_hash: 'hash-abc-123',
  };

  // Reserva confirmada con 36h de antelación (válida para desistir, ratificada previamente)
  const confirmedBooking36h: BookingDetailResponse = {
    ...pendingBooking48h,
    id_reserva: 102,
    codigo_reserva: 'RES-2026-0102',
    estado: 'CONFIRMADA',
    fecha_inicio: new Date(Date.now() + 36 * 3600 * 1000).toISOString(),
    fecha_ratificacion: new Date(Date.now() - 1800 * 1000).toISOString(),
  };

  // Reserva cerrada con 12h de antelación (inhabilitada para ratificar y desistir por corte T-24h)
  const closedBooking12h: BookingDetailResponse = {
    ...pendingBooking48h,
    id_reserva: 103,
    codigo_reserva: 'RES-2026-0103',
    fecha_inicio: new Date(Date.now() + 12 * 3600 * 1000).toISOString(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.clear();
    recommendationService.setMode('mock');
    bookingService.setMode('mock');
    bookingService.getMockAdapter().resetToDefaults();
    bookingService.setCurrentTime(fixedNow);

    // Guardar token JWT del estudiante institucional
    const testPayload = { sub: studentEmail, role: 'MENTOREADO' };
    authService.saveToken(`h.${btoa(JSON.stringify(testPayload))}.s`);
  });

  afterEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  // ==========================================================================
  // 1. Navegación hacia Mis Reservas
  // ==========================================================================
  it('1. Permite navegar hacia Mis Reservas desde el selector principal de pestañas', async () => {
    render(<App />);

    const bookingsTab = screen.getByRole('button', { name: /^📅 Mis Reservas$/i });
    expect(bookingsTab).toBeInTheDocument();

    fireEvent.click(bookingsTab);

    await waitFor(() => {
      expect(
        screen.getAllByRole('heading', {
          name: /Mis Reservas de Mentoría/i,
        }).length
      ).toBeGreaterThanOrEqual(1);
      expect(
        screen.getByText(/Revisa tus sesiones reservadas, confirma tu asistencia/i)
      ).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 2. Protección de Acceso sin Autenticación
  // ==========================================================================
  it('2. Bloquea el acceso a Mis Reservas sin sesión activa y permite redirigir al login', async () => {
    authService.clearToken();
    window.history.pushState({}, '', '?tab=bookings');

    render(<App />);

    await waitFor(() => {
      expect(screen.getByText(/Acceso Restringido a Mis Reservas/i)).toBeInTheDocument();
      expect(
        screen.getByText(/debes iniciar sesión con tu cuenta institucional/i)
      ).toBeInTheDocument();
    });

    const loginRedirectBtn = screen.getByRole('button', {
      name: /Iniciar Sesión Institucional/i,
    });
    fireEvent.click(loginRedirectBtn);

    await waitFor(() => {
      expect(
        screen.getAllByRole('heading', { name: /Iniciar Sesión Institucional/i }).length
      ).toBeGreaterThanOrEqual(1);
      expect(screen.getByLabelText(/Correo Electrónico Institucional/i)).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 3. Consulta de Reservas Personales y Estado Vacío Pedagógico
  // ==========================================================================
  it('3. Muestra estado vacío pedagógico cuando no hay reservas y permite explorar la cartelera', async () => {
    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([]);

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText(/No se encontraron reservas/i)).toBeInTheDocument();
      expect(
        screen.getByText(/Aún no te has inscrito en ninguna sesión de mentoría académica/i)
      ).toBeInTheDocument();
    });

    const exploreBtn = screen.getByRole('button', {
      name: /Explorar Clases Recomendadas/i,
    });
    fireEvent.click(exploreBtn);

    await waitFor(() => {
      expect(
        screen.getByRole('heading', {
          name: /Mentorías Recomendadas y Reserva de Sesiones/i,
        })
      ).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 4. Navegación desde Reserva Provisional (Botón en Comprobante)
  // ==========================================================================
  it('4. Flujo End-to-End: formaliza reserva provisional y navega hacia Mis Reservas mediante el comprobante', async () => {
    render(<App />);

    // Navegar a recomendaciones
    fireEvent.click(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i }));

    const reserveButtons = await screen.findAllByRole('button', { name: /Reservar Cupo/i });
    expect(reserveButtons.length).toBeGreaterThan(0);
    fireEvent.click(reserveButtons[0]);

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    // Confirmar la reserva provisional
    const confirmBtn = screen.getByRole('button', { name: /Confirmar Reserva de Cupo/i });
    fireEvent.click(confirmBtn);

    // Comprobante desplegado con botón "Ver Mis Reservas"
    await waitFor(() => {
      expect(screen.getByTestId('booking-success-panel')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Ver Mis Reservas/i })).toBeInTheDocument();
    });

    // Pulsar botón de navegación hacia Mis Reservas
    const viewBookingsBtn = screen.getByRole('button', { name: /Ver Mis Reservas/i });
    fireEvent.click(viewBookingsBtn);

    // Modal se cierra y la aplicación activa la pestaña Mis Reservas
    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
      expect(
        screen.getAllByRole('heading', {
          name: /Mis Reservas de Mentoría/i,
        }).length
      ).toBeGreaterThanOrEqual(1);
    });
  });

  // ==========================================================================
  // 5. Apertura del Diálogo de Ratificación Pedagógica (RF13 / RN-08 / RN-09)
  // ==========================================================================
  it('5. Abre el diálogo modal de ratificación pedagógica desplegando detalles y quórum RN-09', async () => {
    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([pendingBooking48h]);

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
    });

    const confirmAttendanceBtn = screen.getByRole('button', {
      name: /Confirmar Asistencia/i,
    });
    fireEvent.click(confirmAttendanceBtn);

    await waitFor(() => {
      const dialog = screen.getByRole('dialog');
      expect(dialog).toBeInTheDocument();
      expect(
        screen.getByRole('heading', { name: /Ratificar Asistencia a Mentoría/i })
      ).toBeInTheDocument();
      expect(screen.getByText(/quórum mínimo del 50%/i)).toBeInTheDocument();
      expect(screen.getByText(/Compromiso de Asistencia y Quórum/i)).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 6. Confirmación Válida de Asistencia
  // ==========================================================================
  it('6. Ratifica asistencia exitosamente, actualiza estado a CONFIRMADA y refresca la nómina', async () => {
    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([pendingBooking48h]);
    const confirmSpy = vi.spyOn(bookingService, 'confirmAttendance').mockResolvedValue({
      ...pendingBooking48h,
      estado: 'CONFIRMADA',
      fecha_ratificacion: new Date().toISOString(),
    });

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /Confirmar Asistencia/i }));

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    const executeBtn = screen.getByRole('button', {
      name: /^✓ Confirmar Asistencia$/i,
    });
    fireEvent.click(executeBtn);

    await waitFor(() => {
      expect(confirmSpy).toHaveBeenCalledWith(101, studentEmail);
      expect(screen.getByText(/¡Asistencia ratificada con éxito/i)).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 7. Bloqueo Preventivo por Ventana Temporal T-24h (RN-08)
  // ==========================================================================
  it('7. Deshabilita la ratificación y muestra advertencia cuando restan <= 24h para la sesión', async () => {
    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([closedBooking12h]);

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText('RES-2026-0103')).toBeInTheDocument();
    });

    const disabledBtn = screen.getByRole('button', { name: /Plazo Vencido/i });
    expect(disabledBtn).toBeDisabled();
    expect(screen.getByText(/Ventana.*cerrada/i)).toBeInTheDocument();
  });

  // ==========================================================================
  // 8. Apertura del Diálogo de Desistimiento Voluntario (RF14 / RN-10 / PB-015)
  // ==========================================================================
  it('8. Abre el diálogo de desistimiento informando la política de liberación de vacante sin penalidad', async () => {
    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([confirmedBooking36h]);

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText('RES-2026-0102')).toBeInTheDocument();
    });

    const cancelBtn = screen.getByRole('button', {
      name: /Cancelar Reserva \/ Desistir/i,
    });
    expect(cancelBtn).not.toBeDisabled();
    fireEvent.click(cancelBtn);

    await waitFor(() => {
      const dialog = screen.getByRole('dialog');
      expect(dialog).toBeInTheDocument();
      expect(
        screen.getByRole('heading', { name: /Desistimiento Voluntario de Cupo/i })
      ).toBeInTheDocument();
      expect(screen.getByText(/Política de Desistimiento y Liberación de Cupo/i)).toBeInTheDocument();
      expect(screen.getByPlaceholderText(/Describe brevemente el motivo/i)).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 9. Desistimiento Voluntario Válido
  // ==========================================================================
  it('9. Cancela reserva voluntariamente, actualiza a CANCELADA_USUARIO y muestra alerta de éxito', async () => {
    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([confirmedBooking36h]);
    const cancelSpy = vi.spyOn(bookingService, 'cancelReservation').mockResolvedValue({
      ...confirmedBooking36h,
      estado: 'CANCELADA_USUARIO',
      motivo_cancelacion: 'Cruce imprevisto con examen parcial',
    });

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText('RES-2026-0102')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    const reasonInput = screen.getByPlaceholderText(/Describe brevemente el motivo/i);
    fireEvent.change(reasonInput, {
      target: { value: 'Cruce imprevisto con examen parcial' },
    });

    const confirmCancelBtn = screen.getByRole('button', {
      name: /Confirmar Desistimiento/i,
    });
    fireEvent.click(confirmCancelBtn);

    await waitFor(() => {
      expect(cancelSpy).toHaveBeenCalledWith(
        102,
        'Cruce imprevisto con examen parcial',
        studentEmail
      );
      expect(screen.getByText(/¡Reserva RES-2026-0102 cancelada con éxito!/i)).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 10. Bloqueo de Acciones en Estados Terminales
  // ==========================================================================
  it('10. No muestra botones de ratificación ni de desistimiento en reservas canceladas o expiradas', async () => {
    const cancelledBooking: BookingDetailResponse = {
      ...pendingBooking48h,
      id_reserva: 104,
      codigo_reserva: 'RES-2026-0104',
      estado: 'CANCELADA_USUARIO',
    };

    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([cancelledBooking]);

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText('RES-2026-0104')).toBeInTheDocument();
    });

    expect(screen.queryByRole('button', { name: /Confirmar Asistencia/i })).not.toBeInTheDocument();
    expect(
      screen.queryByRole('button', { name: /Cancelar Reserva \/ Desistir/i })
    ).not.toBeInTheDocument();
    expect(screen.getByText('Desistimiento Voluntario')).toBeInTheDocument();
  });

  // ==========================================================================
  // 11. Manejo de Errores HTTP Controlados
  // ==========================================================================
  it('11. Maneja error 403 FORBIDDEN mostrando alerta pedagógica sin colapsar la vista', async () => {
    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([pendingBooking48h]);
    vi.spyOn(bookingService, 'confirmAttendance').mockRejectedValueOnce(
      new BookingException('FORBIDDEN', 'No autorizado para operar sobre esta reserva', 403)
    );

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /Confirmar Asistencia/i }));
    fireEvent.click(screen.getByRole('button', { name: /^✓ Confirmar Asistencia$/i }));

    await waitFor(() => {
      expect(
        screen.getByText(/No tienes autorización para ratificar una reserva de otro estudiante/i)
      ).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 12. Manejo de ENDPOINT_NOT_IMPLEMENTED (T-26 / T-28 Renzo)
  // ==========================================================================
  it('12. Despliega aviso formativo cuando el backend retorna ENDPOINT_NOT_IMPLEMENTED', async () => {
    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([pendingBooking48h]);
    vi.spyOn(bookingService, 'confirmAttendance').mockRejectedValueOnce(
      new BookingException('ENDPOINT_NOT_IMPLEMENTED', 'En desarrollo por Renzo', 501)
    );

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /Confirmar Asistencia/i }));
    fireEvent.click(screen.getByRole('button', { name: /^✓ Confirmar Asistencia$/i }));

    await waitFor(() => {
      expect(
        screen.getByText(/Servicio en integración/i)
      ).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 13. Prevención de Dobles Envíos
  // ==========================================================================
  it('13. Previene la doble pulsación durante el procesamiento asíncrono de confirmación', async () => {
    let resolver: (val: BookingDetailResponse) => void;
    const pendingPromise = new Promise<BookingDetailResponse>((res) => {
      resolver = res;
    });

    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([pendingBooking48h]);
    vi.spyOn(bookingService, 'confirmAttendance').mockReturnValue(pendingPromise);

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /Confirmar Asistencia/i }));

    const submitBtn = screen.getByRole('button', {
      name: /^✓ Confirmar Asistencia$/i,
    });
    fireEvent.click(submitBtn);

    // Debe deshabilitar el botón y mostrar texto de espera
    expect(screen.getByRole('button', { name: /Ratificando asistencia\.\.\./i })).toBeDisabled();

    // Resolver promesa
    resolver!({
      ...pendingBooking48h,
      estado: 'CONFIRMADA',
    });

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 14. Actualización Reactiva de Nómina
  // ==========================================================================
  it('14. El botón Actualizar invoca nuevamente al servicio para refrescar la nómina', async () => {
    const listSpy = vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([pendingBooking48h]);

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(listSpy).toHaveBeenCalledTimes(1);
    });

    const refreshBtn = screen.getByRole('button', {
      name: /Actualizar nómina de reservas personales/i,
    });
    fireEvent.click(refreshBtn);

    await waitFor(() => {
      expect(listSpy).toHaveBeenCalledTimes(2);
    });
  });

  // ==========================================================================
  // 15. Filtrado por Estado de Reservas
  // ==========================================================================
  it('15. Permite alternar entre pestañas de filtrado (Todas, Por Ratificar, Ratificadas, Histórico)', async () => {
    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([
      pendingBooking48h,
      confirmedBooking36h,
    ]);

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      expect(screen.getByText('RES-2026-0102')).toBeInTheDocument();
    });

    // Filtrar a Ratificadas
    const ratificadasFilter = screen.getByRole('button', { name: /Ratificadas \(1\)/i });
    fireEvent.click(ratificadasFilter);

    expect(screen.queryByText('RES-2026-0101')).not.toBeInTheDocument();
    expect(screen.getByText('RES-2026-0102')).toBeInTheDocument();

    // Volver a Todas
    const todasFilter = screen.getByRole('button', { name: /Todas \(2\)/i });
    fireEvent.click(todasFilter);

    expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
    expect(screen.getByText('RES-2026-0102')).toBeInTheDocument();
  });

  // ==========================================================================
  // 16. Accesibilidad Modal y Cierre con Tecla Escape (RNF05)
  // ==========================================================================
  it('16. Cierra los diálogos modales de ratificación y desistimiento al pulsar la tecla Escape', async () => {
    vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([pendingBooking48h]);

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^📅 Mis Reservas$/i }));

    await waitFor(() => {
      expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
    });

    // Abrir ratificación
    fireEvent.click(screen.getByRole('button', { name: /Confirmar Asistencia/i }));
    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    // Cerrar con Escape
    fireEvent.keyDown(window, { key: 'Escape', code: 'Escape' });
    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });

    // Abrir desistimiento
    fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));
    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    // Cerrar con Escape
    fireEvent.keyDown(window, { key: 'Escape', code: 'Escape' });
    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 17. Diferenciación Estricta entre Mocks y API Real (Seguridad B.1)
  // ==========================================================================
  it('17. Impide activar modo mock si import.meta.env.PROD está configurado', () => {
    const errorSpy = vi.spyOn(console, 'error').mockImplementation(() => {});

    // Forzar temporalmente PROD
    const originalProd = import.meta.env.PROD;
    try {
      (import.meta.env as { PROD: boolean }).PROD = true;
      bookingService.setMode('mock');
      expect(errorSpy).toHaveBeenCalledWith(
        expect.stringMatching(/El modo mock está estrictamente prohibido en compilaciones de producción/i)
      );
      expect(bookingService.getMode()).toBe('api');
    } finally {
      (import.meta.env as { PROD: boolean }).PROD = originalProd;
    }
  });
});
