/**
 * Servicio de Recomendaciones Top-k y Motor EdRecSys — (T-18 / RF06 / CUS02 / RN-11)
 *
 * Trazabilidad:
 * - Requerimiento Funcional: RF06 (Inferencia de recomendaciones personalizadas y ranking Top-k)
 * - Caso de Uso: CUS02 (Explorar feed de recomendaciones personalizadas)
 * - Regla de Negocio RN-03: Mérito académico de mentores (ciclo >= VII)
 * - Regla de Negocio RN-04: Exclusión de sesiones vencidas o con antelación <= 24 h
 * - Regla de Negocio RN-05: Control estricto de aforos inmutables (10 presencial / 20 virtual)
 * - Regla de Negocio RN-11: Priorización y desempate algorítmico (multiplicadores 1.0x a 1.3x)
 * - Requerimiento No Funcional: RNF03 (Explicabilidad y consistencia algorítmica)
 *
 * Contratos REST consumidos:
 * - GET  /api/v1/recommendations/offers   -> Ranking Top-k de sesiones de mentoría en catálogo activo
 * - GET  /api/v1/recommendations/mentors  -> Ranking Top-k de mentores pares más afines
 * - POST /api/v1/recommendations/explain  -> Desglose explicable de compatibilidad (XAI)
 * - GET  /api/v1/recommendations/simulation/testbench -> Ejecución de testbench algorítmico
 */

import { getApiBaseUrl } from './apiClient';
import { authService } from './authService';

// ============================================================================
// Tipos e Interfaces de Datos del Algoritmo EdRecSys (Esquemas Pydantic v2)
// ============================================================================

/**
 * Desglose explicable multifactorial del algoritmo EdRecSys (RNF03).
 */
export interface ScoreBreakdown {
  curricular_affinity: number; // Proporción de asignaturas comunes de interés (0.0 a 1.0)
  course_weight_factor: number; // Factor ponderador de asignatura crítica / filtro (1.0x a 1.3x)
  critical_course_applied: string | null; // Código de la asignatura crítica (ej. 'CI-101')
  topic_overlap_jaccard: number; // Coeficiente de similitud de Jaccard sobre temas silábicos (0.0 a 1.0)
  topic_overlap_dice: number; // Coeficiente de coincidencia de Dice sobre temas silábicos (0.0 a 1.0)
  schedule_compatibility: number; // Compatibilidad de agenda horaria semanal (0.0 a 1.0)
  schedule_matching_slots_count: number; // Cantidad de franjas horarias comunes de 1h
  matching_slots: string[]; // Listado legible de franjas horarias (ej. 'Lun 10:00-11:00')
  modality_compatibility: number; // Concordancia de modalidad formativa (0.0 a 1.0)
  institutional_merit_eligible: boolean; // Cumplimiento de regla de mérito RN-03 (ciclo >= VII)
  explanation_text: string; // Resumen cualitativo explicable en lenguaje natural institucional
}

/**
 * Oferta o sesión de mentoría recomendada en ranking Top-k.
 */
export interface OfferRecommendationItem {
  id_oferta: string;
  id_sesion?: number;
  codigo_sesion: string;
  id_asignatura: number;
  codigo_asignatura: string;
  nombre_asignatura: string;
  id_tema: number;
  nombre_tema: string;
  fecha_inicio: string; // ISO 8601
  duracion_minutos: number;
  modalidad: 'presencial' | 'virtual' | string;
  aforo_maximo: number;
  aforo_disponible: number;
  espacio_asignado: string;
  mentor_email: string;
  mentor_nombre: string | null;
  mentor_ciclo: number; // 7 a 10 según RN-03
  score_total: number;
  breakdown: ScoreBreakdown;
}

/**
 * Mentor académico recomendado en ranking Top-k.
 */
export interface MentorRecommendationItem {
  mentor_email: string;
  mentor_codigo: string | null;
  mentor_nombres: string;
  mentor_apellidos: string;
  mentor_ciclo: number; // 7 a 10 según RN-03
  materias_ofrecidas: number[];
  materias_nombres: string[];
  temas_ofrecidos: number[];
  modalidad_preferida: string;
  score_total: number;
  breakdown: ScoreBreakdown;
}

