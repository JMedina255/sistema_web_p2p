import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { ProfileAvailabilityView } from '../ProfileAvailabilityView';
import * as apiClient from '../../services/apiClient';
import { profileService } from '../../services/profileService';

describe('ProfileAvailabilityView Component (T-11 / RF04 / CUS15)', () => {
  const testEmail = '2022074255@upt.pe';

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

  beforeEach(() => {
    vi.restoreAllMocks();
    profileService.setMode('mock');
    vi.spyOn(apiClient, 'fetchCourses').mockResolvedValue(mockCourses);
  });

  it('1. Renderiza el formulario de perfil formativo académico', async () => {
    render(<ProfileAvailabilityView userEmail={testEmail} />);

    expect(screen.getByText(/Cargando perfil formativo y agenda semanal.../i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getByText(/Configuración del Perfil Académico/i)).toBeInTheDocument();
      expect(screen.getByText(/Ciclo Académico Actual/i)).toBeInTheDocument();
      expect(screen.getByText(/Rol de Participación en la Plataforma/i)).toBeInTheDocument();
    });
  });

  it('2. Muestra advertencia de la regla RN-03 al seleccionar Mentor con ciclo menor a VII', async () => {
    render(<ProfileAvailabilityView userEmail={testEmail} />);

    await waitFor(() => {
      expect(screen.getByText(/Configuración del Perfil Académico/i)).toBeInTheDocument();
    });

    const mentorButton = screen.getByRole('button', { name: /Postulante a Mentor/i });
    fireEvent.click(mentorButton);

    // Como Joan por defecto tiene ciclo 6 (< 7), debe saltar la advertencia RN-03
    expect(screen.getByText(/Regla de Mérito RN-03/i)).toBeInTheDocument();
  });

  it('3. Permite alternar a la pestaña de disponibilidad y muestra la grilla semanal', async () => {
    render(<ProfileAvailabilityView userEmail={testEmail} />);

    await waitFor(() => {
      expect(screen.getByText(/2. Matriz Semanal de Disponibilidad/i)).toBeInTheDocument();
    });

    const scheduleTab = screen.getByText(/2. Matriz Semanal de Disponibilidad/i);
    fireEvent.click(scheduleTab);

    expect(screen.getByText(/Agenda Semanal de Disponibilidad/i)).toBeInTheDocument();
    expect(screen.getByText('Lunes')).toBeInTheDocument();
    expect(screen.getByText('Viernes')).toBeInTheDocument();
    expect(screen.getByText('Sábado')).toBeInTheDocument();
  });

  it('4. Permite usar el botón de Limpiar para vaciar la selección horaria', async () => {
    render(<ProfileAvailabilityView userEmail={testEmail} />);

    await waitFor(() => {
      const scheduleTab = screen.getByText(/2. Matriz Semanal de Disponibilidad/i);
      fireEvent.click(scheduleTab);
    });

    const clearButton = screen.getByRole('button', { name: /Limpiar/i });
    fireEvent.click(clearButton);

    expect(screen.getByText(/0 bloques de 1 hora/i)).toBeInTheDocument();
  });

  it('5. Guarda exitosamente el perfil y muestra notificación de confirmación', async () => {
    const onSavedMock = vi.fn();
    render(<ProfileAvailabilityView userEmail={testEmail} onSaved={onSavedMock} />);

    await waitFor(() => {
      expect(screen.getByText(/Guardar Perfil y Disponibilidad/i)).toBeInTheDocument();
    });

    const saveButton = screen.getByRole('button', { name: /Guardar Perfil y Disponibilidad/i });
    fireEvent.click(saveButton);

    await waitFor(() => {
      expect(screen.getByText(/guardados exitosamente/i)).toBeInTheDocument();
      expect(onSavedMock).toHaveBeenCalled();
    });
  });
});
