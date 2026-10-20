import React, { useState, useEffect, useCallback } from 'react';
import { fetchCourses, fetchCourseDetail } from '../services/apiClient';
import type { Course, CourseDetail } from '../services/apiClient';

export const CurriculumCatalogView: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [selectedCourse, setSelectedCourse] = useState<CourseDetail | null>(null);
  const [onlyPriority, setOnlyPriority] = useState<boolean>(true);
  const [selectedCiclo, setSelectedCiclo] = useState<number | undefined>(undefined);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  const loadCourses = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchCourses(onlyPriority, selectedCiclo);
      setCourses(data);
      if (data.length > 0) {
        setSelectedCourse((current) => {
          const stillValid = current && data.some((c) => c.id_asignatura === current.id_asignatura);
          if (!stillValid) {
            fetchCourseDetail(data[0].id_asignatura)
              .then(setSelectedCourse)
              .catch(() => {});
          }
          return current;
        });
      } else {
        setSelectedCourse(null);
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

  const handleSelectCourse = async (courseId: number) => {
    try {
      const detail = await fetchCourseDetail(courseId);
      setSelectedCourse(detail);
    } catch (err: unknown) {
      setError(err instanceof Error ? err.message : 'Error al cargar detalle de asignatura.');
    }
  };

  return (
    <div style={{ width: '100%', maxWidth: '1000px', margin: '0 auto' }}>
      {/* Controles de Filtro */}
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          padding: '1.25rem 1.5rem',
          boxShadow: '0 4px 12px rgba(28, 42, 89, 0.05)',
          border: '1px solid #E2E8F0',
          marginBottom: '1.5rem',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem', flexWrap: 'wrap' }}>
          <label style={{ display: 'flex', alignItems: 'center', gap: '0.4rem', fontSize: '0.86rem', fontWeight: 600, color: '#1C2A59', cursor: 'pointer' }}>
            <input
              type="checkbox"
              checked={onlyPriority}
              onChange={(e) => setOnlyPriority(e.target.checked)}
              style={{ accentColor: '#1C2A59' }}
            />
            Solo Materias Filtro / Críticas (T-09)
          </label>

          <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.86rem' }}>
            <span style={{ color: '#64748B' }}>Ciclo:</span>
            <select
              value={selectedCiclo ?? ''}
              onChange={(e) => setSelectedCiclo(e.target.value ? Number(e.target.value) : undefined)}
              style={{
                padding: '0.35rem 0.65rem',
                borderRadius: '6px',
                border: '1px solid #CBD5E1',
                fontSize: '0.82rem',
                color: '#1C2A59',
                backgroundColor: '#FFFFFF',
              }}
            >
              <option value="">Todos los Ciclos</option>
              <option value="1">Ciclo I</option>
              <option value="2">Ciclo II</option>
              <option value="3">Ciclo III</option>
              <option value="4">Ciclo IV</option>
            </select>
          </div>
        </div>

        <button
          onClick={loadCourses}
          style={{
            background: '#1C2A59',
            color: '#FFFFFF',
            border: 'none',
            borderRadius: '6px',
            padding: '0.45rem 0.9rem',
            fontSize: '0.82rem',
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          🔄 Actualizar Catálogo
        </button>
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
          <h3 style={{ fontSize: '1rem', color: '#1C2A59', margin: '0 0 0.85rem 0', fontWeight: 700 }}>
            📚 Asignaturas del Plan de Estudios ({courses.length})
          </h3>
          {isLoading ? (
            <div style={{ padding: '2rem', textAlign: 'center', color: '#64748B' }}>Cargando catálogo curricular...</div>
          ) : courses.length === 0 ? (
            <div style={{ padding: '2rem', textAlign: 'center', color: '#64748B' }}>No se encontraron asignaturas con los filtros seleccionados.</div>
          ) : (
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
              {courses.map((course) => {
                const isSelected = selectedCourse?.id_asignatura === course.id_asignatura;
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
                    </div>
                    <h4 style={{ margin: '0 0 0.25rem 0', fontSize: '0.96rem', color: '#1C2A59', fontWeight: 700 }}>
                      {course.nombre_curso}
                    </h4>
                    <div style={{ fontSize: '0.78rem', color: '#64748B', display: 'flex', gap: '0.85rem' }}>
                      <span>Créditos: <strong>{course.creditos}</strong></span>
                      <span>Factor Ponderación: <strong>{course.factor_ponderacion}x</strong></span>
                    </div>
                  </div>
                );
              })}
            </div>
          )}
        </div>

        {/* Detalle de Asignatura y Temas Silábicos */}
        <div>
          <h3 style={{ fontSize: '1rem', color: '#1C2A59', margin: '0 0 0.85rem 0', fontWeight: 700 }}>
            📖 Temario Silábico Oficial (CUS21)
          </h3>
          {selectedCourse ? (
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
                  {selectedCourse.codigo_curso}
                </span>
                <h4 style={{ margin: '0.2rem 0', fontSize: '1.15rem', color: '#1C2A59', fontWeight: 800 }}>
                  {selectedCourse.nombre_curso}
                </h4>
                <p style={{ margin: 0, fontSize: '0.8rem', color: '#64748B' }}>
                  Plan de Estudios EPIS-UPT • Ciclo {selectedCourse.ciclo_plan} • {selectedCourse.creditos} Créditos
                </p>
              </div>

              <h5 style={{ margin: '0 0 0.75rem 0', fontSize: '0.85rem', color: '#1C2A59', fontWeight: 700 }}>
                Unidades Conceptuales Silábicas ({selectedCourse.temas?.length || 0}):
              </h5>

              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.65rem' }}>
                {selectedCourse.temas && selectedCourse.temas.length > 0 ? (
                  selectedCourse.temas.map((tema) => (
                    <div
                      key={tema.id_tema}
                      style={{
                        backgroundColor: '#F8FAFC',
                        border: '1px solid #E2E8F0',
                        borderRadius: '8px',
                        padding: '0.75rem 0.9rem',
                      }}
                    >
                      <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.2rem' }}>
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
                      </div>
                      {tema.descripcion_silabo && (
                        <p style={{ margin: 0, fontSize: '0.78rem', color: '#64748B', lineHeight: 1.4 }}>
                          {tema.descripcion_silabo}
                        </p>
                      )}
                    </div>
                  ))
                ) : (
                  <p style={{ fontSize: '0.8rem', color: '#64748B' }}>No hay temas silábicos registrados para este curso.</p>
                )}
              </div>
            </div>
          ) : (
            <div style={{ padding: '2rem', textAlign: 'center', color: '#64748B', background: '#FFFFFF', borderRadius: '12px', border: '1px solid #E2E8F0' }}>
              Selecciona una asignatura para visualizar sus unidades silábicas.
            </div>
          )}
        </div>
      </div>
    </div>
  );
};
