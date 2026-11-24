/**
 * Modal de Encuesta de Calidad y Satisfacción Post-Mentoría (T-38 / PB-020 / RF18 / CUS05 / RN-12 / RN-13 / RNF05)
 */

import React, { useState, useId, useEffect, useRef } from 'react';
import './PostSessionSurveyModal.css';
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
  onAlreadySubmitted?: () => void;
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
  onAlreadySubmitted,
}) => {
  const titleId = useId();
  const descId = useId();

  const dialog = useRef<HTMLDivElement>(null);
  useEffect(() => {
    if (!isOpen || !asistenciaConfirmada || !dialog.current) return;
    const trigger = document.activeElement as HTMLElement | null;
    const overflow = document.body.style.overflow;
    document.body.style.overflow = 'hidden';
    dialog.current.focus();
    return () => { document.body.style.overflow = overflow; trigger?.focus(); };
  }, [isOpen, asistenciaConfirmada]);

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
      if (err instanceof Error && err.message.includes('DUPLICATE_SURVEY_SUBMISSION')) {
        onAlreadySubmitted?.();
        setSuccessSubmitted(true);
        return;
      }
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
      className="survey-overlay"
      ref={dialog}
      tabIndex={-1}
      onKeyDown={event => {
        if (event.key !== 'Tab') return;
        const controls = Array.from(event.currentTarget.querySelectorAll<HTMLElement>(
          'button:not(:disabled), textarea:not(:disabled)'
        ));
        const target = event.shiftKey ? controls[controls.length - 1] : controls[0];
        if (event.shiftKey ? (document.activeElement === controls[0] || document.activeElement === dialog.current)
            : document.activeElement === controls[controls.length - 1]) {
          event.preventDefault();
          target?.focus();
        }
      }}
      role="dialog"
      aria-modal="true"
      aria-labelledby={titleId}
      aria-describedby={descId}
  >
      <div className="survey-panel">
        {/* Cabecera */}
        <div className="survey-heading">
          <div>
            <span>
              Evaluación Formativa Post-Mentoría (RF18)
            </span>
            <h2 id={titleId}>
              Encuesta de Calidad Docente
            </h2>
            <p id={descId}>
              {sessionTitle} — Mentor: {mentorName}
            </p>
          </div>
          <button
            onClick={onClose}
            aria-label="Cerrar modal de evaluación"
        >
            <svg  fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M6 18L18 6M6 6l12 12" />
            </svg>
          </button>
        </div>

        {/* Contenido / Cuerpo */}
        <div className="survey-content">
          {/* Alerta de Ventana de 24 horas Expirada (RN-13) */}
          {isExpired && (
            <div
              className="survey-notice"
              role="alert"
          >
              <svg  fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <div>
                <p>
                  Encuesta Cerrada (Plazo de 24h Vencido)
                </p>
                <p>
                  Conforme a la regla <strong>RN-13</strong>, las encuestas deben emitirse dentro de las 24 horas posteriores al cierre formal de la mentoría. Esta sesión ha superado la ventana reglamentaria.
                </p>
              </div>
            </div>
          )}

          {/* Banner de Éxito Tras el Envío */}
          {successSubmitted ? (
            <div
              className="survey-success"
              aria-live="polite"
          >
              <div>
                <svg  fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M5 13l4 4L19 7" />
                </svg>
              </div>
              <h3>
                ¡Gracias por tu Evaluación!
              </h3>
              <p>
                Tu retroalimentación cualitativa y psicométrica ha sido registrada exitosamente. Tus aportes son fundamentales para la acreditación académica y mejora formativa en la EPIS-UPT.
              </p>
              <button
                type="button"
                onClick={onClose}
                className="survey-primary"
            >
                Cerrar Ventana
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit}  aria-busy={submitting}>
              {/* Alerta de Error */}
              {errorMessage && (
                <div
                  className="survey-notice"
                  role="alert"
              >
                  <svg  fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  <span>{errorMessage}</span>
                </div>
              )}

              {/* Escalas Likert por Dimensión */}
              <div>
                {DIMENSIONS.map((dim) => {
                  const currentValue = ratings[dim.id];
                  return (
                    <div
                      key={dim.id}
                      className="survey-dimension"
                  >
                      <div>
                        <div>
                          <label>
                            {dim.label}
                          </label>
                          <p>
                            {dim.description}
                          </p>
                        </div>
                        {/* Selector de 1 a 5 Estrellas */}
                        <div
                          className="survey-stars"
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
                                title={`${star} estrella${star> 1 ? 's' : ''}`}
                                aria-pressed={star === currentValue}
                                data-filled={isSelected}
                            >
                                <svg
                                  viewBox="0 0 20 20"
                              >
                                  <path d="M9.049 2.927c.3-.921 1.603-.921 1.902 0l1.07 3.292a1 1 0 00.95.69h3.462c.969 0 1.371 1.24.588 1.81l-2.8 2.034a1 1 0 00-.364 1.118l1.07 3.292c.3.921-.755 1.688-1.54 1.118l-2.8-2.034a1 1 0 00-1.175 0l-2.8 2.034c-.784.57-1.838-.197-1.539-1.118l1.07-3.292a1 1 0 00-.364-1.118L2.98 8.72c-.783-.57-.38-1.81.588-1.81h3.461a1 1 0 00.951-.69l1.07-3.292z" />
                                </svg>
                              </button>
                            );
                          })}
                          <span>
                            {currentValue > 0 ? `${currentValue}/5` : '—'}
                          </span>
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>

              {/* Área de Texto de Retroalimentación Cualitativa (>= 20 caracteres) */}
              <div>
                <div className="survey-feedback-label">
                  <label htmlFor="feedback-qualitative-input">Retroalimentación y observaciones constructivas</label>
                  <span>{cleanComentarios.length}/20 caracteres mínimos</span>
                </div>
                <textarea
                  id="feedback-qualitative-input"
                  rows={3}
                  disabled={isExpired || submitting}
                  value={comentarios}
                  onChange={(e) => setComentarios(e.target.value)}
                  placeholder="Detalla aspectos pedagógicos relevantes de la sesión: dominio del tema, ejemplos resueltos, claridad y recomendaciones (mínimo 20 caracteres)..."
                />
                {cleanComentarios.length > 0 && cleanComentarios.length < 20 && (
                  <p>
                    Ingresa al menos {20 - cleanComentarios.length} caracteres más para habilitar el envío.
                  </p>
                )}
              </div>

              {/* Botones de Acción */}
              <div className="survey-actions">
                <button
                  type="button"
                  disabled={submitting}
                  onClick={onClose}
              >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={!canSubmit}
                  className="survey-primary"
              >
                  {submitting ? (
                    <>
                      <svg  fill="none" viewBox="0 0 24 24">
                        <circle  cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4" />
                        <path  fill="currentColor" d="M4 12a8 8 0 018-8v8z" />
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
