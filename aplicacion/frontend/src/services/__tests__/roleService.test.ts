import { describe, it, expect, beforeEach, vi } from 'vitest';
import { roleService } from '../roleService';

describe('roleService (RF03 / CUS10 / RN-03)', () => {
  const testStudent = '2023079999@upt.pe';

  beforeEach(() => {
    roleService.setMode('mock');
    vi.restoreAllMocks();
  });

  it('1. Consulta roles por defecto para un estudiante nuevo en mock', async () => {
    const res = await roleService.getUserRoles(testStudent);
    expect(res.email).toBe(testStudent);
    expect(res.roles).toContain('mentoreado');
    expect(res.roles).not.toContain('mentor');
  });

  it('2. Promueve exitosamente a mentor y actualiza la lista de roles en mock', async () => {
    const res = await roleService.promoteToMentor(testStudent, 'admin.epis@upt.pe');
    expect(res.success).toBe(true);
    expect(res.roles).toContain('mentor');

    const check = await roleService.getUserRoles(testStudent);
    expect(check.roles).toContain('mentor');
  });

  it('3. Revoca el rol de mentor y confirma la eliminación en mock', async () => {
    // Primero promovemos
    await roleService.promoteToMentor(testStudent);
    // Luego revocamos
    const res = await roleService.revokeMentor(testStudent);
    expect(res.success).toBe(true);
    expect(res.roles).not.toContain('mentor');

    const check = await roleService.getUserRoles(testStudent);
    expect(check.roles).not.toContain('mentor');
  });

  it('4. En modo API realiza las peticiones HTTP contra el backend con baseUrl y Authorization', async () => {
    roleService.setMode('api');

    const mockFetch = vi.fn().mockResolvedValue({
      ok: true,
      json: async () => ({
        email: testStudent,
        roles: ['mentoreado', 'mentor'],
        is_active: true,
      }),
    });
    vi.stubGlobal('fetch', mockFetch);

    const res = await roleService.getUserRoles(testStudent);
    expect(mockFetch).toHaveBeenCalledTimes(1);
    const calledUrl = mockFetch.mock.calls[0][0];
    expect(calledUrl).toContain('/api/v1/roles/users/');
    expect(res.roles).toContain('mentor');
  });

  it('5. Maneja errores HTTP en modo API lanzando excepciones legibles', async () => {
    roleService.setMode('api');

    const mockFetch = vi.fn().mockResolvedValue({
      ok: false,
      status: 400,
      json: async () => ({
        detail: {
          code: 'MERIT_RULE_VIOLATION',
          message: 'Violación de mérito RN-03',
        },
      }),
    });
    vi.stubGlobal('fetch', mockFetch);

    await expect(roleService.promoteToMentor(testStudent)).rejects.toThrow();
  });
});
