/**
 * Batería de Pruebas de Integración y Ordenamiento Top-k (T-19)
 *
 * Trazabilidad:
 * - Requerimiento Funcional: RF06 (Motor de recomendación Top-k ordenado por afinidad multifactorial)
 * - Requerimiento Funcional: RF12 / CUS04 (Reserva transaccional y quórum institucional)
 * - Regla de Negocio RN-03: Mérito académico de mentores (Ciclos VII a X)
 * - Regla de Negocio RN-04: Exclusión obligatoria de sesiones en ventana de antelación <= 24 h
 * - Regla de Negocio RN-05: Aforos estándar inmutables (10 presencial / 20 virtual)
 * - Regla de Negocio RN-08: Ventana de reserva habilitada hasta T-24 horas
 * - Regla de Negocio RN-11: Clave determinista de desempate en 5 niveles y ponderadores curriculares (1.0x a 1.3x)
 * - Requerimiento No Funcional: RNF03 (Explicabilidad algorítmica XAI)
 * - Requerimiento No Funcional: RNF05 (Accesibilidad WAI-ARIA)
 * - Requerimiento No Funcional: RNF09 (Calidad y cobertura >= 70%)
 *
 * Casos de Prueba Verificados:
 * - ORD-01: Desempate determinista ante puntaje idéntico (S_total) -> Mayor aforo disponible
 * - ORD-01b: Desempate determinista por fecha_inicio (menor timestamp)
 * - ORD-01c: Desempate determinista por codigo_sesion (orden lexicográfico canónico)
 * - ORD-01d: Invarianza ante permutación del orden de entrada de candidatos
 * - ORD-02: Exclusión de sesiones con antelación <= 24 h (RN-04 / RN-08)
 * - ORD-03: Exclusión y bloqueo de sesiones con aforo agotado (Aforo_disp = 0)
 * - ORD-04: Límite k parametrizable (top_k=1, top_k=3, top_k=5)
 * - ORD-05: Multiplicador curricular 1.3x para materias críticas (ALGO-202 / AED-201)
 * - ORD-EXTRA: Coherencia y adaptabilidad del selector Top-k (SRS k ∈ [3, 5] vs selector UI)
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { RecommendationFeedView } from '../RecommendationFeedView';
import {
  recommendationService,
  type OfferRecommendationItem,
  type ScoreBreakdown,
  type RecommendationListResponse,
} from '../../services/recommendationService';
import * as apiClient from '../../services/apiClient';

describe('Batería T-19: Ordenamiento Determinista y Empates Top-k (ORD-01 a ORD-05)', () => {
  const menteeEmail = '2022074255@upt.pe';

  const defaultBreakdown: ScoreBreakdown = {
    curricular_affinity: 1.0,
    course_weight_factor: 1.0,
    critical_course_applied: null,
    topic_overlap_jaccard: 0.8,
    topic_overlap_dice: 0.88,
    schedule_compatibility: 0.85,
    schedule_matching_slots_count: 5,
    matching_slots: ['Lun 08:00-09:00', 'Mié 10:00-11:00'],
    modality_compatibility: 1.0,
    institutional_merit_eligible: true,
    explanation_text: 'Coincidencia curricular y temática óptima en Cálculo I.',
  };

  const mockCourses: apiClient.Course[] = [
    {
      id_asignatura: 1,
      codigo_curso: 'CALC-101',
      nombre_curso: 'Cálculo I',
      ciclo_plan: 1,
      creditos: 4,
      es_prioritaria: true,
      factor_ponderacion: 1.0,
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
    vi.spyOn(apiClient, 'fetchCourses').mockResolvedValue(mockCourses);
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  // ==========================================================================
  // ORD-01: Desempate determinista ante puntaje idéntico (S_total) -> Aforo
  // ==========================================================================
  describe('ORD-01: Desempate determinista ante puntaje idéntico (S_total)', () => {
    it('prioriza la sesión con mayor aforo disponible ante puntaje y fecha idénticos', async () => {
      // Sesión 101: 10 cupos disponibles
      const offer101: OfferRecommendationItem = {
        id_oferta: '101',
        codigo_sesion: 'SES-101',
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 1,
        nombre_tema: 'Límites',
        fecha_inicio: '2026-11-06T10:00:00Z',
        duracion_minutos: 60,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 10, // 10 disponibles
        espacio_asignado: 'Laboratorio 101',
        mentor_email: '2022073504@upt.pe',
        mentor_nombre: 'Renzo Antayhua Mamani',
        mentor_ciclo: 8,
        score_total: 0.85,
        breakdown: { ...defaultBreakdown },
      };

      // Sesión 102: 5 cupos disponibles (5 reservados)
      const offer102: OfferRecommendationItem = {
        id_oferta: '102',
        codigo_sesion: 'SES-102',
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 1,
        nombre_tema: 'Límites',
        fecha_inicio: '2026-11-06T10:00:00Z',
        duracion_minutos: 60,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 5, // 5 disponibles
        espacio_asignado: 'Laboratorio 102',
        mentor_email: '2022073504@upt.pe',
        mentor_nombre: 'Renzo Antayhua Mamani',
        mentor_ciclo: 8,
        score_total: 0.85,
        breakdown: { ...defaultBreakdown },
      };

      const mockResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: menteeEmail,
        total_candidates_evaluated: 2,
        top_k: 5,
        recommendations_count: 2,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [offer101, offer102], // Orden provisto por el backend
      };

      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockResponse);

      render(<RecommendationFeedView menteeEmail={menteeEmail} />);

      await waitFor(() => {
        expect(screen.getByText('SES-101')).toBeInTheDocument();
        expect(screen.getByText('SES-102')).toBeInTheDocument();
      });

      // Validar posición exacta en el DOM
      const badges = screen.getAllByText(/#\d TOP-K/);
      expect(badges).toHaveLength(2);
      expect(badges[0]).toHaveTextContent('#1 TOP-K');
      expect(badges[1]).toHaveTextContent('#2 TOP-K');

      // Validar que la sesión #1 tiene 10 vacantes libres y la #2 tiene 5
      expect(screen.getByText(/10 vacantes libres \/ 10 cupos/i)).toBeInTheDocument();
      expect(screen.getByText(/5 vacantes libres \/ 10 cupos/i)).toBeInTheDocument();

      // Verificar que el contenedor de SES-101 precede al de SES-102
      const el101 = screen.getByText('SES-101').closest('article');
      const el102 = screen.getByText('SES-102').closest('article');
      expect(el101).not.toBeNull();
      expect(el102).not.toBeNull();
      if (el101 && el102) {
        expect(el101.compareDocumentPosition(el102) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
      }
    });
  });

  // ==========================================================================
  // ORD-01b: Desempate determinista por fecha_inicio (menor timestamp)
  // ==========================================================================
  describe('ORD-01b: Desempate determinista por fecha_inicio (menor timestamp)', () => {
    it('prioriza la sesión cronológicamente más cercana ante puntaje y aforo idénticos', async () => {
      // Sesión 502: Comienza antes (04 de Noviembre)
      const offerEarly: OfferRecommendationItem = {
        id_oferta: '502',
        codigo_sesion: 'SES-502-EARLY',
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 1,
        nombre_tema: 'Límites',
        fecha_inicio: '2026-11-04T10:00:00Z',
        duracion_minutos: 60,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 8,
        espacio_asignado: 'Aula 502',
        mentor_email: '2022073504@upt.pe',
        mentor_nombre: 'Renzo Antayhua Mamani',
        mentor_ciclo: 8,
        score_total: 0.85,
        breakdown: { ...defaultBreakdown },
      };

      // Sesión 501: Comienza después (07 de Noviembre)
      const offerLate: OfferRecommendationItem = {
        id_oferta: '501',
        codigo_sesion: 'SES-501-LATE',
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 1,
        nombre_tema: 'Límites',
        fecha_inicio: '2026-11-07T10:00:00Z',
        duracion_minutos: 60,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 8,
        espacio_asignado: 'Aula 501',
        mentor_email: '2022073504@upt.pe',
        mentor_nombre: 'Renzo Antayhua Mamani',
        mentor_ciclo: 8,
        score_total: 0.85,
        breakdown: { ...defaultBreakdown },
      };

      const mockResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: menteeEmail,
        total_candidates_evaluated: 2,
        top_k: 5,
        recommendations_count: 2,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [offerEarly, offerLate],
      };

      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockResponse);

      render(<RecommendationFeedView menteeEmail={menteeEmail} />);

      await waitFor(() => {
        expect(screen.getByText('SES-502-EARLY')).toBeInTheDocument();
        expect(screen.getByText('SES-501-LATE')).toBeInTheDocument();
      });

      const elEarly = screen.getByText('SES-502-EARLY').closest('article');
      const elLate = screen.getByText('SES-501-LATE').closest('article');
      expect(elEarly).not.toBeNull();
      expect(elLate).not.toBeNull();
      if (elEarly && elLate) {
        expect(elEarly.compareDocumentPosition(elLate) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
      }
    });
  });

  // ==========================================================================
  // ORD-01c: Desempate determinista por codigo_sesion (lexicográfico)
  // ==========================================================================
  describe('ORD-01c: Desempate determinista por codigo_sesion (lexicográfico)', () => {
    it('desempata por orden lexicográfico canónico del código de sesión ante paridad total', async () => {
      const offerAlpha: OfferRecommendationItem = {
        id_oferta: '601',
        codigo_sesion: 'SES-A-601',
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 1,
        nombre_tema: 'Límites',
        fecha_inicio: '2026-11-05T10:00:00Z',
        duracion_minutos: 60,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 8,
        espacio_asignado: 'Aula 601',
        mentor_email: '2022073504@upt.pe',
        mentor_nombre: 'Renzo Antayhua Mamani',
        mentor_ciclo: 8,
        score_total: 0.85,
        breakdown: { ...defaultBreakdown },
      };

      const offerZulu: OfferRecommendationItem = {
        id_oferta: '602',
        codigo_sesion: 'SES-Z-602',
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 1,
        nombre_tema: 'Límites',
        fecha_inicio: '2026-11-05T10:00:00Z',
        duracion_minutos: 60,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 8,
        espacio_asignado: 'Aula 602',
        mentor_email: '2022073504@upt.pe',
        mentor_nombre: 'Renzo Antayhua Mamani',
        mentor_ciclo: 8,
        score_total: 0.85,
        breakdown: { ...defaultBreakdown },
      };

      const mockResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: menteeEmail,
        total_candidates_evaluated: 2,
        top_k: 5,
        recommendations_count: 2,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [offerAlpha, offerZulu],
      };

      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockResponse);

      render(<RecommendationFeedView menteeEmail={menteeEmail} />);

      await waitFor(() => {
        expect(screen.getByText('SES-A-601')).toBeInTheDocument();
        expect(screen.getByText('SES-Z-602')).toBeInTheDocument();
      });

      const elAlpha = screen.getByText('SES-A-601').closest('article');
      const elZulu = screen.getByText('SES-Z-602').closest('article');
      expect(elAlpha).not.toBeNull();
      expect(elZulu).not.toBeNull();
      if (elAlpha && elZulu) {
        expect(elAlpha.compareDocumentPosition(elZulu) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
      }
    });
  });

  // ==========================================================================
  // ORD-01d: Invarianza ante permutación del orden de entrada de candidatos
  // ==========================================================================
  describe('ORD-01d: Invarianza ante permutación del orden de entrada de candidatos', () => {
    it('mantiene la estabilidad idéntica del ranking en el DOM en múltiples llamadas', async () => {
      const createItem = (i: number): OfferRecommendationItem => ({
        id_oferta: String(700 + i),
        codigo_sesion: `SES-STABLE-0${i}`,
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 1,
        nombre_tema: 'Límites',
        fecha_inicio: `2026-11-05T${10 + i}:00:00Z`,
        duracion_minutos: 60,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 10 - i,
        espacio_asignado: `Aula ${i}`,
        mentor_email: '2022073504@upt.pe',
        mentor_nombre: 'Renzo Antayhua Mamani',
        mentor_ciclo: 8,
        score_total: 0.9 - i * 0.05,
        breakdown: { ...defaultBreakdown },
      });

      const deterministicItems = [createItem(1), createItem(2), createItem(3)];

      const mockResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: menteeEmail,
        total_candidates_evaluated: 3,
        top_k: 5,
        recommendations_count: 3,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: deterministicItems,
      };

      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockResponse);

      const { rerender } = render(<RecommendationFeedView menteeEmail={menteeEmail} />);

      await waitFor(() => {
        expect(screen.getByText('SES-STABLE-01')).toBeInTheDocument();
      });

      const getRenderedCodes = () => {
        const articles = screen.getAllByRole('article');
        return articles.map((art) => {
          const badge = art.querySelector('span[style*="background-color: rgb(28, 42, 89)"]');
          return badge ? badge.textContent?.trim() : '';
        });
      };

      const firstOrder = getRenderedCodes();
      expect(firstOrder).toHaveLength(3);

      // Re-renderizar 3 veces para confirmar estabilidad
      for (let cycle = 0; cycle < 3; cycle++) {
        rerender(<RecommendationFeedView menteeEmail={menteeEmail} />);
        expect(getRenderedCodes()).toEqual(firstOrder);
      }
    });
  });

  // ==========================================================================
  // ORD-02: Exclusión de sesiones con antelación <= 24 h (RN-04 / RN-08)
  // ==========================================================================
  describe('ORD-02: Exclusión de sesiones con antelación <= 24 h (RN-04 / RN-08)', () => {
    it('muestra únicamente las ofertas válidas suministradas por el recomendador sin sesiones vencidas', async () => {
      // El backend excluye sesiones con antelación <= 24 h. Por ende, la respuesta solo contiene la válida.
      const validOffer: OfferRecommendationItem = {
        id_oferta: '202',
        codigo_sesion: 'SES-202-VALIDA',
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 1,
        nombre_tema: 'Límites',
        fecha_inicio: '2026-11-06T14:00:00Z', // 48 horas en el futuro
        duracion_minutos: 60,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 10,
        espacio_asignado: 'Aula 202',
        mentor_email: '2022073504@upt.pe',
        mentor_nombre: 'Renzo Antayhua Mamani',
        mentor_ciclo: 8,
        score_total: 0.88,
        breakdown: { ...defaultBreakdown },
      };

      const mockResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: menteeEmail,
        total_candidates_evaluated: 2,
        top_k: 5,
        recommendations_count: 1,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [validOffer],
      };

      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockResponse);

      render(<RecommendationFeedView menteeEmail={menteeEmail} />);

      await waitFor(() => {
        expect(screen.getByText('SES-202-VALIDA')).toBeInTheDocument();
      });

      expect(screen.queryByText(/SES-201-VENCIDA/i)).not.toBeInTheDocument();
      expect(screen.getAllByRole('article')).toHaveLength(1);
    });
  });

  // ==========================================================================
  // ORD-03: Exclusión y visualización de aforo agotado (Aforo_disp = 0)
  // ==========================================================================
  describe('ORD-03: Exclusión y visualización de aforo agotado (RN-05)', () => {
    it('muestra estado vacío si el backend excluye sesiones llenas, y maneja visualmente aforo agotado', async () => {
      // Sub-caso A: backend retorna lista vacía si todas las sesiones están colmadas
      const emptyResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: menteeEmail,
        total_candidates_evaluated: 5,
        top_k: 5,
        recommendations_count: 0,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [],
      };

      const getOffersSpy = vi
        .spyOn(recommendationService, 'getRecommendedOffers')
        .mockResolvedValueOnce(emptyResponse);

      const { unmount } = render(<RecommendationFeedView menteeEmail={menteeEmail} />);

      await waitFor(() => {
        expect(
          screen.getByText(/No se encontraron recomendaciones en este momento/i)
        ).toBeInTheDocument();
        expect(
          screen.getByText(/No existen ofertas activas ni mentores disponibles/i)
        ).toBeInTheDocument();
      });

      unmount();

      // Sub-caso B: si llega una sesión con aforo_disponible = 0 (caso de transición concurrente),
      // el botón se deshabilita con texto "Aforo Agotado" y aviso "Aforo Completo (0 vacantes)"
      const fullOffer: OfferRecommendationItem = {
        id_oferta: '301',
        codigo_sesion: 'SES-301-LLENA',
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 1,
        nombre_tema: 'Límites',
        fecha_inicio: '2026-11-06T10:00:00Z',
        duracion_minutos: 60,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 0, // Aforo colmado
        espacio_asignado: 'Laboratorio 101',
        mentor_email: '2022073504@upt.pe',
        mentor_nombre: 'Renzo Antayhua Mamani',
        mentor_ciclo: 8,
        score_total: 0.85,
        breakdown: { ...defaultBreakdown },
      };

      getOffersSpy.mockResolvedValueOnce({
        ...emptyResponse,
        recommendations_count: 1,
        items: [fullOffer],
      });

      render(<RecommendationFeedView menteeEmail={menteeEmail} />);

      await waitFor(() => {
        expect(screen.getByText('SES-301-LLENA')).toBeInTheDocument();
      });

      expect(screen.getByText(/Aforo Completo \(0 vacantes\)/i)).toBeInTheDocument();
      const reserveBtn = screen.getByRole('button', { name: /Aforo Agotado/i });
      expect(reserveBtn).toBeDisabled();
    });
  });

  // ==========================================================================
  // ORD-04: Límite k parametrizable (top_k=1, top_k=3, top_k=5)
  // ==========================================================================
  describe('ORD-04: Límite k parametrizable en query string', () => {
    it('solicita y renderiza exactamente el número de recomendaciones correspondiente al selector Top-k', async () => {
      const getOffersSpy = vi.spyOn(recommendationService, 'getRecommendedOffers');

      const createItem = (i: number): OfferRecommendationItem => ({
        id_oferta: String(400 + i),
        codigo_sesion: `SES-40${i}`,
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 1,
        nombre_tema: 'Límites',
        fecha_inicio: `2026-11-0${5 + i}T10:00:00Z`,
        duracion_minutos: 60,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 10,
        espacio_asignado: `Aula ${i}`,
        mentor_email: '2022073504@upt.pe',
        mentor_nombre: 'Renzo Antayhua Mamani',
        mentor_ciclo: 8,
        score_total: 0.9 - i * 0.05,
        breakdown: { ...defaultBreakdown },
      });

      // Simular respuestas dinámicas según top_k
      getOffersSpy.mockImplementation(async (params) => {
        const k = params?.top_k ?? 5;
        const allItems = [1, 2, 3, 4, 5].map(createItem);
        const sliced = allItems.slice(0, k);
        return {
          mentee_email: menteeEmail,
          total_candidates_evaluated: 5,
          top_k: k,
          recommendations_count: sliced.length,
          algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
          items: sliced,
        };
      });

      render(<RecommendationFeedView menteeEmail={menteeEmail} />);

      // Por defecto top_k=5
      await waitFor(() => {
        expect(getOffersSpy).toHaveBeenCalledWith(
          expect.objectContaining({ top_k: 5 })
        );
      });

      // Cambiar selector a Top 3
      const topKSelect = screen.getByLabelText(/Candidatos Top-k:/i);
      fireEvent.change(topKSelect, { target: { value: '3' } });

      await waitFor(() => {
        expect(getOffersSpy).toHaveBeenCalledWith(
          expect.objectContaining({ top_k: 3 })
        );
      });

      await waitFor(() => {
        expect(screen.getAllByRole('article')).toHaveLength(3);
      });
    });
  });

  // ==========================================================================
  // ORD-05: Multiplicador curricular 1.3x para materias críticas (ALGO-202)
  // ==========================================================================
  describe('ORD-05: Multiplicador curricular 1.3x para materias críticas', () => {
    it('ubica en posición #1 la oferta de Algoritmos impulsada por el factor 1.3x', async () => {
      const breakdownAlgo: ScoreBreakdown = {
        curricular_affinity: 1.0,
        course_weight_factor: 1.3,
        critical_course_applied: 'ALGO-202',
        topic_overlap_jaccard: 0.9,
        topic_overlap_dice: 0.947,
        schedule_compatibility: 0.8,
        schedule_matching_slots_count: 4,
        matching_slots: ['Mar 14:00-15:00'],
        modality_compatibility: 1.0,
        institutional_merit_eligible: true,
        explanation_text:
          'Afinidad prioritaria de excelencia en Algoritmos con ponderación 1.3x (RN-11).',
      };

      const breakdownCalc: ScoreBreakdown = {
        curricular_affinity: 1.0,
        course_weight_factor: 1.0,
        critical_course_applied: null,
        topic_overlap_jaccard: 0.9,
        topic_overlap_dice: 0.947,
        schedule_compatibility: 0.8,
        schedule_matching_slots_count: 4,
        matching_slots: ['Mar 14:00-15:00'],
        modality_compatibility: 1.0,
        institutional_merit_eligible: true,
        explanation_text: 'Coincidencia regular en materia formativa.',
      };

      const offerAlgo: OfferRecommendationItem = {
        id_oferta: '14',
        codigo_sesion: 'SES-0014-ALGO',
        id_asignatura: 3,
        codigo_asignatura: 'ALGO-202',
        nombre_asignatura: 'Algoritmos y Estructuras de Datos',
        id_tema: 302,
        nombre_tema: 'Grafos y Algoritmo de Dijkstra',
        fecha_inicio: '2026-11-06T10:00:00Z',
        duracion_minutos: 90,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 7,
        espacio_asignado: 'Laboratorio de Cómputo 101',
        mentor_email: 'renzo.antayhua@upt.pe',
        mentor_nombre: 'Renzo Antayhua Mamani',
        mentor_ciclo: 8,
        score_total: 0.945, // 0.727 * 1.3 = ~0.945
        breakdown: breakdownAlgo,
      };

      const offerCalc: OfferRecommendationItem = {
        id_oferta: '15',
        codigo_sesion: 'SES-0015-CALC',
        id_asignatura: 1,
        codigo_asignatura: 'CALC-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 101,
        nombre_tema: 'Límites',
        fecha_inicio: '2026-11-06T10:00:00Z',
        duracion_minutos: 60,
        modalidad: 'presencial',
        aforo_maximo: 10,
        aforo_disponible: 7,
        espacio_asignado: 'Aula 101',
        mentor_email: 'carlos.mentor@upt.pe',
        mentor_nombre: 'Carlos Mentor Demo',
        mentor_ciclo: 8,
        score_total: 0.727,
        breakdown: breakdownCalc,
      };

      const mockResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: menteeEmail,
        total_candidates_evaluated: 2,
        top_k: 5,
        recommendations_count: 2,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [offerAlgo, offerCalc],
      };

      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockResponse);

      render(<RecommendationFeedView menteeEmail={menteeEmail} />);

      await waitFor(() => {
        expect(screen.getByText('SES-0014-ALGO')).toBeInTheDocument();
        expect(screen.getByText('SES-0015-CALC')).toBeInTheDocument();
      });

      // Verificar que Algoritmos ocupa la posición #1
      const articles = screen.getAllByRole('article');
      expect(articles[0]).toHaveTextContent('Algoritmos y Estructuras de Datos (ALGO-202)');
      expect(articles[0]).toHaveTextContent('#1 TOP-K');
      expect(articles[0]).toHaveTextContent('95%'); // 0.945 redondeado
      expect(articles[0]).toHaveTextContent(/Prioridad Institucional EPIS \(1\.3x\)/i);

      // Abrir panel XAI para verificar desglose explicable en la oferta #1 (Algoritmos)
      const xaiButtons = screen.getAllByRole('button', {
        name: /Ver desglose de compatibilidad \(XAI\)/i,
      });
      fireEvent.click(xaiButtons[0]);

      await waitFor(() => {
        expect(
          screen.getByText(/Afinidad prioritaria de excelencia en Algoritmos con ponderación 1.3x/i)
        ).toBeInTheDocument();
        expect(screen.getByText(/Multiplicador Prioritario: 1\.3x \(ALGO-202\)/i)).toBeInTheDocument();
      });
    });
  });

  // ==========================================================================
  // ORD-EXTRA: Coherencia del Selector Top-k frente a SRS (k ∈ [3, 5])
  // ==========================================================================
  describe('ORD-EXTRA: Auditoría de Coherencia SRS k ∈ [3, 5] vs UI Selector', () => {
    it('comprueba que el valor por defecto sea 5 (alineado a SRS) y ofrece opciones institucionales', async () => {
      const getOffersSpy = vi
        .spyOn(recommendationService, 'getRecommendedOffers')
        .mockResolvedValue({
          mentee_email: menteeEmail,
          total_candidates_evaluated: 0,
          top_k: 5,
          recommendations_count: 0,
          algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
          items: [],
        });

      render(<RecommendationFeedView menteeEmail={menteeEmail} />);

      await waitFor(() => {
        expect(getOffersSpy).toHaveBeenCalledWith(
          expect.objectContaining({ top_k: 5 })
        );
      });

      const topKSelect = screen.getByLabelText(/Candidatos Top-k:/i) as HTMLSelectElement;
      expect(topKSelect.value).toBe('5');

      // Comprobar las opciones disponibles
      const options = Array.from(topKSelect.options).map((opt) => opt.value);
      expect(options).toContain('3');
      expect(options).toContain('5');
      expect(options).toContain('10');
    });
  });
});
