import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import {
  recommendationService,
  ApiRecommendationAdapter,
  MockRecommendationAdapter,
  RecommendationException,
  type OfferRecommendationItem,
  type MentorRecommendationItem,
  type ScoreBreakdown,
  type RecommendationListResponse,
  type RecommendationExplainResponse,
} from '../recommendationService';
import { authService } from '../authService';

describe('recommendationService & ApiRecommendationAdapter (T-18 / RF06 / CUS02 / RN-11)', () => {
  const testBaseUrl = 'http://localhost:8000';
  let apiAdapter: ApiRecommendationAdapter;

  const mockScoreBreakdown: ScoreBreakdown = {
    curricular_affinity: 1.0,
    course_weight_factor: 1.3,
    critical_course_applied: 'AED-201',
    topic_overlap_jaccard: 0.75,
    topic_overlap_dice: 0.857,
    schedule_compatibility: 0.8,
    schedule_matching_slots_count: 5,
    matching_slots: ['Lun 10:00-11:00', 'Mié 14:00-15:00'],
    modality_compatibility: 1.0,
    institutional_merit_eligible: true,
    explanation_text:
      'Alta afinidad temática en Algoritmos con ponderador institucional 1.3x y compatibilidad horaria.',
  };

  const sampleOffer1: OfferRecommendationItem = {
    id_oferta: '14',
    codigo_sesion: 'SES-0014',
    id_asignatura: 3,
    codigo_asignatura: 'AED-201',
    nombre_asignatura: 'Algoritmos y Estructuras de Datos',
    id_tema: 302,
    nombre_tema: 'Grafos y Algoritmo de Dijkstra',
    fecha_inicio: '2026-11-05T10:00:00Z',
    duracion_minutos: 90,
    modalidad: 'presencial',
    aforo_maximo: 10,
    aforo_disponible: 7,
    espacio_asignado: 'Laboratorio de Cómputo 101 - Pabellón G (EPIS)',
    mentor_email: 'renzo.antayhua@upt.pe',
    mentor_nombre: 'Renzo Antayhua Mamani',
    mentor_ciclo: 8,
    score_total: 0.945,
    breakdown: mockScoreBreakdown,
  };

  const sampleOffer2: OfferRecommendationItem = {
    id_oferta: '15',
    codigo_sesion: 'SES-0015',
    id_asignatura: 1,
    codigo_asignatura: 'CI-101',
    nombre_asignatura: 'Cálculo I',
    id_tema: 101,
    nombre_tema: 'Límites Notables',
    fecha_inicio: '2026-11-06T14:00:00Z',
    duracion_minutos: 60,
    modalidad: 'virtual',
    aforo_maximo: 20,
    aforo_disponible: 18,
    espacio_asignado: 'https://meet.google.com/upt-ci-101-demo',
    mentor_email: 'carlos.mentor@upt.pe',
    mentor_nombre: 'Carlos Mentor Demo',
    mentor_ciclo: 9,
    score_total: 0.82,
    breakdown: {
      ...mockScoreBreakdown,
      course_weight_factor: 1.2,
      critical_course_applied: 'CI-101',
      score_total: 0.82,
    } as unknown as ScoreBreakdown,
  };

  const sampleMentor: MentorRecommendationItem = {
    mentor_email: 'renzo.antayhua@upt.pe',
    mentor_codigo: '2021071234',
    mentor_nombres: 'Renzo Antonio',
    mentor_apellidos: 'Antayhua Mamani',
    mentor_ciclo: 8,
    materias_ofrecidas: [1, 3],
    materias_nombres: ['Cálculo I', 'Algoritmos y Estructuras de Datos'],
    temas_ofrecidos: [101, 302],
    modalidad_preferida: 'presencial',
    score_total: 0.945,
    breakdown: mockScoreBreakdown,
  };

  beforeEach(() => {
    apiAdapter = new ApiRecommendationAdapter(testBaseUrl);
    recommendationService.setMode('api');
    recommendationService.setBaseUrl(testBaseUrl);
    authService.clearToken();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    authService.clearToken();
    recommendationService.setMode('api');
  });

  // ==========================================================================
  // 1. Consulta de Ofertas Recomendadas (GET /api/v1/recommendations/offers)
  // ==========================================================================
  describe('1. Consulta de Ofertas Recomendadas (T-18 / CUS02-U01 / RF06)', () => {
    it('consume el endpoint real con los parámetros por defecto y sin token', async () => {
      const mockResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: '2022074255@upt.pe',
        total_candidates_evaluated: 5,
        top_k: 5,
        recommendations_count: 2,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [sampleOffer1, sampleOffer2],
      };

      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockResponse,
      } as Response);

      const result = await apiAdapter.getRecommendedOffers();

      expect(fetchSpy).toHaveBeenCalledTimes(1);
      const [url, options] = fetchSpy.mock.calls[0];
      expect(url).toBe('http://localhost:8000/api/v1/recommendations/offers');
      expect(options?.method).toBe('GET');
      expect(options?.headers).toEqual({ Accept: 'application/json' });
      expect(result.items.length).toBe(2);
      expect(result.items[0].codigo_sesion).toBe('SES-0014');
    });

    it('incluye parámetros query mentee_email, id_asignatura y top_k', async () => {
      const mockResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: 'estudiante.test@upt.pe',
        total_candidates_evaluated: 3,
        top_k: 3,
        recommendations_count: 1,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [sampleOffer1],
      };

      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockResponse,
      } as Response);

      const result = await apiAdapter.getRecommendedOffers({
        mentee_email: 'estudiante.test@upt.pe',
        id_asignatura: 3,
        top_k: 3,
      });

      const [url] = fetchSpy.mock.calls[0];
      const parsedUrl = new URL(url as string);
      expect(parsedUrl.pathname).toBe('/api/v1/recommendations/offers');
      expect(parsedUrl.searchParams.get('mentee_email')).toBe('estudiante.test@upt.pe');
      expect(parsedUrl.searchParams.get('id_asignatura')).toBe('3');
      expect(parsedUrl.searchParams.get('top_k')).toBe('3');
      expect(result.recommendations_count).toBe(1);
    });

    it('adjunta el token de autorización Bearer cuando el usuario está autenticado', async () => {
      authService.saveToken('jwt.test.token.secret');

      const mockResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: 'estudiante.auth@upt.pe',
        total_candidates_evaluated: 1,
        top_k: 5,
        recommendations_count: 1,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [sampleOffer1],
      };

      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockResponse,
      } as Response);

      await apiAdapter.getRecommendedOffers();

      const [, options] = fetchSpy.mock.calls[0];
      expect(options?.headers).toEqual({
        Accept: 'application/json',
        Authorization: 'Bearer jwt.test.token.secret',
      });
    });

    it('preserva estrictamente el ordenamiento Top-k emitido por el backend (ORD-01)', async () => {
      const mockResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: '2022074255@upt.pe',
        total_candidates_evaluated: 2,
        top_k: 5,
        recommendations_count: 2,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [sampleOffer1, sampleOffer2],
      };

      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockResponse,
      } as Response);

      const result = await apiAdapter.getRecommendedOffers();

      expect(result.items[0].codigo_sesion).toBe('SES-0014');
      expect(result.items[0].score_total).toBe(0.945);
      expect(result.items[1].codigo_sesion).toBe('SES-0015');
      expect(result.items[1].score_total).toBe(0.82);
    });

    it('maneja ordenadamente una respuesta con conjunto vacío (empty-state / CUS03)', async () => {
      const emptyResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: '2022074255@upt.pe',
        total_candidates_evaluated: 0,
        top_k: 5,
        recommendations_count: 0,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [],
      };

      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => emptyResponse,
      } as Response);

      const result = await apiAdapter.getRecommendedOffers({ id_asignatura: 99 });
      expect(result.items).toEqual([]);
      expect(result.recommendations_count).toBe(0);
      expect(result.total_candidates_evaluated).toBe(0);
    });

    it('rechaza en el cliente un parámetro top_k menor a 1 o mayor a 20', async () => {
      await expect(apiAdapter.getRecommendedOffers({ top_k: 0 })).rejects.toThrowError(
        expect.objectContaining({ code: 'INVALID_TOP_K' })
      );

      try {
        await apiAdapter.getRecommendedOffers({ top_k: 0 });
      } catch (err) {
        expect(err).toBeInstanceOf(RecommendationException);
        expect((err as RecommendationException).name).toBe('RecommendationException');
      }

      await expect(apiAdapter.getRecommendedOffers({ top_k: 25 })).rejects.toThrowError(
        expect.objectContaining({ code: 'INVALID_TOP_K' })
      );
    });

    it('rechaza en el cliente un correo de mentoreado con formato inválido', async () => {
      await expect(
        apiAdapter.getRecommendedOffers({ mentee_email: 'invalido-sin-arroba' })
      ).rejects.toThrowError(expect.objectContaining({ code: 'INVALID_EMAIL' }));
    });
  });

  // ==========================================================================
  // 2. Consulta de Mentores Recomendados (GET /api/v1/recommendations/mentors)
  // ==========================================================================
  describe('2. Consulta de Mentores Recomendados (T-18 / RF06)', () => {
    it('obtiene el ranking Top-k de mentores con mérito académico RN-03 verificado', async () => {
      const mockResponse: RecommendationListResponse<MentorRecommendationItem> = {
        mentee_email: '2022074255@upt.pe',
        total_candidates_evaluated: 3,
        top_k: 5,
        recommendations_count: 1,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [sampleMentor],
      };

      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockResponse,
      } as Response);

      const result = await apiAdapter.getRecommendedMentors({
        mentee_email: '2022074255@upt.pe',
        top_k: 5,
      });

      expect(fetchSpy).toHaveBeenCalledTimes(1);
      const [url] = fetchSpy.mock.calls[0];
      expect(url).toContain('/api/v1/recommendations/mentors');
      expect(result.items[0].mentor_email).toBe('renzo.antayhua@upt.pe');
      expect(result.items[0].mentor_ciclo).toBeGreaterThanOrEqual(7);
      expect(result.items[0].breakdown.institutional_merit_eligible).toBe(true);
    });
  });

  // ==========================================================================
  // 3. Desglose Explicable de Compatibilidad (POST /api/v1/recommendations/explain)
  // ==========================================================================
  describe('3. Desglose Explicable XAI (T-18 / RNF03)', () => {
    it('solicita la explicación detallada de una oferta enviando JSON en el body', async () => {
      const explainResponse: RecommendationExplainResponse = {
        target_type: 'offer',
        target_id: '14',
        mentee_email: '2022074255@upt.pe',
        score_total: 0.945,
        breakdown: mockScoreBreakdown,
        institutional_summary:
          'Compatibilidad óptima con factor de bonificación 1.3x en Algoritmos.',
      };

      const fetchSpy = vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => explainResponse,
      } as Response);

      const result = await apiAdapter.explainRecommendation({
        mentee_email: '2022074255@upt.pe',
        id_oferta: '14',
      });

      expect(fetchSpy).toHaveBeenCalledTimes(1);
      const [url, options] = fetchSpy.mock.calls[0];
      expect(url).toBe('http://localhost:8000/api/v1/recommendations/explain');
      expect(options?.method).toBe('POST');
      expect(options?.headers).toMatchObject({
        Accept: 'application/json',
        'Content-Type': 'application/json',
      });
      expect(JSON.parse(options?.body as string)).toEqual({
        mentee_email: '2022074255@upt.pe',
        id_oferta: '14',
      });
      expect(result.breakdown.course_weight_factor).toBe(1.3);
      expect(result.breakdown.critical_course_applied).toBe('AED-201');
      expect(result.breakdown.topic_overlap_jaccard).toBe(0.75);
    });

    it('valida la presencia obligatoria de mentee_email y target_id antes del envío', async () => {
      await expect(
        apiAdapter.explainRecommendation({ mentee_email: '' })
      ).rejects.toThrowError(expect.objectContaining({ code: 'EXPLAIN_FAILED' }));

      await expect(
        apiAdapter.explainRecommendation({ mentee_email: '2022074255@upt.pe' })
      ).rejects.toThrowError(expect.objectContaining({ code: 'EXPLAIN_FAILED' }));
    });
  });

  // ==========================================================================
  // 4. Testbench Algorítmico y Casos Frontera
  // ==========================================================================
  describe('4. Testbench Algorítmico (T-18 / RNF03)', () => {
    it('consume exitosamente el endpoint de benchmark algorítmico', async () => {
      const benchmarkData = {
        timestamp: '2026-11-02T12:00:00Z',
        total_evaluations: 100,
        average_latency_ms: 2.4,
        edge_cases_passed: 4,
      };

      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => benchmarkData,
      } as Response);

      const result = await apiAdapter.runSimulationTestbench();
      expect(result.edge_cases_passed).toBe(4);
      expect(result.total_evaluations).toBe(100);
    });
  });

  // ==========================================================================
  // 5. Manejo Canónico de Errores HTTP y de Red
  // ==========================================================================
  describe('5. Manejo Canónico de Errores HTTP y de Red', () => {
    it('mapea respuesta HTTP 401 a excepción UNAUTHORIZED', async () => {
      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: false,
        status: 401,
        statusText: 'Unauthorized',
      } as Response);

      await expect(apiAdapter.getRecommendedOffers()).rejects.toThrowError(
        expect.objectContaining({ code: 'UNAUTHORIZED', status: 401 })
      );
    });

    it('mapea respuesta HTTP 403 a excepción FORBIDDEN', async () => {
      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: false,
        status: 403,
        statusText: 'Forbidden',
      } as Response);

      await expect(apiAdapter.getRecommendedOffers()).rejects.toThrowError(
        expect.objectContaining({ code: 'FORBIDDEN', status: 403 })
      );
    });

    it('mapea respuesta HTTP 404 a excepción NOT_FOUND', async () => {
      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: false,
        status: 404,
        statusText: 'Not Found',
      } as Response);

      await expect(apiAdapter.getRecommendedOffers()).rejects.toThrowError(
        expect.objectContaining({ code: 'NOT_FOUND', status: 404 })
      );
    });

    it('mapea respuesta HTTP 422 a excepción INVALID_RESPONSE', async () => {
      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: false,
        status: 422,
        statusText: 'Unprocessable Entity',
      } as Response);

      await expect(apiAdapter.getRecommendedOffers()).rejects.toThrowError(
        expect.objectContaining({ code: 'INVALID_RESPONSE', status: 422 })
      );
    });

    it('mapea respuesta HTTP 500 a excepción SERVER_ERROR', async () => {
      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: false,
        status: 500,
        statusText: 'Internal Server Error',
      } as Response);

      await expect(apiAdapter.getRecommendedOffers()).rejects.toThrowError(
        expect.objectContaining({ code: 'SERVER_ERROR', status: 500 })
      );
    });

    it('mapea fallos de conexión a NETWORK_ERROR', async () => {
      vi.spyOn(globalThis, 'fetch').mockRejectedValueOnce(new Error('Connection reset by peer'));

      await expect(apiAdapter.getRecommendedOffers()).rejects.toThrowError(
        expect.objectContaining({ code: 'NETWORK_ERROR' })
      );
    });

    it('mapea respuestas malformadas sin array items a INVALID_RESPONSE', async () => {
      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => ({ no_items: true }),
      } as Response);

      await expect(apiAdapter.getRecommendedOffers()).rejects.toThrowError(
        expect.objectContaining({ code: 'INVALID_RESPONSE' })
      );
    });
  });

  // ==========================================================================
  // 6. Fachada recommendationService y Adaptador Mock
  // ==========================================================================
  describe('6. Fachada recommendationService y Alternancia de Modo', () => {
    it('opera por defecto en modo API e interactúa con el adaptador real', async () => {
      expect(recommendationService.getMode()).toBe('api');

      const mockResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: '2022074255@upt.pe',
        total_candidates_evaluated: 1,
        top_k: 5,
        recommendations_count: 1,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [sampleOffer1],
      };

      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockResponse,
      } as Response);

      const res = await recommendationService.getRecommendedOffers();
      expect(res.items.length).toBe(1);
      expect(res.items[0].codigo_sesion).toBe('SES-0014');
    });

    it('permite alternar a modo mock para pruebas controladas de UI sin red', async () => {
      recommendationService.setMode('mock');
      expect(recommendationService.getMode()).toBe('mock');

      const mockAdapter = recommendationService.getMockAdapter();
      expect(mockAdapter).toBeInstanceOf(MockRecommendationAdapter);

      const offersRes = await recommendationService.getRecommendedOffers({ top_k: 2 });
      expect(offersRes.items.length).toBeLessThanOrEqual(2);
      expect(offersRes.algorithm).toBe('EdRecSys-v1.0-HybridMultifactorial');

      const mentorsRes = await recommendationService.getRecommendedMentors();
      expect(mentorsRes.items.length).toBeGreaterThan(0);

      const explainRes = await recommendationService.explainRecommendation({
        mentee_email: '2022074255@upt.pe',
        id_oferta: '101',
      });
      expect(explainRes.breakdown.course_weight_factor).toBe(1.3);
    });

    it('permite personalizar ofertas y mentores en el adaptador mock', async () => {
      const mockAdapter = new MockRecommendationAdapter();
      mockAdapter.setMockOffers([sampleOffer1]);
      mockAdapter.setMockMentors([sampleMentor]);

      const offers = await mockAdapter.getRecommendedOffers({ id_asignatura: 3 });
      expect(offers.items.length).toBe(1);
      expect(offers.items[0].codigo_sesion).toBe('SES-0014');

      const noOffers = await mockAdapter.getRecommendedOffers({ id_asignatura: 999 });
      expect(noOffers.items.length).toBe(0);
    });
  });
});
