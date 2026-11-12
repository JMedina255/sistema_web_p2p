/**
 * Modal de Encuesta de Calidad y Satisfacción Post-Mentoría (T-38 / PB-020 / RF18 / CUS05 / RN-12 / RN-13 / RNF05)
 */

import React, { useState, useId, useEffect } from 'react';
import { surveyService, type SurveyPayload, type SurveyResponse } from '../services/surveyService';

export interface PostSessionSurveyModalProps {
  isOpen: boolean;
  onClose: () => void;
  sessionId: string | number;
  sessionTitle?: string;
  mentorName?: string;
  sessionEndDate?: string | Date;
  asistenciaConfirmada?: boolean;
  currentTime?: number;
  onSurveySubmitted?: (survey: SurveyResponse) => void;
}

interface Dimension {
  id: keyof Omit<SurveyPayload, 'comentarios'>;
  label: string;
  description: string;
}

const DIMENSIONS: Dimension[] = [
  {
    id: 'puntualidad',
    label: 'Puntualidad e Inicio de Sesión',
    description: 'Cumplimiento del horario fijado e inicio puntual de la tutoría.',
  },
  {
    id: 'dominio_tema',
    label: 'Dominio Conceptual y Temático',
    description: 'Solvencia técnica y dominio del temario silábico impartido.',
  },
  {
    id: 'claridad_explicacion',
    label: 'Claridad Expositiva y Metodología Didáctica',
    description: 'Capacidad didáctica, resolución de dudas y ritmo de explicación.',
  },
  {
    id: 'calificacion_general',
    label: 'Calificación General del Servicio de Mentoría',
    description: 'Satisfacción global con el desarrollo de la sesión.',
  },
];

