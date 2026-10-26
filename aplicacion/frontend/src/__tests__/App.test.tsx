import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { App } from '../App';

describe('App Component (Sprint Navigation)', () => {
  it('permite alternar entre las pestañas de Acceso, Consentimiento, Catálogo, Perfil y Publicar Ofertas', async () => {
    render(<App />);

    // 1. Por defecto inicia en pestaña de acceso (T-02)
    expect(screen.getByText(/Acceso & OTP/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Correo Electrónico Institucional/i)).toBeInTheDocument();

    // 2. Cambiar a Consentimiento Ley 29733 (T-04)
    const consentTab = screen.getByRole('button', { name: /Consentimiento Ley 29733/i });
    fireEvent.click(consentTab);
    await waitFor(() => {
      expect(screen.getAllByText(/Consentimiento Informado Digital/i).length).toBeGreaterThanOrEqual(1);
    });

    // 3. Cambiar a Catálogo Curricular (T-10)
    const curriculumTab = screen.getByRole('button', { name: /Catálogo Curricular/i });
    fireEvent.click(curriculumTab);
    await waitFor(() => {
      expect(screen.getByText(/Buscar por curso, código o tema silábico/i)).toBeInTheDocument();
    });

    // 4. Cambiar a Perfil & Disponibilidad (T-11)
    const profileTab = screen.getByRole('button', { name: /Perfil & Disponibilidad/i });
    fireEvent.click(profileTab);
    await waitFor(() => {
      expect(screen.getByText(/1. Perfil Formativo Académico/i)).toBeInTheDocument();
    });

    // 5. Cambiar a Publicar Ofertas (T-14)
    const offersTab = screen.getByRole('button', { name: /Publicar Ofertas/i });
    fireEvent.click(offersTab);
    await waitFor(() => {
      expect(screen.getByText(/Publicar Nueva Oferta de Mentoría/i)).toBeInTheDocument();
      expect(screen.getByText(/Modo de prueba local — Backend pendiente/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Asignatura formativa/i)).toBeInTheDocument();
    });

    // 6. Cambiar a Monitor de Servicios (T-01)
    const monitorTab = screen.getByRole('button', { name: /Monitor de Servicios/i });
    fireEvent.click(monitorTab);
    await waitFor(() => {
      expect(screen.getByText(/Monitor de Servicios \(Hito 2 · T-01\)/i)).toBeInTheDocument();
    });
  });
});
