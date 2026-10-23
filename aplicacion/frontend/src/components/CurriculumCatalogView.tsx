import React, { useState, useEffect, useCallback, useMemo } from 'react';
import { fetchCourses, fetchCourseDetail } from '../services/apiClient';
import type { Course, CourseDetail } from '../services/apiClient';

export const CurriculumCatalogView: React.FC = () => {
  const [courses, setCourses] = useState<Course[]>([]);
  const [courseDetailsMap, setCourseDetailsMap] = useState<Record<number, CourseDetail>>({});
  const [selectedCourseId, setSelectedCourseId] = useState<number | null>(null);
  const [searchTerm, setSearchTerm] = useState<string>('');
  const [onlyPriority, setOnlyPriority] = useState<boolean>(true);
  const [selectedCiclo, setSelectedCiclo] = useState<number | undefined>(undefined);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Carga inicial y por filtros de asignaturas
  const loadCourses = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await fetchCourses(onlyPriority, selectedCiclo);
      setCourses(data);

      if (data.length > 0) {
        // Precargar detalles de los primeros cursos si aún no están en cache
        const firstId = data[0].id_asignatura;
        setSelectedCourseId((prev) => (prev && data.some((c) => c.id_asignatura === prev) ? prev : firstId));

        // Cargar en background detalles para habilitar búsqueda profunda por temas
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

  // Filtrado reactivo en memoria combinando búsqueda textual (código, nombre y temas silábicos)
  const filteredCourses = useMemo(() => {
    if (!searchTerm.trim()) return courses;
    const term = searchTerm.toLowerCase().trim();

    return courses.filter((course) => {
      // 1. Coincidencia en nombre o código
      const matchesCourse =
        course.nombre_curso.toLowerCase().includes(term) ||
        course.codigo_curso.toLowerCase().includes(term);

      if (matchesCourse) return true;

      // 2. Coincidencia profunda en temas del sílabo (si está cargado en cache)
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

  return (
    <div style={{ width: '100%', maxWidth: '1000px', margin: '0 auto' }}>
      {/* Controles de Búsqueda y Filtro Avanzado (T-10) */}
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
              🔍 Buscar por curso, código o tema silábico (T-10 / RF05):
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
          <h3 style={{ fontSize: '1rem', color: '#1C2A59', margin: '0 0 0.85rem 0', fontWeight: 700 }}>
            📚 Asignaturas del Plan Curricular ({filteredCourses.length})
          </h3>
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

                    <div style={{ fontSize: '0.76rem', color: '#64748B', display: 'flex', justifyContent: 'space-between', marginTop: '0.4rem' }}>
                      <span>Créditos: <strong>{course.creditos}</strong></span>
                      <span>Factor Top-k: <strong>{course.factor_ponderacion}x</strong></span>
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
          <h3 style={{ fontSize: '1rem', color: '#1C2A59', margin: '0 0 0.85rem 0', fontWeight: 700 }}>
            📖 Temario Silábico Oficial (CUS21)
          </h3>
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
                  Plan de Estudios EPIS-UPT • Ciclo {selectedCourseDetail.ciclo_plan} • {selectedCourseDetail.creditos} Créditos • Ponderador Top-k {selectedCourseDetail.factor_ponderacion}x
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
                          {isTermMatch && (
                            <span style={{ fontSize: '0.65rem', background: '#FEF08A', color: '#854D0E', padding: '0.1rem 0.35rem', borderRadius: '4px', fontWeight: 700 }}>
                              Coincidencia
                            </span>
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
    </div>
  );
};
