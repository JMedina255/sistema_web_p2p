import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { RecommendationFeedView } from '../RecommendationFeedView';
import {
  recommendationService,
  RecommendationException,
  type OfferRecommendationItem,
  type MentorRecommendationItem,
  type ScoreBreakdown,
  type RecommendationListResponse,
} from '../../services/recommendationService';
import * as apiClient from '../../services/apiClient';

describe('RecommendationFeedView Component (T-20 / RF06 / CUS02 / RN-11)', () => {
  const mockBreakdown1: ScoreBreakdown = {
    curricular_affinity: 1.0,
    course_weight_factor: 1.3,
    critical_course_applied: 'AED-201',
    topic_overlap_jaccard: 0.85,
    topic_overlap_dice: 0.9189,
    schedule_compatibility: 0.9,
    schedule_matching_slots_count: 6,
    matching_slots: ['Lun 10:00-11:00', 'Mié 14:00-15:00'],
    modality_compatibility: 1.0,
    institutional_merit_eligible: true,
    explanation_text:
      'Afinidad conceptual de excelencia en Algoritmos con ponderación 1.3x y disponibilidad óptima.',
  };

  const mockBreakdown2: ScoreBreakdown = {
    curricular_affinity: 0.8,
    course_weight_factor: 1.0,
    critical_course_applied: null,
    topic_overlap_jaccard: 0.5,
    topic_overlap_dice: 0.6667,
    schedule_compatibility: 0.6,
    schedule_matching_slots_count: 3,
    matching_slots: ['Mar 09:00-10:00'],
    modality_compatibility: 0.8,
    institutional_merit_eligible: true,
    explanation_text:
      'Compatibilidad regular en materia electiva.',
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
    aforo_disponible: 6,
    espacio_asignado: 'Laboratorio de Cómputo 101 - Pabellón G (EPIS)',
    mentor_email: 'renzo.antayhua@upt.pe',
    mentor_nombre: 'Renzo Antayhua Mamani',
    mentor_ciclo: 8,
    score_total: 0.945,
    breakdown: mockBreakdown1,
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
    aforo_disponible: 0, // Aforo completo para prueba de botón deshabilitado
    espacio_asignado: 'https://meet.google.com/upt-ci-101-demo',
    mentor_email: 'carlos.mentor@upt.pe',
    mentor_nombre: 'Carlos Mentor Demo',
    mentor_ciclo: 9,
    score_total: 0.82,
    breakdown: mockBreakdown2,
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
    breakdown: mockBreakdown1,
  };

  const mockOffersResponse: RecommendationListResponse<OfferRecommendationItem> = {
    mentee_email: '2022074255@upt.pe',
    total_candidates_evaluated: 5,
    top_k: 5,
    recommendations_count: 2,
    algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
    items: [sampleOffer1, sampleOffer2],
  };

  const mockMentorsResponse: RecommendationListResponse<MentorRecommendationItem> = {
    mentee_email: '2022074255@upt.pe',
    total_candidates_evaluated: 3,
    top_k: 5,
    recommendations_count: 1,
    algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
    items: [sampleMentor],
  };

  const mockCourses: apiClient.Course[] = [
    {
      id_asignatura: 1,
      codigo_curso: 'CI-101',
      nombre_curso: 'Cálculo I',
      ciclo_plan: 1,
      creditos: 4,
      es_prioritaria: true,
      factor_ponderacion: 1.2,
      estado_activo: true,
    },
    {
      id_asignatura: 3,
      codigo_curso: 'AED-201',
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

  // ==========================================================================
  // 1. Renderizado inicial y estado de carga
  // ==========================================================================
  describe('1. Renderizado inicial y estado de carga', () => {
    it('muestra el indicador de carga accesible mientras consulta el servicio', async () => {
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockReturnValue(new Promise(() => {}));
      vi.spyOn(apiClient, 'fetchCourses').mockReturnValue(new Promise(() => {}));

      render(<RecommendationFeedView />);

      expect(screen.getByRole('status')).toBeInTheDocument();
      expect(screen.getByText(/Calculando afinidad multifactorial con EdRecSys/i)).toBeInTheDocument();
      expect(screen.getByText(/Cartelera Inteligente de Mentorías/i)).toBeInTheDocument();
    });

    it('renderiza el encabezado institucional y las pestañas principales', async () => {
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockOffersResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByText(/Cartelera Inteligente de Mentorías \(EdRecSys v1.0\)/i)).toBeInTheDocument();
      });

      expect(screen.getByRole('tab', { name: /Sesiones Recomendadas/i })).toBeInTheDocument();
      expect(screen.getByRole('tab', { name: /Mentores Académicos/i })).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 2. Visualización de recomendaciones y preservación del orden Top-k
  // ==========================================================================
  describe('2. Visualización de recomendaciones y orden Top-k (RF06 / CUS02)', () => {
    it('despliega las sesiones respetando estrictamente el orden emitido por el backend', async () => {
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockOffersResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByText(/SES-0014/i)).toBeInTheDocument();
      });

      const headings = screen.getAllByRole('heading', { level: 3 });
      expect(headings[0]).toHaveTextContent('Algoritmos y Estructuras de Datos (AED-201)');
      expect(headings[1]).toHaveTextContent('Cálculo I (CI-101)');

      expect(screen.getByText(/#1 TOP-K/i)).toBeInTheDocument();
      expect(screen.getByText(/#2 TOP-K/i)).toBeInTheDocument();
      expect(screen.getByText('95%')).toBeInTheDocument(); // 0.945 redondeado a 95%
      expect(screen.getByText('82%')).toBeInTheDocument();
    });

    it('muestra atributos de mentor, modalidad, fecha y vacantes', async () => {
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockOffersResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByText(/Renzo Antayhua Mamani \(Ciclo 8\)/i)).toBeInTheDocument();
      });

      expect(screen.getByText(/6 vacantes libres \/ 10 cupos/i)).toBeInTheDocument();
      expect(screen.getByText(/Laboratorio de Cómputo 101/i)).toBeInTheDocument();
      expect(screen.getByText(/Grafos y Algoritmo de Dijkstra/i)).toBeInTheDocument();
    });

    it('identifica y resalta asignaturas de Prioridad Institucional EPIS (RN-11 / RF24)', async () => {
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockOffersResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByText(/Prioridad Institucional EPIS \(1.3x\)/i)).toBeInTheDocument();
      });
    });

    it('deshabilita el botón de reserva y señala "Aforo Completo" cuando aforo_disponible <= 0', async () => {
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockOffersResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByText(/Aforo Completo \(0 vacantes\)/i)).toBeInTheDocument();
      });

      const disabledBtn = screen.getByRole('button', { name: /Aforo Agotado/i });
      expect(disabledBtn).toBeDisabled();

      const activeBtn = screen.getByRole('button', { name: /Reservar Cupo/i });
      expect(activeBtn).toBeEnabled();
    });
  });

  // ==========================================================================
  // 3. Explicabilidad algorítmica XAI (RNF03)
  // ==========================================================================
  describe('3. Panel expandible de explicabilidad XAI (RNF03)', () => {
    it('expande el panel explicable al pulsar el botón de desglose', async () => {
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockOffersResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getAllByRole('button', { name: /Ver desglose de compatibilidad/i })[0]).toBeInTheDocument();
      });

      const expandBtn = screen.getAllByRole('button', { name: /Ver desglose de compatibilidad/i })[0];
      expect(expandBtn).toHaveAttribute('aria-expanded', 'false');

      fireEvent.click(expandBtn);

      expect(expandBtn).toHaveAttribute('aria-expanded', 'true');
      expect(screen.getByText(/Justificación algorítmica:/i)).toBeInTheDocument();
      expect(
        screen.getByText(/Afinidad conceptual de excelencia en Algoritmos con ponderación 1.3x/i)
      ).toBeInTheDocument();

      // Métricas matemáticas
      expect(screen.getByText(/Similitud Temática Jaccard/i)).toBeInTheDocument();
      expect(screen.getByText(/Índice de Dice:/i)).toBeInTheDocument();
      expect(screen.getByText(/91\.9%/i)).toBeInTheDocument();
      expect(screen.getByText(/Multiplicador Prioritario: 1.3x \(AED-201\)/i)).toBeInTheDocument();
      expect(screen.getByText(/Mérito Docente Acreditado \(RN-03: Ciclo VII-X\)/i)).toBeInTheDocument();

      // Franjas horarias
      expect(screen.getByText('Lun 10:00-11:00')).toBeInTheDocument();
      expect(screen.getByText('Mié 14:00-15:00')).toBeInTheDocument();

      // Colapsar nuevamente
      fireEvent.click(expandBtn);
      expect(expandBtn).toHaveAttribute('aria-expanded', 'false');
      expect(screen.queryByText(/Justificación algorítmica:/i)).not.toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 4. Alternancia entre Sesiones y Mentores Académicos
  // ==========================================================================
  describe('4. Navegación entre pestañas de exploración', () => {
    it('permite alternar a la pestaña de mentores y despliega el ranking de candidatos', async () => {
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockOffersResponse);
      const mentorsSpy = vi
        .spyOn(recommendationService, 'getRecommendedMentors')
        .mockResolvedValue(mockMentorsResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByRole('tab', { name: /Mentores Académicos/i })).toBeInTheDocument();
      });

      const mentorsTab = screen.getByRole('tab', { name: /Mentores Académicos/i });
      fireEvent.click(mentorsTab);

      await waitFor(() => {
        expect(mentorsSpy).toHaveBeenCalledTimes(1);
        expect(screen.getByText(/#1 TOP-K MENTOR/i)).toBeInTheDocument();
      });

      expect(screen.getByText('Renzo Antonio Antayhua Mamani')).toBeInTheDocument();
      expect(screen.getByText(/Ciclo 8 \(RN-03\)/i)).toBeInTheDocument();
      expect(screen.getByText(/Asignaturas de asesoría académica:/i)).toBeInTheDocument();
      expect(screen.getByText('Algoritmos y Estructuras de Datos')).toBeInTheDocument();
    });
  });

  // ==========================================================================
  // 5. Manejo de conjunto vacío (Empty-State) y CUS03 / RF07
  // ==========================================================================
  describe('5. Empty-State pedagógico y orientación a demanda (CUS03 / RF07)', () => {
    it('muestra el panel orientativo institucional cuando no hay recomendaciones', async () => {
      const emptyResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: '2022074255@upt.pe',
        total_candidates_evaluated: 0,
        top_k: 5,
        recommendations_count: 0,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [],
      };

      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(emptyResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByRole('status', { name: /No hay recomendaciones disponibles/i })).toBeInTheDocument();
      });

      expect(screen.getByText(/No se encontraron recomendaciones en este momento/i)).toBeInTheDocument();
      expect(screen.getByText(/Banco de Solicitudes por Demanda/i)).toBeInTheDocument();
      expect(screen.getByText(/¿Necesitas asesoría en un tema específico\? \(RF07 \/ CUS03\)/i)).toBeInTheDocument();
    });

    it('ejecuta el callback onRequestDemand al presionar el botón de solicitud por demanda', async () => {
      const emptyResponse: RecommendationListResponse<OfferRecommendationItem> = {
        mentee_email: '2022074255@upt.pe',
        total_candidates_evaluated: 0,
        top_k: 5,
        recommendations_count: 0,
        algorithm: 'EdRecSys-v1.0-HybridMultifactorial',
        items: [],
      };

      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(emptyResponse);
      const onDemandSpy = vi.fn();

      render(<RecommendationFeedView onRequestDemand={onDemandSpy} />);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /Registrar Solicitud por Demanda \(CUS03\)/i })).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Registrar Solicitud por Demanda \(CUS03\)/i }));
      expect(onDemandSpy).toHaveBeenCalledTimes(1);
    });
  });

  // ==========================================================================
  // 6. Manejo de errores y reintento
  // ==========================================================================
  describe('6. Manejo de errores y reintentos', () => {
    it('muestra mensaje de alerta y botón de reintentar ante fallo del servicio', async () => {
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockRejectedValue(
        new RecommendationException('NETWORK_ERROR', 'Servidor no disponible momentáneamente.')
      );

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByRole('alert')).toBeInTheDocument();
      });

      expect(screen.getByText(/Servidor no disponible momentáneamente/i)).toBeInTheDocument();

      // Simular recuperación en el reintento
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockOffersResponse);
      const retryBtn = screen.getByRole('button', { name: /Reintentar/i });
      fireEvent.click(retryBtn);

      await waitFor(() => {
        expect(screen.getByText(/Algoritmos y Estructuras de Datos/i)).toBeInTheDocument();
      });
    });
  });

  // ==========================================================================
  // 7. Filtros y Callbacks de Interacción
  // ==========================================================================
  describe('7. Filtros reactivos e interacciones', () => {
    it('dispara onSelectOffer al presionar el botón de reservar', async () => {
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockOffersResponse);
      const onSelectSpy = vi.fn();

      render(<RecommendationFeedView onSelectOffer={onSelectSpy} />);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /Reservar Cupo/i })).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Reservar Cupo/i }));
      expect(onSelectSpy).toHaveBeenCalledTimes(1);
      expect(onSelectSpy).toHaveBeenCalledWith(sampleOffer1);
    });

    it('permite filtrar por asignatura disparando la consulta con id_asignatura', async () => {
      const getOffersSpy = vi
        .spyOn(recommendationService, 'getRecommendedOffers')
        .mockResolvedValue(mockOffersResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByLabelText(/Asignatura:/i)).toBeInTheDocument();
      });

      const courseSelect = screen.getByLabelText(/Asignatura:/i);
      fireEvent.change(courseSelect, { target: { value: '3' } });

      await waitFor(() => {
        expect(getOffersSpy).toHaveBeenCalledWith(
          expect.objectContaining({
            id_asignatura: 3,
          })
        );
      });
    });

    it('permite cambiar el valor del selector Top-k', async () => {
      const getOffersSpy = vi
        .spyOn(recommendationService, 'getRecommendedOffers')
        .mockResolvedValue(mockOffersResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByLabelText(/Candidatos Top-k:/i)).toBeInTheDocument();
      });

      const topkSelect = screen.getByLabelText(/Candidatos Top-k:/i);
      fireEvent.change(topkSelect, { target: { value: '3' } });

      await waitFor(() => {
        expect(getOffersSpy).toHaveBeenCalledWith(
          expect.objectContaining({
            top_k: 3,
          })
        );
      });
    });

    it('el botón Actualizar dispara una nueva recarga manual', async () => {
      const getOffersSpy = vi
        .spyOn(recommendationService, 'getRecommendedOffers')
        .mockResolvedValue(mockOffersResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /Actualizar recomendaciones/i })).toBeInTheDocument();
      });

      fireEvent.click(screen.getByRole('button', { name: /Actualizar recomendaciones/i }));
      await waitFor(() => {
        expect(getOffersSpy).toHaveBeenCalledTimes(2);
      });
    });
  });

  // ==========================================================================
  // 8. Accesibilidad WAI-ARIA
  // ==========================================================================
  describe('8. Accesibilidad WAI-ARIA (RNF05)', () => {
    it('cuenta con atributos tablist, tab, tabpanel y progressbar accesibles', async () => {
      vi.spyOn(recommendationService, 'getRecommendedOffers').mockResolvedValue(mockOffersResponse);

      render(<RecommendationFeedView />);

      await waitFor(() => {
        expect(screen.getByRole('tablist')).toBeInTheDocument();
      });

      const tablist = screen.getByRole('tablist');
      expect(tablist).toHaveAttribute('aria-label', 'Modo de exploración de recomendaciones');

      const offersTab = screen.getByRole('tab', { name: /Sesiones Recomendadas/i });
      expect(offersTab).toHaveAttribute('aria-selected', 'true');

      const tabpanel = screen.getByRole('tabpanel');
      expect(tabpanel).toBeInTheDocument();
    });
  });
});
