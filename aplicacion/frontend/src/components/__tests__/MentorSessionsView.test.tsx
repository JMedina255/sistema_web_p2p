import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { MentorSessionsView } from '../MentorSessionsView';
import { offerService } from '../../services/offerService';

describe('MentorSessionsView Component (RF08 / RN-05 / RN-08 / RN-09 / Sprint 5 & 6)', () => {
  const mentorEmail = 'mentor.avanzado@upt.pe';

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('1. Muestra estado vacío cuando el mentor no tiene sesiones y permite navegar a publicar', async () => {
    vi.spyOn(offerService, 'getOffers').mockResolvedValue([]);
    const onPublish = vi.fn();

    render(
      <MentorSessionsView
        mentorEmail={mentorEmail}
        onNavigateToPublish={onPublish}
      />
    );

    await waitFor(() => {
      expect(screen.getByText(/No tienes sesiones de mentoría publicadas actualmente/i)).toBeInTheDocument();
    });

    const publishBtn = screen.getByRole('button', { name: /Publicar Mi Primera Sesión/i });
    fireEvent.click(publishBtn);
    expect(onPublish).toHaveBeenCalledTimes(1);
  });

  it('2. Soporta onPublishNewOffer prop alternativa para navegación', async () => {
    vi.spyOn(offerService, 'getOffers').mockResolvedValue([]);
    const onPublishAlt = vi.fn();

    render(
      <MentorSessionsView
        mentorEmail={mentorEmail}
        onPublishNewOffer={onPublishAlt}
      />
    );

    await waitFor(() => {
      expect(screen.getByText(/No tienes sesiones de mentoría publicadas actualmente/i)).toBeInTheDocument();
    });

    const publishBtn = screen.getByRole('button', { name: /Publicar Mi Primera Sesión/i });
    fireEvent.click(publishBtn);
    expect(onPublishAlt).toHaveBeenCalledTimes(1);
  });

  it('3. Despliega sesiones publicadas calculando aforo y estado de quórum', async () => {
    vi.spyOn(offerService, 'getOffers').mockResolvedValue([
      {
        id_oferta: '101',
        codigo_sesion: 'SES-0101',
        estado: 'PUBLICADA',
        mensaje: 'Oferta publicada exitosamente',
        fecha_publicacion: new Date().toISOString(),
        espacio_asignado: 'Lab 101',
        modo: 'api',
        aforo: 10,
        offer: {
          id_asignatura: 1,
          codigo_asignatura: 'CALC-101',
          nombre_asignatura: 'Cálculo I',
          id_tema: 1,
          nombre_tema: 'Límites y Continuidad',
          fecha_inicio: new Date(Date.now() + 48 * 3600 * 1000).toISOString(),
          duracion_minutos: 60,
          modalidad: 'presencial',
          aforo_maximo: 10,
          espacio_asignado: 'Lab 101',
          mentor_email: mentorEmail,
        },
      },
    ]);

    render(<MentorSessionsView mentorEmail={mentorEmail} />);

    await waitFor(() => {
      expect(screen.getByText('Cálculo I')).toBeInTheDocument();
      expect(screen.getByText(/Límites y Continuidad/i)).toBeInTheDocument();
      expect(screen.getByText(/10 plazas/i)).toBeInTheDocument();
    });
  });
});
