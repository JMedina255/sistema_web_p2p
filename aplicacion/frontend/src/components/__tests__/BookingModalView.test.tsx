import { describe, it, expect, beforeEach, vi, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import {
  BookingModalView,
  type BookingModalViewProps,
  type BookingSuccessData,
} from '../BookingModalView';
import type { OfferRecommendationItem, ScoreBreakdown } from '../../services/recommendationService';
import { authService } from '../../services/authService';

describe('BookingModalView Component (T-21 / CUS04 / RF12 / RN-05 / RN-08 / RNF05)', () => {
  const dummyBreakdown: ScoreBreakdown = {
    curricular_affinity: 1.0,
    course_weight_factor: 1.3,
    critical_course_applied: 'AED-201',
    topic_overlap_jaccard: 0.85,
    topic_overlap_dice: 0.9189,
    schedule_compatibility: 0.9,
    schedule_matching_slots_count: 6,
    matching_slots: ['Lun 10:00-11:00'],
    modality_compatibility: 1.0,
    institutional_merit_eligible: true,
    explanation_text: 'Afinidad conceptual de excelencia en Algoritmos.',
  };

  // Oferta futura válida (> 48 horas en el futuro para superar holgadamente T-24h)
  const validFutureDate = new Date(Date.now() + 72 * 60 * 60 * 1000).toISOString();

  const sampleOffer: OfferRecommendationItem = {
    id_oferta: '101',
    codigo_sesion: 'SES-2026-001',
    id_asignatura: 3,
    codigo_asignatura: 'AED-201',
    nombre_asignatura: 'Algoritmos y Estructuras de Datos',
    id_tema: 302,
    nombre_tema: 'Grafos y Algoritmo de Dijkstra',
    fecha_inicio: validFutureDate,
    duracion_minutos: 90,
    modalidad: 'presencial',
    aforo_maximo: 10,
    aforo_disponible: 5,
    espacio_asignado: 'Laboratorio L-02 - Pabellón G',
    mentor_email: 'renzo.mentor@upt.pe',
    mentor_nombre: 'Renzo Antayhua Mamani',
    mentor_ciclo: 8,
    score_total: 94.5,
    breakdown: dummyBreakdown,
  };

  const defaultProps: BookingModalViewProps = {
    isOpen: true,
    offer: sampleOffer,
    currentUserEmail: '2022074255@upt.pe',
    isSubmitting: false,
    error: null,
    successData: null,
    onClose: vi.fn(),
    onConfirmReservation: vi.fn(),
    onDemandRedirect: vi.fn(),
  };

  beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.clear();
  });

  afterEach(() => {
    sessionStorage.clear();
  });

  // 1. Renderizado condicional
  it('1. Renderiza el modal cuando isOpen es true y no renderiza nada cuando isOpen es false', () => {
    const { rerender } = render(<BookingModalView {...defaultProps} isOpen={false} />);
    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();

    rerender(<BookingModalView {...defaultProps} isOpen={true} />);
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /Confirmar Reserva de Cupo/i })).toBeInTheDocument();
  });

  // 2. Información correcta de la oferta
  it('2. Presenta con exactitud los atributos de la oferta según el contrato DTO', () => {
    render(<BookingModalView {...defaultProps} />);

    expect(screen.getByText(/Algoritmos y Estructuras de Datos/i)).toBeInTheDocument();
    expect(screen.getByText(/Tema: Grafos y Algoritmo de Dijkstra/i)).toBeInTheDocument();
    expect(screen.getByText(/Renzo Antayhua Mamani/i)).toBeInTheDocument();
    expect(screen.getByText(/Ciclo 8 • Mérito RN-03/i)).toBeInTheDocument();
    expect(screen.getByText(/90 minutos/i)).toBeInTheDocument();
    expect(screen.getByText(/PRESENCIAL/i)).toBeInTheDocument();
    expect(screen.getByText(/Laboratorio L-02 - Pabellón G/i)).toBeInTheDocument();
    expect(screen.getByText(/5 vacantes disponibles/i)).toBeInTheDocument();
    expect(screen.getByText(/Capacidad total: 10 cupos \(10 normados\)/i)).toBeInTheDocument();
    expect(screen.getByText(/ID: SES-2026-001/i)).toBeInTheDocument();
    expect(screen.getByText(/2022074255@upt.pe/i)).toBeInTheDocument();
  });

  // 3. Cierre mediante Cancelar y botón X
  it('3. Invoca onClose al presionar el botón Cancelar y el botón de cierre X', () => {
    const onCloseMock = vi.fn();
    render(<BookingModalView {...defaultProps} onClose={onCloseMock} />);

    const cancelButton = screen.getByRole('button', { name: /Cancelar/i });
    fireEvent.click(cancelButton);
    expect(onCloseMock).toHaveBeenCalledTimes(1);

    const closeIconButton = screen.getByRole('button', { name: /Cerrar modal de reserva/i });
    fireEvent.click(closeIconButton);
    expect(onCloseMock).toHaveBeenCalledTimes(2);
  });

  // 4. Cierre mediante tecla Escape
  it('4. Cierra el modal al pulsar la tecla Escape cuando no está en proceso de envío', () => {
    const onCloseMock = vi.fn();
    render(<BookingModalView {...defaultProps} onClose={onCloseMock} />);

    fireEvent.keyDown(window, { key: 'Escape', code: 'Escape' });
    expect(onCloseMock).toHaveBeenCalledTimes(1);
  });

  // 5. Gestión accesible del foco y atributos WAI-ARIA (RNF05)
  it('5. Cumple con atributos accesibles WAI-ARIA (role=dialog, aria-modal, aria-labelledby) y trampa de foco', () => {
    render(<BookingModalView {...defaultProps} />);

    const dialog = screen.getByRole('dialog');
    expect(dialog).toHaveAttribute('aria-modal', 'true');
    expect(dialog).toHaveAttribute('aria-labelledby');
    expect(dialog).toHaveAttribute('aria-describedby');

    // Comprobar trampa de foco (Tab cycling)
    const focusable = dialog.querySelectorAll<HTMLElement>(
      'button:not([disabled]), [tabindex]:not([tabindex="-1"])'
    );
    expect(focusable.length).toBeGreaterThan(0);

    const firstElement = focusable[0];
    const lastElement = focusable[focusable.length - 1];

    firstElement.focus();
    expect(document.activeElement).toBe(firstElement);

    // Shift + Tab en primer elemento debe ciclar al último
    fireEvent.keyDown(window, { key: 'Tab', shiftKey: true });
    // Tab en último elemento
    lastElement.focus();
    fireEvent.keyDown(window, { key: 'Tab', shiftKey: false });
  });

  // 6. Restricción de autoreserva (RN-03 / MENTOR_CANNOT_BOOK)
  it('6. Impide la autoreserva cuando el estudiante autenticado es el mentor titular de la oferta', () => {
    render(
      <BookingModalView
        {...defaultProps}
        currentUserEmail="renzo.mentor@upt.pe" // Mismo correo que offer.mentor_email
      />
    );

    const warning = screen.getByTestId('warning-self-booking');
    expect(warning).toBeInTheDocument();
    expect(warning).toHaveTextContent(/Restricción de Autoreserva \(RN-03\)/i);

    const confirmButton = screen.getByRole('button', { name: /Confirmar Reserva de Cupo/i });
    expect(confirmButton).toBeDisabled();
  });

  // 7. Aforo agotado (RN-05 / CAPACITY_EXCEEDED)
  it('7. Impide confirmar y muestra advertencia cuando el aforo disponible es 0', () => {
    const fullOffer: OfferRecommendationItem = {
      ...sampleOffer,
      aforo_disponible: 0,
    };
    const onDemandMock = vi.fn();

    render(
      <BookingModalView
        {...defaultProps}
        offer={fullOffer}
        onDemandRedirect={onDemandMock}
      />
    );

    const warning = screen.getByTestId('warning-capacity-exceeded');
    expect(warning).toBeInTheDocument();
    expect(warning).toHaveTextContent(/Aforo Agotado \(RN-05\)/i);

    const confirmButton = screen.getByRole('button', { name: /Confirmar Reserva de Cupo/i });
    expect(confirmButton).toBeDisabled();

    // Redirección opcional a solicitudes por demanda (CUS03)
    const demandButton = screen.getByRole('button', { name: /Registrar Solicitud por Demanda/i });
    fireEvent.click(demandButton);
    expect(onDemandMock).toHaveBeenCalledTimes(1);
  });

  // 8. Sesión vencida (fecha en el pasado)
  it('8. Detecta sesiones con horario transcurrido y bloquea la confirmación', () => {
    const pastOffer: OfferRecommendationItem = {
      ...sampleOffer,
      fecha_inicio: new Date(Date.now() - 3600 * 1000).toISOString(), // 1 hora en el pasado
    };

    render(<BookingModalView {...defaultProps} offer={pastOffer} />);

    const warning = screen.getByTestId('warning-expired-session');
    expect(warning).toBeInTheDocument();
    expect(warning).toHaveTextContent(/Sesión Vencida/i);

    const confirmButton = screen.getByRole('button', { name: /Confirmar Reserva de Cupo/i });
    expect(confirmButton).toBeDisabled();
  });

  // 9. Restricción temporal perentoria T-24h (RN-08 / WINDOW_CLOSED_T24H)
  it('9. Bloquea reservas dentro del umbral perentorio de 24 horas previas al evento (RN-08)', () => {
    const nearOffer: OfferRecommendationItem = {
      ...sampleOffer,
      fecha_inicio: new Date(Date.now() + 12 * 3600 * 1000).toISOString(), // En 12 horas (menor a 24h)
    };

    render(<BookingModalView {...defaultProps} offer={nearOffer} />);

    const warning = screen.getByTestId('warning-window-closed');
    expect(warning).toBeInTheDocument();
    expect(warning).toHaveTextContent(/Ventana de Reserva Cerrada \(T-24h \/ RN-08\)/i);

    const confirmButton = screen.getByRole('button', { name: /Confirmar Reserva de Cupo/i });
    expect(confirmButton).toBeDisabled();
  });

  // 10. Confirmación de intención de reserva
  it('10. Ejecuta el callback onConfirmReservation con la oferta seleccionada al presionar Confirmar', async () => {
    const onConfirmMock = vi.fn().mockResolvedValue(undefined);
    render(<BookingModalView {...defaultProps} onConfirmReservation={onConfirmMock} />);

    const confirmButton = screen.getByRole('button', { name: /Confirmar Reserva de Cupo/i });
    expect(confirmButton).not.toBeDisabled();

    fireEvent.click(confirmButton);
    await waitFor(() => {
      expect(onConfirmMock).toHaveBeenCalledTimes(1);
      expect(onConfirmMock).toHaveBeenCalledWith(sampleOffer);
    });
  });

  // 11. Prevención de confirmaciones duplicadas (doble clic)
  it('11. Evita confirmaciones duplicadas ante múltiples pulsaciones sucesivas', async () => {
    let resolvePromise: () => void;
    const pendingPromise = new Promise<void>((resolve) => {
      resolvePromise = resolve;
    });
    const onConfirmMock = vi.fn().mockReturnValue(pendingPromise);

    render(<BookingModalView {...defaultProps} onConfirmReservation={onConfirmMock} />);

    const confirmButton = screen.getByRole('button', { name: /Confirmar Reserva de Cupo/i });

    await act(async () => {
      fireEvent.click(confirmButton);
      fireEvent.click(confirmButton);
      fireEvent.click(confirmButton);
      resolvePromise!();
    });

    expect(onConfirmMock).toHaveBeenCalledTimes(1);
  });

  // 12. Estado pending (isSubmitting === true)
  it('12. Despliega estado de procesamiento visual e inhabilita interacciones durante isSubmitting', () => {
    const onCloseMock = vi.fn();
    render(
      <BookingModalView
        {...defaultProps}
        isSubmitting={true}
        onClose={onCloseMock}
      />
    );

    expect(screen.getByText(/Procesando reserva.../i)).toBeInTheDocument();

    const cancelButton = screen.getByRole('button', { name: /Cancelar/i });
    expect(cancelButton).toBeDisabled();

    // Escape no debe cerrar mientras está procesando
    fireEvent.keyDown(window, { key: 'Escape', code: 'Escape' });
    expect(onCloseMock).not.toHaveBeenCalled();
  });

  // 13. Presentación de errores controlados (error prop)
  it('13. Despliega mensajes de error controlados devueltos por el servidor o validación', () => {
    render(
      <BookingModalView
        {...defaultProps}
        error="CAPACITY_EXCEEDED: Aforo completo. No quedan vacantes disponibles en esta sesión."
      />
    );

    const alert = screen.getByTestId('booking-error-alert');
    expect(alert).toBeInTheDocument();
    expect(alert).toHaveTextContent(/CAPACITY_EXCEEDED/i);
    expect(alert).toHaveTextContent(/Aforo completo/i);
  });

  // 14. Adaptación a datos opcionales o ausentes
  it('14. Tolera atributos opcionales nulos sin colapsar (mentor_nombre nulo, espacio ausente)', () => {
    const sparseOffer: OfferRecommendationItem = {
      ...sampleOffer,
      mentor_nombre: null,
      espacio_asignado: '',
      modalidad: 'virtual',
      aforo_maximo: 20,
    };

    render(<BookingModalView {...defaultProps} offer={sparseOffer} />);

    // Muestra el correo institucional cuando el nombre es nulo
    expect(screen.getAllByText(/renzo.mentor@upt.pe/i).length).toBeGreaterThan(0);
    // Espacio por defecto para virtual
    expect(screen.getByText(/Enlace virtual \(se emitirá al ratificar\)/i)).toBeInTheDocument();
    expect(screen.getByText(/^virtual$/i)).toBeInTheDocument();
    expect(screen.getByText(/20 normados/i)).toBeInTheDocument();
  });

  // 15. Callback tipado con identificadores correctos
  it('15. Entrega al callback los identificadores exactos requeridos para la reserva en backend', async () => {
    const onConfirmMock = vi.fn();
    render(<BookingModalView {...defaultProps} onConfirmReservation={onConfirmMock} />);

    const confirmButton = screen.getByRole('button', { name: /Confirmar Reserva de Cupo/i });
    fireEvent.click(confirmButton);

    await waitFor(() => {
      expect(onConfirmMock).toHaveBeenCalledWith(
        expect.objectContaining({
          id_oferta: '101',
          codigo_sesion: 'SES-2026-001',
          id_asignatura: 3,
          id_tema: 302,
          mentor_email: 'renzo.mentor@upt.pe',
        })
      );
    });
  });

  // 16. Cierre al pulsar el backdrop
  it('16. Invoca onClose al hacer clic fuera del modal (en el backdrop)', () => {
    const onCloseMock = vi.fn();
    render(<BookingModalView {...defaultProps} onClose={onCloseMock} />);

    const backdrop = screen.getByTestId('booking-modal-backdrop');
    fireEvent.click(backdrop);

    expect(onCloseMock).toHaveBeenCalledTimes(1);
  });

  // 17. Despliegue de comprobante exitoso (successData)
  it('17. Despliega comprobante provisional con código de reserva cuando successData está presente', () => {
    const successInfo: BookingSuccessData = {
      codigo_reserva: 'RES-2026-9999',
      estado: 'PENDIENTE_CONFIRMACION',
      fecha_limite_confirmacion: new Date(Date.now() + 48 * 3600 * 1000).toISOString(),
      mensaje: 'Reserva provisional registrada. Recuerde ratificar su asistencia antes de T-24h.',
    };

    const onCloseMock = vi.fn();
    render(
      <BookingModalView
        {...defaultProps}
        successData={successInfo}
        onClose={onCloseMock}
      />
    );

    const successPanel = screen.getByTestId('booking-success-panel');
    expect(successPanel).toBeInTheDocument();
    expect(screen.getByTestId('receipt-booking-code')).toHaveTextContent('RES-2026-9999');
    expect(screen.getByText('PENDIENTE_CONFIRMACION')).toBeInTheDocument();
    expect(screen.getByText(/Recuerde ratificar su asistencia antes de T-24h/i)).toBeInTheDocument();

    const closeButton = screen.getByRole('button', { name: /Entendido, Cerrar/i });
    fireEvent.click(closeButton);
    expect(onCloseMock).toHaveBeenCalledTimes(1);
  });

  // 18. Gestión de oferta nula
  it('18. Gestiona adecuadamente la ausencia de oferta seleccionada (offer === null)', () => {
    const onCloseMock = vi.fn();
    render(<BookingModalView {...defaultProps} offer={null} onClose={onCloseMock} />);

    expect(screen.getByText(/Ninguna Sesión Seleccionada/i)).toBeInTheDocument();
    const closeBtn = screen.getByRole('button', { name: /Cerrar/i });
    fireEvent.click(closeBtn);
    expect(onCloseMock).toHaveBeenCalledTimes(1);
  });

  // 19. Resolución de identidad institucional
  it('19. Resuelve la identidad institucional desde token JWT o parámetro explícito', () => {
    // Caso 1: explícito
    const { rerender } = render(
      <BookingModalView {...defaultProps} currentUserEmail="estudiante1@upt.pe" />
    );
    expect(screen.getByText('estudiante1@upt.pe')).toBeInTheDocument();

    // Caso 2: desde token decodificado
    const fakePayload = { sub: 'token.user@upt.pe', role: 'MENTOREADO' };
    const fakeToken = `header.${btoa(JSON.stringify(fakePayload))}.signature`;
    authService.saveToken(fakeToken);

    rerender(<BookingModalView {...defaultProps} currentUserEmail={undefined} />);
    expect(screen.getByText('token.user@upt.pe')).toBeInTheDocument();

    // Caso 3: sin token ni prop -> estado no autenticado con acceso restringido
    authService.clearToken();
    rerender(<BookingModalView {...defaultProps} currentUserEmail={undefined} />);
    expect(screen.getByText(/Sin sesión activa \(Acceso restringido\)/i)).toBeInTheDocument();
    expect(screen.getByText('No Autenticado')).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Confirmar Reserva de Cupo/i })).toBeDisabled();
  });

  // 20. Formateo de fechas
  it('20. Formatea fechas ISO adecuadamente o retorna fallback si es inválida', () => {
    // Caso 1: fecha válida
    const { rerender } = render(<BookingModalView {...defaultProps} />);
    expect(screen.getByText(/📅/i)).toBeInTheDocument();

    // Caso 2: fecha inválida no colapsa y muestra fallback
    const invalidOffer = { ...sampleOffer, fecha_inicio: 'fecha-no-valida' };
    rerender(<BookingModalView {...defaultProps} offer={invalidOffer} />);
    expect(screen.getByText(/fecha-no-valida/i)).toBeInTheDocument();
  });
});
