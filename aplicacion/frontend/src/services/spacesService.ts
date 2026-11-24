/**
 * Servicio de Espacios Físicos, Cronogramas y Parser de Horarios (RF10 / CUS11 / RN-06 / MOD-04).
 */

import { authService } from './authService';

export interface FreeSlotItem {
  aula: string;
  dia: string;
  hora_inicio: string;
  hora_fin: string;
  estado: string;
  fila_origen?: number | null;
  pagina?: number | null;
}

export interface ScheduleImportResponse {
  status: string;
  archivo: string;
  total_aulas_libres_identificadas: number;
  reservas_activas_preservadas: number;
  aulas_libres: FreeSlotItem[];
}

export interface ClassroomListResponse {
  aulas: string[];
  total: number;
}

const useMock = import.meta.env.VITE_SERVICE_MODE === 'mock' || import.meta.env.MODE === 'test';

const DEFAULT_MOCK_SLOTS: FreeSlotItem[] = [
  { aula: 'Lab 01', dia: 'Lunes', hora_inicio: '08:00', hora_fin: '10:00', estado: 'LIBRE' },
  { aula: 'Lab 01', dia: 'Miércoles', hora_inicio: '14:00', hora_fin: '16:00', estado: 'LIBRE' },
  { aula: 'Lab 02', dia: 'Martes', hora_inicio: '10:00', hora_fin: '12:00', estado: 'LIBRE' },
  { aula: 'Lab 02', dia: 'Jueves', hora_inicio: '16:00', hora_fin: '18:00', estado: 'LIBRE' },
  { aula: 'Aula 101', dia: 'Lunes', hora_inicio: '10:00', hora_fin: '12:00', estado: 'LIBRE' },
  { aula: 'Aula 202', dia: 'Miércoles', hora_inicio: '08:00', hora_fin: '10:00', estado: 'LIBRE' },
  { aula: 'Aula 302', dia: 'Viernes', hora_inicio: '14:00', hora_fin: '16:00', estado: 'LIBRE' },
];

let mockSlotsMemory: FreeSlotItem[] = [...DEFAULT_MOCK_SLOTS];
let lastImportedFileMemory: string = 'cronograma_oficial_base_2026.xlsx';

class SpacesService {
  private getBaseUrl(): string {
    return (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
  }

  /**
   * Sube un archivo Excel (.xls, .xlsx) o PDF (.pdf) oficial para parseo automático por el backend (RF10 / CUS11).
   */
  public async uploadSchedule(file: File): Promise<ScheduleImportResponse> {
    const formData = new FormData();
    formData.append('file', file);

    const token = authService.getToken();
    const headers: Record<string, string> = {};
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }

    try {
      const response = await fetch(`${this.getBaseUrl()}/api/v1/spaces/import-schedule`, {
        method: 'POST',
        headers,
        body: formData,
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `Error al procesar cronograma (HTTP ${response.status})`);
      }

      const data: ScheduleImportResponse = await response.json();
      mockSlotsMemory = [...data.aulas_libres];
      lastImportedFileMemory = data.archivo;
      return data;
    } catch (err: unknown) {
      // Fallback en desarrollo / modo mock
      if (useMock && (err instanceof TypeError || String(err).includes('Failed to fetch'))) {
        const ext = file.name.split('.').pop()?.toLowerCase();
        if (ext !== 'xlsx' && ext !== 'xls' && ext !== 'pdf') {
          throw new Error("Extensión no soportada. Solo se admiten archivos oficiales en Excel (.xls, .xlsx) y PDF (.pdf).");
        }

        const simulatedSlots: FreeSlotItem[] = [
          { aula: 'Lab 01', dia: 'Lunes', hora_inicio: '08:00', hora_fin: '10:00', estado: 'LIBRE' },
          { aula: 'Lab 02', dia: 'Martes', hora_inicio: '14:00', hora_fin: '16:00', estado: 'LIBRE' },
          { aula: 'Aula 204', dia: 'Jueves', hora_inicio: '10:00', hora_fin: '12:00', estado: 'LIBRE' },
          { aula: 'Aula 301', dia: 'Viernes', hora_inicio: '16:00', hora_fin: '18:00', estado: 'LIBRE' },
        ];
        mockSlotsMemory = simulatedSlots;
        lastImportedFileMemory = file.name;

        return {
          status: 'PROCESADO_EXITOSAMENTE',
          archivo: file.name,
          total_aulas_libres_identificadas: simulatedSlots.length,
          reservas_activas_preservadas: 0,
          aulas_libres: simulatedSlots,
        };
      }
      throw err;
    }
  }

  /**
   * Consulta las franjas horarias libres activas en la infraestructura física (RN-06).
   */
  public async getFreeSlots(dia?: string, aula?: string): Promise<FreeSlotItem[]> {
    const params = new URLSearchParams();
    if (dia) params.append('dia', dia);
    if (aula) params.append('aula', aula);

    const qs = params.toString();
    const url = `${this.getBaseUrl()}/api/v1/spaces/free-slots${qs ? `?${qs}` : ''}`;

    try {
      const response = await fetch(url);
      if (!response.ok) {
        throw new Error('Error al consultar franjas libres de infraestructura.');
      }
      return await response.json();
    } catch (err) {
      if (!useMock) throw err;
      let filtered = [...mockSlotsMemory];
      if (dia) {
        filtered = filtered.filter((s) => s.dia.toLowerCase() === dia.toLowerCase());
      }
      if (aula) {
        filtered = filtered.filter((s) => s.aula.toLowerCase().includes(aula.toLowerCase()));
      }
      return filtered;
    }
  }

  /**
   * Obtiene la lista de aulas y laboratorios validados (RN-06).
   */
  public async getClassrooms(start?: string, duration = 60): Promise<string[]> {
    try {
      const query = start ? '?' + new URLSearchParams({ fecha_inicio: start, duracion_minutos: String(duration) }) : '';
      const response = await fetch(`${this.getBaseUrl()}/api/v1/spaces/classrooms${query}`);
      if (response.ok) {
        const data: ClassroomListResponse = await response.json();
        return data.aulas;
      }
      if (!useMock) throw new Error('No se pudieron consultar las aulas del cronograma.');
    } catch (err) {
      if (!useMock) throw err;
    }
    return Array.from(new Set(mockSlotsMemory.map((s) => s.aula))).sort();
  }

  public getLastImportedFilename(): string {
    return lastImportedFileMemory;
  }
}

export const spacesService = new SpacesService();
