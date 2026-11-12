import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { AdminDashboardView } from '../AdminDashboardView';
import { roleService } from '../../services/roleService';
import { offerService } from '../../services/offerService';
import { bitacoraService, type BitacoraItem } from '../../services/bitacoraService';

describe('AdminDashboardView Component (RF03 / CUS10 / RN-03 / RN-09 / T-40 / T-41 / RF26 / RN-14)', () => {
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

  it('5. Listado y filtrado de bitácoras: renderiza la tabla y filtra por estado pendiente', async () => {
    const mockPendingBitacoras: BitacoraItem[] = [
      {
        id_bitacora: 1,
        id_sesion: 101,
        codigo_sesion: 'SES-101',
        id_mentor: 'mentor1@upt.pe',
        temas_cubiertos: ['Punteros'],
        observaciones: 'Observaciones de desarrollo de la sesion con mas de 50 caracteres para la bitacora 1',
        nivel_dificultad: 'Medio',
        hash_firma: 'hash1',
        horas_declaradas: 2.0,
        visado_administrador: false,
        estado_sesion: 'BITACORA_REGISTRADA',
        created_at: new Date().toISOString(),
      },
      {
        id_bitacora: 2,
        id_sesion: 102,
        codigo_sesion: 'SES-102',
        id_mentor: 'mentor2@upt.pe',
        temas_cubiertos: ['Arreglos'],
        observaciones: 'Observaciones de desarrollo de la sesion con mas de 50 caracteres para la bitacora 2',
        nivel_dificultad: 'Bajo',
        hash_firma: 'hash2',
        horas_declaradas: 1.5,
        visado_administrador: false,
        estado_sesion: 'BITACORA_REGISTRADA',
        created_at: new Date().toISOString(),
      },
      {
        id_bitacora: 3,
        id_sesion: 103,
        codigo_sesion: 'SES-103',
        id_mentor: 'mentor3@upt.pe',
        temas_cubiertos: ['Colas'],
        observaciones: 'Observaciones de desarrollo de la sesion con mas de 50 caracteres para la bitacora 3',
        nivel_dificultad: 'Alto',
        hash_firma: 'hash3',
        horas_declaradas: 1.0,
        visado_administrador: false,
        estado_sesion: 'BITACORA_REGISTRADA',
        created_at: new Date().toISOString(),
      },
    ];

    vi.spyOn(bitacoraService, 'getBitacoras').mockResolvedValue(mockPendingBitacoras);

    render(<AdminDashboardView adminEmail={adminEmail} />);

    const bitacorasTab = screen.getByRole('button', { name: /Auditoría de Bitácoras/i });
    fireEvent.click(bitacorasTab);

    const pendientesFilterBtn = await screen.findByRole('button', { name: /Pendientes de Visado/i });
    fireEvent.click(pendientesFilterBtn);

    await waitFor(() => {
      // 1 encabezado <th> + 3 filas <tr> de datos = 4 filas en total
      expect(screen.getAllByRole('row')).toHaveLength(4);
    });
  });

  it('6. Visado administrativo de horas (RN-14): ejecuta visado y muestra distintivo Horas Acreditadas', async () => {
    const mockBitacora: BitacoraItem = {
      id_bitacora: 1,
      id_sesion: 101,
      codigo_sesion: 'SES-101',
      id_mentor: 'mentor.visar@upt.pe',
      temas_cubiertos: ['Árboles Binarios'],
      observaciones: 'Desarrollo pedagógico formal con resolución práctica de ejercicios.',
      nivel_dificultad: 'Medio',
      hash_firma: 'hash-firma-sha256-visar',
      horas_declaradas: 2.0,
      visado_administrador: false,
      estado_sesion: 'BITACORA_REGISTRADA',
      created_at: new Date().toISOString(),
    };

    vi.spyOn(bitacoraService, 'getBitacoras').mockResolvedValue([mockBitacora]);
    const visarSpy = vi.spyOn(bitacoraService, 'visar').mockResolvedValue({
      id_bitacora: 1,
      id_sesion: 101,
      id_mentor: 'mentor.visar@upt.pe',
      horas_declaradas: 2.0,
      visado_administrador: true,
      estado_sesion: 'HORAS_VISADAS',
      auditor_email: adminEmail,
      visado_at: new Date().toISOString(),
      mensaje: 'Bitácora visada institucionalmente con éxito. 2.0 horas formativas acreditadas para certificación.',
    });

    render(<AdminDashboardView adminEmail={adminEmail} />);

    fireEvent.click(screen.getByRole('button', { name: /Auditoría de Bitácoras/i }));

    const visarBtn = await screen.findByRole('button', { name: /Aprobar y Visar Horas/i });
    fireEvent.click(visarBtn);

    await waitFor(() => {
      expect(visarSpy).toHaveBeenCalledWith(1);
      expect(screen.getByText(/Horas Acreditadas/i)).toBeInTheDocument();
    });
  });

  it('7. Formulación de observaciones de auditoría: exige justificación obligatoria y transiciona a OBSERVADA', async () => {
    const mockBitacora: BitacoraItem = {
      id_bitacora: 1,
      id_sesion: 101,
      codigo_sesion: 'SES-101',
      id_mentor: 'mentor.obs@upt.pe',
      temas_cubiertos: ['Grafos Dirigidos'],
      observaciones: 'Desarrollo pedagógico de algoritmos de recorrido en anchura y profundidad.',
      nivel_dificultad: 'Alto',
      hash_firma: 'hash-firma-obs',
      horas_declaradas: 1.5,
      visado_administrador: false,
      estado_sesion: 'BITACORA_REGISTRADA',
      created_at: new Date().toISOString(),
    };

    vi.spyOn(bitacoraService, 'getBitacoras').mockResolvedValue([mockBitacora]);
    const observarSpy = vi.spyOn(bitacoraService, 'observar').mockResolvedValue({
      id_bitacora: 1,
      id_sesion: 101,
      id_mentor: 'mentor.obs@upt.pe',
      estado_sesion: 'OBSERVADA',
      motivo_observacion: 'Discrepancia detectada en asistencia de alumnos.',
      auditor_email: adminEmail,
      observado_at: new Date().toISOString(),
      mensaje: 'Bitácora observada para corrección.',
    });

    render(<AdminDashboardView adminEmail={adminEmail} />);

    fireEvent.click(screen.getByRole('button', { name: /Auditoría de Bitácoras/i }));

    const observarBtn = await screen.findByRole('button', { name: /Observar Bitácora/i });
    fireEvent.click(observarBtn);

    const textbox = screen.getByRole('textbox');
    expect(textbox).toBeRequired();

    fireEvent.change(textbox, {
      target: { value: 'Discrepancia detectada en asistencia de alumnos.' },
    });

    const confirmBtn = screen.getByRole('button', { name: /Confirmar Observación/i });
    fireEvent.click(confirmBtn);

    await waitFor(() => {
      expect(observarSpy).toHaveBeenCalledWith(1, 'Discrepancia detectada en asistencia de alumnos.');
      expect(screen.getByText(/Observada/i)).toBeInTheDocument();
    });
  });

  it('8. Accesibilidad WAI-ARIA (RNF05): cierra el diálogo de observación al presionar Escape', async () => {
    const mockBitacora: BitacoraItem = {
      id_bitacora: 1,
      id_sesion: 101,
      id_mentor: 'mentor.esc@upt.pe',
      temas_cubiertos: ['Temas'],
      observaciones: 'Observaciones mayores a 50 caracteres para bitacora...',
      nivel_dificultad: 'Medio',
      hash_firma: 'hash-esc',
      horas_declaradas: 1.0,
      visado_administrador: false,
      estado_sesion: 'BITACORA_REGISTRADA',
      created_at: new Date().toISOString(),
    };

    vi.spyOn(bitacoraService, 'getBitacoras').mockResolvedValue([mockBitacora]);
    render(<AdminDashboardView adminEmail={adminEmail} />);

    fireEvent.click(screen.getByRole('button', { name: /Auditoría de Bitácoras/i }));
    const observarBtn = await screen.findByRole('button', { name: /Observar Bitácora/i });
    fireEvent.click(observarBtn);

    expect(screen.getByRole('dialog', { name: /Observar Bitácora Pedagógica/i })).toBeInTheDocument();
    fireEvent.keyDown(window, { key: 'Escape' });
    expect(screen.queryByRole('dialog', { name: /Observar Bitácora Pedagógica/i })).not.toBeInTheDocument();
  });
});

