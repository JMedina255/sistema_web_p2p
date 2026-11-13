import React, { useState, useEffect, useMemo, useCallback } from 'react';
import { fetchCourses, fetchCourseDetail } from '../services/apiClient';
import type { Course, Topic } from '../services/apiClient';
import {
  offerService,
  validateOfferPayload,
  calculateAdvanceHours,
  STANDARD_CAPACITY,
  SUGGESTED_CLASSROOMS,
  type SessionModality,
  type SessionDuration,
  type PublishOfferPayload,
  type PublishOfferResponse,
} from '../services/offerService';

export interface OfferPublishViewProps {
  mentorEmail?: string;
  mentorName?: string;
  onOfferPublished?: (response: PublishOfferResponse) => void;
  showDevControls?: boolean;
}

/**
 * Genera una fecha por defecto en formato local YYYY-MM-DDTHH:mm con antelación >= 48 h recomendada
 */
function getDefaultStartDateTime(): string {
  const d = new Date(Date.now() + 49 * 3600 * 1000);
  d.setMinutes(0);
  d.setSeconds(0);
  d.setMilliseconds(0);
  // Formato local YYYY-MM-DDTHH:mm
  const year = d.getFullYear();
  const month = String(d.getMonth() + 1).padStart(2, '0');
  const day = String(d.getDate()).padStart(2, '0');
  const hours = String(d.getHours()).padStart(2, '0');
  const minutes = String(d.getMinutes()).padStart(2, '0');
  return `${year}-${month}-${day}T${hours}:${minutes}`;
}

