import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { App } from '../App';

describe('App Component (Navegación Institucional)', () => {
  it('permite alternar entre las pestañas de Acceso, Consentimiento, Cursos, Perfil y Publicar Ofertas', async () => {
    render(<App />);

    // 1. Por defecto inicia en pestaña de acceso (Iniciar sesión)
    expect(screen.getByRole('button', { name: /Iniciar sesión/i })).toBeInTheDocument();
    expect(screen.getByLabelText(/Correo Electrónico Institucional/i)).toBeInTheDocument();

    // 2. Cambiar a Consentimiento
    const consentTab = screen.getByRole('button', { name: /^⚖️ Consentimiento$/i });
    fireEvent.click(consentTab);
    await waitFor(() => {
      expect(screen.getAllByText(/Consentimiento Informado/i).length).toBeGreaterThanOrEqual(1);
    });

    // 3. Cambiar a Cursos
    const curriculumTab = screen.getByRole('button', { name: /Cursos/i });
    fireEvent.click(curriculumTab);
    await waitFor(() => {
      expect(screen.getByText(/Buscar por curso, código o tema silábico/i)).toBeInTheDocument();
    });

    // 4. Cambiar a Mi perfil
    const profileTab = screen.getByRole('button', { name: /Mi perfil/i });
    fireEvent.click(profileTab);
    await waitFor(() => {
      expect(screen.getByText(/1. Perfil Formativo Académico/i)).toBeInTheDocument();
    });

    // 5. Cambiar a Publicar mentoría
    const offersTab = screen.getByRole('button', { name: /Publicar mentoría/i });
    fireEvent.click(offersTab);
    await waitFor(() => {
      expect(screen.getByText(/Publicar Nueva Oferta de Mentoría/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Asignatura formativa/i)).toBeInTheDocument();
    });

    // 6. Cambiar a Mis Reservas
    const bookingsTab = screen.getByRole('button', { name: /^📅 Mis Reservas$/i });
    fireEvent.click(bookingsTab);
    await waitFor(() => {
      expect(screen.getByText(/Mis Reservas de Mentoría/i)).toBeInTheDocument();
    });

    // 7. Cambiar a Estado del sistema
    const monitorTab = screen.getByRole('button', { name: /Estado del sistema/i });
    fireEvent.click(monitorTab);
    await waitFor(() => {
      expect(screen.getByText(/Estado de los Servicios del Sistema/i)).toBeInTheDocument();
    });
  });
});
