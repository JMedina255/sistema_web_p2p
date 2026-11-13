/**
 * Modal de Registro de Solicitud de Mentoría por Demanda (CUS03 / RF07)
 * Permite a los estudiantes mentoreados registrar necesidades académicas insatisfechas
 * cuando no existen ofertas de sesiones activas o el aforo está colapsado.
 */

import React, { useState, useEffect, useCallback } from 'react';
import { fetchCourses, fetchCourseDetail, type Course, type Topic } from '../services/apiClient';
import { bookingService, type DemandRequestResponse } from '../services/bookingService';

export interface MentoringDemandModalViewProps {
  isOpen: boolean;
  onClose: () => void;
  preselectedCourseId?: number;
  preselectedTopicId?: number;
  onDemandCreated?: (demand: DemandRequestResponse) => void;
}

export const MentoringDemandModalView: React.FC<MentoringDemandModalViewProps> = ({
  isOpen,
  onClose,
  preselectedCourseId,
  preselectedTopicId,
  onDemandCreated,
}) => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [selectedCourseId, setSelectedCourseId] = useState<number>(preselectedCourseId || 0);
  const [selectedTopicId, setSelectedTopicId] = useState<number>(preselectedTopicId || 0);
  const [observaciones, setObservaciones] = useState<string>('');

  const [isLoadingCatalog, setIsLoadingCatalog] = useState<boolean>(false);
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [createdDemand, setCreatedDemand] = useState<DemandRequestResponse | null>(null);

  // Carga de catálogo curricular institucional
  const loadCourses = useCallback(async () => {
    setIsLoadingCatalog(true);
    setErrorMessage(null);
    try {
      const list = await fetchCourses(true);
      setCourses(list);
      if (list.length > 0 && !preselectedCourseId) {
        setSelectedCourseId(list[0].id_asignatura);
      }
    } catch (err: unknown) {
      setErrorMessage(
        err instanceof Error ? err.message : 'Error al consultar el catálogo curricular.'
      );
    } finally {
      setIsLoadingCatalog(false);
    }
  }, [preselectedCourseId]);

  // Carga de temas según asignatura
  useEffect(() => {
    if (!selectedCourseId) {
      setTopics([]);
      setSelectedTopicId(0);
      return;
    }

    let isMounted = true;
    const loadTopics = async () => {
      try {
        const detail = await fetchCourseDetail(selectedCourseId);
        if (isMounted && detail.temas && detail.temas.length > 0) {
          setTopics(detail.temas);
          if (preselectedTopicId && detail.temas.some((t) => t.id_tema === preselectedTopicId)) {
            setSelectedTopicId(preselectedTopicId);
          } else {
            setSelectedTopicId(detail.temas[0].id_tema);
          }
        } else if (isMounted) {
          setTopics([]);
          setSelectedTopicId(0);
        }
      } catch {
        if (isMounted) {
          setTopics([]);
          setSelectedTopicId(0);
        }
      }
    };

    loadTopics();
    return () => {
      isMounted = false;
    };
  }, [selectedCourseId, preselectedTopicId]);

  useEffect(() => {
    if (isOpen) {
      setCreatedDemand(null);
      setErrorMessage(null);
      setObservaciones('');
      loadCourses();
    }
  }, [isOpen, loadCourses]);

  // Cierre con Escape
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && isOpen && !isSubmitting) {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isOpen, isSubmitting, onClose]);

  if (!isOpen) return null;

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCourseId || !selectedTopicId) {
      setErrorMessage('Por favor seleccione una asignatura y un tema curricular válido.');
      return;
    }

    setIsSubmitting(true);
    setErrorMessage(null);

    try {
      const resp = await bookingService.createDemandRequest({
        id_asignatura: selectedCourseId,
        id_tema: selectedTopicId,
        observaciones: observaciones.trim() || undefined,
      });

      setCreatedDemand(resp);
      if (onDemandCreated) {
        onDemandCreated(resp);
      }
    } catch (err: unknown) {
      setErrorMessage(
        err instanceof Error ? err.message : 'Error al registrar la solicitud por demanda.'
      );
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div
      role="dialog"
      aria-modal="true"
      aria-labelledby="demand-modal-title"
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(15, 23, 42, 0.65)',
        backdropFilter: 'blur(4px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 9999,
        padding: '1rem',
      }}
    >
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '16px',
          maxWidth: '560px',
          width: '100%',
          boxShadow: '0 25px 50px -12px rgba(0, 0, 0, 0.25)',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          maxHeight: '90vh',
        }}
      >
        {/* Cabecera */}
        <div
          style={{
            backgroundColor: '#1C2A59',
            color: '#FFFFFF',
            padding: '1.25rem 1.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
          }}
        >
          <div>
            <h2
              id="demand-modal-title"
              style={{ margin: 0, fontSize: '1.2rem', fontWeight: 700 }}
            >
              📋 Registrar Solicitud de Mentoría por Demanda
            </h2>
            <p style={{ margin: '0.25rem 0 0', fontSize: '0.8rem', color: '#CBD5E1' }}>
              Caso de Uso CUS03 / RF07 — Banco Institucional EPIS UPT
            </p>
          </div>
          <button
            type="button"
            onClick={onClose}
            aria-label="Cerrar modal"
            style={{
              background: 'none',
              border: 'none',
              color: '#FFFFFF',
              fontSize: '1.5rem',
              cursor: 'pointer',
              lineHeight: 1,
            }}
          >
            &times;
          </button>
        </div>

        {/* Contenido */}
        <div style={{ padding: '1.5rem', overflowY: 'auto' }}>
          {createdDemand ? (
            <div style={{ textAlign: 'center', padding: '1rem 0' }}>
              <div
                style={{
                  width: '64px',
                  height: '64px',
                  borderRadius: '50%',
                  backgroundColor: '#DCFCE7',
                  color: '#16A34A',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  fontSize: '2rem',
                  margin: '0 auto 1rem',
                }}
              >
                ✓
              </div>
              <h3 style={{ color: '#166534', margin: '0 0 0.5rem', fontSize: '1.25rem' }}>
                ¡Solicitud Registrada con Éxito!
              </h3>
              <p style={{ color: '#475569', fontSize: '0.9rem', lineHeight: 1.5 }}>
                Tu solicitud ha sido incorporada al banco de demanda académica con folio institucional{' '}
                <strong>#DEM-{createdDemand.id_demanda}</strong>. Los mentores acreditados podrán revisarla
                para formular sesiones dirigidas a este tema.
              </p>
              <div
                style={{
                  backgroundColor: '#F8FAFC',
                  borderRadius: '8px',
                  padding: '1rem',
                  marginTop: '1rem',
                  textAlign: 'left',
                  fontSize: '0.85rem',
                  border: '1px solid #E2E8F0',
                }}
              >
                <div><strong>Estado:</strong> <span style={{ color: '#2563EB', fontWeight: 700 }}>{createdDemand.estado}</span></div>
                <div><strong>Solicitante:</strong> {createdDemand.estudiante_email}</div>
                <div><strong>Fecha de Registro:</strong> {new Date(createdDemand.created_at).toLocaleString()}</div>
              </div>
              <button
                type="button"
                onClick={onClose}
                style={{
                  marginTop: '1.5rem',
                  backgroundColor: '#1C2A59',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '8px',
                  padding: '0.75rem 2rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  fontSize: '0.95rem',
                }}
              >
                Entendido
              </button>
            </div>
          ) : (
            <form onSubmit={handleSubmit}>
              <p style={{ color: '#475569', fontSize: '0.88rem', margin: '0 0 1.25rem', lineHeight: 1.5 }}>
                Si no encuentras una sesión que cubra tu tema de interés o los cupos están agotados,
                registra tu solicitud para que los mentores de ciclos superiores puedan programar una oferta específica.
              </p>

              {errorMessage && (
                <div
                  role="alert"
                  style={{
                    backgroundColor: '#FEF2F2',
                    border: '1px solid #FCA5A5',
                    color: '#991B1B',
                    padding: '0.75rem 1rem',
                    borderRadius: '8px',
                    marginBottom: '1rem',
                    fontSize: '0.85rem',
                  }}
                >
                  ⚠️ {errorMessage}
                </div>
              )}

              {/* Selector de Asignatura */}
              <div style={{ marginBottom: '1.25rem' }}>
                <label
                  htmlFor="demand-course-select"
                  style={{ display: 'block', fontWeight: 700, fontSize: '0.85rem', color: '#1E293B', marginBottom: '0.4rem' }}
                >
                  Asignatura Curricular <span style={{ color: '#DC2626' }}>*</span>
                </label>
                <select
                  id="demand-course-select"
                  value={selectedCourseId}
                  onChange={(e) => setSelectedCourseId(Number(e.target.value))}
                  disabled={isLoadingCatalog || isSubmitting}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1px solid #CBD5E1',
                    fontSize: '0.9rem',
                    backgroundColor: '#FFFFFF',
                  }}
                >
                  {isLoadingCatalog && <option value={0}>Cargando catálogo curricular...</option>}
                  {courses.map((c) => (
                    <option key={c.id_asignatura} value={c.id_asignatura}>
                      {c.codigo_curso} — {c.nombre_curso} (Ciclo {c.ciclo_plan})
                    </option>
                  ))}
                </select>
              </div>

              {/* Selector de Tema */}
              <div style={{ marginBottom: '1.25rem' }}>
                <label
                  htmlFor="demand-topic-select"
                  style={{ display: 'block', fontWeight: 700, fontSize: '0.85rem', color: '#1E293B', marginBottom: '0.4rem' }}
                >
                  Tema o Unidad Específica <span style={{ color: '#DC2626' }}>*</span>
                </label>
                <select
                  id="demand-topic-select"
                  value={selectedTopicId}
                  onChange={(e) => setSelectedTopicId(Number(e.target.value))}
                  disabled={topics.length === 0 || isSubmitting}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1px solid #CBD5E1',
                    fontSize: '0.9rem',
                    backgroundColor: '#FFFFFF',
                  }}
                >
                  {topics.length === 0 && <option value={0}>No hay temas registrados para esta materia</option>}
                  {topics.map((t) => (
                    <option key={t.id_tema} value={t.id_tema}>
                      Unidad {t.unidad_silabica}: {t.nombre_tema}
                    </option>
                  ))}
                </select>
              </div>

              {/* Observaciones pedagógicas */}
              <div style={{ marginBottom: '1.5rem' }}>
                <label
                  htmlFor="demand-obs-input"
                  style={{ display: 'block', fontWeight: 700, fontSize: '0.85rem', color: '#1E293B', marginBottom: '0.4rem' }}
                >
                  Observaciones o Justificación de Necesidad Formativa
                </label>
                <textarea
                  id="demand-obs-input"
                  rows={3}
                  value={observaciones}
                  onChange={(e) => setObservaciones(e.target.value)}
                  disabled={isSubmitting}
                  placeholder="Ej: Requiero nivelación en límites algebraicos y aplicaciones de derivadas para la próxima práctica calificada."
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1px solid #CBD5E1',
                    fontSize: '0.88rem',
                    resize: 'vertical',
                    boxSizing: 'border-box',
                  }}
                />
              </div>

              {/* Acciones */}
              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
                <button
                  type="button"
                  onClick={onClose}
                  disabled={isSubmitting}
                  style={{
                    backgroundColor: '#F1F5F9',
                    color: '#475569',
                    border: '1px solid #CBD5E1',
                    borderRadius: '8px',
                    padding: '0.65rem 1.25rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                    fontSize: '0.88rem',
                  }}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={isSubmitting || !selectedCourseId || !selectedTopicId}
                  style={{
                    backgroundColor: isSubmitting || !selectedCourseId || !selectedTopicId ? '#94A3B8' : '#1C2A59',
                    color: '#FFFFFF',
                    border: 'none',
                    borderRadius: '8px',
                    padding: '0.65rem 1.5rem',
                    fontWeight: 700,
                    cursor: isSubmitting || !selectedCourseId || !selectedTopicId ? 'not-allowed' : 'pointer',
                    fontSize: '0.88rem',
                  }}
                >
                  {isSubmitting ? 'Registrando...' : 'Enviar Solicitud'}
                </button>
              </div>
            </form>
          )}
        </div>
      </div>
    </div>
  );
};
