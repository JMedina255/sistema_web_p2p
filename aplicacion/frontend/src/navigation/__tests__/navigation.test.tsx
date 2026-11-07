/**
 * Batería de Pruebas Automatizadas de Navegación y Control de Acceso por Rol (RBAC)
 * Sistema Web P2P de Mentorías Académicas — EPIS UPT
 *
 * Cobertura de escenarios canónicos NAV-01 a NAV-14:
 * - NAV-01: Visitante solo visualiza 'auth' y 'curriculum'.
 * - NAV-02: Visitante intentando acceder a '?tab=admin' recibe Acceso Restringido.
 * - NAV-03: Visitante intentando acceder a '?tab=sessions' recibe Acceso Restringido.
 * - NAV-04: Mentoreado visualiza menú de estudiante ('recommendations', 'bookings', 'curriculum', 'profile').
 * - NAV-05: Mentoreado intentando acceder a '?tab=admin' recibe Acceso No Autorizado.
 * - NAV-06: Mentor visualiza menú de mentor ('sessions', 'offers', 'curriculum', 'profile').
 * - NAV-07: Mentor intentando acceder a '?tab=admin' recibe Acceso No Autorizado.
 * - NAV-08: Administrador visualiza menú directivo ('admin', 'curriculum', 'services').
 * - NAV-09: Usuario multi-rol alterna perfiles, actualizando menú y vistas de forma reactiva.
 * - NAV-10: Cierre de sesión desmonta vistas privadas y restablece estado de visitante.
 * - NAV-11: Falta de consentimiento legal bloquea interacción en vistas privadas.
 * - NAV-12: Reanudación de sesión desde almacenamiento restaura rol y vista sin parpadeos.
 * - NAV-13: Pestaña inválida en URL (?tab=xyz) redirige a la vista permitida por defecto.
 * - NAV-14: Acceso autorizado renderiza íntegramente los controles y vistas de negocio.
 */

import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { App } from '../../App';
import { authService } from '../../services/authService';

