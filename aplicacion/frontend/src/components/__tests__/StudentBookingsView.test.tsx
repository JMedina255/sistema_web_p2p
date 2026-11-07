import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { StudentBookingsView } from '../StudentBookingsView';
import { bookingService, type BookingDetailResponse, BookingException } from '../../services/bookingService';
import { authService } from '../../services/authService';

describe('StudentBookingsView Component (T-25 / RF13 / CUS24 / RN-08 / RN-09 / RNF05)', () => {
  const studentEmail = '2022074255@upt.pe';
  // Generador de un token simulado con correo @upt.pe codificado en el payload
  const mockJwtToken = `header.${btoa(JSON.stringify({ sub: studentEmail, role: 'student' }))}.signature`;

  // Fecha fija para pruebas deterministas
  const fixedNow = new Date('2026-11-02T10:00:00Z').getTime();
  // Sesión en 48 horas (holgadamente dentro del plazo > 24h según RN-08)
  const sessionIn48h = new Date(fixedNow + 48 * 3600 * 1000).toISOString();
  // Sesión exactamente en 24 horas (límite perentorio de cierre RN-08)
  const sessionIn24h = new Date(fixedNow + 24 * 3600 * 1000).toISOString();
  // Sesión en 12 horas (plazo vencido < 24h)
  const sessionIn12h = new Date(fixedNow + 12 * 3600 * 1000).toISOString();
  // Sesión en el pasado (vencida)
  const sessionPast = new Date(fixedNow - 2 * 3600 * 1000).toISOString();

  const samplePendingBooking: BookingDetailResponse = {
    id_reserva: 101,
    codigo_reserva: 'RES-2026-0101',
    id_sesion: 12,
    codigo_sesion: 'SES-0012',
    estudiante_email: studentEmail,
    estado: 'PENDIENTE_CONFIRMACION',
    fecha_reserva: '2026-11-01T08:00:00Z',
    nombre_asignatura: 'Algoritmos y Estructuras de Datos',
    nombre_tema: 'Grafos y Algoritmo de Dijkstra',
    fecha_inicio: sessionIn48h,
    duracion_minutos: 90,
    modalidad: 'presencial',
    espacio_asignado: 'Laboratorio L-02',
    mentor_email: 'renzo.mentor@upt.pe',
  };

  const sampleConfirmedBooking: BookingDetailResponse = {
    id_reserva: 102,
    codigo_reserva: 'RES-2026-0102',
    id_sesion: 14,
    codigo_sesion: 'SES-0014',
    estudiante_email: studentEmail,
    estado: 'CONFIRMADA',
    fecha_reserva: '2026-11-01T09:00:00Z',
    fecha_ratificacion: '2026-11-02T08:30:00Z',
    nombre_asignatura: 'Bases de Datos I',
    nombre_tema: 'Normalización y Tercera Forma Normal',
    fecha_inicio: sessionIn48h,
    duracion_minutos: 90,
    modalidad: 'virtual',
    espacio_asignado: 'Google Meet',
    mentor_email: 'renzo.mentor@upt.pe',
  };

  const sampleCancelledBooking: BookingDetailResponse = {
    id_reserva: 103,
    codigo_reserva: 'RES-2026-0103',
    id_sesion: 16,
    codigo_sesion: 'SES-0016',
    estudiante_email: studentEmail,
    estado: 'CANCELADA_USUARIO',
    fecha_reserva: '2026-10-28T10:00:00Z',
    motivo_cancelacion: 'Cruce con examen parcial de Matemáticas',
    nombre_asignatura: 'Ingeniería de Software',
    nombre_tema: 'Modelado CUS y UWE',
    fecha_inicio: sessionIn48h,
    duracion_minutos: 90,
    modalidad: 'presencial',
    espacio_asignado: 'Aula A-101',
    mentor_email: 'maria.mentor@upt.pe',
  };

  beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.clear();
    authService.saveToken(mockJwtToken);
    bookingService.setMode('mock');
    bookingService.resetToDefaults();
    bookingService.setCurrentTime(fixedNow);
  });

  afterEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
    bookingService.setCurrentTime(null);
  });

  // ==========================================================================
  // 1. Autenticación y Carga Inicial
  // ==========================================================================
  describe('1. Autenticación y Control de Acceso (RN-01)', () => {
    it('muestra pantalla de acceso restringido si el estudiante no está autenticado', async () => {
      authService.clearToken();
      const mockLoginRedirect = vi.fn();

      render(<StudentBookingsView onLoginRedirect={mockLoginRedirect} />);

      expect(screen.getByText(/Acceso Restringido a Mis Reservas/i)).toBeInTheDocument();
      expect(screen.getByText(/@upt\.pe/i)).toBeInTheDocument();

      const loginBtn = screen.getByRole('button', { name: /Iniciar Sesión Institucional/i });
      fireEvent.click(loginBtn);
      expect(mockLoginRedirect).toHaveBeenCalledTimes(1);
    });

    it('muestra indicador de carga accesible mientras consulta el servicio', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockImplementation(
        () => new Promise(() => {}) // Promesa pendiente permanente
      );

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      expect(screen.getByRole('status')).toBeInTheDocument();
      expect(
        screen.getByText(/Consultando nómina de reservas de mentoría.../i)
      ).toBeInTheDocument();
    });

    it('muestra estado vacío pedagógico cuando el estudiante no registra reservas', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([]);
      const mockExplore = vi.fn();

      render(
        <StudentBookingsView
          studentEmail={studentEmail}
          currentTime={fixedNow}
          onExploreRecommendations={mockExplore}
        />
      );

      await waitFor(() => {
        expect(screen.getByText(/No se encontraron reservas/i)).toBeInTheDocument();
      });

      const exploreBtn = screen.getByRole('button', { name: /Explorar Clases Recomendadas/i });
      fireEvent.click(exploreBtn);
      expect(mockExplore).toHaveBeenCalledTimes(1);
    });

    it('maneja errores de consulta mostrando alerta accesible y botón de reintento', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockRejectedValueOnce(
        new BookingException('NETWORK_ERROR', 'Fallo de conexión con el servidor')
      );

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument();
        expect(screen.getByText(/No fue posible cargar tus reservas/i)).toBeInTheDocument();
        expect(screen.getByText(/Fallo de conexión con el servidor/i)).toBeInTheDocument();
      });

      // Simular reintento exitoso
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValueOnce([samplePendingBooking]);
      const retryBtn = screen.getByRole('button', { name: /Reintentar Consulta/i });
      fireEvent.click(retryBtn);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });
    });
  });

  // ==========================================================================
  // 2. Renderizado de Tarjetas y Atributos (RF13 / MOD-05)
  // ==========================================================================
  describe('2. Renderizado de Tarjetas y Atributos de Reserva', () => {
    it('renderiza correctamente todos los atributos del contrato de reserva', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      expect(screen.getByText('Algoritmos y Estructuras de Datos')).toBeInTheDocument();
      expect(screen.getByText(/Tema: Grafos y Algoritmo de Dijkstra/i)).toBeInTheDocument();
      expect(screen.getByText(/Laboratorio L-02/i)).toBeInTheDocument();
      expect(screen.getByText('renzo.mentor@upt.pe')).toBeInTheDocument();
      expect(screen.getByText(/Pendiente de Ratificación/i)).toBeInTheDocument();
    });

    it('excluye reservas que pertenezcan a otros estudiantes para proteger la privacidad', async () => {
      const foreignBooking: BookingDetailResponse = {
        ...samplePendingBooking,
        id_reserva: 999,
        codigo_reserva: 'RES-OTRO-999',
        estudiante_email: 'otro.estudiante@upt.pe',
      };

      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([
        samplePendingBooking,
        foreignBooking,
      ]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      expect(screen.queryByText('RES-OTRO-999')).not.toBeInTheDocument();
    });

    it('despliega insignias correctas para estados CONFIRMADA y CANCELADA_USUARIO', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([
        sampleConfirmedBooking,
        sampleCancelledBooking,
      ]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0102')).toBeInTheDocument();
        expect(screen.getByText('RES-2026-0103')).toBeInTheDocument();
      });

      expect(screen.getByText('Asistencia Ratificada')).toBeInTheDocument();
      expect(screen.getByText('Desistimiento Voluntario')).toBeInTheDocument();
      expect(screen.getByText(/Cruce con examen parcial de Matemáticas/i)).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 3. Ventana Temporal RN-08 y Botón de Ratificación
  // ==========================================================================
  describe('3. Validación Temporal RN-08 (Corte a T-24 Horas)', () => {
    it('habilita el botón Confirmar Asistencia cuando la reserva está en PENDIENTE_CONFIRMACION y > 24h', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      const confirmBtn = screen.getByRole('button', { name: /Confirmar Asistencia/i });
      expect(confirmBtn).toBeEnabled();
    });

    it('deshabilita el botón con aviso cuando la antelación es exactamente 24 horas (límite perentorio cerrado)', async () => {
      const boundaryBooking: BookingDetailResponse = {
        ...samplePendingBooking,
        id_reserva: 104,
        codigo_reserva: 'RES-LIMITE-24H',
        fecha_inicio: sessionIn24h,
      };

      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([boundaryBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-LIMITE-24H')).toBeInTheDocument();
      });

      const disabledBtn = screen.getByRole('button', { name: /Plazo Vencido/i });
      expect(disabledBtn).toBeDisabled();
      expect(screen.getByText(/Ventana.*cerrada/i)).toBeInTheDocument();
    });

    it('deshabilita el botón cuando la antelación es menor a 24 horas (T=12h)', async () => {
      const expiredBooking: BookingDetailResponse = {
        ...samplePendingBooking,
        id_reserva: 105,
        codigo_reserva: 'RES-VENCIDA-12H',
        fecha_inicio: sessionIn12h,
      };

      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([expiredBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-VENCIDA-12H')).toBeInTheDocument();
      });

      expect(screen.getByRole('button', { name: /Plazo Vencido/i })).toBeDisabled();
      expect(screen.queryByRole('button', { name: /^✓ Confirmar Asistencia$/i })).not.toBeInTheDocument();
    });

    it('indica que la sesión ya culminó cuando fecha_inicio está en el pasado', async () => {
      const pastBooking: BookingDetailResponse = {
        ...samplePendingBooking,
        id_reserva: 106,
        codigo_reserva: 'RES-PASADA',
        fecha_inicio: sessionPast,
      };

      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([pastBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-PASADA')).toBeInTheDocument();
      });

      expect(screen.getByText(/La sesión de mentoría ya se encuentra en curso o concluida/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /Plazo Vencido/i })).toBeDisabled();
    });

    it('no muestra el botón Confirmar Asistencia para reservas ya confirmadas', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([sampleConfirmedBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0102')).toBeInTheDocument();
      });

      expect(screen.queryByRole('button', { name: /Confirmar Asistencia/i })).not.toBeInTheDocument();
      expect(screen.getByText('✓ Asistencia Confirmada')).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 4. Diálogo de Ratificación Pedagógica (T-25 / RF13 / CUS24 / PB-014 / RN-09)
  // ==========================================================================
  describe('4. Diálogo Modal de Ratificación Pedagógica', () => {
    it('abre el diálogo accesible con rol dialog y detalles formativos al pulsar Confirmar', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      const openDialogBtn = screen.getByRole('button', { name: /Confirmar Asistencia/i });
      fireEvent.click(openDialogBtn);

      const dialog = screen.getByRole('dialog');
      expect(dialog).toBeInTheDocument();
      expect(dialog).toHaveAttribute('aria-modal', 'true');
      expect(screen.getByText(/Ratificar Asistencia a Mentoría/i)).toBeInTheDocument();
      expect(screen.getByText(/Compromiso de Asistencia y Quórum/i)).toBeInTheDocument();
      expect(screen.getByText(/quórum mínimo del 50%/i)).toBeInTheDocument();
      expect(screen.getByText(/desistir voluntariamente hasta 24 horas/i)).toBeInTheDocument();
    });

    it('cierra el diálogo sin ejecutar cambios al hacer clic en Cancelar', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      const spyConfirm = vi.spyOn(bookingService, 'confirmAttendance');

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Confirmar Asistencia/i }));
      expect(screen.getByRole('dialog')).toBeInTheDocument();

      const cancelBtn = screen.getByRole('button', { name: /^Cancelar$/i });
      fireEvent.click(cancelBtn);

      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
      expect(spyConfirm).not.toHaveBeenCalled();
    });

    it('cierra el diálogo al presionar la tecla Escape (WAI-ARIA RNF05)', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Confirmar Asistencia/i }));
      expect(screen.getByRole('dialog')).toBeInTheDocument();

      act(() => {
        window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
      });

      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });

    it('ejecuta confirmAttendance con éxito, cierra el diálogo y refresca el estado a CONFIRMADA', async () => {
      bookingService.seedBooking(samplePendingBooking);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      // Abrir diálogo
      fireEvent.click(screen.getByRole('button', { name: /Confirmar Asistencia/i }));

      // Confirmar en el diálogo
      const confirmDialogBtn = screen.getByRole('button', { name: /^✓ Confirmar Asistencia$/i });
      fireEvent.click(confirmDialogBtn);

      await waitFor(() => {
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
      });

      // Notificación de éxito presente
      expect(screen.getByRole('alert')).toHaveTextContent(/¡Asistencia ratificada con éxito/i);
      // Estado mutado a confirmado
      expect(screen.getByText('Asistencia Ratificada')).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 5. Manejo de Errores y Excepciones de Negocio
  // ==========================================================================
  describe('5. Manejo de Excepciones y Casos Límite', () => {
    it('muestra aviso pedagógico cuando el backend retorna ENDPOINT_NOT_IMPLEMENTED (T-26 en progreso)', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      vi.spyOn(bookingService, 'confirmAttendance').mockRejectedValueOnce(
        new BookingException(
          'ENDPOINT_NOT_IMPLEMENTED',
          'El endpoint POST /api/v1/bookings/{id_reserva}/confirm está en desarrollo por Renzo',
          501
        )
      );

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

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
      // El diálogo permanece abierto para no perder contexto
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    it('maneja error WINDOW_CLOSED_T24H informando infracción de antelación', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      vi.spyOn(bookingService, 'confirmAttendance').mockRejectedValueOnce(
        new BookingException(
          'WINDOW_CLOSED_T24H',
          'WINDOW_CLOSED_T24H: El plazo de ratificación expiró',
          400
        )
      );

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Confirmar Asistencia/i }));
      fireEvent.click(screen.getByRole('button', { name: /^✓ Confirmar Asistencia$/i }));

      await waitFor(() => {
        expect(
          screen.getByText(/El plazo para ratificar tu asistencia cerró/i)
        ).toBeInTheDocument();
      });
    });

    it('maneja error FORBIDDEN si se intenta ratificar una reserva ajena', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      vi.spyOn(bookingService, 'confirmAttendance').mockRejectedValueOnce(
        new BookingException('FORBIDDEN', 'No autorizado', 403)
      );

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

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

    it('maneja error de red NETWORK_ERROR mostrando mensaje explicativo', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      vi.spyOn(bookingService, 'confirmAttendance').mockRejectedValueOnce(
        new BookingException('NETWORK_ERROR', 'Network offline')
      );

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Confirmar Asistencia/i }));
      fireEvent.click(screen.getByRole('button', { name: /^✓ Confirmar Asistencia$/i }));

      await waitFor(() => {
        expect(
          screen.getByText(/No fue posible contactar al servidor. Verifica tu conectividad/i)
        ).toBeInTheDocument();
      });
    });

    it('previene la doble confirmación deshabilitando el botón durante el procesamiento', async () => {
      let resolveConfirm!: (value: BookingDetailResponse) => void;
      const pendingPromise = new Promise<BookingDetailResponse>((resolve) => {
        resolveConfirm = resolve;
      });

      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      vi.spyOn(bookingService, 'confirmAttendance').mockReturnValue(pendingPromise);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Confirmar Asistencia/i }));
      const submitBtn = screen.getByRole('button', { name: /^✓ Confirmar Asistencia$/i });
      fireEvent.click(submitBtn);

      // Botón debe cambiar a texto de procesamiento y estar deshabilitado
      expect(screen.getByRole('button', { name: /Ratificando asistencia.../i })).toBeDisabled();

      // Resolver la promesa
      await act(async () => {
        resolveConfirm({ ...samplePendingBooking, estado: 'CONFIRMADA' });
      });

      await waitFor(() => {
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
      });
    });
  });

  // ==========================================================================
  // 6. Filtros y Navegación Reactiva
  // ==========================================================================
  describe('6. Filtros y Recarga de la Nómina', () => {
    it('permite alternar entre pestañas de filtrado (Todas, Por Ratificar, Ratificadas, Histórico)', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([
        samplePendingBooking,
        sampleConfirmedBooking,
        sampleCancelledBooking,
      ]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
        expect(screen.getByText('RES-2026-0102')).toBeInTheDocument();
        expect(screen.getByText('RES-2026-0103')).toBeInTheDocument();
      });

      // Filtrar solo por ratificar
      const pendientesFilterBtn = screen.getByRole('button', { name: /Por Ratificar \(1\)/i });
      fireEvent.click(pendientesFilterBtn);
      expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      expect(screen.queryByText('RES-2026-0102')).not.toBeInTheDocument();
      expect(screen.queryByText('RES-2026-0103')).not.toBeInTheDocument();

      // Filtrar solo ratificadas
      const confirmadasFilterBtn = screen.getByRole('button', { name: /Ratificadas \(1\)/i });
      fireEvent.click(confirmadasFilterBtn);
      expect(screen.queryByText('RES-2026-0101')).not.toBeInTheDocument();
      expect(screen.getByText('RES-2026-0102')).toBeInTheDocument();
      expect(screen.queryByText('RES-2026-0103')).not.toBeInTheDocument();

      // Filtrar histórico
      const historicoFilterBtn = screen.getByRole('button', { name: /Histórico \/ Otras \(1\)/i });
      fireEvent.click(historicoFilterBtn);
      expect(screen.queryByText('RES-2026-0101')).not.toBeInTheDocument();
      expect(screen.queryByText('RES-2026-0102')).not.toBeInTheDocument();
      expect(screen.getByText('RES-2026-0103')).toBeInTheDocument();
    });

    it('el botón Actualizar dispara una nueva consulta a getMyReservations', async () => {
      const spyGet = vi
        .spyOn(bookingService, 'getMyReservations')
        .mockResolvedValue([samplePendingBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      expect(spyGet).toHaveBeenCalledTimes(1);

      const refreshBtn = screen.getByRole('button', { name: /Actualizar nómina de reservas/i });
      await act(async () => {
        fireEvent.click(refreshBtn);
      });

      expect(spyGet).toHaveBeenCalledTimes(2);
    });
  });

  // ==========================================================================
  // 7. Desistimiento Voluntario de Reservas (T-27 / RF14 / CUS17 / RN-10 / PB-015)
  // ==========================================================================
  describe('7. Desistimiento Voluntario de Reservas (T-27 / RF14 / CUS17 / RN-10 / PB-015)', () => {
    it('muestra el botón Cancelar Reserva / Desistir habilitado en reserva pendiente dentro de plazo', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      const cancelBtn = screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i });
      expect(cancelBtn).toBeEnabled();
    });

    it('muestra el botón Cancelar Reserva / Desistir habilitado en reserva confirmada dentro de plazo', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([sampleConfirmedBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0102')).toBeInTheDocument();
      });

      const cancelBtn = screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i });
      expect(cancelBtn).toBeEnabled();
    });

    it('no muestra el botón de desistir en reservas ya canceladas', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([sampleCancelledBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0103')).toBeInTheDocument();
      });

      expect(screen.queryByRole('button', { name: /Cancelar Reserva \/ Desistir/i })).not.toBeInTheDocument();
      expect(screen.getByText('Reserva no activa')).toBeInTheDocument();
    });

    it('deshabilita la opción de desistir con aviso de plazo cerrado en el límite exacto de 24 horas', async () => {
      const boundaryBooking: BookingDetailResponse = {
        ...samplePendingBooking,
        id_reserva: 201,
        codigo_reserva: 'RES-BOUNDARY-24H',
        fecha_inicio: sessionIn24h,
      };

      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([boundaryBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-BOUNDARY-24H')).toBeInTheDocument();
      });

      const disabledCancelBtn = screen.getByRole('button', { name: /Desistimiento Cerrado \(Cierre 24h\)/i });
      expect(disabledCancelBtn).toBeDisabled();
    });

    it('deshabilita la opción de desistir cuando la antelación es menor a 24 horas (T=12h)', async () => {
      const lateBooking: BookingDetailResponse = {
        ...sampleConfirmedBooking,
        id_reserva: 202,
        codigo_reserva: 'RES-LATE-12H',
        fecha_inicio: sessionIn12h,
      };

      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([lateBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-LATE-12H')).toBeInTheDocument();
      });

      const disabledCancelBtn = screen.getByRole('button', { name: /Desistimiento Cerrado \(Cierre 24h\)/i });
      expect(disabledCancelBtn).toBeDisabled();
    });

    it('abre el diálogo accesible con detalles de la sesión y política RN-10 al presionar Desistir', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      const cancelBtn = screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i });
      fireEvent.click(cancelBtn);

      const dialog = screen.getByRole('dialog');
      expect(dialog).toBeInTheDocument();
      expect(dialog).toHaveAttribute('aria-modal', 'true');
      expect(screen.getByText(/Desistimiento Voluntario de Cupo/i)).toBeInTheDocument();
      expect(screen.getByText(/Política de Desistimiento y Liberación de Cupo/i)).toBeInTheDocument();
      expect(screen.getByText(/Liberación efectiva del aforo/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Motivo de desistimiento \(opcional\):/i)).toBeInTheDocument();
    });

    it('permite ingresar el motivo de cancelación respetando el límite de caracteres', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));

      const textarea = screen.getByLabelText(/Motivo de desistimiento \(opcional\):/i) as HTMLTextAreaElement;
      fireEvent.change(textarea, { target: { value: 'Cruce horario con laboratorio de Redes' } });

      expect(textarea.value).toBe('Cruce horario con laboratorio de Redes');
      expect(screen.getByText(/38 \/ 300 caracteres/i)).toBeInTheDocument();
    });

    it('cierra el diálogo sin ejecutar cancelación al presionar el botón Volver', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      const spyCancel = vi.spyOn(bookingService, 'cancelReservation');

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));
      expect(screen.getByRole('dialog')).toBeInTheDocument();

      const backBtn = screen.getByRole('button', { name: /^Volver$/i });
      fireEvent.click(backBtn);

      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
      expect(spyCancel).not.toHaveBeenCalled();
    });

    it('cierra el diálogo de desistimiento al presionar la tecla Escape', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));
      expect(screen.getByRole('dialog')).toBeInTheDocument();

      act(() => {
        window.dispatchEvent(new KeyboardEvent('keydown', { key: 'Escape' }));
      });

      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });

    it('cierra el diálogo al presionar el botón de cierre X de la cabecera', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));
      expect(screen.getByRole('dialog')).toBeInTheDocument();

      const closeBtn = screen.getByRole('button', { name: /Cerrar diálogo de desistimiento/i });
      fireEvent.click(closeBtn);

      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });

    it('ejecuta cancelReservation con éxito, cierra el diálogo, notifica y refresca a CANCELADA_USUARIO', async () => {
      bookingService.seedBooking(samplePendingBooking);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      // Abrir diálogo de desistimiento
      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));

      // Ingresar motivo
      const textarea = screen.getByLabelText(/Motivo de desistimiento \(opcional\):/i);
      fireEvent.change(textarea, { target: { value: 'Imprevisto de salud con certificado médico' } });

      // Confirmar desistimiento
      const confirmCancelBtn = screen.getByRole('button', { name: /Confirmar Desistimiento/i });
      fireEvent.click(confirmCancelBtn);

      await waitFor(() => {
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
      });

      // Notificación de éxito
      expect(screen.getByRole('alert')).toHaveTextContent(/cancelada con éxito! La vacante ha sido liberada/i);
      // Nueva insignia en la tarjeta
      expect(screen.getByText('Desistimiento Voluntario')).toBeInTheDocument();
      expect(screen.getByText(/Imprevisto de salud con certificado médico/i)).toBeInTheDocument();
    });

    it('muestra aviso pedagógico cuando el backend retorna ENDPOINT_NOT_IMPLEMENTED (T-28 en desarrollo)', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      vi.spyOn(bookingService, 'cancelReservation').mockRejectedValueOnce(
        new BookingException(
          'ENDPOINT_NOT_IMPLEMENTED',
          'El endpoint POST /api/v1/bookings/{id_reserva}/cancel está en desarrollo por Renzo',
          501
        )
      );

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));
      fireEvent.click(screen.getByRole('button', { name: /Confirmar Desistimiento/i }));

      await waitFor(() => {
        expect(
          screen.getByText(/Servicio en integración/i)
        ).toBeInTheDocument();
      });
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    it('maneja error WINDOW_CLOSED_T24H informando infracción de antelación para desistimiento', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      vi.spyOn(bookingService, 'cancelReservation').mockRejectedValueOnce(
        new BookingException('WINDOW_CLOSED_T24H', 'Plazo cerrado', 400)
      );

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));
      fireEvent.click(screen.getByRole('button', { name: /Confirmar Desistimiento/i }));

      await waitFor(() => {
        expect(
          screen.getByText(/El desistimiento voluntario solo está permitido/i)
        ).toBeInTheDocument();
      });
    });

    it('maneja error ALREADY_CANCELLED en el diálogo de desistimiento', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      vi.spyOn(bookingService, 'cancelReservation').mockRejectedValueOnce(
        new BookingException('ALREADY_CANCELLED', 'Ya cancelada', 400)
      );

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));
      fireEvent.click(screen.getByRole('button', { name: /Confirmar Desistimiento/i }));

      await waitFor(() => {
        expect(screen.getByText(/Esta reserva ya fue cancelada con anterioridad/i)).toBeInTheDocument();
      });
    });

    it('maneja error FORBIDDEN si se intenta desistir de una reserva ajena', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      vi.spyOn(bookingService, 'cancelReservation').mockRejectedValueOnce(
        new BookingException('FORBIDDEN', 'No autorizado', 403)
      );

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));
      fireEvent.click(screen.getByRole('button', { name: /Confirmar Desistimiento/i }));

      await waitFor(() => {
        expect(
          screen.getByText(/No tienes autorización para cancelar una reserva de otro estudiante/i)
        ).toBeInTheDocument();
      });
    });

    it('maneja error de red NETWORK_ERROR en desistimiento', async () => {
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      vi.spyOn(bookingService, 'cancelReservation').mockRejectedValueOnce(
        new BookingException('NETWORK_ERROR', 'Offline')
      );

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));
      fireEvent.click(screen.getByRole('button', { name: /Confirmar Desistimiento/i }));

      await waitFor(() => {
        expect(
          screen.getByText(/No fue posible contactar al servidor. Verifica tu conectividad/i)
        ).toBeInTheDocument();
      });
    });

    it('previene envíos duplicados de desistimiento deshabilitando los botones mientras procesa', async () => {
      let resolveCancel!: (value: BookingDetailResponse) => void;
      const pendingPromise = new Promise<BookingDetailResponse>((resolve) => {
        resolveCancel = resolve;
      });

      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);
      vi.spyOn(bookingService, 'cancelReservation').mockReturnValue(pendingPromise);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));
      const submitBtn = screen.getByRole('button', { name: /Confirmar Desistimiento/i });
      fireEvent.click(submitBtn);

      expect(screen.getByRole('button', { name: /Procesando desistimiento.../i })).toBeDisabled();
      expect(screen.getByRole('button', { name: /^Volver$/i })).toBeDisabled();

      await act(async () => {
        resolveCancel({
          ...samplePendingBooking,
          estado: 'CANCELADA_USUARIO',
          motivo_cancelacion: 'Cancelación procesada',
        });
      });

      await waitFor(() => {
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
      });
    });

    it('recorta espacios en blanco en el motivo antes de despachar la petición', async () => {
      const spyCancel = vi.spyOn(bookingService, 'cancelReservation').mockResolvedValue({
        ...samplePendingBooking,
        estado: 'CANCELADA_USUARIO',
        motivo_cancelacion: 'Motivo limpio',
      });
      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([samplePendingBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-2026-0101')).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i }));

      const textarea = screen.getByLabelText(/Motivo de desistimiento \(opcional\):/i);
      fireEvent.change(textarea, { target: { value: '   Motivo con espacios alrededor   ' } });

      fireEvent.click(screen.getByRole('button', { name: /Confirmar Desistimiento/i }));

      await waitFor(() => {
        expect(spyCancel).toHaveBeenCalledWith(
          samplePendingBooking.id_reserva,
          'Motivo con espacios alrededor',
          studentEmail
        );
      });
    });

    it('permite desistir con 25 horas de anticipación (caso de borde positivo de RN-10)', async () => {
      const sessionIn25h = new Date(fixedNow + 25 * 3600 * 1000).toISOString();
      const nearBooking: BookingDetailResponse = {
        ...samplePendingBooking,
        id_reserva: 205,
        codigo_reserva: 'RES-NEAR-25H',
        fecha_inicio: sessionIn25h,
      };

      vi.spyOn(bookingService, 'getMyReservations').mockResolvedValue([nearBooking]);

      render(<StudentBookingsView studentEmail={studentEmail} currentTime={fixedNow} />);

      await waitFor(() => {
        expect(screen.getByText('RES-NEAR-25H')).toBeInTheDocument();
      });

      // Con 25 horas, el botón de desistimiento debe estar habilitado
      const cancelBtn = screen.getByRole('button', { name: /Cancelar Reserva \/ Desistir/i });
      expect(cancelBtn).toBeEnabled();
    });
  });
});
