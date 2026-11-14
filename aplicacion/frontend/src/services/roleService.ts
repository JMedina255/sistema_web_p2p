/**
 * Servicio de Gestión de Roles Institucionales (RF03 / CUS10 / RN-03)
 * Soporta consulta de roles, promoción a mentor con mérito y revocación.
 */

import { authService } from './authService';

export interface UserRolesResponse {
  email: string;
  roles: string[];
  is_active: boolean;
}

export interface RoleOperationResponse {
  email: string;
  success: boolean;
  message: string;
  roles: string[];
}

function resolveInitialServiceMode(): 'mock' | 'api' {
  if (import.meta.env.PROD) {
    return 'api';
  }
  const envMode = import.meta.env.VITE_SERVICE_MODE;
  if (envMode === 'mock') {
    return 'mock';
  }
  if (envMode === 'api') {
    return 'api';
  }
  if (import.meta.env.MODE === 'test') {
    return 'mock';
  }
  return 'api';
}

class RoleService {
  private mode: 'mock' | 'api' = resolveInitialServiceMode();
  private mockStore: Record<string, string[]> = {
    'admin.epis@upt.pe': ['administrador'],
    'mentor.avanzado@upt.pe': ['mentor', 'mentoreado'],
    '2022073504@upt.pe': ['mentor', 'mentoreado'],
    '2022074255@upt.pe': ['mentoreado'],
    '2023079999@upt.pe': ['mentoreado'],
  };

  public setMode(mode: 'mock' | 'api') {
    this.mode = mode;
  }

  public getMode(): 'mock' | 'api' {
    return this.mode;
  }

  private getBaseUrl(): string {
    return (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
  }

  private getAuthHeaders(customHeaders: Record<string, string> = {}): Record<string, string> {
    const headers: Record<string, string> = {
      Accept: 'application/json',
      ...customHeaders,
    };
    const token = authService.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  public async getUserRoles(email: string): Promise<UserRolesResponse> {
    const cleanEmail = email.trim().toLowerCase();

    if (this.mode === 'mock') {
      const roles = this.mockStore[cleanEmail] ?? ['mentoreado'];
      return {
        email: cleanEmail,
        roles,
        is_active: true,
      };
    }

    const res = await fetch(`${this.getBaseUrl()}/api/v1/roles/users/${encodeURIComponent(cleanEmail)}`, {
      headers: this.getAuthHeaders(),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || `Error al consultar roles (${res.status})`);
    }

    return res.json();
  }

  public async promoteToMentor(email: string, assignedBy?: string): Promise<RoleOperationResponse> {
    const cleanEmail = email.trim().toLowerCase();

    if (this.mode === 'mock') {
      const current = this.mockStore[cleanEmail] ?? ['mentoreado'];
      if (!current.includes('mentor')) {
        current.push('mentor');
      }
      this.mockStore[cleanEmail] = current;
      return {
        email: cleanEmail,
        success: true,
        message: `Estudiante ${cleanEmail} promovido al rol de Mentor exitosamente bajo verificación de mérito RN-03.`,
        roles: current,
      };
    }

    const res = await fetch(`${this.getBaseUrl()}/api/v1/roles/promote-mentor`, {
      method: 'POST',
      headers: this.getAuthHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        email: cleanEmail,
        assigned_by: assignedBy,
      }),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || `Error al promover a mentor (${res.status})`);
    }

    return res.json();
  }

  public async revokeMentor(email: string): Promise<RoleOperationResponse> {
    const cleanEmail = email.trim().toLowerCase();

    if (this.mode === 'mock') {
      const current = (this.mockStore[cleanEmail] ?? ['mentoreado']).filter((r) => r !== 'mentor');
      this.mockStore[cleanEmail] = current;
      return {
        email: cleanEmail,
        success: true,
        message: `Rol de Mentor revocado exitosamente para ${cleanEmail}.`,
        roles: current,
      };
    }

    const res = await fetch(`${this.getBaseUrl()}/api/v1/roles/revoke-mentor`, {
      method: 'POST',
      headers: this.getAuthHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({ email: cleanEmail }),
    });

    if (!res.ok) {
      const errorData = await res.json().catch(() => ({}));
      throw new Error(errorData.detail || `Error al revocar rol (${res.status})`);
    }

    return res.json();
  }
}

export const roleService = new RoleService();