/**
 * Contenedor genérico de respuestas Top-k emitidas por EdRecSys.
 */
export interface RecommendationListResponse<T> {
  mentee_email: string;
  total_candidates_evaluated: number;
  top_k: number;
  recommendations_count: number;
  algorithm: string;
  items: T[];
}

/**
 * Solicitud de desglose explicable individual (XAI).
 */
export interface RecommendationExplainRequest {
  mentee_email: string;
  mentor_email?: string;
  id_oferta?: string;
}

/**
 * Respuesta detallada con explicabilidad completa del algoritmo EdRecSys.
 */
export interface RecommendationExplainResponse {
  target_type: 'mentor' | 'offer';
  target_id: string;
  mentee_email: string;
  score_total: number;
  breakdown: ScoreBreakdown;
  institutional_summary: string;
}

/**
 * Parámetros para la consulta de ofertas recomendadas.
 */
export interface GetRecommendedOffersParams {
  mentee_email?: string;
  id_asignatura?: number;
  top_k?: number; // 1 a 20, default 5
}

/**
 * Parámetros para la consulta de mentores recomendados.
 */
export interface GetRecommendedMentorsParams {
  mentee_email?: string;
  top_k?: number; // 1 a 20, default 5
}

// ============================================================================
// Manejo Canónico de Excepciones del Recomendador
// ============================================================================

export type RecommendationErrorCode =
  | 'INVALID_EMAIL'
  | 'INVALID_TOP_K'
  | 'UNAUTHORIZED'
  | 'FORBIDDEN'
  | 'NOT_FOUND'
  | 'SERVER_ERROR'
  | 'NETWORK_ERROR'
  | 'INVALID_RESPONSE'
  | 'MOCK_DISABLED'
  | 'EXPLAIN_FAILED';

export class RecommendationException extends Error {
  public code: RecommendationErrorCode;
  public status?: number;

  constructor(code: RecommendationErrorCode, message: string, status?: number) {
    super(message);
    this.name = 'RecommendationException';
    this.code = code;
    this.status = status;
  }
}

// ============================================================================
// Adaptador de API REST Real (FastAPI Backend)
// ============================================================================

export class ApiRecommendationAdapter {
  private baseUrl: string;

  constructor(baseUrl?: string) {
    this.baseUrl = (baseUrl || getApiBaseUrl()).replace(/\/+$/, '');
  }

  public setBaseUrl(url: string): void {
    this.baseUrl = url.replace(/\/+$/, '');
  }

  public getBaseUrl(): string {
    return this.baseUrl;
  }

