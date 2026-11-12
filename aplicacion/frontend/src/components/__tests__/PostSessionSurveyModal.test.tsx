import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { PostSessionSurveyModal } from '../PostSessionSurveyModal';
import { surveyService } from '../../services/surveyService';

describe('PostSessionSurveyModal Component (T-38 / PB-020 / RF18 / RN-12 / RN-13 / RNF05)', () => {
  const sessionId = 14;
  const sessionTitle = 'Estructuras de Datos y Algoritmos en C++';
  const mentorName = 'mentor.sistemas@upt.pe';

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('1. Bloqueo por inasistencia (RN-12): oculta el formulario si el estudiante fue marcado como inasistente', () => {
    render(
      <PostSessionSurveyModal
        isOpen={true}
        onClose={vi.fn()}
        sessionId={sessionId}
        sessionTitle={sessionTitle}
        mentorName={mentorName}
        asistenciaConfirmada={false}
      />
    );

    expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
  });

  it('2. Cierre por ventana 24h (RN-13): despliega alerta de expiración cuando la sesión concluyó hace más de 24 horas', () => {
    const fixedNow = new Date('2026-11-10T12:00:00Z').getTime();
    // Sesión concluida hace 26 horas
    const sessionEndDate = new Date(fixedNow - 26 * 3600 * 1000).toISOString();

    render(
      <PostSessionSurveyModal
        isOpen={true}
        onClose={vi.fn()}
        sessionId={sessionId}
        sessionTitle={sessionTitle}
        mentorName={mentorName}
        sessionEndDate={sessionEndDate}
        currentTime={fixedNow}
        asistenciaConfirmada={true}
      />
    );

    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText(/Plazo de 24h Vencido/i)).toBeInTheDocument();

    const submitBtn = screen.getByRole('button', { name: /Enviar Evaluación/i });
    expect(submitBtn).toBeDisabled();
  });

  it('3. Validación Likert y longitud de texto: bloquea botón de envío hasta seleccionar estrellas e ingresar >= 20 caracteres', () => {
    const fixedNow = new Date('2026-11-10T12:00:00Z').getTime();
    // Sesión concluida hace 2 horas (dentro de 24h)
    const sessionEndDate = new Date(fixedNow - 2 * 3600 * 1000).toISOString();

    render(
      <PostSessionSurveyModal
        isOpen={true}
        onClose={vi.fn()}
        sessionId={sessionId}
        sessionTitle={sessionTitle}
        mentorName={mentorName}
        sessionEndDate={sessionEndDate}
        currentTime={fixedNow}
        asistenciaConfirmada={true}
      />
    );

    const submitBtn = screen.getByRole('button', { name: /Enviar Evaluación/i });
    expect(submitBtn).toBeDisabled();

    // Seleccionar estrellas para las 4 dimensiones (puntualidad, dominio, claridad, general)
    const star5Buttons = screen.getAllByRole('button', { name: /Calificar con 5 estrellas/i });
    expect(star5Buttons.length).toBeGreaterThanOrEqual(4);
    star5Buttons.forEach((btn) => fireEvent.click(btn));

    // El botón sigue deshabilitado porque falta retroalimentación >= 20 caracteres
    expect(submitBtn).toBeDisabled();

    // Ingresar texto breve (< 20 chars)
    const textarea = screen.getByPlaceholderText(/Detalla aspectos pedagógicos relevantes/i);
    fireEvent.change(textarea, { target: { value: 'Texto breve' } });
    expect(submitBtn).toBeDisabled();

    // Ingresar texto válido (>= 20 chars)
    fireEvent.change(textarea, {
      target: {
        value: 'Excelente sesión, el mentor explicó con suma claridad y resolvió todas las dudas.',
      },
    });

    // Ahora debe habilitarse
    expect(submitBtn).toBeEnabled();
  });

  it('4. Envío asíncrono y feedback de éxito: despacha payload completo a API y muestra banner accesible de agradecimiento', async () => {
    const fixedNow = new Date('2026-11-10T12:00:00Z').getTime();
    const sessionEndDate = new Date(fixedNow - 2 * 3600 * 1000).toISOString();
    const onSurveySubmittedMock = vi.fn();

    const submitSpy = vi.spyOn(surveyService, 'submitSurvey').mockResolvedValue({
      id_encuesta: 101,
      id_sesion: sessionId,
      estudiante_email: '2022074255@upt.pe',
      calificacion_general: 5,
      dominio_tema: 5,
      claridad_explicacion: 5,
      puntualidad: 5,
      comentarios: 'Excelente sesión de punteros en C++, muy recomendado para todos los compañeros.',
      created_at: new Date(fixedNow).toISOString(),
      mensaje: 'Evaluación de calidad post-mentoría registrada con éxito.',
    });

    render(
      <PostSessionSurveyModal
        isOpen={true}
        onClose={vi.fn()}
        sessionId={sessionId}
        sessionTitle={sessionTitle}
        mentorName={mentorName}
        sessionEndDate={sessionEndDate}
        currentTime={fixedNow}
        asistenciaConfirmada={true}
        onSurveySubmitted={onSurveySubmittedMock}
      />
    );

    // Calificar con 5 estrellas en las dimensiones
    const starButtons = screen.getAllByRole('button', { name: /Calificar con 5 estrellas/i });
    starButtons.forEach((btn) => fireEvent.click(btn));

    // Llenar comentarios
    const textarea = screen.getByPlaceholderText(/Detalla aspectos pedagógicos relevantes/i);
    fireEvent.change(textarea, {
      target: {
        value: 'Excelente sesión de punteros en C++, muy recomendado para todos los compañeros.',
      },
    });

    const submitBtn = screen.getByRole('button', { name: /Enviar Evaluación/i });
    expect(submitBtn).toBeEnabled();
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(submitSpy).toHaveBeenCalledWith(
        sessionId,
        expect.objectContaining({
          calificacion_general: 5,
          dominio_tema: 5,
          claridad_explicacion: 5,
          puntualidad: 5,
          comentarios: 'Excelente sesión de punteros en C++, muy recomendado para todos los compañeros.',
        })
      );
      expect(screen.getByText(/¡Gracias por tu Evaluación!/i)).toBeInTheDocument();
      expect(onSurveySubmittedMock).toHaveBeenCalled();
    });
  });

  it('5. Accesibilidad WAI-ARIA (RNF05): cierra el diálogo modal al presionar la tecla Escape', () => {
    const onCloseMock = vi.fn();
    render(
      <PostSessionSurveyModal
        isOpen={true}
        onClose={onCloseMock}
        sessionId={sessionId}
        sessionTitle={sessionTitle}
        mentorName={mentorName}
        asistenciaConfirmada={true}
      />
    );

    expect(screen.getByRole('dialog')).toBeInTheDocument();
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(onCloseMock).toHaveBeenCalled();
  });

  it('6. Accesibilidad (WCAG 2.1 AA): soporta navegación por teclado para calificar estrellas', () => {
    render(
      <PostSessionSurveyModal
        isOpen={true}
        onClose={vi.fn()}
        sessionId={sessionId}
        sessionTitle={sessionTitle}
        mentorName={mentorName}
        asistenciaConfirmada={true}
      />
    );

    const firstStarBtn = screen.getAllByRole('button', { name: /Calificar con 3 estrellas/i })[0];
    fireEvent.keyDown(firstStarBtn, { key: 'ArrowRight' });
    // Al pulsar ArrowRight desde 3, sube a 4
    expect(screen.getByText('4/5')).toBeInTheDocument();
  });
});
