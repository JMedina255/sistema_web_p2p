/**
 * Componente: Feed Interactivo de Recomendaciones Top-k (T-20)
 *
 * Trazabilidad:
 * - Requerimiento Funcional: RF06 (Inferencia de recomendaciones Top-k y ordenamiento afín)
 * - Requerimiento Funcional: RF07 / CUS03 (Empty-state con orientación a solicitudes por demanda)
 * - Requerimiento Funcional: RF24 / CUS12 (Priorización y distinción de materias críticas)
 * - Regla de Negocio RN-03: Mérito académico de mentores (ciclos VII a X)
 * - Regla de Negocio RN-04: Exclusión de sesiones vencidas o con antelación <= 24 h
 * - Regla de Negocio RN-05: Aforos estándar inmutables (10 presencial / 20 virtual)
 * - Regla de Negocio RN-11: Ponderadores curriculares (1.0x a 1.3x) y clave determinista
 * - Requerimiento No Funcional: RNF03 (Explicabilidad algorítmica XAI)
 * - Requerimiento No Funcional: RNF05 (Accesibilidad WAI-ARIA y diseño responsive)
 */

import React, { useState, useEffect, useCallback, useId } from 'react';
import {
  recommendationService,
  type OfferRecommendationItem,
  type MentorRecommendationItem,
  type ScoreBreakdown,
  type RecommendationListResponse,
} from '../services/recommendationService';
import { fetchCourses, type Course } from '../services/apiClient';

export interface RecommendationFeedViewProps {
  menteeEmail?: string;
  onSelectOffer?: (offer: OfferRecommendationItem) => void;
  onSelectMentor?: (mentor: MentorRecommendationItem) => void;
  onRequestDemand?: () => void;
}

type TabType = 'offers' | 'mentors';