  private getAuthHeaders(): Record<string, string> {
    const headers: Record<string, string> = {
      'Accept': 'application/json',
    };
    const token = authService.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  /**
   * Consulta el ranking Top-k de ofertas/sesiones de mentoría recomendadas.
   * Preserva estrictamente el ordenamiento determinista provisto por el backend.
   */
  public async getRecommendedOffers(
    params: GetRecommendedOffersParams = {}
  ): Promise<RecommendationListResponse<OfferRecommendationItem>> {
    const { mentee_email, id_asignatura, top_k } = params;

    if (top_k !== undefined && (top_k < 1 || top_k > 20)) {
      throw new RecommendationException(
        'INVALID_TOP_K',
        'El parámetro top_k debe encontrarse estrictamente entre 1 y 20.'
      );
    }

    if (mentee_email !== undefined && mentee_email.trim() !== '') {
      const emailTrim = mentee_email.trim().toLowerCase();
      if (!emailTrim.includes('@')) {
        throw new RecommendationException(
          'INVALID_EMAIL',
          'El correo del mentoreado proporcionado no tiene una estructura de correo válida.'
        );
      }
    }

    const searchParams = new URLSearchParams();
    if (mentee_email && mentee_email.trim() !== '') {
      searchParams.append('mentee_email', mentee_email.trim().toLowerCase());
    }
    if (id_asignatura !== undefined && id_asignatura > 0) {
      searchParams.append('id_asignatura', id_asignatura.toString());
    }
    if (top_k !== undefined) {
      searchParams.append('top_k', top_k.toString());
    }

    const queryStr = searchParams.toString() ? `?${searchParams.toString()}` : '';
    const endpointUrl = `${this.baseUrl}/api/v1/recommendations/offers${queryStr}`;

    let response: Response;
    try {
      response = await fetch(endpointUrl, {
        method: 'GET',
        headers: this.getAuthHeaders(),
      });
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      throw new RecommendationException(
        'NETWORK_ERROR',
        `Error de red al consultar ofertas recomendadas: ${message}`
      );
    }

    if (!response.ok) {
      this.handleHttpErrors(response, 'ofertas recomendadas');
    }

    try {
      const data = await response.json();
      if (!data || typeof data !== 'object' || !Array.isArray(data.items)) {
        throw new RecommendationException(
          'INVALID_RESPONSE',
          'La respuesta del servidor no contiene la estructura canónica esperada para la lista de recomendaciones.'
        );
      }
      return data as RecommendationListResponse<OfferRecommendationItem>;
    } catch (err) {
      if (err instanceof RecommendationException) throw err;
      throw new RecommendationException(
        'INVALID_RESPONSE',
        'Error al deserializar la respuesta JSON del servidor de recomendaciones.'
      );
    }
  }

  /**
   * Consulta el ranking Top-k de mentores más afines para un estudiante mentoreado.
   * Preserva estrictamente el ordenamiento determinista provisto por el backend.
   */
  public async getRecommendedMentors(
    params: GetRecommendedMentorsParams = {}
  ): Promise<RecommendationListResponse<MentorRecommendationItem>> {
    const { mentee_email, top_k } = params;

    if (top_k !== undefined && (top_k < 1 || top_k > 20)) {
      throw new RecommendationException(
        'INVALID_TOP_K',
        'El parámetro top_k debe encontrarse estrictamente entre 1 y 20.'
      );
    }

    if (mentee_email !== undefined && mentee_email.trim() !== '') {
      const emailTrim = mentee_email.trim().toLowerCase();
      if (!emailTrim.includes('@')) {
        throw new RecommendationException(
          'INVALID_EMAIL',
          'El correo del mentoreado proporcionado no tiene una estructura de correo válida.'
        );
      }
    }

    const searchParams = new URLSearchParams();
    if (mentee_email && mentee_email.trim() !== '') {
      searchParams.append('mentee_email', mentee_email.trim().toLowerCase());
    }
    if (top_k !== undefined) {
      searchParams.append('top_k', top_k.toString());
    }

    const queryStr = searchParams.toString() ? `?${searchParams.toString()}` : '';
    const endpointUrl = `${this.baseUrl}/api/v1/recommendations/mentors${queryStr}`;

    let response: Response;
    try {
      response = await fetch(endpointUrl, {
        method: 'GET',
        headers: this.getAuthHeaders(),
      });
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      throw new RecommendationException(
        'NETWORK_ERROR',
        `Error de red al consultar mentores recomendados: ${message}`
      );
    }

    if (!response.ok) {
      this.handleHttpErrors(response, 'mentores recomendados');
    }

    try {
      const data = await response.json();
      if (!data || typeof data !== 'object' || !Array.isArray(data.items)) {
        throw new RecommendationException(
          'INVALID_RESPONSE',
          'La respuesta del servidor no contiene la estructura canónica esperada para la lista de mentores recomendados.'
        );
      }
      return data as RecommendationListResponse<MentorRecommendationItem>;
    } catch (err) {
      if (err instanceof RecommendationException) throw err;
      throw new RecommendationException(
        'INVALID_RESPONSE',
        'Error al deserializar la respuesta JSON del servidor de mentores recomendados.'
      );
    }
  }

  /**
   * Solicita el desglose matemático y explicable (XAI) de afinidad.
   */
  public async explainRecommendation(
    request: RecommendationExplainRequest
  ): Promise<RecommendationExplainResponse> {
    if (!request || !request.mentee_email || request.mentee_email.trim() === '') {
      throw new RecommendationException(
        'EXPLAIN_FAILED',
        'El correo del mentoreado es obligatorio para solicitar la explicación.'
      );
    }

    if (!request.mentor_email && !request.id_oferta) {
      throw new RecommendationException(
        'EXPLAIN_FAILED',
        'Debe proporcionar mentor_email o id_oferta para desglosar la compatibilidad.'
      );
    }

    const endpointUrl = `${this.baseUrl}/api/v1/recommendations/explain`;
    const headers = {
      ...this.getAuthHeaders(),
      'Content-Type': 'application/json',
    };

    let response: Response;
    try {
      response = await fetch(endpointUrl, {
        method: 'POST',
        headers,
        body: JSON.stringify(request),
      });
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      throw new RecommendationException(
        'NETWORK_ERROR',
        `Error de red al solicitar desglose explicable: ${message}`
      );
    }

    if (!response.ok) {
      this.handleHttpErrors(response, 'desglose explicable');
    }

    try {
      const data = await response.json();
      if (!data || typeof data !== 'object' || !data.breakdown) {
        throw new RecommendationException(
          'INVALID_RESPONSE',
          'La respuesta del desglose explicable no cuenta con la estructura requerida.'
        );
      }
      return data as RecommendationExplainResponse;
    } catch (err) {
      if (err instanceof RecommendationException) throw err;
      throw new RecommendationException(
        'INVALID_RESPONSE',
        'Error al deserializar la respuesta JSON del desglose explicable.'
      );
    }
  }

  /**
   * Ejecuta el banco de pruebas algorítmico y casos frontera en el backend.
   */
  public async runSimulationTestbench(): Promise<Record<string, unknown>> {
    const endpointUrl = `${this.baseUrl}/api/v1/recommendations/simulation/testbench`;
    let response: Response;
    try {
      response = await fetch(endpointUrl, {
        method: 'GET',
        headers: this.getAuthHeaders(),
      });
    } catch (err: unknown) {
      const message = err instanceof Error ? err.message : String(err);
      throw new RecommendationException(
        'NETWORK_ERROR',
        `Error de red al ejecutar testbench: ${message}`
      );
    }

    if (!response.ok) {
      this.handleHttpErrors(response, 'testbench de simulación');
    }

    return response.json();
  }

  private handleHttpErrors(response: Response, action: string): never {
    const status = response.status;
    if (status === 401) {
      throw new RecommendationException(
        'UNAUTHORIZED',
        'Sesión no autorizada o token JWT expirado para consultar ' + action + '.',
        status
      );
    }
    if (status === 403) {
      throw new RecommendationException(
        'FORBIDDEN',
        'Acceso restringido: no posee los permisos requeridos para consultar ' + action + '.',
        status
      );
    }
    if (status === 404) {
      throw new RecommendationException(
        'NOT_FOUND',
        'El recurso solicitado no fue localizado en el servidor de recomendaciones.',
        status
      );
    }
    if (status === 422) {
      throw new RecommendationException(
        'INVALID_RESPONSE',
        'Los parámetros de la solicitud no son válidos según el esquema del servidor.',
        status
      );
    }
    if (status >= 500) {
      throw new RecommendationException(
        'SERVER_ERROR',
        `Error interno en el servidor de recomendaciones (${status}).`,
        status
      );
    }
    throw new RecommendationException(
      'SERVER_ERROR',
      `Error HTTP ${status}: ${response.statusText}`,
      status
    );
  }
}

// ============================================================================
// Adaptador Mock Controlado para Entornos de Prueba Local
// ============================================================================

export class MockRecommendationAdapter {
  private mockOffers: OfferRecommendationItem[] = [];
  private mockMentors: MentorRecommendationItem[] = [];

