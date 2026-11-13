import type { HealthResponse, DbHealthResponse } from '../data/types';
import { authService } from './authService';

const API_BASE_URL: string =
  (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';

function getAuthHeaders(): Record<string, string> {
  const token = authService.getToken();
  const headers: Record<string, string> = {
    'Accept': 'application/json',
    'Content-Type': 'application/json',
  };
  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }
  return headers;
}

export async function fetchHealth(): Promise<HealthResponse> {
  const url = `${API_BASE_URL}/api/v1/health`;
  const response = await fetch(url, {
    method: 'GET',
    headers: {
      'Accept': 'application/json',
    },
  });

  if (!response.ok) {
    throw new Error(`Error HTTP ${response.status}: ${response.statusText}`);
  }

  const data: HealthResponse = await response.json();
  return data;
}

export async function fetchDbHealth(): Promise<DbHealthResponse | null> {
  const url = `${API_BASE_URL}/api/v1/health/db`;
  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Accept': 'application/json',
      },
    });

    if (response.status === 404) {
      // Endpoint no expuesto fuera de desarrollo
      return null;
    }

    const data = await response.json();
    return data as DbHealthResponse;
  } catch (err) {
    console.warn('No fue posible consultar /health/db:', err);
    return null;
  }
}

export function getApiBaseUrl(): string {
  return API_BASE_URL;
}

export interface Course {
  id_asignatura: number;
  codigo_curso: string;
  nombre_curso: string;
  ciclo_plan: number;
  creditos: number;
  es_prioritaria: boolean;
  factor_ponderacion: number;
  estado_activo: boolean;
}

export interface Topic {
  id_tema: number;
  id_asignatura: number;
  nombre_tema: string;
  descripcion_silabo?: string;
  unidad_silabica: number;
  estado_activo: boolean;
}

export interface CourseDetail extends Course {
  temas: Topic[];
}

export async function fetchCourses(onlyPriority: boolean = false, ciclo?: number): Promise<Course[]> {
  const params = new URLSearchParams();
  if (onlyPriority) params.append('only_priority', 'true');
  if (ciclo !== undefined) params.append('ciclo', ciclo.toString());

  const queryString = params.toString() ? `?${params.toString()}` : '';
  const url = `${API_BASE_URL}/api/v1/curriculum/courses${queryString}`;
  const response = await fetch(url, {
    method: 'GET',
    headers: { 'Accept': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`Error HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

export async function fetchCourseDetail(id: number): Promise<CourseDetail> {
  const url = `${API_BASE_URL}/api/v1/curriculum/courses/${id}`;
  const response = await fetch(url, {
    method: 'GET',
    headers: { 'Accept': 'application/json' },
  });

  if (!response.ok) {
    throw new Error(`Error HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

export interface CourseCreatePayload {
  codigo_curso: string;
  nombre_curso: string;
  ciclo_plan: number;
  creditos: number;
  es_prioritaria?: boolean;
  factor_ponderacion?: number;
  estado_activo?: boolean;
}

export interface CourseUpdatePayload {
  codigo_curso?: string;
  nombre_curso?: string;
  ciclo_plan?: number;
  creditos?: number;
  es_prioritaria?: boolean;
  factor_ponderacion?: number;
  estado_activo?: boolean;
}

export interface TopicCreatePayload {
  nombre_tema: string;
  descripcion_silabo?: string;
  unidad_silabica?: number;
  estado_activo?: boolean;
}

export interface TopicUpdatePayload {
  nombre_tema?: string;
  descripcion_silabo?: string;
  unidad_silabica?: number;
  estado_activo?: boolean;
}

export async function createCourse(payload: CourseCreatePayload): Promise<Course> {
  const url = `${API_BASE_URL}/api/v1/curriculum/courses`;
  const response = await fetch(url, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Error HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

export async function updateCourse(id: number, payload: CourseUpdatePayload): Promise<Course> {
  const url = `${API_BASE_URL}/api/v1/curriculum/courses/${id}`;
  const response = await fetch(url, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Error HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

export async function deleteCourse(id: number): Promise<{ mensaje: string; id_asignatura: number }> {
  const url = `${API_BASE_URL}/api/v1/curriculum/courses/${id}`;
  const response = await fetch(url, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Error HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

export async function createTopic(idAsignatura: number, payload: TopicCreatePayload): Promise<Topic> {
  const url = `${API_BASE_URL}/api/v1/curriculum/courses/${idAsignatura}/topics`;
  const response = await fetch(url, {
    method: 'POST',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Error HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

export async function updateTopic(idTema: number, payload: TopicUpdatePayload): Promise<Topic> {
  const url = `${API_BASE_URL}/api/v1/curriculum/topics/${idTema}`;
  const response = await fetch(url, {
    method: 'PUT',
    headers: getAuthHeaders(),
    body: JSON.stringify(payload),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Error HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}

export async function deleteTopic(idTema: number): Promise<{ mensaje: string; id_tema: number }> {
  const url = `${API_BASE_URL}/api/v1/curriculum/topics/${idTema}`;
  const response = await fetch(url, {
    method: 'DELETE',
    headers: getAuthHeaders(),
  });
  if (!response.ok) {
    const err = await response.json().catch(() => ({}));
    throw new Error(err.detail || `Error HTTP ${response.status}: ${response.statusText}`);
  }
  return response.json();
}
