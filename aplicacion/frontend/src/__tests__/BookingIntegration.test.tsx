import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { App } from '../App';
import { bookingService, BookingException } from '../services/bookingService';
import { recommendationService } from '../services/recommendationService';
import { authService } from '../services/authService';

describe('BookingIntegration Flow (T-23 / RF06 / RF12 / CUS02 / CUS04)', () => {
  const studentEmail = '2022074255@upt.pe';

  beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.clear();
    recommendationService.setMode('mock');
    bookingService.setMode('mock');
    bookingService.getMockAdapter().resetToDefaults();
    // Autenticación institucional por defecto para pruebas de flujo
    const testPayload = { sub: studentEmail, role: 'MENTOREADO' };
    authService.saveToken(`h.${btoa(JSON.stringify(testPayload))}.s`);
  });

  afterEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  it('1. Permite navegar hacia la pestaña de Recomendaciones & Reservas y cargar el feed Top-k', async () => {
    render(<App />);

    const recTab = screen.getByRole('button', {
      name: /^🎯 Explorar mentorías$/i,
    });
    expect(recTab).toBeInTheDocument();

    fireEvent.click(recTab);

    await waitFor(() => {
      expect(
        screen.getByRole('heading', {
          name: /Mentorías Recomendadas y Reserva de Sesiones/i,
        })
      ).toBeInTheDocument();
      expect(
        screen.getByText(/Encuentra sesiones de mentoría afines a tus asignaturas y reserva tu vacante/i)
      ).toBeInTheDocument();
    });

    // Esperar a que cargue la lista de ofertas recomendadas
    await waitFor(() => {
      expect(screen.getAllByText(/Algoritmos y Estructuras de Datos/i).length).toBeGreaterThan(0);
    });
  });

  it('2. Abre BookingModalView al seleccionar una oferta desde la cartelera Top-k', async () => {
    render(<App />);

    // Navegar a recomendaciones
    fireEvent.click(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i }));

    // Esperar a que aparezcan los botones de reservar
    const reserveButtons = await screen.findAllByRole('button', {
      name: /Reservar Cupo/i,
    });
    expect(reserveButtons.length).toBeGreaterThan(0);

    // Seleccionar la primera oferta
    fireEvent.click(reserveButtons[0]);

    // Verificar que el modal de confirmación se abre con los datos correspondientes
    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
      expect(
        screen.getByRole('heading', { name: /Confirmar Reserva de Cupo/i })
      ).toBeInTheDocument();
      expect(screen.getByText(/Reserva de Cupo de Mentoría/i)).toBeInTheDocument();
      expect(screen.getByText(studentEmail)).toBeInTheDocument();
    });
  });

  it('3. Flujo completo exitoso: selecciona oferta, confirma intención, invoca bookingService y despliega comprobante provisional', async () => {
    const reserveSpy = vi.spyOn(bookingService, 'reserveSeat');

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i }));

    const reserveButtons = await screen.findAllByRole('button', { name: /Reservar Cupo/i });
    fireEvent.click(reserveButtons[0]);

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    const confirmButton = screen.getByRole('button', {
      name: /Confirmar Reserva de Cupo/i,
    });
    expect(confirmButton).not.toBeDisabled();

    fireEvent.click(confirmButton);

    // Verificar que el servicio fue invocado con el correo del estudiante y un ID de sesión válido
    await waitFor(() => {
      expect(reserveSpy).toHaveBeenCalledTimes(1);
      expect(reserveSpy).toHaveBeenCalledWith(
        expect.objectContaining({
          estudiante_email: studentEmail,
        })
      );
    });

    // Verificar despliegue del comprobante provisional con código de reserva
    await waitFor(() => {
      expect(screen.getByTestId('booking-success-panel')).toBeInTheDocument();
      expect(screen.getByText(/¡Cupo Reservado Exitosamente!/i)).toBeInTheDocument();
      expect(screen.getByTestId('receipt-booking-code')).toHaveTextContent(/RES-2026-/i);
      expect(screen.getByText('PENDIENTE_CONFIRMACION')).toBeInTheDocument();
    });

    // Cerrar comprobante
    const closeBtn = screen.getByRole('button', { name: /Entendido, Cerrar/i });
    fireEvent.click(closeBtn);

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
  });

  it('4. Maneja colisión de aforo concurrente (409 CAPACITY_EXCEEDED) y sincroniza la cartelera', async () => {
    vi.spyOn(bookingService, 'reserveSeat').mockRejectedValueOnce(
      new BookingException(
        'CAPACITY_EXCEEDED',
        'CAPACITY_EXCEEDED: Aforo completo. No quedan vacantes disponibles en esta sesión.',
        409
      )
    );

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i }));

    const reserveButtons = await screen.findAllByRole('button', { name: /Reservar Cupo/i });
    fireEvent.click(reserveButtons[0]);

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    const confirmButton = screen.getByRole('button', {
      name: /Confirmar Reserva de Cupo/i,
    });
    fireEvent.click(confirmButton);

    await waitFor(() => {
      const errorAlert = screen.getByTestId('booking-error-alert');
      expect(errorAlert).toBeInTheDocument();
      expect(errorAlert).toHaveTextContent(/CAPACITY_EXCEEDED/i);
      expect(errorAlert).toHaveTextContent(/Aforo completo/i);
    });
  });

  it('5. Maneja error de reserva duplicada (400 DUPLICATE_BOOKING)', async () => {
    vi.spyOn(bookingService, 'reserveSeat').mockRejectedValueOnce(
      new BookingException(
        'DUPLICATE_BOOKING',
        'DUPLICATE_BOOKING: Ya cuentas con una reserva registrada para esta clase.',
        400
      )
    );

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i }));

    const reserveButtons = await screen.findAllByRole('button', { name: /Reservar Cupo/i });
    fireEvent.click(reserveButtons[0]);

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    const confirmButton = screen.getByRole('button', {
      name: /Confirmar Reserva de Cupo/i,
    });
    fireEvent.click(confirmButton);

    await waitFor(() => {
      const errorAlert = screen.getByTestId('booking-error-alert');
      expect(errorAlert).toBeInTheDocument();
      expect(errorAlert).toHaveTextContent(/DUPLICATE_BOOKING/i);
      expect(errorAlert).toHaveTextContent(/Ya cuentas con una reserva registrada/i);
    });
  });

  it('6. Maneja error de ventana temporal cerrada (400 WINDOW_CLOSED_T24H)', async () => {
    vi.spyOn(bookingService, 'reserveSeat').mockRejectedValueOnce(
      new BookingException(
        'WINDOW_CLOSED_T24H',
        'WINDOW_CLOSED_T24H: Las reservas cierran 24 horas antes del inicio de la sesión.',
        400
      )
    );

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i }));

    const reserveButtons = await screen.findAllByRole('button', { name: /Reservar Cupo/i });
    fireEvent.click(reserveButtons[0]);

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    const confirmButton = screen.getByRole('button', {
      name: /Confirmar Reserva de Cupo/i,
    });
    fireEvent.click(confirmButton);

    await waitFor(() => {
      const errorAlert = screen.getByTestId('booking-error-alert');
      expect(errorAlert).toBeInTheDocument();
      expect(errorAlert).toHaveTextContent(/WINDOW_CLOSED_T24H/i);
      expect(errorAlert).toHaveTextContent(/Las reservas cierran 24 horas antes/i);
    });
  });

  it('7. Maneja exigencia de consentimiento (403 CONSENT_REQUIRED)', async () => {
    vi.spyOn(bookingService, 'reserveSeat').mockRejectedValueOnce(
      new BookingException(
        'CONSENT_REQUIRED',
        'CONSENT_REQUIRED: Debes aceptar los términos de tratamiento de datos personales conforme a la Ley Nº 29733 (RN-02).',
        403
      )
    );

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i }));

    const reserveButtons = await screen.findAllByRole('button', { name: /Reservar Cupo/i });
    fireEvent.click(reserveButtons[0]);

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    const confirmButton = screen.getByRole('button', {
      name: /Confirmar Reserva de Cupo/i,
    });
    fireEvent.click(confirmButton);

    await waitFor(() => {
      const errorAlert = screen.getByTestId('booking-error-alert');
      expect(errorAlert).toBeInTheDocument();
      expect(errorAlert).toHaveTextContent(/CONSENT_REQUIRED/i);
      expect(errorAlert).toHaveTextContent(/Ley Nº 29733 \(RN-02\)/i);
    });
  });

  it('8. Maneja indisponibilidad temporal (503 DATABASE_BUSY) sin reintentos automáticos destructivos', async () => {
    const reserveSpy = vi.spyOn(bookingService, 'reserveSeat').mockRejectedValueOnce(
      new BookingException(
        'DATABASE_BUSY',
        'DATABASE_BUSY: El servicio de reservas se encuentra temporalmente sobrecargado. Reintente en unos momentos.',
        503
      )
    );

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i }));

    const reserveButtons = await screen.findAllByRole('button', { name: /Reservar Cupo/i });
    fireEvent.click(reserveButtons[0]);

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    const confirmButton = screen.getByRole('button', {
      name: /Confirmar Reserva de Cupo/i,
    });
    fireEvent.click(confirmButton);

    await waitFor(() => {
      const errorAlert = screen.getByTestId('booking-error-alert');
      expect(errorAlert).toBeInTheDocument();
      expect(errorAlert).toHaveTextContent(/DATABASE_BUSY/i);
    });

    // Se efectuó una única llamada controlada
    expect(reserveSpy).toHaveBeenCalledTimes(1);
  });

  it('9. Resuelve la identidad del estudiante desde el token JWT guardado en authService', async () => {
    const fakePayload = { sub: 'estudiante.honor@upt.pe', role: 'MENTOREADO' };
    authService.saveToken(`h.${btoa(JSON.stringify(fakePayload))}.s`);

    const reserveSpy = vi.spyOn(bookingService, 'reserveSeat');

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i }));

    const reserveButtons = await screen.findAllByRole('button', { name: /Reservar Cupo/i });
    fireEvent.click(reserveButtons[0]);

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
      expect(screen.getByText('estudiante.honor@upt.pe')).toBeInTheDocument();
    });

    const confirmButton = screen.getByRole('button', {
      name: /Confirmar Reserva de Cupo/i,
    });
    fireEvent.click(confirmButton);

    await waitFor(() => {
      expect(reserveSpy).toHaveBeenCalledWith(
        expect.objectContaining({
          estudiante_email: 'estudiante.honor@upt.pe',
        })
      );
    });
  });

  it('10. Rechaza de forma estricta identificadores de oferta alfanuméricos arbitrarios sin invocar a bookingService', async () => {
    const reserveSpy = vi.spyOn(bookingService, 'reserveSeat');

    // Forzar que el feed entregue una oferta con id_oferta no numérico (e.g. código de formato espurio)
    vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValueOnce({
      mentee_email: studentEmail,
      total_candidates_evaluated: 1,
      top_k: 5,
      recommendations_count: 1,
      algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
      items: [
        {
          id_oferta: 'OFR-INVALID-CODE-XYZ',
          codigo_sesion: 'SES-999',
          id_asignatura: 1,
          codigo_asignatura: 'CALC-101',
          nombre_asignatura: 'Cálculo I',
          id_tema: 1,
          nombre_tema: 'Límites',
          fecha_inicio: new Date(Date.now() + 48 * 3600 * 1000).toISOString(),
          duracion_minutos: 60,
          modalidad: 'presencial',
          aforo_maximo: 10,
          aforo_disponible: 5,
          espacio_asignado: 'Aula 101',
          mentor_email: 'mentor@upt.pe',
          mentor_nombre: 'Mentor Test',
          mentor_ciclo: 8,
          score_total: 0.9,
          breakdown: {
            curricular_affinity: 1.0,
            course_weight_factor: 1.0,
            critical_course_applied: null,
            topic_overlap_jaccard: 0.8,
            topic_overlap_dice: 0.88,
            schedule_compatibility: 0.8,
            schedule_matching_slots_count: 3,
            matching_slots: ['Lun 10:00-11:00'],
            modality_compatibility: 1.0,
            institutional_merit_eligible: true,
            explanation_text: 'Test',
          },
        },
      ],
    });

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i }));

    const reserveButtons = await screen.findAllByRole('button', { name: /Reservar Cupo/i });
    fireEvent.click(reserveButtons[0]);

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    const confirmButton = screen.getByRole('button', {
      name: /Confirmar Reserva de Cupo/i,
    });
    fireEvent.click(confirmButton);

    await waitFor(() => {
      const errorAlert = screen.getByTestId('booking-error-alert');
      expect(errorAlert).toBeInTheDocument();
      expect(errorAlert).toHaveTextContent(/Identificador de sesión inválido/i);
    });

    // bookingService NO debe haber sido invocado con un ID espurio o inventado
    expect(reserveSpy).not.toHaveBeenCalled();
  });

  it('11. Bloquea el flujo de reserva e induce autenticación si no existe sesión institucional activa (Auditoría B.2)', async () => {
    authService.clearToken();
    window.history.pushState({}, '', '?tab=recommendations');

    render(<App />);

    // Con guardas RBAC, el feed privado no se monta y se despliega acceso restringido
    await waitFor(() => {
      expect(screen.getByText(/Acceso Restringido a Explorar mentorías/i)).toBeInTheDocument();
      expect(
        screen.getByText(/debes iniciar sesión con tu cuenta institucional/i)
      ).toBeInTheDocument();
    });

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();

    // Debe inducir la navegación hacia el login
    const loginRedirectBtn = screen.getByRole('button', {
      name: /Iniciar Sesión Institucional/i,
    });
    fireEvent.click(loginRedirectBtn);

    await waitFor(() => {
      expect(
        screen.getAllByRole('heading', { name: /Iniciar Sesión Institucional/i }).length
      ).toBeGreaterThanOrEqual(1);
    });
  });
});