  constructor() {
    this.resetToDefaults();
  }

  public resetToDefaults(): void {
    const defaultBreakdown: ScoreBreakdown = {
      curricular_affinity: 1.0,
      course_weight_factor: 1.3,
      critical_course_applied: 'AED-201',
      topic_overlap_jaccard: 0.8,
      topic_overlap_dice: 0.8889,
      schedule_compatibility: 0.75,
      schedule_matching_slots_count: 6,
      matching_slots: ['Lun 10:00-11:00', 'Mié 14:00-15:00', 'Vie 09:00-10:00'],
      modality_compatibility: 1.0,
      institutional_merit_eligible: true,
      explanation_text:
        'Alta afinidad conceptual en Algoritmos con multiplicador institucional 1.3x y compatibilidad horaria.',
    };

    this.mockOffers = [
      {
        id_oferta: '101',
        codigo_sesion: 'SES-0101',
        id_asignatura: 3,
        codigo_asignatura: 'ALGO-202',
        nombre_asignatura: 'Algoritmos y Estructuras de Datos',
        id_tema: 9,
        nombre_tema: 'Análisis Asintótico y Notación Big-O',
        fecha_inicio: new Date(Date.now() + 72 * 3600 * 1000).toISOString(),
        duracion_minutos: 90,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 8,
        espacio_asignado: 'Laboratorio de Cómputo 101 - Pabellón G (EPIS)',
        mentor_email: 'renzo.antayhua@upt.pe',
        mentor_nombre: 'Renzo Antayhua',
        mentor_ciclo: 8,
        score_total: 0.942,
        breakdown: {
          ...defaultBreakdown,
          critical_course_applied: 'ALGO-202',
        },
      },
      {
        id_oferta: '102',
        codigo_sesion: 'SES-0102',
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 1,
        nombre_tema: 'Límites y Continuidad',
        fecha_inicio: new Date(Date.now() + 96 * 3600 * 1000).toISOString(),
        duracion_minutos: 60,
        modalidad: 'virtual',
        aforo_maximo: 20,
        aforo_disponible: 15,
        espacio_asignado: 'https://meet.google.com/upt-calc-101-demo',
        mentor_email: 'mentor.demo@upt.pe',
        mentor_nombre: 'Carlos Mentor Demo',
        mentor_ciclo: 9,
        score_total: 0.815,
        breakdown: {
          ...defaultBreakdown,
          course_weight_factor: 1.2,
          critical_course_applied: 'CALC-101',
          score_total: 0.815,
        } as unknown as ScoreBreakdown,
      },
    ];

    this.mockMentors = [
      {
        mentor_email: 'renzo.antayhua@upt.pe',
        mentor_codigo: '2021071234',
        mentor_nombres: 'Renzo Antonio',
        mentor_apellidos: 'Antayhua Mamani',
        mentor_ciclo: 8,
        materias_ofrecidas: [1, 3],
        materias_nombres: ['Cálculo I', 'Algoritmos y Estructuras de Datos'],
        temas_ofrecidos: [101, 301],
        modalidad_preferida: 'presencial',
        score_total: 0.942,
        breakdown: defaultBreakdown,
      },
    ];
  }