export const OfferPublishView: React.FC<OfferPublishViewProps> = ({
  mentorEmail = '2022074255@upt.pe',
  mentorName = 'Mentor Académico',
  onOfferPublished,
  showDevControls = false,
}) => {
  // Datos del catálogo
  const [courses, setCourses] = useState<Course[]>([]);
  const [topics, setTopics] = useState<Topic[]>([]);
  const [isLoadingCourses, setIsLoadingCourses] = useState<boolean>(true);
  const [catalogError, setCatalogError] = useState<string | null>(null);

  // Campos del formulario
  const [selectedCourseId, setSelectedCourseId] = useState<number>(0);
  const [selectedTopicId, setSelectedTopicId] = useState<number>(0);
  const [modality, setModality] = useState<SessionModality>('presencial');
  const [duration, setDuration] = useState<SessionDuration>(60);
  const [startDateTime, setStartDateTime] = useState<string>(getDefaultStartDateTime);
  const [assignedSpace, setAssignedSpace] = useState<string>(SUGGESTED_CLASSROOMS[0]);
  const [additionalNotes, setAdditionalNotes] = useState<string>('');

  // Estados de control
  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [publishedSuccess, setPublishedSuccess] = useState<PublishOfferResponse | null>(null);
  const [submissionError, setSubmissionError] = useState<string | null>(null);
  const [recentOffers, setRecentOffers] = useState<PublishOfferResponse[]>([]);

  // Cargar catálogo de cursos y temas iniciales
  const loadCatalog = useCallback(async () => {
    setIsLoadingCourses(true);
    setCatalogError(null);
    try {
      const fetched = await fetchCourses(true);
      if (fetched.length > 0) {
        setCourses(fetched);
        const firstCourseId = fetched[0].id_asignatura;
        setSelectedCourseId(firstCourseId);
        try {
          const detail = await fetchCourseDetail(firstCourseId);
          if (detail.temas && detail.temas.length > 0) {
            setTopics(detail.temas);
            setSelectedTopicId(detail.temas[0].id_tema);
          }
        } catch {
          // Ignorar fallo secundario de detalle
        }
      } else {
        setCatalogError('No se encontraron asignaturas activas registradas en el catálogo curricular.');
      }
    } catch (err: unknown) {
      setCatalogError(
        err instanceof Error
          ? `No se pudo conectar con el catálogo curricular del servidor: ${err.message}`
          : 'Error al conectar con el servidor institucional para cargar el catálogo.'
      );
    } finally {
      setIsLoadingCourses(false);
    }
  }, []);

  useEffect(() => {
    loadCatalog();
  }, [loadCatalog]);

  // Cargar temas cuando cambie la asignatura seleccionada
  useEffect(() => {
    let isMounted = true;
    if (!selectedCourseId) {
      setTopics([]);
      setSelectedTopicId(0);
      return;
    }
    const loadTopics = async () => {
      try {
        const detail = await fetchCourseDetail(selectedCourseId);
        if (isMounted && detail.temas && detail.temas.length > 0) {
          setTopics(detail.temas);
          setSelectedTopicId(detail.temas[0].id_tema);
          return;
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
  }, [selectedCourseId]);

  // Cargar ofertas publicadas del mentor en este entorno de prueba
  const refreshRecentOffers = useCallback(async () => {
    try {
      const list = await offerService.getOffers(mentorEmail);
      setRecentOffers(list);
    } catch {
      // Ignorar
    }
  }, [mentorEmail]);

  useEffect(() => {
    refreshRecentOffers();
  }, [refreshRecentOffers]);

  // Asignatura y tema actualmente seleccionados
  const currentCourse = useMemo(
    () => courses.find((c) => c.id_asignatura === selectedCourseId) || courses[0],
    [courses, selectedCourseId]
  );

  const currentTopic = useMemo(
    () => topics.find((t) => t.id_tema === selectedTopicId) || topics[0],
    [topics, selectedTopicId]
  );

  // Aforo estricto e inmutable según RN-05
  const currentCapacity = STANDARD_CAPACITY[modality];

  // Ajuste reactivo de infraestructura al cambiar modalidad
  const handleModalityChange = (newModality: SessionModality) => {
    setModality(newModality);
    if (newModality === 'presencial') {
      setAssignedSpace(SUGGESTED_CLASSROOMS[0]);
    } else {
      const link = offerService.generateVirtualLink(currentCourse ? currentCourse.codigo_curso : 'epis');
      setAssignedSpace(link);
    }
  };

  // Cálculo reactivo de antelación y validaciones (RN-04)
  const validation = useMemo(() => {
    const payload: Partial<PublishOfferPayload> = {
      id_asignatura: selectedCourseId,
      id_tema: selectedTopicId,
      modalidad: modality,
      duracion_minutos: duration,
      fecha_inicio: startDateTime,
      aforo_maximo: currentCapacity,
      espacio_asignado: assignedSpace,
    };
    return validateOfferPayload(payload);
  }, [selectedCourseId, selectedTopicId, modality, duration, startDateTime, currentCapacity, assignedSpace]);

  const hoursAdvance = useMemo(() => {
    return calculateAdvanceHours(startDateTime);
  }, [startDateTime]);

  // Cálculo de hora de término estimada
  const estimatedEndTime = useMemo(() => {
    if (!startDateTime) return '';
    const start = new Date(startDateTime);
    if (isNaN(start.getTime())) return '';
    const end = new Date(start.getTime() + duration * 60 * 1000);
    return end.toLocaleTimeString('es-PE', { hour: '2-digit', minute: '2-digit', hour12: true });
  }, [startDateTime, duration]);

  // Manejo de envío del formulario
  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!validation.isValid || isSubmitting) return;

    setIsSubmitting(true);
    setSubmissionError(null);

    const payload: PublishOfferPayload = {
      id_asignatura: selectedCourseId,
      codigo_asignatura: currentCourse.codigo_curso,
      nombre_asignatura: currentCourse.nombre_curso,
      id_tema: selectedTopicId,
      nombre_tema: currentTopic ? currentTopic.nombre_tema : 'Tema específico',
      fecha_inicio: new Date(startDateTime).toISOString(),
      duracion_minutos: duration,
      modalidad: modality,
      aforo_maximo: currentCapacity,
      espacio_asignado: assignedSpace,
      mentor_email: mentorEmail,
      mentor_nombre: mentorName,
      notas_adicionales: additionalNotes.trim() || undefined,
    };

    try {
      const response = await offerService.publishOffer(payload);
      setPublishedSuccess(response);
      refreshRecentOffers();
      if (onOfferPublished) {
        onOfferPublished(response);
      }
    } catch (err: unknown) {
      setSubmissionError(err instanceof Error ? err.message : 'Error al publicar la oferta de mentoría.');
    } finally {
      setIsSubmitting(false);
    }
  };

  const handleResetForm = () => {
    setPublishedSuccess(null);
    setSubmissionError(null);
    setStartDateTime(getDefaultStartDateTime());
    setAdditionalNotes('');
  };

  return (
    <div style={{ width: '100%', maxWidth: '920px', margin: '0 auto' }}>
      {/* Banner de Aviso de Modo Simulado (Solo en modo desarrollo explícito) */}
      {showDevControls && !import.meta.env.PROD && (
        <div
          role="status"
          aria-label="Aviso de Modo de Prueba"
          style={{
            backgroundColor: '#EFF6FF',
            border: '1px solid #BFDBFE',
            borderRadius: '10px',
            padding: '0.85rem 1.25rem',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '0.75rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            <span style={{ fontSize: '1.25rem' }}>ℹ️</span>
            <div>
              <strong style={{ color: '#1E40AF', fontSize: '0.85rem', display: 'block' }}>
                Modo de prueba local
              </strong>
              <span style={{ color: '#3B82F6', fontSize: '0.78rem' }}>
                La interfaz y las validaciones de publicación operan en entorno local de pruebas.
              </span>
            </div>
          </div>
          <span
            style={{
              backgroundColor: '#DBEAFE',
              color: '#1E40AF',
              fontSize: '0.72rem',
              fontWeight: 700,
              padding: '0.25rem 0.6rem',
              borderRadius: '9999px',
              border: '1px solid #93C5FD',
            }}
          >
            Entorno de pruebas
          </span>
        </div>
      )}

      {/* Alerta de Error en Carga de Catálogo Curricular Institucional */}
      {catalogError && (
        <div
          role="alert"
          aria-live="assertive"
          style={{
            backgroundColor: '#FEF2F2',
            border: '1px solid #FCA5A5',
            borderRadius: '10px',
            padding: '1rem 1.25rem',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'space-between',
            flexWrap: 'wrap',
            gap: '0.75rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.65rem' }}>
            <span style={{ fontSize: '1.25rem' }}>⚠️</span>
            <span style={{ color: '#991B1B', fontSize: '0.88rem', fontWeight: 600 }}>
              {catalogError}
            </span>
          </div>
          <button
            type="button"
            onClick={loadCatalog}
            style={{
              backgroundColor: '#DC2626',
              color: '#FFFFFF',
              border: 'none',
              borderRadius: '6px',
              padding: '0.45rem 0.9rem',
              fontSize: '0.82rem',
              fontWeight: 700,
              cursor: 'pointer',
            }}
          >
            🔄 Reintentar
          </button>
        </div>
      )}

      {/* Tarjeta del Formulario Principal */}
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #E2E8F0',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
          padding: '1.75rem 2rem',
          marginBottom: '2rem',
        }}
      >
        {/* Cabecera del Formulario */}
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'flex-start',
            flexWrap: 'wrap',
            gap: '1rem',
            borderBottom: '1px solid #F1F5F9',
            paddingBottom: '1.25rem',
            marginBottom: '1.5rem',
          }}
        >
          <div>
            <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.35rem' }}>
              <span
                style={{
                  backgroundColor: '#FEF3C7',
                  color: '#92400E',
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  padding: '0.2rem 0.55rem',
                  borderRadius: '6px',
                  border: '1px solid #FDE68A',
                }}
              >
                🎓 Rol: Mentor Académico
              </span>
            </div>
            <h3 style={{ margin: '0 0 0.25rem 0', color: '#1C2A59', fontSize: '1.35rem', fontWeight: 800 }}>
              Publicar Nueva Oferta de Mentoría
            </h3>
            <p style={{ margin: 0, color: '#64748B', fontSize: '0.84rem' }}>
              Mentor acreditado:{' '}
              <strong style={{ color: '#1E293B' }}>{mentorName}</strong> ({mentorEmail})
            </p>
          </div>

          <div
            style={{
              textAlign: 'right',
              fontSize: '0.75rem',
              color: '#64748B',
              backgroundColor: '#F8FAFC',
              padding: '0.5rem 0.75rem',
              borderRadius: '8px',
              border: '1px solid #E2E8F0',
            }}
          >
            <div>
              Antelación mín:{' '}
              <strong style={{ color: '#1C2A59' }}>&gt; 24 h</strong>
            </div>
            <div>
              Recomendada:{' '}
              <strong style={{ color: '#B99451' }}>&ge; 48 h</strong>
            </div>
          </div>
        </div>

        {/* Tarjeta de Éxito al Publicar */}
        {publishedSuccess && (
          <div
            role="alert"
            style={{
              backgroundColor: '#ECFDF5',
              border: '1px solid #A7F3D0',
              borderRadius: '10px',
              padding: '1.25rem 1.5rem',
              marginBottom: '1.75rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
              <span style={{ fontSize: '1.5rem' }}>🎉</span>
              <div>
                <h4 style={{ margin: 0, color: '#065F46', fontSize: '1.05rem', fontWeight: 800 }}>
                  ¡Oferta de mentoría publicada exitosamente!
                </h4>
                <p style={{ margin: 0, color: '#047857', fontSize: '0.82rem' }}>
                  Código oficial de sesión:{' '}
                  <strong style={{ letterSpacing: '0.05em' }}>{publishedSuccess.codigo_sesion}</strong> · Estado:{' '}
                  <span
                    style={{
                      background: '#10B981',
                      color: '#FFFFFF',
                      padding: '0.1rem 0.45rem',
                      borderRadius: '4px',
                      fontSize: '0.75rem',
                      fontWeight: 700,
                    }}
                  >
                    {publishedSuccess.estado}
                  </span>
                </p>
              </div>
            </div>

            <div
              style={{
                backgroundColor: '#FFFFFF',
                borderRadius: '8px',
                border: '1px solid #D1FAE5',
                padding: '0.85rem 1rem',
                fontSize: '0.82rem',
                color: '#1F2937',
                marginBottom: '1rem',
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                gap: '0.5rem',
              }}
            >
              <div>
                <span style={{ color: '#6B7280', display: 'block', fontSize: '0.75rem' }}>Asignatura y Tema</span>
                <strong>{publishedSuccess.offer.nombre_asignatura}</strong>: {publishedSuccess.offer.nombre_tema}
              </div>
              <div>
                <span style={{ color: '#6B7280', display: 'block', fontSize: '0.75rem' }}>Modalidad & Aforo</span>
                <span style={{ textTransform: 'capitalize' }}>{publishedSuccess.offer.modalidad}</span> ·{' '}
                <strong>{publishedSuccess.aforo} estudiantes</strong>
              </div>
              <div>
                <span style={{ color: '#6B7280', display: 'block', fontSize: '0.75rem' }}>Inicio programado</span>
                <strong>
                  {new Date(publishedSuccess.offer.fecha_inicio).toLocaleString('es-PE', {
                    dateStyle: 'medium',
                    timeStyle: 'short',
                  })}
                </strong>{' '}
                ({publishedSuccess.offer.duracion_minutos} min)
              </div>
              <div>
                <span style={{ color: '#6B7280', display: 'block', fontSize: '0.75rem' }}>Infraestructura asignada</span>
                <span style={{ wordBreak: 'break-all' }}>{publishedSuccess.espacio_asignado}</span>
              </div>
            </div>

            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
              <button
                type="button"
                onClick={handleResetForm}
                style={{
                  backgroundColor: '#10B981',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '0.5rem 1rem',
                  fontSize: '0.82rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                }}
              >
                + Publicar Otra Oferta
              </button>
            </div>
          </div>
        )}

        {/* Mensaje de Error de Envío */}
        {submissionError && (
          <div
            role="alert"
            style={{
              backgroundColor: '#FEF2F2',
              border: '1px solid #FECACA',
              borderRadius: '8px',
              padding: '0.85rem 1.25rem',
              marginBottom: '1.5rem',
              color: '#991B1B',
              fontSize: '0.84rem',
            }}
          >
            <strong>Error al publicar:</strong> {submissionError}
          </div>
        )}

        {/* Formulario */}
        <form onSubmit={handleSubmit}>
          {/* Fila 1: Asignatura y Tema Silábico */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
              gap: '1.25rem',
              marginBottom: '1.25rem',
            }}
          >
            {/* Campo: Asignatura */}
            <div>
              <label
                htmlFor="select-course"
                style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1E293B', marginBottom: '0.35rem' }}
              >
                1. Asignatura Formativa Crítica (Catálogo EPIS) *
              </label>
              <select
                id="select-course"
                aria-label="Asignatura formativa"
                value={selectedCourseId}
                onChange={(e) => setSelectedCourseId(Number(e.target.value))}
                disabled={isLoadingCourses || isSubmitting}
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '8px',
                  border: '1px solid #CBD5E1',
                  fontSize: '0.86rem',
                  backgroundColor: '#FFFFFF',
                  color: '#1E293B',
                }}
              >
                {courses.map((c) => (
                  <option key={c.id_asignatura} value={c.id_asignatura}>
                    {c.codigo_curso} — {c.nombre_curso} (Ciclo {c.ciclo_plan})
                  </option>
                ))}
              </select>
              <span style={{ fontSize: '0.73rem', color: '#64748B', display: 'block', marginTop: '0.25rem' }}>
                Cursos prioritarios de I a IV ciclo.
              </span>
            </div>

            {/* Campo: Unidad Temática Silábica */}
            <div>
              <label
                htmlFor="select-topic"
                style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1E293B', marginBottom: '0.35rem' }}
              >
                2. Unidad Temática / Tema Conceptual del Sílabo *
              </label>
              <select
                id="select-topic"
                aria-label="Unidad temática silábica"
                value={selectedTopicId}
                onChange={(e) => setSelectedTopicId(Number(e.target.value))}
                disabled={isSubmitting || topics.length === 0}
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '8px',
                  border: '1px solid #CBD5E1',
                  fontSize: '0.86rem',
                  backgroundColor: '#FFFFFF',
                  color: '#1E293B',
                }}
              >
                {topics.map((t) => (
                  <option key={t.id_tema} value={t.id_tema}>
                    [U{t.unidad_silabica}] {t.nombre_tema}
                  </option>
                ))}
              </select>
              <span style={{ fontSize: '0.73rem', color: '#64748B', display: 'block', marginTop: '0.25rem' }}>
                Unidades taxonómicas oficiales del plan de estudios.
              </span>
            </div>
          </div>

          {/* Fila 2: Modalidad y Aforo Inmutable (RN-05) */}
          <div
            style={{
              backgroundColor: '#F8FAFC',
              borderRadius: '10px',
              border: '1px solid #E2E8F0',
              padding: '1.25rem',
              marginBottom: '1.25rem',
            }}
          >
            <div
              style={{
                display: 'grid',
                gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
                gap: '1.25rem',
                alignItems: 'center',
              }}
            >
              {/* Selector de Modalidad */}
              <div>
                <label
                  style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1E293B', marginBottom: '0.45rem' }}
                >
                  3. Modalidad Pedagógica *
                </label>
                <div style={{ display: 'flex', gap: '0.75rem' }}>
                  <button
                    type="button"
                    aria-pressed={modality === 'presencial'}
                    onClick={() => handleModalityChange('presencial')}
                    style={{
                      flex: 1,
                      padding: '0.65rem 0.9rem',
                      borderRadius: '8px',
                      border: modality === 'presencial' ? '2px solid #1C2A59' : '1px solid #CBD5E1',
                      backgroundColor: modality === 'presencial' ? '#1C2A59' : '#FFFFFF',
                      color: modality === 'presencial' ? '#FFFFFF' : '#475569',
                      fontWeight: 700,
                      fontSize: '0.84rem',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '0.4rem',
                      transition: 'all 0.15s ease',
                    }}
                  >
                    <span>🏢</span> Presencial
                  </button>

                  <button
                    type="button"
                    aria-pressed={modality === 'virtual'}
                    onClick={() => handleModalityChange('virtual')}
                    style={{
                      flex: 1,
                      padding: '0.65rem 0.9rem',
                      borderRadius: '8px',
                      border: modality === 'virtual' ? '2px solid #1C2A59' : '1px solid #CBD5E1',
                      backgroundColor: modality === 'virtual' ? '#1C2A59' : '#FFFFFF',
                      color: modality === 'virtual' ? '#FFFFFF' : '#475569',
                      fontWeight: 700,
                      fontSize: '0.84rem',
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      gap: '0.4rem',
                      transition: 'all 0.15s ease',
                    }}
                  >
                    <span>🌐</span> Virtual
                  </button>
                </div>
              </div>

              {/* Aforo Reglamentario Automático (RN-05) */}
              <div>
                <label
                  htmlFor="input-capacity"
                  style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1E293B', marginBottom: '0.45rem' }}
                >
                  4. Aforo Reglamentario Inmutable 🔒
                </label>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                  <input
                    id="input-capacity"
                    aria-label="Aforo reglamentario"
                    type="text"
                    readOnly
                    value={`${currentCapacity} Estudiantes`}
                    style={{
                      width: '140px',
                      padding: '0.65rem 0.85rem',
                      borderRadius: '8px',
                      border: '1px solid #94A3B8',
                      backgroundColor: '#E2E8F0',
                      color: '#0F172A',
                      fontWeight: 800,
                      fontSize: '0.9rem',
                      textAlign: 'center',
                    }}
                  />
                  <span
                    style={{
                      fontSize: '0.74rem',
                      color: '#475569',
                      lineHeight: 1.3,
                    }}
                  >
                    {modality === 'presencial'
                      ? 'Límite institucional de 10 participantes para sesiones presenciales.'
                      : 'Límite institucional de 20 participantes para sesiones virtuales.'}
                  </span>
                </div>
              </div>
            </div>
          </div>

          {/* Fila 3: Fecha, Hora, Antelación (RN-04) y Duración */}
          <div
            style={{
              display: 'grid',
              gridTemplateColumns: 'repeat(auto-fit, minmax(260px, 1fr))',
              gap: '1.25rem',
              marginBottom: '1.25rem',
            }}
          >
            {/* Fecha y Hora */}
            <div>
              <label
                htmlFor="input-datetime"
                style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1E293B', marginBottom: '0.35rem' }}
              >
                5. Fecha y Hora de Inicio *
              </label>
              <input
                id="input-datetime"
                aria-label="Fecha y hora de inicio"
                type="datetime-local"
                value={startDateTime}
                onChange={(e) => setStartDateTime(e.target.value)}
                disabled={isSubmitting}
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '8px',
                  border: validation.errors.fecha_inicio ? '1px solid #EF4444' : '1px solid #CBD5E1',
                  fontSize: '0.86rem',
                  backgroundColor: '#FFFFFF',
                  color: '#1E293B',
                }}
              />

              {/* Indicador reactivo de antelación y validación de RN-04 */}
              <div style={{ marginTop: '0.45rem' }}>
                {hoursAdvance < 0 ? (
                  <span style={{ color: '#DC2626', fontSize: '0.74rem', fontWeight: 600 }}>
                    ⚠️ Ingrese una fecha válida en el futuro.
                  </span>
                ) : hoursAdvance <= 24 ? (
                  <div
                    role="alert"
                    style={{
                      backgroundColor: '#FEF2F2',
                      border: '1px solid #FCA5A5',
                      borderRadius: '6px',
                      padding: '0.45rem 0.65rem',
                      color: '#B91C1C',
                      fontSize: '0.74rem',
                      lineHeight: 1.35,
                    }}
                  >
                    <strong>⚠️ Antelación insuficiente ({hoursAdvance.toFixed(1)} h):</strong> Toda
                    mentoría debe publicarse con más de 24 horas de anticipación para garantizar la convocatoria.
                  </div>
                ) : hoursAdvance < 48 ? (
                  <div
                    style={{
                      backgroundColor: '#FFFBEB',
                      border: '1px solid #FDE68A',
                      borderRadius: '6px',
                      padding: '0.45rem 0.65rem',
                      color: '#92400E',
                      fontSize: '0.74rem',
                      lineHeight: 1.35,
                    }}
                  >
                    <strong>ℹ️ Antelación válida ({hoursAdvance.toFixed(1)} h &gt; 24 h):</strong> Recomendación
                    institucional: se aconseja programar con al menos 48 h de antelación para optimizar la indexación en
                    el recomendador.
                  </div>
                ) : (
                  <div
                    style={{
                      backgroundColor: '#F0FDF4',
                      border: '1px solid #BBF7D0',
                      borderRadius: '6px',
                      padding: '0.45rem 0.65rem',
                      color: '#166534',
                      fontSize: '0.74rem',
                      lineHeight: 1.35,
                    }}
                  >
                    <strong>✅ Antelación óptima ({hoursAdvance.toFixed(1)} h &ge; 48 h):</strong> Cumple holgadamente el
                    estándar recomendado institucional para difusión y recomendación.
                  </div>
                )}
              </div>
            </div>

            {/* Duración en Bloques Lectivos */}
            <div>
              <label
                htmlFor="select-duration"
                style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1E293B', marginBottom: '0.35rem' }}
              >
                6. Duración de la Sesión *
              </label>
              <select
                id="select-duration"
                aria-label="Duración de la sesión"
                value={duration}
                onChange={(e) => setDuration(Number(e.target.value) as SessionDuration)}
                disabled={isSubmitting}
                style={{
                  width: '100%',
                  padding: '0.65rem 0.85rem',
                  borderRadius: '8px',
                  border: '1px solid #CBD5E1',
                  fontSize: '0.86rem',
                  backgroundColor: '#FFFFFF',
                  color: '#1E293B',
                }}
              >
                <option value={60}>60 minutos (1 hora pedagógica)</option>
                <option value={90}>90 minutos (1.5 horas pedagógicas)</option>
              </select>
              <span style={{ fontSize: '0.73rem', color: '#64748B', display: 'block', marginTop: '0.25rem' }}>
                {estimatedEndTime ? `Término estimado: ${estimatedEndTime}` : 'Bloques lectivos oficiales de 60 o 90 min.'}
              </span>
            </div>
          </div>

          {/* Fila 4: Infraestructura Asignada (RN-06 / RN-07) */}
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '10px',
              border: '1px solid #E2E8F0',
              padding: '1.25rem',
              marginBottom: '1.25rem',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.45rem' }}>
              <label
                htmlFor="input-space"
                style={{ fontSize: '0.82rem', fontWeight: 700, color: '#1E293B' }}
              >
                7. Asignación de Infraestructura ({modality === 'presencial' ? 'Aula / Laboratorio' : 'Enlace Virtual'}) *
              </label>
              <span
                style={{
                  fontSize: '0.72rem',
                  fontWeight: 700,
                  color: modality === 'presencial' ? '#047857' : '#4338CA',
                  backgroundColor: modality === 'presencial' ? '#D1FAE5' : '#EEF2FF',
                  padding: '0.15rem 0.5rem',
                  borderRadius: '4px',
                }}
              >
                {modality === 'presencial' ? 'Aula / Laboratorio' : 'Aprovisionamiento Virtual'}
              </span>
            </div>

            {modality === 'presencial' ? (
              <div>
                <select
                  id="input-space"
                  aria-label="Aula o laboratorio asignado"
                  value={assignedSpace}
                  onChange={(e) => setAssignedSpace(e.target.value)}
                  disabled={isSubmitting}
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.85rem',
                    borderRadius: '8px',
                    border: '1px solid #CBD5E1',
                    fontSize: '0.86rem',
                    backgroundColor: '#FFFFFF',
                    color: '#1E293B',
                  }}
                >
                  {SUGGESTED_CLASSROOMS.map((room) => (
                    <option key={room} value={room}>
                      {room}
                    </option>
                  ))}
                </select>
                <span style={{ fontSize: '0.73rem', color: '#64748B', display: 'block', marginTop: '0.35rem' }}>
                  Recinto sugerido por el parser de cronogramas EPIS sin cruces con la carga lectiva regular.
                </span>
              </div>
            ) : (
              <div>
                <div style={{ display: 'flex', gap: '0.5rem' }}>
                  <input
                    id="input-space"
                    aria-label="Enlace de teleconferencia virtual"
                    placeholder="https://meet.google.com/xxx-yyyy-zzz o Teams/Zoom"
                    type="text"
                    value={assignedSpace}
                    onChange={(e) => setAssignedSpace(e.target.value)}
                    disabled={isSubmitting}
                    style={{
                      flex: 1,
                      padding: '0.65rem 0.85rem',
                      borderRadius: '8px',
                      border: '1px solid #CBD5E1',
                      fontSize: '0.86rem',
                      backgroundColor: '#FFFFFF',
                      color: '#1E293B',
                    }}
                  />
                  <button
                    type="button"
                    onClick={() =>
                      setAssignedSpace(offerService.generateVirtualLink(currentCourse ? currentCourse.codigo_curso : 'epis'))
                    }
                    disabled={isSubmitting}
                    title="Generar automáticamente por el sistema"
                    style={{
                      backgroundColor: '#EEF2FF',
                      color: '#4338CA',
                      border: '1px solid #C7D2FE',
                      borderRadius: '8px',
                      padding: '0.5rem 0.85rem',
                      fontSize: '0.78rem',
                      fontWeight: 700,
                      cursor: 'pointer',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    🔄 Generar automáticamente por el sistema
                  </button>
                </div>
                <span style={{ fontSize: '0.73rem', color: '#64748B', display: 'block', marginTop: '0.35rem' }}>
                  Ingresa tu propio enlace de Google Meet, Zoom o Teams, o pulsa "Generar automáticamente por el sistema".
                </span>
              </div>
            )}
          </div>

          {/* Fila 5: Observaciones Pedagógicas (Opcional) */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label
              htmlFor="textarea-notes"
              style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1E293B', marginBottom: '0.35rem' }}
            >
              8. Observaciones Pedagógicas y Requisitos Previos (Opcional)
            </label>
            <textarea
              id="textarea-notes"
              aria-label="Observaciones pedagógicas"
              rows={2}
              value={additionalNotes}
              onChange={(e) => setAdditionalNotes(e.target.value)}
              disabled={isSubmitting}
              placeholder="Ej. Traer guía de ejercicios N° 2 resuelta. Sesión orientada a la preparación de la práctica calificada."
              style={{
                width: '100%',
                padding: '0.65rem 0.85rem',
                borderRadius: '8px',
                border: '1px solid #CBD5E1',
                fontSize: '0.84rem',
                backgroundColor: '#FFFFFF',
                color: '#1E293B',
                resize: 'vertical',
              }}
            />
          </div>

          {/* Botón de Publicación */}
          <div
            style={{
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
              flexWrap: 'wrap',
              gap: '1rem',
              borderTop: '1px solid #F1F5F9',
              paddingTop: '1.25rem',
            }}
          >
            <div style={{ fontSize: '0.78rem', color: '#64748B' }}>
              {!validation.isValid && (
                <span style={{ color: '#DC2626', fontWeight: 600 }}>
                  ⚠️ Corrija los campos señalados antes de publicar.
                </span>
              )}
            </div>

            <button
              type="submit"
              disabled={!validation.isValid || isSubmitting}
              style={{
                backgroundColor: !validation.isValid || isSubmitting ? '#94A3B8' : '#1C2A59',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '8px',
                padding: '0.75rem 1.75rem',
                fontSize: '0.92rem',
                fontWeight: 700,
                cursor: !validation.isValid || isSubmitting ? 'not-allowed' : 'pointer',
                boxShadow: !validation.isValid || isSubmitting ? 'none' : '0 2px 4px rgba(28, 42, 89, 0.25)',
                transition: 'all 0.2s ease',
              }}
            >
              {isSubmitting ? 'Publicando Oferta...' : '🚀 Publicar Oferta de Mentoría'}
            </button>
          </div>
        </form>
      </div>

      {/* Historial de Ofertas Publicadas por este Mentor en la Sesión */}
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #E2E8F0',
          padding: '1.5rem',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
          <div>
            <h4 style={{ margin: 0, color: '#1C2A59', fontSize: '1.1rem', fontWeight: 800 }}>
              Mis Ofertas de Mentoría Publicadas
            </h4>
            <span style={{ fontSize: '0.78rem', color: '#64748B' }}>
              Sesiones activas registradas por el mentor {mentorName}.
            </span>
          </div>
          <span
            style={{
              backgroundColor: '#F1F5F9',
              color: '#475569',
              fontSize: '0.75rem',
              fontWeight: 700,
              padding: '0.2rem 0.6rem',
              borderRadius: '9999px',
            }}
          >
            Total: {recentOffers.length}
          </span>
        </div>

        {recentOffers.length === 0 ? (
          <div
            style={{
              textAlign: 'center',
              padding: '2rem 1rem',
              backgroundColor: '#F8FAFC',
              borderRadius: '8px',
              border: '1px dashed #CBD5E1',
              color: '#64748B',
              fontSize: '0.84rem',
            }}
          >
            Aún no has publicado ofertas de mentoría. Completa el formulario superior para
            publicar tu primera clase grupal.
          </div>
        ) : (
          <div style={{ display: 'grid', gap: '0.75rem' }}>
            {recentOffers.map((item) => (
              <div
                key={item.id_oferta}
                style={{
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                  padding: '0.85rem 1rem',
                  borderRadius: '8px',
                  border: '1px solid #E2E8F0',
                  backgroundColor: '#F8FAFC',
                  flexWrap: 'wrap',
                  gap: '0.75rem',
                }}
              >
                <div>
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.2rem' }}>
                    <span
                      style={{
                        backgroundColor: '#1C2A59',
                        color: '#FFFFFF',
                        fontWeight: 700,
                        fontSize: '0.7rem',
                        padding: '0.15rem 0.45rem',
                        borderRadius: '4px',
                      }}
                    >
                      {item.codigo_sesion}
                    </span>
                    <strong style={{ color: '#0F172A', fontSize: '0.88rem' }}>
                      {item.offer.nombre_asignatura} ({item.offer.codigo_asignatura})
                    </strong>
                    <span
                      style={{
                        backgroundColor: item.offer.modalidad === 'presencial' ? '#D1FAE5' : '#EEF2FF',
                        color: item.offer.modalidad === 'presencial' ? '#065F46' : '#3730A3',
                        fontSize: '0.7rem',
                        fontWeight: 700,
                        padding: '0.1rem 0.4rem',
                        borderRadius: '4px',
                        textTransform: 'capitalize',
                      }}
                    >
                      {item.offer.modalidad} · {item.aforo} cupos
                    </span>
                  </div>
                  <div style={{ color: '#475569', fontSize: '0.8rem' }}>
                    Tema: <em>{item.offer.nombre_tema}</em> · Recinto: <span>{item.espacio_asignado}</span>
                  </div>
                </div>

                <div style={{ textAlign: 'right', fontSize: '0.76rem', color: '#64748B' }}>
                  <div>
                    📅{' '}
                    {new Date(item.offer.fecha_inicio).toLocaleString('es-PE', {
                      dateStyle: 'short',
                      timeStyle: 'short',
                    })}
                  </div>
                  <span
                    style={{
                      backgroundColor: '#10B981',
                      color: '#FFFFFF',
                      fontSize: '0.68rem',
                      fontWeight: 700,
                      padding: '0.1rem 0.4rem',
                      borderRadius: '9999px',
                    }}
                  >
                    {item.estado}
                  </span>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};