export const RecommendationFeedView: React.FC<RecommendationFeedViewProps> = ({
  menteeEmail = '2022074255@upt.pe',
  onSelectOffer,
  onSelectMentor,
  onRequestDemand,
}) => {
  const componentId = useId();

  // Estados de navegación
  const [activeTab, setActiveTab] = useState<TabType>('offers');
  const [expandedItems, setExpandedItems] = useState<Record<string, boolean>>({});

  // Filtros
  const [selectedCourseId, setSelectedCourseId] = useState<number | undefined>(undefined);
  const [topK, setTopK] = useState<number>(5);
  const [coursesList, setCoursesList] = useState<Course[]>([]);

  // Datos de recomendaciones
  const [offersData, setOffersData] = useState<RecommendationListResponse<OfferRecommendationItem> | null>(null);
  const [mentorsData, setMentorsData] = useState<RecommendationListResponse<MentorRecommendationItem> | null>(null);

  // Estados de interfaz
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);

  // Cargar catálogo de asignaturas para el filtro opcional
  useEffect(() => {
    let isMounted = true;
    async function loadCatalog() {
      try {
        const courses = await fetchCourses(false);
        if (isMounted) {
          setCoursesList(courses);
        }
      } catch {
        // Silencioso: si la API curricular falla, el filtro de curso opera con todas
      }
    }
    loadCatalog();
    return () => {
      isMounted = false;
    };
  }, []);

  // Cargar recomendaciones según la pestaña activa y filtros
  const loadRecommendations = useCallback(async () => {
    setIsLoading(true);
    setErrorMessage(null);

    try {
      if (activeTab === 'offers') {
        const response = await recommendationService.getRecommendedOffers({
          mentee_email: menteeEmail,
          id_asignatura: selectedCourseId,
          top_k: topK,
        });
        setOffersData(response);
      } else {
        const response = await recommendationService.getRecommendedMentors({
          mentee_email: menteeEmail,
          top_k: topK,
        });
        setMentorsData(response);
      }
    } catch (err: unknown) {
      const msg = err instanceof Error ? err.message : 'Error al consultar el servicio de recomendaciones.';
      setErrorMessage(msg);
    } finally {
      setIsLoading(false);
    }
  }, [activeTab, menteeEmail, selectedCourseId, topK]);

  useEffect(() => {
    loadRecommendations();
  }, [loadRecommendations]);

  // Alternar expansión del desglose explicable (XAI)
  const toggleExpand = (itemId: string) => {
    setExpandedItems((prev) => ({
      ...prev,
      [itemId]: !prev[itemId],
    }));
  };

  // Helper para renderizar barra de afinidad con color institucional
  const renderAffinityBar = (score: number, label: string) => {
    const percentage = Math.min(100, Math.max(0, Math.round(score * 100)));
    let barColor = '#059669'; // Verde óptimo
    if (percentage < 50) barColor = '#DC2626'; // Rojo bajo
    else if (percentage < 75) barColor = '#D97706'; // Ámbar medio

    return (
      <div style={{ marginTop: '0.5rem', marginBottom: '0.5rem' }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.82rem', marginBottom: '0.2rem' }}>
          <span style={{ fontWeight: 600, color: '#334155' }}>{label}</span>
          <span style={{ fontWeight: 700, color: barColor }}>{percentage}%</span>
        </div>
        <div
          role="progressbar"
          aria-valuenow={percentage}
          aria-valuemin={0}
          aria-valuemax={100}
          aria-label={label}
          style={{
            height: '8px',
            backgroundColor: '#E2E8F0',
            borderRadius: '9999px',
            overflow: 'hidden',
          }}
        >
          <div
            style={{
              width: `${percentage}%`,
              height: '100%',
              backgroundColor: barColor,
              borderRadius: '9999px',
              transition: 'width 0.4s ease',
            }}
          />
        </div>
      </div>
    );
  };

  // Renderizar componente de desglose explicable individual (XAI)
  const renderExplainabilityPanel = (breakdown: ScoreBreakdown, itemId: string) => {
    const isExpanded = Boolean(expandedItems[itemId]);
    const panelId = `xai-panel-${componentId}-${itemId}`;
    const buttonId = `xai-btn-${componentId}-${itemId}`;

    return (
      <div style={{ marginTop: '0.85rem', borderTop: '1px solid #E2E8F0', paddingTop: '0.75rem' }}>
        <button
          id={buttonId}
          type="button"
          onClick={() => toggleExpand(itemId)}
          aria-expanded={isExpanded}
          aria-controls={panelId}
          style={{
            display: 'inline-flex',
            alignItems: 'center',
            gap: '0.4rem',
            background: 'none',
            border: 'none',
            color: '#1C2A59',
            fontSize: '0.85rem',
            fontWeight: 600,
            cursor: 'pointer',
            padding: '0.2rem 0',
          }}
        >
          <span>{isExpanded ? '▼ Ocultar desglose de compatibilidad' : '▶ Ver desglose de compatibilidad (XAI)'}</span>
        </button>

        {isExpanded && (
          <div
            id={panelId}
            role="region"
            aria-labelledby={buttonId}
            style={{
              marginTop: '0.75rem',
              backgroundColor: '#F8FAFC',
              border: '1px solid #CBD5E1',
              borderRadius: '8px',
              padding: '1rem',
            }}
          >
            {/* Resumen explicable en lenguaje natural */}
            <div
              style={{
                backgroundColor: '#EFF6FF',
                borderLeft: '4px solid #2563EB',
                padding: '0.65rem 0.85rem',
                borderRadius: '4px',
                marginBottom: '0.85rem',
                fontSize: '0.85rem',
                color: '#1E3A8A',
                lineHeight: '1.4',
              }}
            >
              <strong>Justificación algorítmica:</strong> {breakdown.explanation_text}
            </div>

            {/* Factores cuantitativos */}
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.85rem' }}>
              <div>
                {renderAffinityBar(breakdown.curricular_affinity, 'Afinidad Curricular')}
                {renderAffinityBar(breakdown.topic_overlap_jaccard, 'Similitud Temática Jaccard')}
                <div style={{ fontSize: '0.78rem', color: '#64748B', marginTop: '0.15rem' }}>
                  Índice de Dice: <strong>{(breakdown.topic_overlap_dice * 100).toFixed(1)}%</strong>
                </div>
              </div>

              <div>
                {renderAffinityBar(breakdown.schedule_compatibility, 'Compatibilidad Horaria')}
                <div style={{ fontSize: '0.8rem', color: '#475569', marginTop: '0.25rem' }}>
                  Franjas coincidentes: <strong>{breakdown.schedule_matching_slots_count}</strong>
                </div>
                {breakdown.matching_slots && breakdown.matching_slots.length > 0 && (
                  <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.35rem', marginTop: '0.4rem' }}>
                    {breakdown.matching_slots.map((slot, idx) => (
                      <span
                        key={idx}
                        style={{
                          backgroundColor: '#E2E8F0',
                          color: '#334155',
                          fontSize: '0.73rem',
                          padding: '0.15rem 0.45rem',
                          borderRadius: '4px',
                        }}
                      >
                        {slot}
                      </span>
                    ))}
                  </div>
                )}
              </div>
            </div>

            {/* Fila de Insignias y Ponderaciones Normativas */}
            <div
              style={{
                display: 'flex',
                flexWrap: 'wrap',
                gap: '0.6rem',
                alignItems: 'center',
                marginTop: '0.85rem',
                paddingTop: '0.65rem',
                borderTop: '1px dashed #CBD5E1',
                fontSize: '0.8rem',
              }}
            >
              {breakdown.course_weight_factor > 1.0 && (
                <span
                  style={{
                    backgroundColor: '#FEF3C7',
                    color: '#92400E',
                    border: '1px solid #F59E0B',
                    padding: '0.2rem 0.55rem',
                    borderRadius: '9999px',
                    fontWeight: 700,
                  }}
                >
                  ★ Multiplicador Prioritario: {breakdown.course_weight_factor.toFixed(1)}x
                  {breakdown.critical_course_applied && ` (${breakdown.critical_course_applied})`}
                </span>
              )}

              {breakdown.institutional_merit_eligible && (
                <span
                  style={{
                    backgroundColor: '#DCFCE7',
                    color: '#166534',
                    border: '1px solid #86EFAC',
                    padding: '0.2rem 0.55rem',
                    borderRadius: '9999px',
                    fontWeight: 600,
                  }}
                >
                  ✓ Mérito Docente Acreditado (RN-03: Ciclo VII-X)
                </span>
              )}

              <span
                style={{
                  backgroundColor: '#F1F5F9',
                  color: '#475569',
                  padding: '0.2rem 0.55rem',
                  borderRadius: '9999px',
                }}
              >
                Concordancia Modalidad: {Math.round(breakdown.modality_compatibility * 100)}%
              </span>
            </div>
          </div>
        )}
      </div>
    );
  };

  // Renderizar Cartelera de Ofertas Recomendadas (Top-k)
  const renderOffersList = () => {
    const items = offersData?.items || [];

    if (items.length === 0) {
      return renderEmptyState();
    }

    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        {items.map((offer, index) => {
          const isFull = offer.aforo_disponible <= 0;
          const isCritical = offer.breakdown.course_weight_factor > 1.0;

          return (
            <article
              key={offer.id_oferta || offer.codigo_sesion}
              style={{
                backgroundColor: '#FFFFFF',
                borderRadius: '12px',
                border: isCritical ? '2px solid #B99451' : '1px solid #E2E8F0',
                padding: '1.25rem 1.5rem',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
                position: 'relative',
              }}
            >
              {/* Encabezado de la Tarjeta */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.6rem', flexWrap: 'wrap' }}>
                  <span
                    style={{
                      backgroundColor: '#1C2A59',
                      color: '#FFFFFF',
                      fontSize: '0.75rem',
                      fontWeight: 700,
                      padding: '0.2rem 0.5rem',
                      borderRadius: '4px',
                      letterSpacing: '0.5px',
                    }}
                  >
                    #{index + 1} TOP-K
                  </span>
                  <span style={{ fontSize: '0.85rem', color: '#64748B', fontWeight: 600 }}>
                    {offer.codigo_sesion}
                  </span>
                  {isCritical && (
                    <span
                      style={{
                        backgroundColor: '#FEF3C7',
                        color: '#92400E',
                        border: '1px solid #F59E0B',
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        padding: '0.2rem 0.5rem',
                        borderRadius: '9999px',
                      }}
                    >
                      Prioridad Institucional EPIS ({offer.breakdown.course_weight_factor.toFixed(1)}x)
                    </span>
                  )}
                </div>

                {/* Score Total */}
                <div style={{ textAlign: 'right' }}>
                  <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#1C2A59' }}>
                    {Math.round(offer.score_total * 100)}%
                  </div>
                  <div style={{ fontSize: '0.72rem', color: '#64748B', fontWeight: 600, textTransform: 'uppercase' }}>
                    Afinidad Global
                  </div>
                </div>
              </div>

              {/* Título de Asignatura y Tema */}
              <h3 style={{ margin: '0.6rem 0 0.2rem 0', fontSize: '1.15rem', color: '#0F172A' }}>
                {offer.nombre_asignatura} ({offer.codigo_asignatura})
              </h3>
              <p style={{ margin: '0 0 0.85rem 0', fontSize: '0.92rem', color: '#475569', fontWeight: 500 }}>
                Tema: <strong>{offer.nombre_tema}</strong>
              </p>

              {/* Atributos Clave: Horario, Modalidad, Aforo y Mentor */}
              <div
                style={{
                  display: 'grid',
                  gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                  gap: '0.75rem',
                  backgroundColor: '#F8FAFC',
                  padding: '0.85rem 1rem',
                  borderRadius: '8px',
                  marginBottom: '0.85rem',
                  fontSize: '0.85rem',
                }}
              >
                <div>
                  <div style={{ color: '#64748B', fontSize: '0.75rem' }}>Fecha y Duración</div>
                  <div style={{ fontWeight: 600, color: '#1E293B', marginTop: '0.1rem' }}>
                    {offer.fecha_inicio.replace('T', ' ').substring(0, 16)} UTC ({offer.duracion_minutos} min)
                  </div>
                </div>

                <div>
                  <div style={{ color: '#64748B', fontSize: '0.75rem' }}>Modalidad y Espacio</div>
                  <div style={{ fontWeight: 600, color: '#1E293B', marginTop: '0.1rem' }}>
                    <span
                      style={{
                        display: 'inline-block',
                        padding: '0.1rem 0.4rem',
                        borderRadius: '4px',
                        backgroundColor: offer.modalidad === 'presencial' ? '#E0E7FF' : '#DCFCE7',
                        color: offer.modalidad === 'presencial' ? '#3730A3' : '#166534',
                        textTransform: 'capitalize',
                        marginRight: '0.4rem',
                        fontSize: '0.75rem',
                      }}
                    >
                      {offer.modalidad}
                    </span>
                    <span style={{ fontSize: '0.8rem', color: '#475569' }}>{offer.espacio_asignado}</span>
                  </div>
                </div>

                <div>
                  <div style={{ color: '#64748B', fontSize: '0.75rem' }}>Disponibilidad (RN-05)</div>
                  <div style={{ marginTop: '0.1rem' }}>
                    {isFull ? (
                      <span
                        style={{
                          backgroundColor: '#FEE2E2',
                          color: '#991B1B',
                          fontWeight: 700,
                          fontSize: '0.8rem',
                          padding: '0.15rem 0.5rem',
                          borderRadius: '4px',
                        }}
                      >
                        Aforo Completo (0 vacantes)
                      </span>
                    ) : (
                      <span style={{ fontWeight: 600, color: '#059669' }}>
                        {offer.aforo_disponible} vacantes libres / {offer.aforo_maximo} cupos
                      </span>
                    )}
                  </div>
                </div>

                <div>
                  <div style={{ color: '#64748B', fontSize: '0.75rem' }}>Estudiante Mentor (RN-03)</div>
                  <div style={{ fontWeight: 600, color: '#1E293B', marginTop: '0.1rem' }}>
                    {offer.mentor_nombre || offer.mentor_email} (Ciclo {offer.mentor_ciclo})
                  </div>
                </div>
              </div>

              {/* Botón de Acción Principal y Desglose */}
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem' }}>
                <div style={{ flex: 1 }}>{renderExplainabilityPanel(offer.breakdown, offer.id_oferta || offer.codigo_sesion)}</div>

                <div style={{ textAlign: 'right' }}>
                  <button
                    type="button"
                    disabled={isFull}
                    onClick={() => onSelectOffer?.(offer)}
                    style={{
                      backgroundColor: isFull ? '#94A3B8' : '#1C2A59',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '6px',
                      padding: '0.55rem 1.25rem',
                      fontSize: '0.88rem',
                      fontWeight: 600,
                      cursor: isFull ? 'not-allowed' : 'pointer',
                      boxShadow: isFull ? 'none' : '0 2px 4px rgba(28, 42, 89, 0.2)',
                    }}
                  >
                    {isFull ? 'Aforo Agotado' : 'Reservar Cupo'}
                  </button>
                </div>
              </div>
            </article>
          );
        })}
      </div>
    );
  };

  // Renderizar Vista de Mentores Recomendados (Top-k)
  const renderMentorsList = () => {
    const items = mentorsData?.items || [];

    if (items.length === 0) {
      return renderEmptyState();
    }

    return (
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1.25rem' }}>
        {items.map((mentor, index) => (
          <article
            key={mentor.mentor_email}
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              border: '1px solid #E2E8F0',
              padding: '1.25rem 1.5rem',
              boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.5rem' }}>
              <div>
                <span
                  style={{
                    backgroundColor: '#1C2A59',
                    color: '#FFFFFF',
                    fontSize: '0.75rem',
                    fontWeight: 700,
                    padding: '0.2rem 0.5rem',
                    borderRadius: '4px',
                    letterSpacing: '0.5px',
                    marginRight: '0.5rem',
                  }}
                >
                  #{index + 1} TOP-K MENTOR
                </span>
                <span
                  style={{
                    backgroundColor: '#DCFCE7',
                    color: '#166534',
                    border: '1px solid #86EFAC',
                    fontSize: '0.75rem',
                    fontWeight: 600,
                    padding: '0.15rem 0.5rem',
                    borderRadius: '9999px',
                  }}
                >
                  Ciclo {mentor.mentor_ciclo} (RN-03)
                </span>
                <h3 style={{ margin: '0.5rem 0 0.2rem 0', fontSize: '1.15rem', color: '#0F172A' }}>
                  {mentor.mentor_nombres} {mentor.mentor_apellidos}
                </h3>
                <div style={{ fontSize: '0.85rem', color: '#64748B' }}>
                  {mentor.mentor_email}
                  {mentor.mentor_codigo && ` • Código: ${mentor.mentor_codigo}`}
                </div>
              </div>

              <div style={{ textAlign: 'right' }}>
                <div style={{ fontSize: '1.25rem', fontWeight: 800, color: '#1C2A59' }}>
                  {Math.round(mentor.score_total * 100)}%
                </div>
                <div style={{ fontSize: '0.72rem', color: '#64748B', fontWeight: 600, textTransform: 'uppercase' }}>
                  Afinidad de Perfil
                </div>
              </div>
            </div>

            {/* Asignaturas impartidas */}
            <div style={{ marginTop: '0.85rem' }}>
              <div style={{ fontSize: '0.8rem', color: '#64748B', fontWeight: 600, marginBottom: '0.35rem' }}>
                Asignaturas de asesoría académica:
              </div>
              <div style={{ display: 'flex', flexWrap: 'wrap', gap: '0.4rem' }}>
                {mentor.materias_nombres.map((materia, idx) => (
                  <span
                    key={idx}
                    style={{
                      backgroundColor: '#EFF6FF',
                      color: '#1E40AF',
                      border: '1px solid #BFDBFE',
                      fontSize: '0.78rem',
                      padding: '0.2rem 0.55rem',
                      borderRadius: '6px',
                      fontWeight: 500,
                    }}
                  >
                    {materia}
                  </span>
                ))}
              </div>
            </div>

            {/* Modalidad preferida */}
            <div style={{ marginTop: '0.65rem', fontSize: '0.82rem', color: '#475569' }}>
              Modalidad formativa preferida:{' '}
              <strong style={{ textTransform: 'capitalize' }}>{mentor.modalidad_preferida}</strong>
            </div>

            {/* Desglose XAI y Acción */}
            <div style={{ marginTop: '0.65rem' }}>
              {renderExplainabilityPanel(mentor.breakdown, mentor.mentor_email)}
            </div>

            {onSelectMentor && (
              <div style={{ marginTop: '0.85rem', textAlign: 'right' }}>
                <button
                  type="button"
                  onClick={() => onSelectMentor(mentor)}
                  style={{
                    backgroundColor: '#B99451',
                    color: '#FFFFFF',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '0.45rem 1rem',
                    fontSize: '0.85rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                  }}
                >
                  Contactar / Solicitar Asesoría
                </button>
              </div>
            )}
          </article>
        ))}
      </div>
    );
  };

  // Renderizar Panel de Lista Vacía (Empty-State) con orientación a Solicitudes por Demanda (CUS03 / RF07)
  const renderEmptyState = () => {
    return (
      <div
        role="status"
        aria-label="No hay recomendaciones disponibles"
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px dashed #CBD5E1',
          padding: '2.5rem 1.5rem',
          textAlign: 'center',
          maxWidth: '700px',
          margin: '1.5rem auto',
        }}
      >
        <div
          style={{
            width: '56px',
            height: '56px',
            borderRadius: '50%',
            backgroundColor: '#FEF3C7',
            color: '#B99451',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            fontSize: '1.75rem',
            margin: '0 auto 1rem auto',
          }}
        >
          🔍
        </div>

        <h3 style={{ margin: '0 0 0.5rem 0', color: '#1C2A59', fontSize: '1.2rem' }}>
          No se encontraron recomendaciones en este momento
        </h3>

        <p style={{ margin: '0 0 1.25rem 0', color: '#64748B', fontSize: '0.92rem', lineHeight: '1.5' }}>
          No existen ofertas activas ni mentores disponibles que coincidan con la asignatura o franjas horarias
          de tu agenda semanal. Recuerda que las sesiones requieren antelación mayor a 24 horas (RN-04) y cupo libre (RN-05).
        </p>

        {/* Orientación Pedagógica conforme a CUS03 / RF07 */}
        <div
          style={{
            backgroundColor: '#F8FAFC',
            border: '1px solid #E2E8F0',
            borderRadius: '8px',
            padding: '1rem',
            fontSize: '0.88rem',
            color: '#334155',
            textAlign: 'left',
            marginBottom: '1rem',
          }}
        >
          <div style={{ fontWeight: 700, color: '#1C2A59', marginBottom: '0.3rem' }}>
            💡 ¿Necesitas asesoría en un tema específico? (RF07 / CUS03)
          </div>
          <div>
            Puedes registrar tu necesidad temática en el <strong>Banco de Solicitudes por Demanda</strong> para que un
            mentor par calificado de ciclos VII al X programe una nueva sesión de mentoría adaptada a tus horarios.
          </div>
        </div>

        {onRequestDemand && (
          <button
            type="button"
            onClick={onRequestDemand}
            style={{
              backgroundColor: '#B99451',
              color: '#FFFFFF',
              border: 'none',
              borderRadius: '6px',
              padding: '0.6rem 1.25rem',
              fontSize: '0.9rem',
              fontWeight: 600,
              cursor: 'pointer',
              boxShadow: '0 2px 4px rgba(185, 148, 81, 0.25)',
            }}
          >
            Registrar Solicitud por Demanda (CUS03)
          </button>
        )}
      </div>
    );
  };

  return (
    <div style={{ width: '100%', maxWidth: '1050px', margin: '0 auto', padding: '1rem 0' }}>
      {/* Encabezado Institucional del Feed */}
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          padding: '1.5rem',
          borderBottom: '3px solid #B99451',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
          marginBottom: '1.5rem',
        }}
      >
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '1rem' }}>
          <div>
            <h2 style={{ margin: 0, color: '#1C2A59', fontSize: '1.45rem', fontWeight: 800 }}>
              Cartelera Inteligente de Mentorías (EdRecSys v1.0)
            </h2>
            <p style={{ margin: '0.35rem 0 0 0', color: '#64748B', fontSize: '0.9rem' }}>
              Recomendaciones personalizadas por afinidad curricular, coincidencia horaria semanal y materias prioritarias EPIS.
            </p>
          </div>

          <button
            type="button"
            onClick={() => loadRecommendations()}
            disabled={isLoading}
            aria-label="Actualizar recomendaciones"
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.4rem',
              backgroundColor: '#F1F5F9',
              color: '#1C2A59',
              border: '1px solid #CBD5E1',
              borderRadius: '6px',
              padding: '0.5rem 0.9rem',
              fontSize: '0.85rem',
              fontWeight: 600,
              cursor: isLoading ? 'not-allowed' : 'pointer',
            }}
          >
            <span>🔄</span> Actualizar
          </button>
        </div>

        {/* Pestañas de Navegación Accesibles (WAI-ARIA) */}
        <div
          role="tablist"
          aria-label="Modo de exploración de recomendaciones"
          style={{
            display: 'flex',
            gap: '0.75rem',
            marginTop: '1.25rem',
            borderBottom: '1px solid #E2E8F0',
            paddingBottom: '0.5rem',
          }}
        >
          <button
            role="tab"
            id={`tab-${componentId}-offers`}
            aria-selected={activeTab === 'offers'}
            aria-controls={`panel-${componentId}-offers`}
            type="button"
            onClick={() => setActiveTab('offers')}
            style={{
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'offers' ? '3px solid #1C2A59' : '3px solid transparent',
              color: activeTab === 'offers' ? '#1C2A59' : '#64748B',
              fontWeight: activeTab === 'offers' ? 700 : 500,
              fontSize: '0.95rem',
              padding: '0.5rem 0.75rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            <span>📚 Sesiones Recomendadas</span>
            {offersData && offersData.recommendations_count > 0 && (
              <span
                style={{
                  backgroundColor: '#1C2A59',
                  color: '#FFFFFF',
                  fontSize: '0.72rem',
                  padding: '0.1rem 0.45rem',
                  borderRadius: '9999px',
                }}
              >
                {offersData.recommendations_count}
              </span>
            )}
          </button>

          <button
            role="tab"
            id={`tab-${componentId}-mentors`}
            aria-selected={activeTab === 'mentors'}
            aria-controls={`panel-${componentId}-mentors`}
            type="button"
            onClick={() => setActiveTab('mentors')}
            style={{
              background: 'none',
              border: 'none',
              borderBottom: activeTab === 'mentors' ? '3px solid #1C2A59' : '3px solid transparent',
              color: activeTab === 'mentors' ? '#1C2A59' : '#64748B',
              fontWeight: activeTab === 'mentors' ? 700 : 500,
              fontSize: '0.95rem',
              padding: '0.5rem 0.75rem',
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            <span>👨‍🏫 Mentores Académicos</span>
            {mentorsData && mentorsData.recommendations_count > 0 && (
              <span
                style={{
                  backgroundColor: '#B99451',
                  color: '#FFFFFF',
                  fontSize: '0.72rem',
                  padding: '0.1rem 0.45rem',
                  borderRadius: '9999px',
                }}
              >
                {mentorsData.recommendations_count}
              </span>
            )}
          </button>
        </div>

        {/* Controles de Filtro: Asignatura y Top-K */}
        <div
          style={{
            display: 'flex',
            flexWrap: 'wrap',
            gap: '1rem',
            alignItems: 'center',
            marginTop: '1rem',
            paddingTop: '0.5rem',
          }}
        >
          {activeTab === 'offers' && (
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <label
                htmlFor={`filter-course-${componentId}`}
                style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569' }}
              >
                Asignatura:
              </label>
              <select
                id={`filter-course-${componentId}`}
                value={selectedCourseId ?? ''}
                onChange={(e) => {
                  const val = e.target.value;
                  setSelectedCourseId(val === '' ? undefined : Number(val));
                }}
                style={{
                  padding: '0.4rem 0.65rem',
                  borderRadius: '6px',
                  border: '1px solid #CBD5E1',
                  fontSize: '0.85rem',
                  color: '#1E293B',
                  backgroundColor: '#FFFFFF',
                }}
              >
                <option value="">Todas las materias formativas</option>
                {coursesList.map((c) => (
                  <option key={c.id_asignatura} value={c.id_asignatura}>
                    {c.nombre_curso} ({c.codigo_curso})
                  </option>
                ))}
              </select>
            </div>
          )}

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
            <label htmlFor={`filter-topk-${componentId}`} style={{ fontSize: '0.85rem', fontWeight: 600, color: '#475569' }}>
              Candidatos Top-k:
            </label>
            <select
              id={`filter-topk-${componentId}`}
              value={topK}
              onChange={(e) => setTopK(Number(e.target.value))}
              style={{
                padding: '0.4rem 0.65rem',
                borderRadius: '6px',
                border: '1px solid #CBD5E1',
                fontSize: '0.85rem',
                color: '#1E293B',
                backgroundColor: '#FFFFFF',
              }}
            >
              <option value={3}>Top 3</option>
              <option value={4}>Top 4</option>
              <option value={5}>Top 5 (Estándar SRS)</option>
            </select>
          </div>
        </div>
      </div>

      {/* Manejo de Estados: Error, Carga o Contenido */}
      {errorMessage && (
        <div
          role="alert"
          style={{
            backgroundColor: '#FEF2F2',
            borderLeft: '4px solid #DC2626',
            color: '#991B1B',
            padding: '1rem 1.25rem',
            borderRadius: '8px',
            marginBottom: '1.25rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexWrap: 'wrap',
            gap: '0.5rem',
          }}
        >
          <div>
            <strong>Error de servicio:</strong> {errorMessage}
          </div>
          <button
            type="button"
            onClick={() => loadRecommendations()}
            style={{
              backgroundColor: '#DC2626',
              color: '#FFFFFF',
              border: 'none',
              borderRadius: '4px',
              padding: '0.35rem 0.75rem',
              fontSize: '0.8rem',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Reintentar
          </button>
        </div>
      )}

      {isLoading ? (
        <div
          role="status"
          aria-live="polite"
          style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '12px',
            padding: '3rem 1.5rem',
            textAlign: 'center',
            border: '1px solid #E2E8F0',
          }}
        >
          <div
            style={{
              display: 'inline-block',
              width: '36px',
              height: '36px',
              border: '3px solid #E2E8F0',
              borderTopColor: '#1C2A59',
              borderRadius: '50%',
              animation: 'spin 0.8s linear infinite',
              marginBottom: '0.75rem',
            }}
          />
          <div style={{ color: '#1C2A59', fontWeight: 600, fontSize: '0.95rem' }}>
            Calculando afinidad multifactorial con EdRecSys...
          </div>
          <div style={{ color: '#64748B', fontSize: '0.82rem', marginTop: '0.25rem' }}>
            Evaluando coincidencia curricular, temática silábica y agenda 6×11
          </div>
        </div>
      ) : (
        <div
          role="tabpanel"
          id={activeTab === 'offers' ? `panel-${componentId}-offers` : `panel-${componentId}-mentors`}
          aria-labelledby={activeTab === 'offers' ? `tab-${componentId}-offers` : `tab-${componentId}-mentors`}
        >
          {activeTab === 'offers' ? renderOffersList() : renderMentorsList()}
        </div>
      )}
    </div>
  );
};