  public setMockOffers(offers: OfferRecommendationItem[]): void {
    this.mockOffers = offers;
  }

  public setMockMentors(mentors: MentorRecommendationItem[]): void {
    this.mockMentors = mentors;
  }

  public async getRecommendedOffers(
    params: GetRecommendedOffersParams = {}
  ): Promise<RecommendationListResponse<OfferRecommendationItem>> {
    const topK = params.top_k ?? 5;
    let filtered = [...this.mockOffers];
    if (params.id_asignatura) {
      filtered = filtered.filter((o) => o.id_asignatura === params.id_asignatura);
    }
    const sliced = filtered.slice(0, topK);
    return {
      mentee_email: params.mentee_email || '2022074255@upt.pe',
      total_candidates_evaluated: this.mockOffers.length,
      top_k: topK,
      recommendations_count: sliced.length,
      algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
      items: sliced,
    };
  }

  public async getRecommendedMentors(
    params: GetRecommendedMentorsParams = {}
  ): Promise<RecommendationListResponse<MentorRecommendationItem>> {
    const topK = params.top_k ?? 5;
    const sliced = this.mockMentors.slice(0, topK);
    return {
      mentee_email: params.mentee_email || '2022074255@upt.pe',
      total_candidates_evaluated: this.mockMentors.length,
      top_k: topK,
      recommendations_count: sliced.length,
      algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
      items: sliced,
    };
  }

