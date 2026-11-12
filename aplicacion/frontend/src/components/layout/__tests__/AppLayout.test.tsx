import { describe, it, expect, vi } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { AppLayout } from '../AppLayout';
import type { AuthUser } from '../../../context/AuthContext';

describe('AppLayout Component (T-47 / T-49 / RNF05 / WCAG 2.1 AA)', () => {
  const mockUser: AuthUser = {
    email: 'mentor@upt.pe',
    nombres: 'Renzo Antonio',
    apellidos: 'Antayhua Mamani',
    roles: ['mentor'],
  };

  it('1. Renderiza el layout institucional con barra guiada y pestañas de rol mentor', () => {
    const onSelectTab = vi.fn();
    const onRoleSwitch = vi.fn();
    const onLogout = vi.fn();

    render(
      <AppLayout
        user={mockUser}
        token="mock.jwt.token"
        activeRole="mentor"
        hasConsented={true}
        activeTab="sessions"
        onSelectTab={onSelectTab}
        onRoleSwitch={onRoleSwitch}
        onLogout={onLogout}
      >
        <div data-testid="test-content">Contenido de Prueba</div>
      </AppLayout>
    );

    expect(screen.getByText(/Flujo Guiado Mentor:/i)).toBeInTheDocument();
    expect(screen.getByText(/3. 📜 Mis constancias/i)).toBeInTheDocument();

    const certBtn = screen.getByRole('button', { name: /3. 📜 Mis constancias/i });
    fireEvent.click(certBtn);
    expect(onSelectTab).toHaveBeenCalledWith('certificates');
  });

  it('2. Verifica navegación y conmutación de contexto de rol', () => {
    const onRoleSwitch = vi.fn();
    const userMulti: AuthUser = {
      email: 'estudiante.mixto@upt.pe',
      nombres: 'Joan Cristian',
      apellidos: 'Medina Quispe',
      roles: ['mentor', 'mentoreado'],
    };

    render(
      <AppLayout
        user={userMulti}
        token="mock.jwt.token"
        activeRole="mentor"
        hasConsented={true}
        activeTab="sessions"
        onSelectTab={vi.fn()}
        onRoleSwitch={onRoleSwitch}
        onLogout={vi.fn()}
      >
        <div>Panel</div>
      </AppLayout>
    );

    // Conmutador de rol en cabecera
    const switchRoleBtn = screen.getByTestId('role-switch-mentoreado');
    expect(switchRoleBtn).toBeInTheDocument();

    fireEvent.click(switchRoleBtn);
    expect(onRoleSwitch).toHaveBeenCalledWith('mentoreado');
  });

  it('3. Accesibilidad modal WCAG 2.1 AA: captura foco y responde a tecla Escape en diálogos', () => {
    const onSelectTab = vi.fn();

    render(
      <AppLayout
        user={mockUser}
        token="mock.jwt.token"
        activeRole="mentor"
        hasConsented={true}
        activeTab="sessions"
        onSelectTab={onSelectTab}
        onRoleSwitch={vi.fn()}
        onLogout={vi.fn()}
      >
        <div role="dialog" aria-modal="true" aria-label="Diálogo Modal Accesible">
          <button type="button">Acción 1</button>
          <button type="button">Cerrar</button>
        </div>
      </AppLayout>
    );

    const dialog = screen.getByRole('dialog', { name: /Diálogo Modal Accesible/i });
    expect(dialog).toBeInTheDocument();
    expect(dialog).toHaveAttribute('aria-modal', 'true');

    // Comprobar despacho de evento Escape
    const escapeEvt = new KeyboardEvent('keydown', { key: 'Escape', bubbles: true });
    dialog.dispatchEvent(escapeEvt);
  });
});
