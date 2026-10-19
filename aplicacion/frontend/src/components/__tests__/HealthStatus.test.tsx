import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { HealthStatus } from '../HealthStatus';
import * as apiClient from '../../services/apiClient';

describe('HealthStatus Component (T-01 / RNF09)', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.restoreAllMocks();
  });

  it('1. Renderiza estado de carga y posteriormente estado de éxito con datos de salud y BD', async () => {
    vi.spyOn(apiClient, 'fetchHealth').mockResolvedValue({
      status: 'ok',
      service: 'backend',
      project: 'Sistema Web P2P - EPIS UPT',
      environment: 'development',
    });

    vi.spyOn(apiClient, 'fetchDbHealth').mockResolvedValue({
      status: 'ok',
      database: 'connected',
      detail: 'Conexión a PostgreSQL (Supabase) verificada con éxito',
      latency_ms: 12.4,
      environment: 'development',
    });

    render(<HealthStatus />);

    // Esperar a que se resuelva la carga
    await waitFor(() => {
      expect(screen.getByText(/Backend FastAPI: Operativo/i)).toBeInTheDocument();
    });

    expect(screen.getByText(/PostgreSQL \(Supabase - p2p-epis-dev\): Conectado/i)).toBeInTheDocument();
  });

  it('2. Renderiza estado de error cuando el backend no responde', async () => {
    vi.spyOn(apiClient, 'fetchHealth').mockRejectedValue(new Error('Connection refused'));

    render(<HealthStatus />);

    await waitFor(() => {
      expect(screen.getByText(/Fallo de conexión con el backend/i)).toBeInTheDocument();
    });

    expect(screen.getByText(/Connection refused/i)).toBeInTheDocument();
  });

  it('3. El botón Reintentar dispara una nueva comprobación', async () => {
    const fetchHealthSpy = vi.spyOn(apiClient, 'fetchHealth').mockResolvedValue({
      status: 'ok',
      service: 'backend',
      project: 'Sistema Web P2P - EPIS UPT',
      environment: 'development',
    });

    vi.spyOn(apiClient, 'fetchDbHealth').mockResolvedValue(null);

    render(<HealthStatus />);

    await waitFor(() => {
      expect(screen.getByText(/Backend FastAPI: Operativo/i)).toBeInTheDocument();
    });

    const refreshBtn = screen.getByRole('button', { name: /Reintentar/i });
    fireEvent.click(refreshBtn);

    expect(fetchHealthSpy).toHaveBeenCalledTimes(2);
  });
});
