import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AdminScheduleUploadView } from '../AdminScheduleUploadView';
import { spacesService, type ScheduleImportResponse } from '../../services/spacesService';

describe('AdminScheduleUploadView Component (RF10 / CUS11 / RN-06)', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('1. Renderiza encabezado institucional, zona de carga y tabla con franjas iniciales', async () => {
    vi.spyOn(spacesService, 'getFreeSlots').mockResolvedValue([
      { aula: 'Lab 01', dia: 'Lunes', hora_inicio: '08:00', hora_fin: '10:00', estado: 'LIBRE' },
      { aula: 'Lab 02', dia: 'Martes', hora_inicio: '10:00', hora_fin: '12:00', estado: 'LIBRE' },
    ]);

    render(<AdminScheduleUploadView />);

    expect(screen.getByText(/Procesamiento de Cronogramas Institucionales/i)).toBeInTheDocument();
    expect(screen.getByText(/RF10 \/ Caso de Uso CUS11 \/ Regla RN-06/i)).toBeInTheDocument();
    expect(screen.getByText(/Arrastra aquí el archivo oficial de horarios/i)).toBeInTheDocument();

    await waitFor(() => {
      expect(screen.getAllByText('Lab 01').length).toBeGreaterThan(0);
      expect(screen.getAllByText('Lab 02').length).toBeGreaterThan(0);
    });
  });

  it('2. Permite seleccionar un archivo Excel y habilita el botón de procesamiento', async () => {
    render(<AdminScheduleUploadView />);

    const fileInput = screen.getByLabelText(/Seleccionar archivo oficial de cronograma/i);
    const mockFile = new File(['fake content'], 'cronograma_semestre_2026.xlsx', {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    });

    fireEvent.change(fileInput, { target: { files: [mockFile] } });

    expect(screen.getByText('cronograma_semestre_2026.xlsx')).toBeInTheDocument();
    const processBtn = screen.getByRole('button', { name: /Procesar Cronograma con Parser/i });
    expect(processBtn).not.toBeDisabled();
  });

  it('3. Procesa el cronograma exitosamente y despliega banner de confirmación con slots actualizados', async () => {
    const mockResponse: ScheduleImportResponse = {
      status: 'PROCESADO_EXITOSAMENTE',
      archivo: 'cronograma_oficial_epis.xlsx',
      total_aulas_libres_identificadas: 3,
      reservas_activas_preservadas: 0,
      aulas_libres: [
        { aula: 'Lab Redes 202', dia: 'Lunes', hora_inicio: '08:00', hora_fin: '10:00', estado: 'LIBRE' },
        { aula: 'Lab BD 104', dia: 'Miércoles', hora_inicio: '14:00', hora_fin: '16:00', estado: 'LIBRE' },
        { aula: 'Aula Magna 301', dia: 'Viernes', hora_inicio: '10:00', hora_fin: '12:00', estado: 'LIBRE' },
      ],
    };

    const uploadSpy = vi.spyOn(spacesService, 'uploadSchedule').mockResolvedValue(mockResponse);
    const onUpdated = vi.fn();

    render(<AdminScheduleUploadView onScheduleUpdated={onUpdated} />);

    const fileInput = screen.getByLabelText(/Seleccionar archivo oficial de cronograma/i);
    const mockFile = new File(['fake excel bytes'], 'cronograma_oficial_epis.xlsx', {
      type: 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
    });

    fireEvent.change(fileInput, { target: { files: [mockFile] } });

    const processBtn = screen.getByRole('button', { name: /Procesar Cronograma con Parser/i });
    fireEvent.click(processBtn);

    await waitFor(() => {
      expect(uploadSpy).toHaveBeenCalledWith(mockFile);
      expect(screen.getByText(/¡Cronograma oficial procesado exitosamente por el Parser de Horarios!/i)).toBeInTheDocument();
      expect(screen.getByText('Lab Redes 202')).toBeInTheDocument();
      expect(screen.getByText('Lab BD 104')).toBeInTheDocument();
      expect(screen.getByText('Aula Magna 301')).toBeInTheDocument();
    });

    expect(onUpdated).toHaveBeenCalledWith(3);
  });

  it('4. Maneja error de formato corrupto o no soportado mostrando alerta accesible', async () => {
    vi.spyOn(spacesService, 'uploadSchedule').mockRejectedValue(
      new Error('Extensión no soportada. Solo se admiten archivos oficiales en Excel (.xlsx) y PDF (.pdf).')
    );

    render(<AdminScheduleUploadView />);

    const fileInput = screen.getByLabelText(/Seleccionar archivo oficial de cronograma/i);
    const mockFile = new File(['texto'], 'archivo_invalido.txt', { type: 'text/plain' });

    fireEvent.change(fileInput, { target: { files: [mockFile] } });

    const processBtn = screen.getByRole('button', { name: /Procesar Cronograma con Parser/i });
    fireEvent.click(processBtn);

    await waitFor(() => {
      expect(screen.getByRole('alert')).toBeInTheDocument();
      expect(screen.getByText(/Extensión no soportada/i)).toBeInTheDocument();
    });
  });

  it('5. Filtra las franjas horarias libres mediante la barra de búsqueda interactiva', async () => {
    vi.spyOn(spacesService, 'getFreeSlots').mockResolvedValue([
      { aula: 'Lab 01', dia: 'Lunes', hora_inicio: '08:00', hora_fin: '10:00', estado: 'LIBRE' },
      { aula: 'Aula 302', dia: 'Viernes', hora_inicio: '14:00', hora_fin: '16:00', estado: 'LIBRE' },
    ]);

    render(<AdminScheduleUploadView />);

    await waitFor(() => {
      expect(screen.getAllByText('Lab 01').length).toBeGreaterThan(0);
      expect(screen.getAllByText('Aula 302').length).toBeGreaterThan(0);
    });

    const searchInput = screen.getByLabelText(/Buscar recinto o día/i);
    fireEvent.change(searchInput, { target: { value: 'Aula 302' } });

    expect(screen.queryByRole('cell', { name: 'Lab 01' })).not.toBeInTheDocument();
    expect(screen.getByRole('cell', { name: 'Aula 302' })).toBeInTheDocument();
  });
});