export const PostSessionSurveyModal: React.FC<PostSessionSurveyModalProps> = ({
  isOpen,
  onClose,
  sessionId,
  sessionTitle = 'Sesión de Mentoría Académica',
  mentorName = 'Mentor Académico',
  sessionEndDate,
  asistenciaConfirmada = true,
  currentTime,
  onSurveySubmitted,
}) => {
  const titleId = useId();
  const descId = useId();

  // Escalas Likert (1 a 5)
  const [ratings, setRatings] = useState<{
    puntualidad: number;
    dominio_tema: number;
    claridad_explicacion: number;
    calificacion_general: number;
  }>({
    puntualidad: 0,
    dominio_tema: 0,
    claridad_explicacion: 0,
    calificacion_general: 0,
  });

  const [comentarios, setComentarios] = useState('');
  const [submitting, setSubmitting] = useState(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successSubmitted, setSuccessSubmitted] = useState(false);
  const [renderTimestamp] = useState<number>(() => currentTime ?? Date.now());

  // Cierre accesible con tecla Escape (WCAG 2.1 AA / RNF05)
  useEffect(() => {
    if (!isOpen) return;
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && !submitting) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, submitting, onClose]);

  // Regla RN-13: Evaluación perentoria dentro de las 24 horas posteriores al cierre
  const nowMs = currentTime !== undefined ? currentTime : renderTimestamp;
  let isExpired = false;
  if (sessionEndDate) {
    const endMs = new Date(sessionEndDate).getTime();
    if (!isNaN(endMs)) {
      const elapsedHours = (nowMs - endMs) / (1000 * 60 * 60);
      if (elapsedHours > 24) {
        isExpired = true;
      }
    }
  }

  const handleRatingChange = (dimension: keyof typeof ratings, star: number) => {
    setRatings((prev) => ({ ...prev, [dimension]: star }));
  };

  const handleRatingKeyDown = (
    e: React.KeyboardEvent,
    dimension: keyof typeof ratings,
    star: number
  ) => {
    if (isExpired || submitting) return;
    if (e.key === 'ArrowRight' || e.key === 'ArrowUp') {
      e.preventDefault();
      const next = Math.min(5, star + 1);
      handleRatingChange(dimension, next);
    } else if (e.key === 'ArrowLeft' || e.key === 'ArrowDown') {
      e.preventDefault();
      const prev = Math.max(1, star - 1);
      handleRatingChange(dimension, prev);
    } else if (e.key === ' ' || e.key === 'Enter') {
      e.preventDefault();
      handleRatingChange(dimension, star);
    }
  };

  const cleanComentarios = comentarios.trim();
  const allRatingsSelected =
    ratings.puntualidad > 0 &&
    ratings.dominio_tema > 0 &&
    ratings.claridad_explicacion > 0 &&
    ratings.calificacion_general > 0;

  // Validación de retroalimentación cualitativa sustantiva (>= 20 caracteres)
  const isFeedbackValid = cleanComentarios.length >= 20;
  const canSubmit = allRatingsSelected && isFeedbackValid && !isExpired && !submitting;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!canSubmit) return;

    setSubmitting(true);
    setErrorMessage(null);

    const payload: SurveyPayload = {
      calificacion_general: ratings.calificacion_general,
      dominio_tema: ratings.dominio_tema,
      claridad_explicacion: ratings.claridad_explicacion,
      puntualidad: ratings.puntualidad,
      comentarios: cleanComentarios,
    };

    try {
      const response = await surveyService.submitSurvey(sessionId, payload);
      setSuccessSubmitted(true);
      if (onSurveySubmitted) {
        onSurveySubmitted(response);
      }
    } catch (err) {
      setErrorMessage(
        err instanceof Error
          ? err.message
          : 'Error al enviar la evaluación. Por favor verifique su conexión.'
      );
    } finally {
      setSubmitting(false);
    }
  };

  // Regla RN-12: Inasistencia o modal cerrado bloquea el renderizado
  if (!isOpen || asistenciaConfirmada === false) {
    return null;
  }

  return (
    <div
      className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-slate-900/60 backdrop-blur-sm animate-fade-in"
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId}
      aria-describedby={descId}
    >
      <div className="relative w-full max-w-2xl bg-white dark:bg-slate-900 rounded-2xl shadow-2xl border border-slate-200 dark:border-slate-800 overflow-hidden flex flex-col max-h-[90vh]">
        {/* Cabecera */}
        <div className="px-6 py-5 bg-gradient-to-r from-blue-700 via-indigo-700 to-indigo-800 text-white flex items-center justify-between">
          <div>
            <span className="text-xs font-semibold tracking-wider uppercase text-blue-200">
              Evaluación Formativa Post-Mentoría (RF18)
            </span>
            <h2 id={titleId} className="text-xl font-bold mt-0.5">
              Encuesta de Calidad Docente
            </h2>
            <p id={descId} className="text-xs text-blue-100 mt-1">
              {sessionTitle} — Mentor: {mentorName}
            </p>
          </div>
          <button
            onClick={onClose}
            className="p-2 rounded-lg text-blue-200 hover:text-white hover:bg-white/10 transition-colors focus:outline-none focus:ring-2 focus:ring-white"
            aria-label="Cerrar modal de evaluación"
          >
            <svg className="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Contenido / Cuerpo */}
        <div className="p-6 overflow-y-auto space-y-6">
          {/* Alerta de Ventana de 24 horas Expirada (RN-13) */}
          {isExpired && (
            <div
              className="p-4 rounded-xl bg-amber-50 dark:bg-amber-950/40 border border-amber-300 dark:border-amber-800 text-amber-900 dark:text-amber-200 text-sm flex items-start gap-3"
              role="alert"
            >
              <svg className="w-5 h-5 text-amber-600 dark:text-amber-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <div>
                <p className="font-semibold text-amber-800 dark:text-amber-300">
                  Encuesta Cerrada (Plazo de 24h Vencido)
                </p>
                <p className="mt-1 text-xs text-amber-700 dark:text-amber-300/90 leading-relaxed">
                  Conforme a la regla <strong>RN-13</strong>, las encuestas deben emitirse dentro de las 24 horas posteriores al cierre formal de la mentoría. Esta sesión ha superado la ventana reglamentaria.
                </p>
              </div>
            </div>
          )}

          {/* Banner de Éxito Tras el Envío */}
          {successSubmitted ? (
            <div
              className="p-6 text-center space-y-4 bg-emerald-50 dark:bg-emerald-950/40 border border-emerald-200 dark:border-emerald-800 rounded-xl"
              aria-live="polite"
            >
              <div className="w-12 h-12 mx-auto rounded-full bg-emerald-100 dark:bg-emerald-900/60 flex items-center justify-center text-emerald-600 dark:text-emerald-400">
                <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3 className="text-lg font-bold text-emerald-900 dark:text-emerald-200">
                ¡Gracias por tu Evaluación!
              </h3>
              <p className="text-sm text-emerald-700 dark:text-emerald-300 max-w-md mx-auto">
                Tu retroalimentación cualitativa y psicométrica ha sido registrada exitosamente. Tus aportes son fundamentales para la acreditación académica y mejora formativa en la EPIS-UPT.
              </p>
              <button
                type="button"
                onClick={onClose}
                className="mt-4 px-6 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-700 text-white font-medium text-sm transition-colors focus:ring-2 focus:ring-emerald-500 focus:outline-none"
              >
                Cerrar Ventana
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit} className="space-y-6" aria-busy={submitting}>
              {/* Alerta de Error */}
              {errorMessage && (
                <div
                  className="p-3.5 rounded-xl bg-rose-50 dark:bg-rose-950/40 border border-rose-300 dark:border-rose-800 text-rose-800 dark:text-rose-200 text-sm flex items-start gap-2.5"
                  role="alert"
                >
                  <svg className="w-5 h-5 text-rose-600 dark:text-rose-400 mt-0.5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{errorMessage}</span>
                </div>
              )}

              {/* Escalas Likert por Dimensión */}
              <div className="space-y-4">
                {DIMENSIONS.map((dim) => {
                  const currentValue = ratings[dim.id];
                  return (
                    <div
                      key={dim.id}
                      className="p-4 rounded-xl border border-slate-200 dark:border-slate-800 bg-slate-50/70 dark:bg-slate-800/40 space-y-2"
                    >
                      <div className="flex flex-col sm:flex-row sm:items-center sm:justify-between gap-1">
                        <div>
                          <label className="text-sm font-semibold text-slate-800 dark:text-slate-100">
                            {dim.label}
                          </label>
                          <p className="text-xs text-slate-500 dark:text-slate-400">
                            {dim.description}
                          </p>
                        </div>
                        {/* Selector de 1 a 5 Estrellas */}
                        <div
                          className="flex items-center gap-1.5 pt-1 sm:pt-0"
                          role="group"
                          aria-label={`Calificación para ${dim.label}`}
                        >
                          {[1, 2, 3, 4, 5].map((star) => {
                            const isSelected = star <= currentValue;
                            return (
                              <button
                                key={star}
                                type="button"
                                disabled={isExpired || submitting}
                                onClick={() => handleRatingChange(dim.id, star)}
                                onKeyDown={(e) => handleRatingKeyDown(e, dim.id, star)}
                                aria-label={`Calificar con ${star} estrellas`}
                                title={`${star} estrella${star > 1 ? 's' : ''}`}
                                className={`p-1.5 rounded-lg transition-transform focus:outline-none focus:ring-2 focus:ring-indigo-500 active:scale-95 ${
                                  isSelected
                                    ? 'text-amber-400 hover:text-amber-500'
                                    : 'text-slate-300 dark:text-slate-600 hover:text-slate-400'
                                }`}
                              >
                                <svg
                                  className="w-6 h-6 fill-current"
                                  viewBox="0 0 20 20"
                                >
                                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                </svg>
                              </button>
                            );
                          })}
                          <span className="text-xs font-semibold ml-1.5 min-w-[32px] text-slate-700 dark:text-slate-300">
                            {currentValue > 0 ? `${currentValue}/5` : '—'}
                          </span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Área de Texto de Retroalimentación Cualitativa (>= 20 caracteres) */}
              <div className="space-y-1.5">
                <div className="flex items-center justify-between">
                  <label
                    htmlFor="feedback-qualitative-input"
                    className="text-sm font-semibold text-slate-800 dark:text-slate-100"
                  >
                    Retroalimentación y Observaciones Constructivas
                  </label>
                  <span
                    className={`text-xs font-medium ${
                      cleanComentarios.length >= 20
                        ? 'text-emerald-600 dark:text-emerald-400'
                        : cleanComentarios.length > 0
                        ? 'text-amber-600 dark:text-amber-400'
                        : 'text-slate-400 dark:text-slate-500'
                    }`}
                  >
                    {cleanComentarios.length}/20 caracteres mínimos
                  </span>
                </div>
                <textarea
                  id="feedback-qualitative-input"
                  rows={3}
                  disabled={isExpired || submitting}
                  value={comentarios}
                  onChange={(e) => setComentarios(e.target.value)}
                  placeholder="Detalla aspectos pedagógicos relevantes de la sesión: dominio del tema, ejemplos resueltos, claridad y recomendaciones (mínimo 20 caracteres)..."
                  className="w-full px-3.5 py-2.5 rounded-xl border border-slate-300 dark:border-slate-700 bg-white dark:bg-slate-800 text-slate-900 dark:text-slate-100 placeholder-slate-400 text-sm focus:ring-2 focus:ring-indigo-500 focus:border-indigo-500 focus:outline-none transition-colors"
                />
                {cleanComentarios.length > 0 && cleanComentarios.length < 20 && (
                  <p className="text-xs text-amber-600 dark:text-amber-400">
                    Ingresa al menos {20 - cleanComentarios.length} caracteres más para habilitar el envío.
                  </p>
                )}
              </div>

              {/* Botones de Acción */}
              <div className="pt-2 flex items-center justify-end gap-3 border-t border-slate-100 dark:border-slate-800">
                <button
                  type="button"
                  disabled={submitting}
                  onClick={onClose}
                  className="px-4 py-2.5 rounded-xl text-sm font-medium text-slate-700 dark:text-slate-300 hover:bg-slate-100 dark:hover:bg-slate-800 transition-colors focus:outline-none focus:ring-2 focus:ring-slate-400"
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={!canSubmit}
                  className="inline-flex items-center gap-2 px-5 py-2.5 rounded-xl text-sm font-semibold text-white bg-indigo-600 hover:bg-indigo-700 disabled:opacity-50 disabled:cursor-not-allowed shadow-md shadow-indigo-600/20 transition-all focus:outline-none focus:ring-2 focus:ring-indigo-500"
                >
                  {submitting ? (
                    <>
                      <svg className="animate-spin -ml-1 mr-2 h-4 w-4 text-white" fill="none" viewBox="0 0 24 24">
                        <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
                      </svg>
                      <span>Enviando...</span>
                    </>
                  ) : (
                    <span>Enviar Evaluación</span>
                  )}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
