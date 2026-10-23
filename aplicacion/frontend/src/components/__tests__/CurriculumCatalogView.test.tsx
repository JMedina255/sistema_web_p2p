import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { CurriculumCatalogView } from '../CurriculumCatalogView';
import * as apiClient from '../../services/apiClient';

describe('CurriculumCatalogView Component (T-09 / T-10 / CUS21 / RF05)', () => {
  const mockCourses: apiClient.Course[] = [
    {
      id_asignatura: 1,
      codigo_curso: 'CALC-101',
      nombre_curso: 'Cálculo I',
      ciclo_plan: 1,
      creditos: 4,
      es_prioritaria: true,
      factor_ponderacion: 1.2,
      estado_activo: true,
    },
    {
      id_asignatura: 3,
      codigo_curso: 'ALGO-202',
      nombre_curso: 'Algoritmos y Estructuras de Datos',
      ciclo_plan: 2,
      creditos: 4,
      es_prioritaria: true,
      factor_ponderacion: 1.3,
      estado_activo: true,
    },
  ];

  const mockDetail: apiClient.CourseDetail = {
    ...mockCourses[0],
    temas: [
      {
        id_tema: 1,
        id_asignatura: 1,
        nombre_tema: 'Límites y Continuidad',
        descripcion_silabo: 'Concepto formal de límites y propiedades.',
        unidad_silabica: 1,
        estado_activo: true,
      },
    ],
  };

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('1. Renderiza el catálogo de asignaturas y carga los cursos iniciales', async () => {
    vi.spyOn(apiClient, 'fetchCourses').mockResolvedValue(mockCourses);
    vi.spyOn(apiClient, 'fetchCourseDetail').mockResolvedValue(mockDetail);

    render(<CurriculumCatalogView />);

    expect(screen.getByText(/Cargando catálogo curricular.../i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getAllByText('Cálculo I').length).toBeGreaterThanOrEqual(1);
      expect(screen.getByText('Algoritmos y Estructuras de Datos')).toBeInTheDocument();
    });

    expect(screen.getByText('Límites y Continuidad')).toBeInTheDocument();
  });

  it('2. Permite seleccionar una materia para ver su temario silábico', async () => {
    vi.spyOn(apiClient, 'fetchCourses').mockResolvedValue(mockCourses);
    vi.spyOn(apiClient, 'fetchCourseDetail').mockImplementation(async (id) => {
      if (id === 3) {
        return {
          ...mockCourses[1],
          temas: [
            {
              id_tema: 11,
              id_asignatura: 3,
              nombre_tema: 'Punteros y Gestión Dinámica de Memoria en C++',
              descripcion_silabo: 'Aritmética de punteros y new/delete.',
              unidad_silabica: 3,
              estado_activo: true,
            },
          ],
        };
      }
      return mockDetail;
    });

    render(<CurriculumCatalogView />);

    await waitFor(() => {
      expect(screen.getByText('Algoritmos y Estructuras de Datos')).toBeInTheDocument();
    });

    const algoCourse = screen.getByText('Algoritmos y Estructuras de Datos');
    fireEvent.click(algoCourse);

    await waitFor(() => {
      expect(screen.getByText(/Punteros y Gestión Dinámica de Memoria en C\+\+/i)).toBeInTheDocument();
    });
  });

  it('3. Filtra interactivamente por campo de búsqueda textual (T-10 / RF05)', async () => {
    vi.spyOn(apiClient, 'fetchCourses').mockResolvedValue(mockCourses);
    vi.spyOn(apiClient, 'fetchCourseDetail').mockResolvedValue(mockDetail);

    render(<CurriculumCatalogView />);

    await waitFor(() => {
      expect(screen.getByText('Algoritmos y Estructuras de Datos')).toBeInTheDocument();
    });

    const searchInput = screen.getByLabelText(/Buscar por curso/i);
    fireEvent.change(searchInput, { target: { value: 'CALC' } });

    expect(screen.getAllByText('Cálculo I').length).toBeGreaterThanOrEqual(1);
    expect(screen.queryByText('Algoritmos y Estructuras de Datos')).not.toBeInTheDocument();
  });

  it('4. Muestra mensaje de error amigable cuando la llamada al API falla', async () => {
    vi.spyOn(apiClient, 'fetchCourses').mockRejectedValue(new Error('Fallo de conexión'));

    render(<CurriculumCatalogView />);

    await waitFor(() => {
      expect(screen.getByRole('alert')).toHaveTextContent(/Fallo de conexión/i);
    });
  });
});
