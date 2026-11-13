import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { MentoringDemandModalView } from '../MentoringDemandModalView';
import * as apiClient from '../../services/apiClient';
import { bookingService } from '../../services/bookingService';

describe('MentoringDemandModalView Component (CUS03 / RF07)', () => {
  const mockCourses: apiClient.Course[] = [
    {
      id_asignatura: 1,
      codigo_curso: 'CALC-101',
      nombre_curso: 'Cálculo I',
      ciclo_plan: 1,
      creditos: 4,
      es_prioritaria: true,
      factor_ponderacion: 1.5,
      estado_activo: true,
    },
    {
      id_asignatura: 3,
      codigo_curso: 'ALGO-202',
      nombre_curso: 'Algoritmos y Estructuras de Datos',
      ciclo_plan: 2,
      creditos: 4,
      es_prioritaria: true,
      factor_ponderacion: 1.4,
      estado_activo: true,
    },
  ];

  const mockDetailCourse1: apiClient.CourseDetail = {
    ...mockCourses[0],
    temas: [
      {
        id_tema: 1,
        id_asignatura: 1,
        nombre_tema: 'Límites y Continuidad',
        descripcion_silabo: 'Cálculo de límites.',
        unidad_silabica: 1,
        estado_activo: true,
      },
      {
        id_tema: 2,
        id_asignatura: 1,
        nombre_tema: 'Derivadas',
        descripcion_silabo: 'Regla de la cadena.',
        unidad_silabica: 2,
        estado_activo: true,
      },
    ],
  };

  const mockDetailCourse3: apiClient.CourseDetail = {
    ...mockCourses[1],
    temas: [
      {
        id_tema: 9,
        id_asignatura: 3,
        nombre_tema: 'Análisis Asintótico y Big-O',
        descripcion_silabo: 'Complejidad algorítmica.',
        unidad_silabica: 1,
        estado_activo: true,
      },
    ],
  };

  beforeEach(() => {
    vi.restoreAllMocks();
    bookingService.setMode('mock');
    bookingService.resetToDefaults();

    vi.spyOn(apiClient, 'fetchCourses').mockResolvedValue(mockCourses);
    vi.spyOn(apiClient, 'fetchCourseDetail').mockImplementation(async (id: number) => {
      if (id === 3) return mockDetailCourse3;
      return mockDetailCourse1;
    });
  });

  it('1. No renderiza nada si isOpen es false', () => {
    const { container } = render(
      <MentoringDemandModalView isOpen={false} onClose={vi.fn()} />
    );
    expect(container.firstChild).toBeNull();
  });

  it('2. Renderiza el modal con catálogo de asignaturas y temas cargados dinámicamente', async () => {
    render(<MentoringDemandModalView isOpen={true} onClose={vi.fn()} />);

    expect(screen.getByRole('dialog')).toBeInTheDocument();
    expect(screen.getByText(/Registrar Solicitud de Mentoría por Demanda/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/CALC-101 — Cálculo I/i)).toBeInTheDocument();
      expect(screen.getByText(/Unidad 1: Límites y Continuidad/i)).toBeInTheDocument();
    });
  });

  it('3. Permite cambiar de curso y actualiza los temas disponibles', async () => {
    render(<MentoringDemandModalView isOpen={true} onClose={vi.fn()} />);

    await waitFor(() => {
      expect(screen.getByLabelText(/Asignatura Curricular/i)).toBeInTheDocument();
    });

    const courseSelect = screen.getByLabelText(/Asignatura Curricular/i);
    fireEvent.change(courseSelect, { target: { value: '3' } });

    await waitFor(() => {
      expect(screen.getByText(/Unidad 1: Análisis Asintótico y Big-O/i)).toBeInTheDocument();
    });
  });

  it('4. Envía solicitud de demanda y despliega pantalla de éxito con folio institucional', async () => {
    const onDemandCreated = vi.fn();
    const onClose = vi.fn();

    render(
      <MentoringDemandModalView
        isOpen={true}
        onClose={onClose}
        onDemandCreated={onDemandCreated}
      />
    );

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /Enviar Solicitud/i })).not.toBeDisabled();
    });

    const obsInput = screen.getByLabelText(/Observaciones o Justificación/i);
    fireEvent.change(obsInput, {
      target: { value: 'Necesito asesoría urgente para la práctica calificada de límites.' },
    });

    const submitBtn = screen.getByRole('button', { name: /Enviar Solicitud/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(screen.getByText(/¡Solicitud Registrada con Éxito!/i)).toBeInTheDocument();
      expect(screen.getByText(/#DEM-\d+/i)).toBeInTheDocument();
      expect(screen.getByText(/PENDIENTE/i)).toBeInTheDocument();
    });

    expect(onDemandCreated).toHaveBeenCalledTimes(1);

    const closeBtn = screen.getByRole('button', { name: /Entendido/i });
    fireEvent.click(closeBtn);
    expect(onClose).toHaveBeenCalledTimes(1);
  });

  it('5. Cierra el modal al presionar la tecla Escape', () => {
    const onClose = vi.fn();
    render(<MentoringDemandModalView isOpen={true} onClose={onClose} />);

    fireEvent.keyDown(window, { key: 'Escape' });
    expect(onClose).toHaveBeenCalledTimes(1);
  });
});