  public async explainRecommendation(
    request: RecommendationExplainRequest
  ): Promise<RecommendationExplainResponse> {
    const isOffer = Boolean(request.id_oferta);
    return {
      target_type: isOffer ? 'offer' : 'mentor',
      target_id: request.id_oferta || request.mentor_email || 'unknown',
      mentee_email: request.mentee_email,
      score_total: 0.942,
      breakdown: {
        curricular_affinity: 1.0,
        course_weight_factor: 1.3,
        critical_course_applied: 'AED-201',
        topic_overlap_jaccard: 0.8,
        topic_overlap_dice: 0.8889,
        schedule_compatibility: 0.75,
        schedule_matching_slots_count: 6,
        matching_slots: ['Lun 10:00-11:00', 'Mié 14:00-15:00'],
        modality_compatibility: 1.0,
        institutional_merit_eligible: true,
        explanation_text:
          'Simulación mock: Alta afinidad conceptual en materias filtro de la EPIS.',
      },
      institutional_summary:
        'Compatibilidad óptima con factor de bonificación 1.3x en Algoritmos y Estructuras de Datos.',
    };
  }
}

// ============================================================================
// Instancias y Fachada del Servicio (recommendationService)
// ============================================================================

function resolveInitialServiceMode(): 'mock' | 'api' {
  if (import.meta.env.PROD) {
    return 'api';
  }
  const envMode = import.meta.env.VITE_SERVICE_MODE;
  if (envMode === 'mock') {
    return 'mock';
  }
  if (envMode === 'api') {
    return 'api';
  }
  if (import.meta.env.MODE === 'test') {
    return 'mock';
  }
  return 'api';
}

const apiAdapterInstance = new ApiRecommendationAdapter();
const mockAdapterInstance = new MockRecommendationAdapter();

// Modo activo: 'api' por defecto en producción/desarrollo, respetando variables de entorno
let currentServiceMode: 'api' | 'mock' = resolveInitialServiceMode();

export const recommendationService = {
  getMode(): 'api' | 'mock' {
    return currentServiceMode;
  },

  setMode(mode: 'api' | 'mock'): void {
    currentServiceMode = mode;
  },

  setBaseUrl(url: string): void {
    apiAdapterInstance.setBaseUrl(url);
  },

  getBaseUrl(): string {
    return apiAdapterInstance.getBaseUrl();
  },

  getApiAdapter(): ApiRecommendationAdapter {
    return apiAdapterInstance;
  },

  getMockAdapter(): MockRecommendationAdapter {
    return mockAdapterInstance;
  },

  /**
   * Consulta el ranking Top-k de ofertas/sesiones de mentoría activas.
   * Preserva estrictamente el orden emitido por el algoritmo EdRecSys.
   */
  async getRecommendedOffers(
    params?: GetRecommendedOffersParams
  ): Promise<RecommendationListResponse<OfferRecommendationItem>> {
    if (currentServiceMode === 'mock') {
      return mockAdapterInstance.getRecommendedOffers(params);
    }
    return apiAdapterInstance.getRecommendedOffers(params);
  },

  /**
   * Consulta el ranking Top-k de mentores más afines.
   * Preserva estrictamente el orden emitido por el algoritmo EdRecSys.
   */
  async getRecommendedMentors(
    params?: GetRecommendedMentorsParams
  ): Promise<RecommendationListResponse<MentorRecommendationItem>> {
    if (currentServiceMode === 'mock') {
      return mockAdapterInstance.getRecommendedMentors(params);
    }
    return apiAdapterInstance.getRecommendedMentors(params);
  },

  /**
   * Obtiene la explicación y desglose transparente (XAI) de la puntuación de compatibilidad.
   */
  async explainRecommendation(
    request: RecommendationExplainRequest
  ): Promise<RecommendationExplainResponse> {
    if (currentServiceMode === 'mock') {
      return mockAdapterInstance.explainRecommendation(request);
    }
    return apiAdapterInstance.explainRecommendation(request);
  },

  /**
   * Ejecuta el banco de pruebas algorítmico y casos frontera.
   */
  async runSimulationTestbench(): Promise<Record<string, unknown>> {
    return apiAdapterInstance.runSimulationTestbench();
  },
};
