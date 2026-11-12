import { describe, it, expect, beforeEach, vi } from 'vitest';
import { surveyService } from '../surveyService';
import { authService } from '../authService';

describe('surveyService (T-38 / T-39 / RF18 / RN-12 / RN-13)', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('1. Envía encuesta exitosamente en modo mock', async () => {
    vi.spyOn(authService, 'getCurrentUser').mockReturnValue({
      email: '2022074255@upt.pe',
    });

    const payload = {
      calificacion_general: 5,
      dominio_tema: 4,
      claridad_explicacion: 5,
      puntualidad: 5,
      comentarios: 'Excelente metodología y explicaciones claras sobre punteros y memoria.',
    };

    const res = await surveyService.submitSurvey(201, payload);
    expect(res.id_sesion).toBe(201);
    expect(res.calificacion_general).toBe(5);
    expect(res.comentarios).toBe(payload.comentarios);
  });

  it('2. Rechaza envío con comentarios cualitativos menores a 20 caracteres', async () => {
    vi.spyOn(authService, 'getCurrentUser').mockReturnValue({
      email: '2022074255@upt.pe',
    });

    const payload = {
      calificacion_general: 5,
      dominio_tema: 4,
      claridad_explicacion: 5,
      puntualidad: 5,
      comentarios: 'Muy corto', // < 20 caracteres
    };

    await expect(surveyService.submitSurvey(202, payload)).rejects.toThrow(
      /SURVEY_FEEDBACK_TOO_SHORT/i
    );
  });

  it('3. Rechaza re-evaluaciones duplicadas por el mismo estudiante', async () => {
    vi.spyOn(authService, 'getCurrentUser').mockReturnValue({
      email: '2022074255@upt.pe',
    });

    const payload = {
      calificacion_general: 5,
      dominio_tema: 5,
      claridad_explicacion: 5,
      puntualidad: 5,
      comentarios: 'Sesión muy provechosa de resolución de problemas con árboles AVL.',
    };

    await surveyService.submitSurvey(203, payload);
    await expect(surveyService.submitSurvey(203, payload)).rejects.toThrow(
      /DUPLICATE_SURVEY_SUBMISSION/i
    );
  });

  it('4. Consulta el estado de elegibilidad y disponibilidad de la encuesta', async () => {
    vi.spyOn(authService, 'getCurrentUser').mockReturnValue({
      email: '2022074255@upt.pe',
    });

    const status = await surveyService.getSurveyStatus(204);
    expect(status.eligible).toBe(true);
    expect(status.window_open).toBe(true);
    expect(status.has_surveyed).toBe(false);
  });

  it('5. Rechaza calificaciones fuera del rango de 1 a 5 estrellas', async () => {
    vi.spyOn(authService, 'getCurrentUser').mockReturnValue({
      email: '2022074255@upt.pe',
    });

    const payload = {
      calificacion_general: 6, // fuera de rango
      dominio_tema: 5,
      claridad_explicacion: 5,
      puntualidad: 5,
      comentarios: 'Sesión muy provechosa de resolución de problemas con árboles AVL.',
    };

    await expect(surveyService.submitSurvey(205, payload)).rejects.toThrow(
      /Todas las dimensiones deben ser evaluadas entre 1 y 5 estrellas/i
    );
  });
});