describe('Suite de Pruebas RBAC: Navegación y Guardas de Protección (NAV-01 a NAV-14)', () => {
  beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.clear();
    authService.clearToken();
    window.history.pushState({}, '', '/');
  });

  afterEach(() => {
    sessionStorage.clear();
    authService.clearToken();
    window.history.pushState({}, '', '/');
    vi.restoreAllMocks();
  });

  // NAV-01: Visitante solo visualiza 'auth' y 'curriculum'
  it('NAV-01: Visitante no autenticado visualiza únicamente las opciones de login y catálogo de cursos', async () => {
    render(<App />);

    expect(screen.getByRole('button', { name: /^🔐 Iniciar sesión$/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^📚 Cursos$/i })).toBeInTheDocument();

    // No debe existir ninguna pestaña privada en la barra de navegación
    expect(screen.queryByRole('button', { name: /^🎯 Explorar mentorías$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^📅 Mis reservas$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^📋 Mis sesiones$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^🏷️ Publicar mentoría$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^🛡️ Administración$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^🛰️ Estado del sistema$/i })).not.toBeInTheDocument();
  });

  // NAV-02: Visitante intentando acceder a '?tab=admin' recibe Acceso Restringido
  it('NAV-02: Visitante que consulta directamente ?tab=admin recibe pantalla de acceso restringido institucional', async () => {
    window.history.pushState({}, '', '?tab=admin');
    render(<App />);

    expect(screen.getByRole('region', { name: /Acceso Restringido/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /Acceso Restringido a Administración/i })).toBeInTheDocument();
    expect(screen.getByText(/debes iniciar sesión con tu cuenta institucional/i)).toBeInTheDocument();

    // No se monta el panel de administración
    expect(screen.queryByText(/Panel de Administración Institucional/i)).not.toBeInTheDocument();
  });

  // NAV-03: Visitante intentando acceder a '?tab=sessions' recibe Acceso Restringido
  it('NAV-03: Visitante que consulta directamente ?tab=sessions recibe pantalla de acceso restringido institucional', async () => {
    window.history.pushState({}, '', '?tab=sessions');
    render(<App />);

    expect(screen.getByRole('region', { name: /Acceso Restringido/i })).toBeInTheDocument();
    expect(screen.getByRole('heading', { name: /Acceso Restringido a Mis sesiones/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Iniciar Sesión Institucional/i })).toBeInTheDocument();

    // No se monta el panel del mentor
    expect(screen.queryByText(/Panel del Mentor: Sesiones y Asistencia/i)).not.toBeInTheDocument();
  });

  // NAV-04: Mentoreado visualiza menú de estudiante
  it('NAV-04: Usuario con rol Mentoreado visualiza el menú correspondiente y entra por defecto a recomendaciones', async () => {
    const studentEmail = '2022074255@upt.pe';
    const payload = { sub: studentEmail, role: 'mentoreado' };
    authService.saveToken(`h.${btoa(JSON.stringify(payload))}.s`);

    render(<App />);

    expect(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^📅 Mis reservas$/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^📚 Cursos$/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^👤 Mi perfil$/i })).toBeInTheDocument();

    // No debe ver módulos de mentor ni administrador
    expect(screen.queryByRole('button', { name: /^📋 Mis sesiones$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^🏷️ Publicar mentoría$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^🛡️ Administración$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^🛰️ Estado del sistema$/i })).not.toBeInTheDocument();

    // Vista por defecto: cartelera de recomendaciones
    expect(screen.getByRole('heading', { name: /Mentorías Recomendadas y Reserva de Sesiones/i })).toBeInTheDocument();
  });

  // NAV-05: Mentoreado intentando acceder a '?tab=admin' recibe Acceso No Autorizado
  it('NAV-05: Usuario Mentoreado que ingresa a ?tab=admin recibe pantalla de acceso no autorizado y botón de retorno', async () => {
    const studentEmail = '2022074255@upt.pe';
    const payload = { sub: studentEmail, role: 'mentoreado' };
    authService.saveToken(`h.${btoa(JSON.stringify(payload))}.s`);
    window.history.pushState({}, '', '?tab=admin');

    render(<App />);

    expect(screen.getByRole('alert', { name: /Acceso No Autorizado/i })).toBeInTheDocument();
    expect(screen.getByText(/no cuenta con permisos para acceder a la sección/i)).toBeInTheDocument();

    // El botón permite volver a su panel por defecto (recomendaciones)
    const returnBtn = screen.getByRole('button', { name: /Volver a mi panel principal/i });
    fireEvent.click(returnBtn);

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Mentorías Recomendadas y Reserva de Sesiones/i })).toBeInTheDocument();
    });
  });

  // NAV-06: Mentor visualiza menú de mentor
  it('NAV-06: Usuario con rol Mentor visualiza el menú correspondiente y entra por defecto a sesiones', async () => {
    const mentorEmail = 'mentor.docente@upt.pe';
    const payload = { sub: mentorEmail, roles: ['mentor', 'mentoreado'] };
    authService.saveToken(`h.${btoa(JSON.stringify(payload))}.s`);

    render(<App />);

    expect(screen.getByRole('button', { name: /^📋 Mis sesiones$/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^🏷️ Publicar mentoría$/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^📚 Cursos$/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^👤 Mi perfil$/i })).toBeInTheDocument();

    // No debe ver módulos directivos
    expect(screen.queryByRole('button', { name: /^🛡️ Administración$/i })).not.toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^🛰️ Estado del sistema$/i })).not.toBeInTheDocument();

    // Vista por defecto: panel de sesiones
    expect(screen.getByRole('heading', { name: /Panel del Mentor: Sesiones y Asistencia/i })).toBeInTheDocument();
  });

  // NAV-07: Mentor intentando acceder a '?tab=admin' recibe Acceso No Autorizado
  it('NAV-07: Usuario Mentor que ingresa a ?tab=admin recibe bloqueo por falta de rol administrativo', async () => {
    const mentorEmail = 'mentor.docente@upt.pe';
    const payload = { sub: mentorEmail, roles: ['mentor', 'mentoreado'] };
    authService.saveToken(`h.${btoa(JSON.stringify(payload))}.s`);
    window.history.pushState({}, '', '?tab=admin');

    render(<App />);

    expect(screen.getByRole('alert', { name: /Acceso No Autorizado/i })).toBeInTheDocument();
    expect(screen.queryByText(/Panel de Administración Institucional/i)).not.toBeInTheDocument();
  });

  // NAV-08: Administrador visualiza menú directivo
  it('NAV-08: Usuario Administrador visualiza menú institucional y entra por defecto al panel directivo', async () => {
    const adminEmail = 'admin.epis@upt.pe';
    const payload = { sub: adminEmail, roles: ['administrador'] };
    authService.saveToken(`h.${btoa(JSON.stringify(payload))}.s`);

    render(<App />);

    expect(screen.getByRole('button', { name: /^🛡️ Administración$/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^📚 Cursos$/i })).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /^🛰️ Estado del sistema$/i })).toBeInTheDocument();

    // No debe ver opciones directas de mentor
    expect(screen.queryByRole('button', { name: /^🏷️ Publicar mentoría$/i })).not.toBeInTheDocument();

    // Vista por defecto: administración
    expect(screen.getByRole('heading', { name: /Panel de Administración Institucional/i })).toBeInTheDocument();
  });

  // NAV-09: Usuario multi-rol alterna perfiles, actualizando menú y vistas
  it('NAV-09: Usuario multi-rol (mentor y mentoreado) puede conmutar rol activo y la navegación se adapta inmediatamente', async () => {
    const multiUserEmail = '2022073504@upt.pe';
    const payload = { sub: multiUserEmail, roles: ['mentor', 'mentoreado'] };
    authService.saveToken(`h.${btoa(JSON.stringify(payload))}.s`);

    render(<App />);

    // Inicia con rol mentor
    expect(screen.getByRole('button', { name: /^📋 Mis sesiones$/i })).toBeInTheDocument();

    // Conmutar a mentoreado mediante el conmutador de la cabecera
    const switchMentoreadoBtn = screen.getByTestId('role-switch-mentoreado');
    fireEvent.click(switchMentoreadoBtn);

    await waitFor(() => {
      // El menú cambia dinámicamente al menú de estudiante
      expect(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i })).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /^📅 Mis reservas$/i })).toBeInTheDocument();
      expect(screen.queryByRole('button', { name: /^📋 Mis sesiones$/i })).not.toBeInTheDocument();
    });
  });

  // NAV-10: Cierre de sesión desmonta vistas privadas y restablece estado de visitante
  it('NAV-10: Al pulsar "Cerrar Sesión", se destruye la sesión, limpia storage y retorna al login', async () => {
    const studentEmail = '2022074255@upt.pe';
    const payload = { sub: studentEmail, role: 'mentoreado' };
    authService.saveToken(`h.${btoa(JSON.stringify(payload))}.s`);

    render(<App />);

    expect(screen.getByRole('button', { name: /^🎯 Explorar mentorías$/i })).toBeInTheDocument();

    const logoutBtn = screen.getByRole('button', { name: /Cerrar Sesión/i });
    fireEvent.click(logoutBtn);

    await waitFor(() => {
      // Retorna a vista de visitante con formulario de acceso
      expect(screen.getByLabelText(/Correo Electrónico Institucional/i)).toBeInTheDocument();
      expect(screen.queryByRole('button', { name: /^🎯 Explorar mentorías$/i })).not.toBeInTheDocument();
      expect(authService.getToken()).toBeNull();
    });
  });

  // NAV-11: Consentimiento legal
  it('NAV-11: Pestaña de consentimiento informed está disponible y refleja la política de privacidad', async () => {
    const studentEmail = '2022074255@upt.pe';
    const payload = { sub: studentEmail, role: 'mentoreado' };
    authService.saveToken(`h.${btoa(JSON.stringify(payload))}.s`);
    window.history.pushState({}, '', '?tab=consent');

    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Consentimiento Informado de Privacidad/i })).toBeInTheDocument();
      expect(screen.getByText(/Tratamiento seguro de datos personales/i)).toBeInTheDocument();
    });
  });

  // NAV-12: Reanudación de sesión desde almacenamiento
  it('NAV-12: Sesión persistida en storage se reanuda de inmediato sin parpadeo de pantalla de login', async () => {
    const mentorEmail = 'mentor.activo@upt.pe';
    const payload = { sub: mentorEmail, roles: ['mentor', 'mentoreado'] };
    authService.saveToken(`h.${btoa(JSON.stringify(payload))}.s`);

    render(<App />);

    // Inicia directamente en Mis sesiones sin mostrar formulario de login
    expect(screen.getByRole('heading', { name: /Panel del Mentor: Sesiones y Asistencia/i })).toBeInTheDocument();
    expect(screen.queryByLabelText(/Correo Electrónico Institucional/i)).not.toBeInTheDocument();
  });

  // NAV-13: Pestaña inválida en URL (?tab=xyz)
  it('NAV-13: Una ruta con pestaña inexistente (?tab=inexistente123) se sanitiza redirigiendo al panel por defecto', async () => {
    const studentEmail = '2022074255@upt.pe';
    const payload = { sub: studentEmail, role: 'mentoreado' };
    authService.saveToken(`h.${btoa(JSON.stringify(payload))}.s`);
    window.history.pushState({}, '', '?tab=inexistente123');

    render(<App />);

    // Sanitiza a la vista por defecto de mentoreado: recomendaciones
    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Mentorías Recomendadas y Reserva de Sesiones/i })).toBeInTheDocument();
    });
  });

  // NAV-14: Acceso autorizado renderiza íntegramente los controles y vistas de negocio
  it('NAV-14: Acceso autorizado a Cursos renderiza el catálogo para cualquier perfil sin restricciones', async () => {
    window.history.pushState({}, '', '?tab=curriculum');
    render(<App />);

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Catálogo Curricular/i })).toBeInTheDocument();
      expect(screen.getByText(/Buscar por curso, código o tema silábico/i)).toBeInTheDocument();
    });
  });
});
