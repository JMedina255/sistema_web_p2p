import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MentorSessionsView } from '../MentorSessionsView';
import { offerService, type PublishOfferResponse } from '../../services/offerService';

describe('MentorSessionsView Component (T-32 / RF16 / CUS07 / RN-04 / RN-10 / WCAG 2.1 AA)', () => {
  const mentorEmail = 'mentor.avanzado@upt.pe';

  const mockSessionInsufficient: PublishOfferResponse = {
    id_oferta: '101',
    codigo_sesion: 'SES-0101',
    estado: 'QUORUM_INSUFICIENTE',
    mensaje: 'Sesión con quórum insuficiente en T-24h',
    fecha_publicacion: new Date().toISOString(),
    espacio_asignado: 'Lab 101',
    modo: 'api',
    aforo: 10,
    offer: {
      id_asignatura: 1,
      codigo_asignatura: 'CALC-101',
      nombre_asignatura: 'Cálculo I',
      id_tema: 1,
      nombre_tema: 'Límites y Continuidad',
      fecha_inicio: new Date(Date.now() + 12 * 3600 * 1000).toISOString(), // Restan 12h (T-24h superado)
      duracion_minutos: 60,
      modalidad: 'presencial',
      aforo_maximo: 10,
      espacio_asignado: 'Lab 101',
      mentor_email: mentorEmail,
    },
  };

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  // 1. Renderiza estado vacío cuando no hay sesiones del mentor
  it('1. Renderiza estado vacío cuando no hay sesiones del mentor y permite navegar a publicar', async () => {
    vi.spyOn(offerService, 'getOffers').mockResolvedValue([]);
    const onPublish = vi.fn();

    render(
      <MentorSessionsView
        mentorEmail={mentorEmail}
        onNavigateToPublish={onPublish}
      />
    );

    await waitFor(() => {
      expect(screen.getByText(/No tienes sesiones de mentoría publicadas actualmente/i)).toBeInTheDocument();
    });

    const publishBtn = screen.getByRole('button', { name: /Publicar Mi Primera Sesión/i });
    fireEvent.click(publishBtn);
    expect(onPublish).toHaveBeenCalledTimes(1);
  });

  // 2. Despliega distintivo ámbar en sesión con quórum insuficiente
  it('2. Despliega distintivo ámbar en sesión con quórum insuficiente (< 3 alumnos confirmados)', async () => {
    vi.spyOn(offerService, 'getOffers').mockResolvedValue([mockSessionInsufficient]);

    render(<MentorSessionsView mentorEmail={mentorEmail} />);

    await waitFor(() => {
      expect(screen.getByText(/Quórum Insuficiente/i)).toBeInTheDocument();
      expect(screen.getByText('Cálculo I')).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /⚡ Resolver Contingencia/i })).toBeInTheDocument();
    });
  });

  // 3. Abre modal de contingencia y permite elegir "Dictar de Todas Formas"
  it('3. Abre modal de contingencia y permite elegir "Dictar de Todas Formas" (PROCEED)', async () => {
    vi.spyOn(offerService, 'getOffers').mockResolvedValue([mockSessionInsufficient]);
    const resolveSpy = vi.spyOn(offerService, 'resolveQuorum').mockResolvedValue({
      id_sesion: 101,
      codigo_sesion: 'SES-0101',
      decision: 'PROCEED',
      estado_nuevo: 'CONFIRMADA',
      nueva_fecha_inicio: null,
      mensaje: 'Resolución registrada exitosamente. La sesión se dictará con aforo reducido.',
    });

    render(<MentorSessionsView mentorEmail={mentorEmail} />);

    const contingencyBtn = await screen.findByRole('button', { name: /⚡ Resolver Contingencia/i });
    fireEvent.click(contingencyBtn);

    // Modal accesible abierto
    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText(/⚡ Resolución de Quórum Insuficiente/i)).toBeInTheDocument();

    // Opción PROCEED seleccionada por defecto
    const confirmBtn = screen.getByRole('button', { name: /Confirmar Decisión/i });
    fireEvent.click(confirmBtn);

    await waitFor(() => {
      expect(resolveSpy).toHaveBeenCalledWith('101', {
        decision: 'PROCEED',
        new_start_time: undefined,
        reason: undefined,
      });
      expect(screen.getByText(/Resolución registrada exitosamente/i)).toBeInTheDocument();
    });
  });

  // 4. Valida nueva fecha > 24h al seleccionar "Reprogramar"
  it('4. Valida nueva fecha > 24h al seleccionar "Reprogramar" (RN-04)', async () => {
    vi.spyOn(offerService, 'getOffers').mockResolvedValue([mockSessionInsufficient]);
    const resolveSpy = vi.spyOn(offerService, 'resolveQuorum');

    render(<MentorSessionsView mentorEmail={mentorEmail} />);

    const contingencyBtn = await screen.findByRole('button', { name: /⚡ Resolver Contingencia/i });
    fireEvent.click(contingencyBtn);

    // Cambiar a opción RESCHEDULE
    const radioReschedule = screen.getByDisplayValue('RESCHEDULE');
    fireEvent.click(radioReschedule);

    // Caso A: Intentar enviar sin fecha
    const confirmBtn = screen.getByRole('button', { name: /Confirmar Decisión/i });
    fireEvent.click(confirmBtn);
    expect(screen.getByText(/Debe ingresar una nueva fecha y hora para la mentoría/i)).toBeInTheDocument();
    expect(resolveSpy).not.toHaveBeenCalled();

    // Caso B: Ingresar fecha con menos de 24h de antelación (< 24h)
    const invalidDate = new Date(Date.now() + 10 * 3600 * 1000).toISOString().slice(0, 16);
    const dateInput = screen.getByLabelText(/Nueva Fecha y Hora/i);
    fireEvent.change(dateInput, { target: { value: invalidDate } });
    fireEvent.click(confirmBtn);
    expect(screen.getByText(/La reprogramación exige una antelación mayor a 24 horas/i)).toBeInTheDocument();
    expect(resolveSpy).not.toHaveBeenCalled();

    // Caso C: Ingresar fecha válida (> 24h)
    const validDate = new Date(Date.now() + 48 * 3600 * 1000).toISOString().slice(0, 16);
    fireEvent.change(dateInput, { target: { value: validDate } });

    resolveSpy.mockResolvedValue({
      id_sesion: 101,
      codigo_sesion: 'SES-0101',
      decision: 'RESCHEDULE',
      estado_nuevo: 'PUBLICADA',
      nueva_fecha_inicio: new Date(validDate).toISOString(),
      mensaje: 'Sesión reprogramada exitosamente.',
    });

    fireEvent.click(confirmBtn);
    await waitFor(() => {
      expect(resolveSpy).toHaveBeenCalledWith('101', expect.objectContaining({
        decision: 'RESCHEDULE',
      }));
    });
  });

  // 5. Exige justificación de texto al seleccionar "Cancelar Sesión"
  it('5. Exige justificación de texto obligatoria al seleccionar "Cancelar Sesión" (RN-10)', async () => {
    vi.spyOn(offerService, 'getOffers').mockResolvedValue([mockSessionInsufficient]);
    const resolveSpy = vi.spyOn(offerService, 'resolveQuorum');

    render(<MentorSessionsView mentorEmail={mentorEmail} />);

    const contingencyBtn = await screen.findByRole('button', { name: /⚡ Resolver Contingencia/i });
    fireEvent.click(contingencyBtn);

    // Seleccionar opción CANCEL
    const radioCancel = screen.getByDisplayValue('CANCEL');
    fireEvent.click(radioCancel);

    // Caso A: Enviar sin motivo
    const confirmBtn = screen.getByRole('button', { name: /Confirmar Decisión/i });
    fireEvent.click(confirmBtn);
    expect(screen.getByText(/Debe ingresar obligatoriamente una justificación académica de cancelación/i)).toBeInTheDocument();
    expect(resolveSpy).not.toHaveBeenCalled();

    // Caso B: Ingresar motivo y confirmar cancelación
    const reasonTextarea = screen.getByLabelText(/Motivo de Cancelación/i);
    fireEvent.change(reasonTextarea, {
      target: { value: 'Inasistencia imprevista y cruce con evaluación de cátedra institucional.' },
    });

    resolveSpy.mockResolvedValue({
      id_sesion: 101,
      codigo_sesion: 'SES-0101',
      decision: 'CANCEL',
      estado_nuevo: 'CANCELADA_QUORUM',
      nueva_fecha_inicio: null,
      mensaje: 'Sesión cancelada formalmente.',
    });

    fireEvent.click(confirmBtn);
    await waitFor(() => {
      expect(resolveSpy).toHaveBeenCalledWith('101', {
        decision: 'CANCEL',
        new_start_time: undefined,
        reason: 'Inasistencia imprevista y cruce con evaluación de cátedra institucional.',
      });
    });
  });
});
