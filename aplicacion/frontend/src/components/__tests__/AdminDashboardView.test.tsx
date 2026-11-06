import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AdminDashboardView } from '../AdminDashboardView';
import { roleService } from '../../services/roleService';
import { offerService } from '../../services/offerService';

describe('AdminDashboardView Component (RF03 / CUS10 / RN-03 / RN-09)', () => {
  const adminEmail = 'admin.epis@upt.pe';
  const targetStudent = '2022074255@upt.pe';

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('1. Renderiza el encabezado institucional del panel de administración', () => {
    render(<AdminDashboardView adminEmail={adminEmail} />);
    expect(screen.getByText(/Panel de Administración y Supervisión EPIS/i)).toBeInTheDocument();
    expect(screen.getByText(new RegExp(adminEmail, 'i'))).toBeInTheDocument();
  });

  it('2. Permite buscar un estudiante y consultar sus roles actuales', async () => {
    vi.spyOn(roleService, 'getUserRoles').mockResolvedValue({
      email: targetStudent,
      roles: ['mentoreado'],
      is_active: true,
    });

    render(<AdminDashboardView adminEmail={adminEmail} />);

    const input = screen.getByPlaceholderText(/2022074255@upt\.pe/i);
    fireEvent.change(input, { target: { value: targetStudent } });

    const searchBtn = screen.getByRole('button', { name: /Buscar Estudiante/i });
    fireEvent.click(searchBtn);

    await waitFor(() => {
      expect(screen.getByText(targetStudent)).toBeInTheDocument();
      expect(screen.getByText(/MENTOREADO/i)).toBeInTheDocument();
    });
  });

  it('3. Permite promover a mentor y revocar el rol interactuando con roleService', async () => {
    vi.spyOn(roleService, 'getUserRoles').mockResolvedValue({
      email: targetStudent,
      roles: ['mentoreado'],
      is_active: true,
    });
    const promoteSpy = vi.spyOn(roleService, 'promoteToMentor').mockResolvedValue({
      email: targetStudent,
      success: true,
      message: 'Promovido exitosamente tras mérito RN-03.',
      roles: ['mentoreado', 'mentor'],
    });

    render(<AdminDashboardView adminEmail={adminEmail} />);

    const input = screen.getByPlaceholderText(/2022074255@upt\.pe/i);
    fireEvent.change(input, { target: { value: targetStudent } });
    fireEvent.click(screen.getByRole('button', { name: /Buscar Estudiante/i }));

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /Promover a Mentor/i })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('button', { name: /Promover a Mentor/i }));

    await waitFor(() => {
      expect(promoteSpy).toHaveBeenCalledWith(targetStudent, adminEmail);
      expect(screen.getByText(/Promovido exitosamente tras mérito RN-03/i)).toBeInTheDocument();
    });
  });

  it('4. Permite alternar a la pestaña de monitoreo de quórum', async () => {
    vi.spyOn(offerService, 'getOffers').mockResolvedValue([]);

    render(<AdminDashboardView adminEmail={adminEmail} />);

    const quorumTab = screen.getByRole('button', { name: /Monitoreo de Quórum/i });
    fireEvent.click(quorumTab);

    await waitFor(() => {
      expect(screen.getByText(/Supervisión de Quórum y Sesiones EPIS/i)).toBeInTheDocument();
    });
  });
});
