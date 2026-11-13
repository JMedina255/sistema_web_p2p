import React, { useState, useEffect, useCallback, useMemo } from 'react';
import {
  fetchCourses,
  fetchCourseDetail,
  createCourse,
  updateCourse,
  deleteCourse,
  createTopic,
  updateTopic,
  deleteTopic,
} from '../services/apiClient';
import type {
  Course,
  CourseDetail,
  Topic,
  CourseCreatePayload,
  CourseUpdatePayload,
  TopicCreatePayload,
  TopicUpdatePayload,
} from '../services/apiClient';
import { useAuth } from '../context/AuthContext';

export interface CurriculumCatalogViewProps {
  isAdmin?: boolean;
}

export const CurriculumCatalogView: React.FC<CurriculumCatalogViewProps> = ({ isAdmin: propIsAdmin }) => {
  // Verificación de privilegios administrativos
  let contextIsAdmin = false;
  try {
    const auth = useAuth();
    contextIsAdmin = auth?.activeRole === 'administrador' || Boolean(auth?.user?.roles?.includes('administrador'));
  } catch {
    // Fuera de AuthProvider en tests aislados
  }
  const effectiveIsAdmin = propIsAdmin !== undefined ? propIsAdmin : contextIsAdmin;

  const [courses, setCourses] = useState<Course[]>([]);
  const [courseDetailsMap, setCourseDetailsMap] = useState<Record<number, CourseDetail>>({});
  const [selectedCourseId, setSelectedCourseId] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [onlyPriority, setOnlyPriority] = useState<boolean>(true);
  const [selectedCiclo, setSelectedCiclo] = useState<number | undefined>(undefined);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);
  const [feedback, setFeedback] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  // Estados de modales administrativos (RF05 / CUS21)
  const [isCourseModalOpen, setIsCourseModalOpen] = useState<boolean>(false);
  const [editingCourse, setEditingCourse] = useState<Course | null>(null);
  const [courseFormData, setCourseFormData] = useState({
    codigo_curso: '',
    nombre_curso: '',
    ciclo_plan: 1,
    creditos: 4,
    factor_ponderacion: 1.0,
    es_prioritaria: true,
  });

  const [isTopicModalOpen, setIsTopicModalOpen] = useState<boolean>(false);
  const [editingTopic, setEditingTopic] = useState<Topic | null>(null);
  const [topicFormData, setTopicFormData] = useState({
    nombre_tema: '',
    unidad_silabica: 1,
    descripcion_silabo: '',
  });

  const [actionLoading, setActionLoading] = useState<boolean>(false);

  // Carga inicial y por filtros de asignaturas
  const loadCourses = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchCourses(onlyPriority, selectedCiclo);
      setCourses(data);

      if (data.length > 0) {
        const firstId = data[0].id_asignatura;
        setSelectedCourseId((prev) => (prev && data.some((c) => c.id_asignatura === prev) ? prev : firstId));

        data.forEach(async (c) => {
          try {
            const detail = await fetchCourseDetail(c.id_asignatura);
            setCourseDetailsMap((prev) => ({ ...prev, [c.id_asignatura]: detail }));
          } catch {
            // Silencioso
          }
        });
      } else {
        setSelectedCourseId(null);
      }
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Error al consultar catálogo curricular.');
    } finally {
      setIsLoading(false);
    }
  }, [onlyPriority, selectedCiclo]);

  useEffect(() => {
    loadCourses();
  }, [loadCourses]);

  // Selección de curso
  const handleSelectCourse = async (courseId: number) => {
    setSelectedCourseId(courseId);
    if (!courseDetailsMap[courseId]) {
      try {
        const detail = await fetchCourseDetail(courseId);
        setCourseDetailsMap((prev) => ({ ...prev, [courseId]: detail }));
      } catch (err: unknown) {
        setError(err instanceof Error ? err.message : 'Error al cargar detalle de asignatura.');
      }
    }
  };

  // Filtrado reactivo en memoria
  const filteredCourses = useMemo(() => {
    if (!searchTerm.trim()) return courses;
    const term = searchTerm.toLowerCase().trim();

    return courses.filter((course) => {
      const matchesCourse =
        course.nombre_curso.toLowerCase().includes(term) ||
        course.codigo_curso.toLowerCase().includes(term);

      if (matchesCourse) return true;

      const detail = courseDetailsMap[course.id_asignatura];
      if (detail && detail.temas) {
        return detail.temas.some(
          (t) =>
            t.nombre_tema.toLowerCase().includes(term) ||
            (t.descripcion_silabo && t.descripcion_silabo.toLowerCase().includes(term))
        );
      }

      return false;
    });
  }, [courses, searchTerm, courseDetailsMap]);

  const selectedCourseDetail = selectedCourseId ? courseDetailsMap[selectedCourseId] : null;

  // Apertura modal de curso (nuevo / editar)
  const openNewCourseModal = () => {
    setEditingCourse(null);
    setCourseFormData({
      codigo_curso: '',
      nombre_curso: '',
      ciclo_plan: 1,
      creditos: 4,
      factor_ponderacion: 1.0,
      es_prioritaria: true,
    });
    setIsCourseModalOpen(true);
  };

  const openEditCourseModal = (c: Course, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();
    setEditingCourse(c);
    setCourseFormData({
      codigo_curso: c.codigo_curso,
      nombre_curso: c.nombre_curso,
      ciclo_plan: c.ciclo_plan,
      creditos: c.creditos,
      factor_ponderacion: c.factor_ponderacion || 1.0,
      es_prioritaria: c.es_prioritaria,
    });
    setIsCourseModalOpen(true);
  };

  // Guardar curso (crear o editar)
  const handleSaveCourse = async (e: React.FormEvent) => {
    e.preventDefault();
    setActionLoading(true);
    setFeedback(null);
    try {
      if (editingCourse) {
        const payload: CourseUpdatePayload = {
          codigo_curso: courseFormData.codigo_curso.trim().toUpperCase(),
          nombre_curso: courseFormData.nombre_curso.trim(),
          ciclo_plan: Number(courseFormData.ciclo_plan),
          creditos: Number(courseFormData.creditos),
          factor_ponderacion: Number(courseFormData.factor_ponderacion),
          es_prioritaria: courseFormData.es_prioritaria,
        };
        await updateCourse(editingCourse.id_asignatura, payload);
        setFeedback({ text: `Asignatura "${payload.nombre_curso}" actualizada con éxito.`, type: 'success' });
      } else {
        const payload: CourseCreatePayload = {
          codigo_curso: courseFormData.codigo_curso.trim().toUpperCase(),
          nombre_curso: courseFormData.nombre_curso.trim(),
          ciclo_plan: Number(courseFormData.ciclo_plan),
          creditos: Number(courseFormData.creditos),
          factor_ponderacion: Number(courseFormData.factor_ponderacion),
          es_prioritaria: courseFormData.es_prioritaria,
        };
        await createCourse(payload);
        setFeedback({ text: `Nueva asignatura "${payload.nombre_curso}" registrada con éxito en el catálogo oficial (RF05).`, type: 'success' });
      }
      setIsCourseModalOpen(false);
      await loadCourses();
    } catch (err: unknown) {
      setFeedback({ text: err instanceof Error ? err.message : 'Error al guardar asignatura.', type: 'error' });
    } finally {
      setActionLoading(false);
    }
  };

  // Desactivar curso
  const handleDeleteCourse = async (c: Course, e?: React.MouseEvent) => {
    if (e) e.stopPropagation();
    if (!window.confirm(`¿Está seguro de desactivar la asignatura "${c.codigo_curso} - ${c.nombre_curso}" del catálogo oficial?`)) {
      return;
    }
    setActionLoading(true);
    setFeedback(null);
    try {
      await deleteCourse(c.id_asignatura);
      setFeedback({ text: `Asignatura ${c.codigo_curso} desactivada correctamente.`, type: 'success' });
      await loadCourses();
    } catch (err: unknown) {
      setFeedback({ text: err instanceof Error ? err.message : 'Error al desactivar asignatura.', type: 'error' });
    } finally {
      setActionLoading(false);
    }
  };

  // Apertura modal de tema (nuevo / editar)
  const openNewTopicModal = () => {
    if (!selectedCourseId) return;
    setEditingTopic(null);
    setTopicFormData({
      nombre_tema: '',
      unidad_silabica: 1,
      descripcion_silabo: '',
    });
    setIsTopicModalOpen(true);
  };

  const openEditTopicModal = (t: Topic) => {
    setEditingTopic(t);
    setTopicFormData({
      nombre_tema: t.nombre_tema,
      unidad_silabica: t.unidad_silabica,
      descripcion_silabo: t.descripcion_silabo || '',
    });
    setIsTopicModalOpen(true);
  };

  // Guardar tema
  const handleSaveTopic = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!selectedCourseId) return;
    setActionLoading(true);
    setFeedback(null);
    try {
      if (editingTopic) {
        const payload: TopicUpdatePayload = {
          nombre_tema: topicFormData.nombre_tema.trim(),
          unidad_silabica: Number(topicFormData.unidad_silabica),
          descripcion_silabo: topicFormData.descripcion_silabo.trim(),
        };
        await updateTopic(editingTopic.id_tema, payload);
        setFeedback({ text: `Tema "${payload.nombre_tema}" actualizado con éxito.`, type: 'success' });
      } else {
        const payload: TopicCreatePayload = {
          nombre_tema: topicFormData.nombre_tema.trim(),
          unidad_silabica: Number(topicFormData.unidad_silabica),
          descripcion_silabo: topicFormData.descripcion_silabo.trim(),
          estado_activo: true,
        };
        await createTopic(selectedCourseId, payload);
        setFeedback({ text: `Tema silábico "${payload.nombre_tema}" incorporado al sílabo oficial (RF05).`, type: 'success' });
      }
      setIsTopicModalOpen(false);
      // Recargar detalle del curso actual
      const updatedDetail = await fetchCourseDetail(selectedCourseId);
      setCourseDetailsMap((prev) => ({ ...prev, [selectedCourseId]: updatedDetail }));
    } catch (err: unknown) {
      setFeedback({ text: err instanceof Error ? err.message : 'Error al guardar tema silábico.', type: 'error' });
    } finally {
      setActionLoading(false);
    }
  };

  // Desactivar tema
  const handleDeleteTopic = async (t: Topic) => {
    if (!window.confirm(`¿Está seguro de desactivar el tema "${t.nombre_tema}" del sílabo oficial?`)) {
      return;
    }
    if (!selectedCourseId) return;
    setActionLoading(true);
    setFeedback(null);
    try {
      await deleteTopic(t.id_tema);
      setFeedback({ text: `Tema "${t.nombre_tema}" desactivado con éxito.`, type: 'success' });
      const updatedDetail = await fetchCourseDetail(selectedCourseId);
      setCourseDetailsMap((prev) => ({ ...prev, [selectedCourseId]: updatedDetail }));
    } catch (err: unknown) {
      setFeedback({ text: err instanceof Error ? err.message : 'Error al desactivar tema.', type: 'error' });
    } finally {
      setActionLoading(false);
    }
  };

  // Cierre con Escape
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (isCourseModalOpen) setIsCourseModalOpen(false);
        if (isTopicModalOpen) setIsTopicModalOpen(false);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isCourseModalOpen, isTopicModalOpen]);

  return (
    <div style={{ width: '100%', maxWidth: '1050px', margin: '0 auto' }}>
      {/* Banner de Feedback Administrativo */}
      {feedback && (
        <div
          role="status"
          style={{
            backgroundColor: feedback.type === 'success' ? '#F0FDF4' : '#FEF2F2',
            border: `1px solid ${feedback.type === 'success' ? '#86EFAC' : '#FCA5A5'}`,
            color: feedback.type === 'success' ? '#166534' : '#991B1B',
            padding: '0.75rem 1.25rem',
            borderRadius: '8px',
            marginBottom: '1rem',
            fontSize: '0.85rem',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <span>{feedback.type === 'success' ? '✅' : '⚠️'} {feedback.text}</span>
          <button
            type="button"
            onClick={() => setFeedback(null)}
            style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '1rem' }}
          >
            ✕
          </button>
        </div>
      )}

      {/* Controles de Búsqueda, Filtro y Acción Administrativa */}
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          padding: '1.25rem 1.5rem',
          boxShadow: '0 4px 12px rgba(28, 42, 89, 0.05)',
          border: '1px solid #E2E8F0',
          marginBottom: '1.5rem',
        }}
      >
        <div style={{ display: 'flex', gap: '1rem', flexWrap: 'wrap', alignItems: 'center', marginBottom: '1rem' }}>
          {/* Campo de búsqueda textual en tiempo real */}
          <div style={{ flex: 1, minWidth: '260px' }}>
            <label
              htmlFor="curriculum-search"
              style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.35rem' }}
            >
              🔍 Buscar por curso, código o tema silábico:
            </label>
            <input
              id="curriculum-search"
              type="text"
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              placeholder="Ej. Cálculo, CALC-101, Derivadas, Punteros, SQL, POO..."
              style={{
                width: '100%',
                padding: '0.55rem 0.85rem',
                borderRadius: '8px',
                border: '1px solid #CBD5E1',
                fontSize: '0.84rem',
                color: '#1E293B',
              }}
            />
          </div>

          {/* Filtro por Ciclo */}
          <div>
            <label
              htmlFor="ciclo-select"
              style={{ display: 'block', fontSize: '0.8rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.35rem' }}
            >
              Ciclo Formativo:
            </label>
            <select
              id="ciclo-select"
              value={selectedCiclo ?? ''}
              onChange={(e) => setSelectedCiclo(e.target.value ? Number(e.target.value) : undefined)}
              style={{
                padding: '0.55rem 0.85rem',
                borderRadius: '8px',
                border: '1px solid #CBD5E1',
                fontSize: '0.84rem',
                color: '#1C2A59',
                backgroundColor: '#FFFFFF',
              }}
            >
              <option value="">Todos los Ciclos (I - IV)</option>
              <option value="1">Ciclo I (Básica)</option>
              <option value="2">Ciclo II</option>
              <option value="3">Ciclo III</option>
              <option value="4">Ciclo IV</option>
            </select>
          </div>

          <button
            type="button"
            onClick={loadCourses}
            style={{
              marginTop: '1.2rem',
              background: '#1C2A59',
              color: '#FFFFFF',
              border: 'none',
              borderRadius: '8px',
              padding: '0.55rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            🔄 Actualizar
          </button>

          {/* Botón de creación de Asignatura exclusivo para Administrador (RF05) */}
          {effectiveIsAdmin && (
            <button
              type="button"
              data-testid="admin-add-course-btn"
              onClick={openNewCourseModal}
              style={{
                marginTop: '1.2rem',
                background: '#B99451',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '8px',
                padding: '0.55rem 1.1rem',
                fontSize: '0.82rem',
                fontWeight: 700,
                cursor: 'pointer',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.35rem',
                boxShadow: '0 2px 6px rgba(185, 148, 81, 0.3)',
              }}
            >
              ➕ Nueva Asignatura Crítica
            </button>
          )}
        </div>

        {/* Fila secundaria: Checkbox y Badges de Conteo */}
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem', borderTop: '1px solid #F1F5F9', paddingTop: '0.75rem' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', fontSize: '0.82rem', fontWeight: 600, color: '#1C2A59', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={onlyPriority}
              onChange={(e) => setOnlyPriority(e.target.checked)}
              style={{ accentColor: '#1C2A59' }}
            />
            Solo Materias Filtro Críticas de Deserción (EPIS-UPT)
          </label>

          <span style={{ fontSize: '0.78rem', color: '#64748B' }}>
            Resultados: <strong style={{ color: '#1C2A59' }}>{filteredCourses.length}</strong> de {courses.length} materias formativas
            {effectiveIsAdmin && (
              <span style={{ marginLeft: '0.75rem', color: '#B99451', fontWeight: 700 }}>
                • Modo Administrador Activo (RF05 / CUS21)
              </span>
            )}
          </span>
        </div>
      </div>

      {error && (
        <div
          role="alert"
          style={{
            backgroundColor: '#FEF2F2',
            border: '1px solid #FCA5A5',
            color: '#991B1B',
            padding: '0.85rem 1.25rem',
            borderRadius: '8px',
            marginBottom: '1.5rem',
            fontSize: '0.85rem',
          }}
        >
          ⚠️ {error}
        </div>
      )}

      {/* Cuadrícula de Contenido */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(320px, 1fr))', gap: '1.5rem' }}>
        {/* Lista de Asignaturas */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
            <h3 style={{ fontSize: '1rem', color: '#1C2A59', margin: 0, fontWeight: 700 }}>
              📚 Asignaturas del Plan Curricular ({filteredCourses.length})
            </h3>
            {effectiveIsAdmin && (
              <span style={{ fontSize: '0.72rem', background: '#F1F5F9', color: '#475569', padding: '0.15rem 0.5rem', borderRadius: '4px', fontWeight: 600 }}>
                Gestión Habilitada
              </span>
            )}
          </div>

          {isLoading ? (
            <div style={{ padding: '2rem', textAlign: 'center', color: '#64748B' }}>
              Cargando catálogo curricular...
            </div>
          ) : filteredCourses.length === 0 ? (
            <div
              style={{
                padding: '2.5rem',
                textAlign: 'center',
                color: '#64748B',
                backgroundColor: '#FFFFFF',
                borderRadius: '12px',
                border: '1px solid #E2E8F0',
              }}
            >
              <p style={{ margin: '0 0 0.5rem 0', fontSize: '0.92rem', fontWeight: 600 }}>
                No se encontraron materias con el criterio especificado.
              </p>
              <button
                type="button"
                onClick={() => {
                  setSearchTerm('');
                  setSelectedCiclo(undefined);
                  setOnlyPriority(false);
                }}
                style={{
                  background: '#F1F5F9',
                  border: '1px solid #CBD5E1',
                  borderRadius: '6px',
                  padding: '0.35rem 0.75rem',
                  fontSize: '0.78rem',
                  cursor: 'pointer',
                  color: '#1C2A59',
                  fontWeight: 600,
                }}
              >
                Restablecer Filtros
              </button>
            </div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
              {filteredCourses.map((course) => {
                const isSelected = selectedCourseId === course.id_asignatura;
                const detail = courseDetailsMap[course.id_asignatura];
                const totalTemas = detail?.temas?.length ?? 0;

                return (
                  <div
                    key={course.id_asignatura}
                    onClick={() => handleSelectCourse(course.id_asignatura)}
                    style={{
                      backgroundColor: isSelected ? '#F0F4FA' : '#FFFFFF',
                      border: isSelected ? '2px solid #1C2A59' : '1px solid #E2E8F0',
                      borderRadius: '10px',
                      padding: '0.9rem 1.1rem',
                      cursor: 'pointer',
                      transition: 'all 0.15s ease-in-out',
                      boxShadow: isSelected ? '0 4px 12px rgba(28, 42, 89, 0.1)' : '0 1px 3px rgba(0,0,0,0.04)',
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.25rem' }}>
                      <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#B99451', letterSpacing: '0.05em' }}>
                        {course.codigo_curso} · Ciclo {course.ciclo_plan}
                      </span>
                      <div style={{ display: 'flex', gap: '0.4rem', alignItems: 'center' }}>
                        {course.es_prioritaria && (
                          <span
                            style={{
                              background: '#FEF3C7',
                              color: '#92400E',
                              fontSize: '0.68rem',
                              fontWeight: 700,
                              padding: '0.15rem 0.45rem',
                              borderRadius: '9999px',
                              border: '1px solid #FCD34D',
                            }}
                          >
                            Filtro Crítica
                          </span>
                        )}
                        {/* Botones de acción administrativa por curso */}
                        {effectiveIsAdmin && (
                          <div style={{ display: 'flex', gap: '0.25rem' }}>
                            <button
                              type="button"
                              title="Editar Asignatura"
                              onClick={(e) => openEditCourseModal(course, e)}
                              style={{
                                background: '#E2E8F0',
                                border: 'none',
                                borderRadius: '4px',
                                padding: '0.15rem 0.45rem',
                                fontSize: '0.72rem',
                                cursor: 'pointer',
                                fontWeight: 600,
                              }}
                            >
                              ✏️
                            </button>
                            <button
                              type="button"
                              title="Desactivar Asignatura"
                              onClick={(e) => handleDeleteCourse(course, e)}
                              style={{
                                background: '#FEE2E2',
                                color: '#991B1B',
                                border: 'none',
                                borderRadius: '4px',
                                padding: '0.15rem 0.45rem',
                                fontSize: '0.72rem',
                                cursor: 'pointer',
                                fontWeight: 600,
                              }}
                            >
                              🗑️
                            </button>
                          </div>
                        )}
                      </div>
                    </div>

                    <h4 style={{ margin: '0 0 0.25rem 0', fontSize: '0.96rem', color: '#1C2A59', fontWeight: 700 }}>
                      {course.nombre_curso}
                    </h4>

                    <div style={{ fontSize: '0.76rem', color: '#64748B', display: 'flex', justifyContent: 'space-between', marginTop: '0.4rem' }}>
                      <span>Créditos: <strong>{course.creditos}</strong></span>
                      <span>Factor: <strong>{course.factor_ponderacion ? `${course.factor_ponderacion}x` : '1.0x'}</strong></span>
                      <span>Temas: <strong>{totalTemas > 0 ? totalTemas : '4'}</strong></span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Detalle de Asignatura y Temas Silábicos */}
        <div>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.85rem' }}>
            <h3 style={{ fontSize: '1rem', color: '#1C2A59', margin: 0, fontWeight: 700 }}>
              📖 Temario Silábico Oficial
            </h3>
            {effectiveIsAdmin && selectedCourseId && (
              <button
                type="button"
                data-testid="admin-add-topic-btn"
                onClick={openNewTopicModal}
                style={{
                  background: '#1C2A59',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '0.35rem 0.75rem',
                  fontSize: '0.74rem',
                  fontWeight: 700,
                  cursor: 'pointer',
                  display: 'inline-flex',
                  alignItems: 'center',
                  gap: '0.3rem',
                }}
              >
                ➕ Nuevo Tema
              </button>
            )}
          </div>

          {selectedCourseDetail ? (
            <div
              style={{
                backgroundColor: '#FFFFFF',
                borderRadius: '12px',
                padding: '1.25rem',
                border: '1px solid #E2E8F0',
                boxShadow: '0 4px 12px rgba(28, 42, 89, 0.05)',
              }}
            >
              <div style={{ borderBottom: '1px solid #E2E8F0', paddingBottom: '0.85rem', marginBottom: '1rem' }}>
                <span style={{ fontSize: '0.75rem', fontWeight: 700, color: '#B99451' }}>
                  {selectedCourseDetail.codigo_curso}
                </span>
                <h4 style={{ margin: '0.2rem 0', fontSize: '1.15rem', color: '#1C2A59', fontWeight: 800 }}>
                  {selectedCourseDetail.nombre_curso}
                </h4>
                <p style={{ margin: 0, fontSize: '0.8rem', color: '#64748B' }}>
                  Plan de Estudios EPIS-UPT • Ciclo {selectedCourseDetail.ciclo_plan} • {selectedCourseDetail.creditos} Créditos
                  {selectedCourseDetail.factor_ponderacion && (
                    <span> • Ponderación Top-k: <strong>{selectedCourseDetail.factor_ponderacion}x</strong></span>
                  )}
                </p>
              </div>

              <h5 style={{ margin: '0 0 0.75rem 0', fontSize: '0.85rem', color: '#1C2A59', fontWeight: 700 }}>
                Unidades Conceptuales Silábicas ({selectedCourseDetail.temas?.length || 0}):
              </h5>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                {selectedCourseDetail.temas && selectedCourseDetail.temas.length > 0 ? (
                  selectedCourseDetail.temas.map((tema) => {
                    const isTermMatch =
                      searchTerm.trim().length > 1 &&
                      (tema.nombre_tema.toLowerCase().includes(searchTerm.toLowerCase().trim()) ||
                        (tema.descripcion_silabo &&
                          tema.descripcion_silabo.toLowerCase().includes(searchTerm.toLowerCase().trim())));

                    return (
                      <div
                        key={tema.id_tema}
                        style={{
                          backgroundColor: isTermMatch ? '#FEFCE8' : '#F8FAFC',
                          border: isTermMatch ? '1px solid #FCD34D' : '1px solid #E2E8F0',
                          borderRadius: '8px',
                          padding: '0.75rem 0.9rem',
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '0.2rem' }}>
                          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                            <span
                              style={{
                                background: '#1C2A59',
                                color: '#FFFFFF',
                                fontSize: '0.68rem',
                                fontWeight: 700,
                                padding: '0.1rem 0.4rem',
                                borderRadius: '4px',
                              }}
                            >
                              U{tema.unidad_silabica}
                            </span>
                            <strong style={{ fontSize: '0.86rem', color: '#1E293B' }}>{tema.nombre_tema}</strong>
                            {isTermMatch && (
                              <span style={{ fontSize: '0.65rem', background: '#FEF08A', color: '#854D0E', padding: '0.1rem 0.35rem', borderRadius: '4px', fontWeight: 700 }}>
                                Coincidencia
                              </span>
                            )}
                          </div>
                          {effectiveIsAdmin && (
                            <div style={{ display: 'flex', gap: '0.25rem' }}>
                              <button
                                type="button"
                                title="Editar Tema"
                                onClick={() => openEditTopicModal(tema)}
                                style={{
                                  background: '#E2E8F0',
                                  border: 'none',
                                  borderRadius: '4px',
                                  padding: '0.15rem 0.45rem',
                                  fontSize: '0.7rem',
                                  cursor: 'pointer',
                                }}
                              >
                                ✏️
                              </button>
                              <button
                                type="button"
                                title="Desactivar Tema"
                                onClick={() => handleDeleteTopic(tema)}
                                style={{
                                  background: '#FEE2E2',
                                  color: '#991B1B',
                                  border: 'none',
                                  borderRadius: '4px',
                                  padding: '0.15rem 0.45rem',
                                  fontSize: '0.7rem',
                                  cursor: 'pointer',
                                }}
                              >
                                🗑️
                              </button>
                            </div>
                          )}
                        </div>
                        {tema.descripcion_silabo && (
                          <p style={{ margin: 0, fontSize: '0.78rem', color: '#64748B', lineHeight: 1.4 }}>
                            {tema.descripcion_silabo}
                          </p>
                        )}
                      </div>
                    );
                  })
                ) : (
                  <p style={{ fontSize: '0.8rem', color: '#64748B' }}>
                    No hay temas silábicos registrados para este curso.
                  </p>
                )}
              </div>
            </div>
          ) : (
            <div
              style={{
                padding: '2rem',
                textAlign: 'center',
                color: '#64748B',
                background: '#FFFFFF',
                borderRadius: '12px',
                border: '1px solid #E2E8F0',
              }}
            >
              Selecciona una asignatura para visualizar sus unidades silábicas.
            </div>
          )}
        </div>
      </div>

      {/* MODAL ADMINISTRATIVO DE ASIGNATURA (CREAR / EDITAR) */}
      {isCourseModalOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="course-modal-title"
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(15, 23, 42, 0.7)',
            backdropFilter: 'blur(3px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 10000,
            padding: '1rem',
          }}
        >
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              padding: '1.75rem',
              width: '100%',
              maxWidth: '520px',
              boxShadow: '0 20px 25px -5px rgba(0,0,0,0.2)',
              border: '1px solid #CBD5E1',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <h3 id="course-modal-title" style={{ margin: 0, color: '#1C2A59', fontSize: '1.15rem', fontWeight: 800 }}>
                {editingCourse ? '✏️ Editar Asignatura Curricular' : '➕ Registrar Asignatura Crítica (RF05)'}
              </h3>
              <button
                type="button"
                onClick={() => setIsCourseModalOpen(false)}
                style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '1.25rem', color: '#64748B' }}
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSaveCourse} style={{ display: 'flex', flexDirection: 'column', gap: '0.9rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.25rem' }}>
                  Código de Asignatura:
                </label>
                <input
                  type="text"
                  required
                  placeholder="ej. CI-101, ALGO-202"
                  value={courseFormData.codigo_curso}
                  onChange={(e) => setCourseFormData({ ...courseFormData, codigo_curso: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #CBD5E1', fontSize: '0.85rem' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.25rem' }}>
                  Nombre Oficial de la Asignatura:
                </label>
                <input
                  type="text"
                  required
                  placeholder="ej. Cálculo I, Estructuras de Datos"
                  value={courseFormData.nombre_curso}
                  onChange={(e) => setCourseFormData({ ...courseFormData, nombre_curso: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #CBD5E1', fontSize: '0.85rem' }}
                />
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.25rem' }}>
                    Ciclo del Plan (1 a 10):
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="10"
                    required
                    value={courseFormData.ciclo_plan}
                    onChange={(e) => setCourseFormData({ ...courseFormData, ciclo_plan: Number(e.target.value) })}
                    style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #CBD5E1', fontSize: '0.85rem' }}
                  />
                </div>
                <div>
                  <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.25rem' }}>
                    Créditos Académicos:
                  </label>
                  <input
                    type="number"
                    min="1"
                    max="10"
                    required
                    value={courseFormData.creditos}
                    onChange={(e) => setCourseFormData({ ...courseFormData, creditos: Number(e.target.value) })}
                    style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #CBD5E1', fontSize: '0.85rem' }}
                  />
                </div>
              </div>

              <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '0.75rem', alignItems: 'center' }}>
                <div>
                  <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.25rem' }}>
                    Factor Ponderación (1.0 - 2.0):
                  </label>
                  <input
                    type="number"
                    step="0.1"
                    min="1.0"
                    max="2.0"
                    required
                    value={courseFormData.factor_ponderacion}
                    onChange={(e) => setCourseFormData({ ...courseFormData, factor_ponderacion: Number(e.target.value) })}
                    style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #CBD5E1', fontSize: '0.85rem' }}
                  />
                </div>
                <div style={{ paddingTop: '1.1rem' }}>
                  <label style={{ display: 'flex', alignItems: 'center', gap: '0.45rem', fontSize: '0.82rem', fontWeight: 600, color: '#1C2A59', cursor: 'pointer' }}>
                    <input
                      type="checkbox"
                      checked={courseFormData.es_prioritaria}
                      onChange={(e) => setCourseFormData({ ...courseFormData, es_prioritaria: e.target.checked })}
                      style={{ accentColor: '#1C2A59' }}
                    />
                    Materia Filtro Crítica
                  </label>
                </div>
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1rem' }}>
                <button
                  type="button"
                  onClick={() => setIsCourseModalOpen(false)}
                  style={{
                    padding: '0.55rem 1rem',
                    borderRadius: '6px',
                    border: '1px solid #CBD5E1',
                    background: '#F1F5F9',
                    color: '#475569',
                    fontWeight: 600,
                    fontSize: '0.82rem',
                    cursor: 'pointer',
                  }}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={actionLoading}
                  style={{
                    padding: '0.55rem 1.25rem',
                    borderRadius: '6px',
                    border: 'none',
                    background: '#1C2A59',
                    color: '#FFFFFF',
                    fontWeight: 700,
                    fontSize: '0.82rem',
                    cursor: 'pointer',
                    opacity: actionLoading ? 0.7 : 1,
                  }}
                >
                  {actionLoading ? 'Guardando...' : editingCourse ? 'Guardar Cambios' : 'Registrar Asignatura'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* MODAL ADMINISTRATIVO DE TEMA SILÁBICO (CREAR / EDITAR) */}
      {isTopicModalOpen && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="topic-modal-title"
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(15, 23, 42, 0.7)',
            backdropFilter: 'blur(3px)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 10000,
            padding: '1rem',
          }}
        >
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '12px',
              padding: '1.75rem',
              width: '100%',
              maxWidth: '500px',
              boxShadow: '0 20px 25px -5px rgba(0,0,0,0.2)',
              border: '1px solid #CBD5E1',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <h3 id="topic-modal-title" style={{ margin: 0, color: '#1C2A59', fontSize: '1.15rem', fontWeight: 800 }}>
                {editingTopic ? '✏️ Editar Tema Silábico' : '➕ Incorporar Tema al Sílabo (RF05)'}
              </h3>
              <button
                type="button"
                onClick={() => setIsTopicModalOpen(false)}
                style={{ background: 'transparent', border: 'none', cursor: 'pointer', fontSize: '1.25rem', color: '#64748B' }}
              >
                ✕
              </button>
            </div>

            <form onSubmit={handleSaveTopic} style={{ display: 'flex', flexDirection: 'column', gap: '0.9rem' }}>
              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.25rem' }}>
                  Título del Concepto o Tema Silábico:
                </label>
                <input
                  type="text"
                  required
                  placeholder="ej. Integrales Definidas, Grafos y Árboles"
                  value={topicFormData.nombre_tema}
                  onChange={(e) => setTopicFormData({ ...topicFormData, nombre_tema: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #CBD5E1', fontSize: '0.85rem' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.25rem' }}>
                  Unidad Silábica Oficial (1 a 10):
                </label>
                <input
                  type="number"
                  min="1"
                  max="10"
                  required
                  value={topicFormData.unidad_silabica}
                  onChange={(e) => setTopicFormData({ ...topicFormData, unidad_silabica: Number(e.target.value) })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #CBD5E1', fontSize: '0.85rem' }}
                />
              </div>

              <div>
                <label style={{ display: 'block', fontSize: '0.78rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.25rem' }}>
                  Descripción Analítica del Contenido (Sílabo):
                </label>
                <textarea
                  rows={3}
                  placeholder="Detalle conceptual de los subtemas a cubrir en la unidad..."
                  value={topicFormData.descripcion_silabo}
                  onChange={(e) => setTopicFormData({ ...topicFormData, descripcion_silabo: e.target.value })}
                  style={{ width: '100%', padding: '0.5rem', borderRadius: '6px', border: '1px solid #CBD5E1', fontSize: '0.85rem' }}
                />
              </div>

              <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem', marginTop: '1rem' }}>
                <button
                  type="button"
                  onClick={() => setIsTopicModalOpen(false)}
                  style={{
                    padding: '0.55rem 1rem',
                    borderRadius: '6px',
                    border: '1px solid #CBD5E1',
                    background: '#F1F5F9',
                    color: '#475569',
                    fontWeight: 600,
                    fontSize: '0.82rem',
                    cursor: 'pointer',
                  }}
                >
                  Cancelar
                </button>
                <button
                  type="submit"
                  disabled={actionLoading}
                  style={{
                    padding: '0.55rem 1.25rem',
                    borderRadius: '6px',
                    border: 'none',
                    background: '#1C2A59',
                    color: '#FFFFFF',
                    fontWeight: 700,
                    fontSize: '0.82rem',
                    cursor: 'pointer',
                    opacity: actionLoading ? 0.7 : 1,
                  }}
                >
                  {actionLoading ? 'Guardando...' : editingTopic ? 'Guardar Cambios' : 'Incorporar Tema'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};
