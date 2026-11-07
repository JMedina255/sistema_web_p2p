import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { App } from '../App';
import { authService } from '../services/authService';

describe('App Component (Navegación Institucional por Rol)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.clear();
    authService.clearToken();
  });

  afterEach(() => {
    sessionStorage.clear();
    vi.restoreAllMocks();
  });

  it('1. Navegación en modo visitante: solo muestra Iniciar sesión y Cursos', async () => {
    render(<App />);

    // Por defecto inicia en pestaña de acceso (Iniciar sesión)
    expect(screen.getAllByRole('heading', { name: /Iniciar Sesión Institucional/i }).length).toBeGreaterThanOrEqual(1);
    expect(screen.getByLabelText(/Correo Electrónico Institucional/i)).toBeInTheDocument();

    // Las pestañas privadas no están visibles en el menú del visitante
    expect(screen.queryByRole('button', { name: /Explorar mentorías/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Mis sesiones/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Administración/i })).not.toBeInTheDocument();

    // Cambiar a Cursos (pestaña pública)
    const curriculumTab = screen.getByRole('button', { name: /Cursos/i });
    fireEvent.click(curriculumTab);
    await waitFor(() => {
      expect(screen.getByText(/Buscar por curso, código o tema silábico/i)).toBeInTheDocument();
    });
  });

  it('2. Navegación en rol mentor: muestra menú específico de mentoría', async () => {
    const mentorEmail = 'mentor.test@upt.pe';
    const testPayload = { sub: mentorEmail, roles: ['mentor', 'mentoreado'] };
    authService.saveToken(`h.${btoa(JSON.stringify(testPayload))}.s`);

    render(<App />);

    // El mentor ve Mis sesiones, Publicar mentoría, Cursos y Mi perfil
    const sessionsTab = screen.getByRole('button', { name: /^📋 Mis sesiones$/i });
    const offersTab = screen.getByRole('button', { name: /^🏷️ Publicar mentoría$/i });
    const curriculumTab = screen.getByRole('button', { name: /^📚 Cursos$/i });
    const profileTab = screen.getByRole('button', { name: /^👤 Mi perfil$/i });

    expect(sessionsTab).toBeInTheDocument();
    expect(offersTab).toBeInTheDocument();
    expect(curriculumTab).toBeInTheDocument();
    expect(profileTab).toBeInTheDocument();

    // No debe ver administración
    expect(screen.queryByRole('button', { name: /^🛡️ Administración$/i })).not.toBeInTheDocument();

    // Alternar a Publicar mentoría
    fireEvent.click(offersTab);
    await waitFor(() => {
      expect(screen.getByText(/Publicar Nueva Oferta de Mentoría/i)).toBeInTheDocument();
      expect(screen.getByLabelText(/Asignatura formativa/i)).toBeInTheDocument();
    });

    // Alternar a Mi perfil
    fireEvent.click(profileTab);
    await waitFor(() => {
      expect(screen.getByText(/1. Perfil Formativo Académico/i)).toBeInTheDocument();
    });
  });

  it('3. Navegación en rol administrador: muestra menú de administración y telemetría', async () => {
    const adminEmail = 'admin.general@upt.pe';
    const testPayload = { sub: adminEmail, roles: ['administrador'] };
    authService.saveToken(`h.${btoa(JSON.stringify(testPayload))}.s`);

    render(<App />);

    const adminTab = screen.getByRole('button', { name: /^🛡️ Administración$/i });
    const servicesTab = screen.getByRole('button', { name: /^🛰️ Estado del sistema$/i });
    const curriculumTab = screen.getByRole('button', { name: /^📚 Cursos$/i });

    expect(adminTab).toBeInTheDocument();
    expect(servicesTab).toBeInTheDocument();
    expect(curriculumTab).toBeInTheDocument();

    // Alternar a Estado del sistema
    fireEvent.click(servicesTab);
    await waitFor(() => {
      expect(screen.getByText(/Estado de los Servicios del Sistema/i)).toBeInTheDocument();
    });
  });
});
