import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, waitFor, fireEvent } from '@testing-library/react';
import { OfferPublishView } from '../OfferPublishView';
import * as apiClient from '../../services/apiClient';
import { offerService } from '../../services/offerService';

describe('OfferPublishView Component (T-14 / RF08 / CUS06)', () => {
  const mentorEmail = '2022074255@upt.pe';
  const mentorName = 'Joan Cristian Medina Quispe';

  const mockCourses: apiClient.Course[] = [
    {
      id_asignatura: 1,
      codigo_curso: 'CI-101',
      nombre_curso: 'Cálculo I',
      ciclo_plan: 1,
      creditos: 4,
      es_prioritaria: true,
      factor_ponderacion: 1.5,
      estado_activo: true,
    },
    {
      id_asignatura: 2,
      codigo_curso: 'CI-201',
      nombre_curso: 'Cálculo II',
      ciclo_plan: 2,
      creditos: 4,
      es_prioritaria: true,
      factor_ponderacion: 1.5,
      estado_activo: true,
    },
  ];

  const mockDetailCourse1: apiClient.CourseDetail = {
    ...mockCourses[0],
    temas: [
      {
        id_tema: 101,
        id_asignatura: 1,
        nombre_tema: 'Límites Indeterminados y Continuidad',
        descripcion_silabo: 'Concepto formal de límites.',
        unidad_silabica: 1,
        estado_activo: true,
      },
      {
        id_tema: 102,
        id_asignatura: 1,
        nombre_tema: 'Derivadas y Optimización',
        descripcion_silabo: 'Cálculo diferencial y aplicaciones.',
        unidad_silabica: 2,
        estado_activo: true,
      },
    ],
  };

  const mockDetailCourse2: apiClient.CourseDetail = {
    ...mockCourses[1],
    temas: [
      {
        id_tema: 201,
        id_asignatura: 2,
        nombre_tema: 'Técnicas de Integración por Partes',
        descripcion_silabo: 'Métodos analíticos de cálculo integral.',
        unidad_silabica: 1,
        estado_activo: true,
      },
    ],
  };

  beforeEach(() => {
    vi.restoreAllMocks();
    offerService.setMode('mock');
    offerService.clearMockOffers();

    vi.spyOn(apiClient, 'fetchCourses').mockResolvedValue(mockCourses);
    vi.spyOn(apiClient, 'fetchCourseDetail').mockImplementation(async (id: number) => {
      if (id === 2) return mockDetailCourse2;
      return mockDetailCourse1;
    });
  });

  it('1. Renderiza el formulario con banner de modo de prueba local y datos del mentor', async () => {
    render(<OfferPublishView mentorEmail={mentorEmail} mentorName={mentorName} />);

    // Verifica banner de modo prueba local (Backend pendiente)
    expect(screen.getByText(/Modo de prueba local — Backend pendiente/i)).toBeInTheDocument();
    expect(screen.getByText(/T-14 · Joan \(Frontend\)/i)).toBeInTheDocument();

    // Verifica título e identidad del mentor
    expect(screen.getByText(/Publicar Nueva Oferta de Mentoría/i)).toBeInTheDocument();
    expect(screen.getAllByText(new RegExp(mentorName, 'i')).length).toBeGreaterThanOrEqual(1);

    await waitFor(() => {
      expect(screen.getByLabelText(/Asignatura formativa/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Unidad temática silábica/i)).toBeInTheDocument();
    });
  });

  describe('CUS06-U02: Control estricto de aforo automático según modalidad (RN-05)', () => {
    it('2. Inicia con modalidad presencial y fija el aforo inmutable en 10 estudiantes', async () => {
      render(<OfferPublishView mentorEmail={mentorEmail} mentorName={mentorName} />);

      await waitFor(() => {
        expect(screen.getByLabelText(/Aforo reglamentario/i)).toHaveValue('10 Estudiantes');
        expect(screen.getByText(/Límite fijo de 10 participantes para sesiones presenciales \(RN-05\)/i)).toBeInTheDocument();
      });
    });

    it('3. Al cambiar a modalidad Virtual, actualiza reactivamente el aforo a 20 estudiantes de forma inmutable', async () => {
      render(<OfferPublishView mentorEmail={mentorEmail} mentorName={mentorName} />);

      await waitFor(() => {
        expect(screen.getByLabelText(/Aforo reglamentario/i)).toHaveValue('10 Estudiantes');
      });

      const virtualBtn = screen.getByRole('button', { name: /Virtual/i });
      fireEvent.click(virtualBtn);

      await waitFor(() => {
        expect(screen.getByLabelText(/Aforo reglamentario/i)).toHaveValue('20 Estudiantes');
        expect(screen.getByText(/Límite fijo de 20 participantes para sesiones virtuales \(RN-05\)/i)).toBeInTheDocument();
        // Verifica que también cambió la infraestructura a enlace virtual con RN-07
        expect(screen.getByText(/RN-07: Aprovisionamiento Virtual/i)).toBeInTheDocument();
      });
    });
  });

  describe('RN-04: Validación reactiva de antelación obligatoria (> 24 h)', () => {
    it('4. Detecta y bloquea la publicación con mensaje de infracción de RN-04 si la antelación es <= 24 horas', async () => {
      render(<OfferPublishView mentorEmail={mentorEmail} mentorName={mentorName} />);

      await waitFor(() => {
        expect(screen.getByLabelText(/Fecha y hora de inicio/i)).toBeInTheDocument();
      });

      // Fecha muy cercana: 5 horas a partir de ahora
      const nearFuture = new Date(Date.now() + 5 * 3600 * 1000);
      const year = nearFuture.getFullYear();
      const month = String(nearFuture.getMonth() + 1).padStart(2, '0');
      const day = String(nearFuture.getDate()).padStart(2, '0');
      const hours = String(nearFuture.getHours()).padStart(2, '0');
      const minutes = String(nearFuture.getMinutes()).padStart(2, '0');
      const dateString = `${year}-${month}-${day}T${hours}:${minutes}`;

      const dateInput = screen.getByLabelText(/Fecha y hora de inicio/i);
      fireEvent.change(dateInput, { target: { value: dateString } });

      await waitFor(() => {
        expect(screen.getByText(/Infracción de RN-04/i)).toBeInTheDocument();
      });

      const submitBtn = screen.getByRole('button', { name: /Publicar Oferta de Mentoría/i });
      expect(submitBtn).toBeDisabled();
    });

    it('5. Habilita el envío e indica recomendación institucional si la antelación es > 24 h', async () => {
      render(<OfferPublishView mentorEmail={mentorEmail} mentorName={mentorName} />);

      await waitFor(() => {
        expect(screen.getByLabelText(/Fecha y hora de inicio/i)).toBeInTheDocument();
      });

      // 36 horas a partir de ahora: mayor a 24 h pero menor a 48 h
      const validFuture = new Date(Date.now() + 36 * 3600 * 1000);
      const dateString = `${validFuture.getFullYear()}-${String(validFuture.getMonth() + 1).padStart(2, '0')}-${String(
        validFuture.getDate()
      ).padStart(2, '0')}T${String(validFuture.getHours()).padStart(2, '0')}:${String(validFuture.getMinutes()).padStart(2, '0')}`;

      const dateInput = screen.getByLabelText(/Fecha y hora de inicio/i);
      fireEvent.change(dateInput, { target: { value: dateString } });

      await waitFor(() => {
        expect(screen.getByText(/Antelación válida/i)).toBeInTheDocument();
        expect(screen.getByText(/Recomendación institucional/i)).toBeInTheDocument();
      });

      const submitBtn = screen.getByRole('button', { name: /Publicar Oferta de Mentoría/i });
      expect(submitBtn).not.toBeDisabled();
    });
  });

  describe('CUS06-F01 & CUS06-F02: Flujo interactivo completo de publicación y feedback', () => {
    it('6. Permite cambiar de curso, actualizar dinámicamente los temas y publicar exitosamente', async () => {
      const onPublishedMock = vi.fn();
      render(
        <OfferPublishView
          mentorEmail={mentorEmail}
          mentorName={mentorName}
          onOfferPublished={onPublishedMock}
        />
      );

      // Esperar a que se carguen los cursos iniciales
      await waitFor(() => {
        expect(screen.getByLabelText(/Asignatura formativa/i)).toBeInTheDocument();
      });

      // Cambiar asignatura a Cálculo II (id: 2)
      const courseSelect = screen.getByLabelText(/Asignatura formativa/i);
      fireEvent.change(courseSelect, { target: { value: '2' } });

      // Verificar que los temas se actualizaron para Cálculo II
      await waitFor(() => {
        expect(screen.getByText(/Técnicas de Integración por Partes/i)).toBeInTheDocument();
      });

      // Modificar duración a 90 minutos
      const durationSelect = screen.getByLabelText(/Duración de la sesión/i);
      fireEvent.change(durationSelect, { target: { value: '90' } });

      // Agregar observaciones pedagógicas
      const notesInput = screen.getByLabelText(/Observaciones pedagógicas/i);
      fireEvent.change(notesInput, { target: { value: 'Preparar ejercicios de integrales impropias para la práctica.' } });

      // Enviar formulario
      const submitBtn = screen.getByRole('button', { name: /Publicar Oferta de Mentoría/i });
      expect(submitBtn).not.toBeDisabled();
      fireEvent.click(submitBtn);

      // Verificar pantalla de confirmación exitosa
      await waitFor(() => {
        expect(screen.getByText(/¡Oferta de mentoría publicada exitosamente!/i)).toBeInTheDocument();
        expect(screen.getByText(/Código oficial de sesión:/i)).toBeInTheDocument();
        expect(screen.getAllByText(/Cálculo II/i).length).toBeGreaterThanOrEqual(1);
      });

      expect(onPublishedMock).toHaveBeenCalledTimes(1);

      // Verificar que la nueva oferta aparece en el listado de ofertas publicadas
      expect(screen.getByText(/Mis Ofertas de Mentoría Publicadas/i)).toBeInTheDocument();
      expect(screen.getAllByText(/Cálculo II/i).length).toBeGreaterThanOrEqual(1);
    });

    it('7. El botón "Publicar Otra Oferta" restablece el estado para un nuevo registro', async () => {
      render(<OfferPublishView mentorEmail={mentorEmail} mentorName={mentorName} />);

      await waitFor(() => {
        expect(screen.getByRole('button', { name: /Publicar Oferta de Mentoría/i })).toBeInTheDocument();
      });

      // Publicar oferta inicial
      const submitBtn = screen.getByRole('button', { name: /Publicar Oferta de Mentoría/i });
      fireEvent.click(submitBtn);

      await waitFor(() => {
        expect(screen.getByText(/¡Oferta de mentoría publicada exitosamente!/i)).toBeInTheDocument();
      });

      // Clic en "Publicar Otra Oferta"
      const resetBtn = screen.getByRole('button', { name: /\+ Publicar Otra Oferta/i });
      fireEvent.click(resetBtn);

      await waitFor(() => {
        expect(screen.queryByText(/¡Oferta de mentoría publicada exitosamente!/i)).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: /Publicar Oferta de Mentoría/i })).toBeInTheDocument();
      });
    });
  });
});
