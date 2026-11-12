import { describe, it, expect, beforeEach, vi } from 'vitest';
import { bitacoraService } from '../bitacoraService';
import { authService } from '../authService';

describe('bitacoraService (T-35 / T-40 / T-41 / RF17 / RF26 / RN-12 / RN-14)', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('1. Registra bitácora pedagógica con más de 50 caracteres', async () => {
    vi.spyOn(authService, 'getCurrentUser').mockReturnValue({
      email: 'mentor@upt.pe',
    });

    const res = await bitacoraService.submitBitacora(10, {
      temas_cubiertos: ['Punteros', 'Referencias'],
      observaciones:
        'Se desarrollaron ejemplos prácticos de punteros y referencias con activa participación estudiantil.',
      nivel_dificultad: 'Medio',
    });

    expect(res.id_bitacora).toBe(10);
    expect(res.hash_firma).toContain('sha256-mock');
    expect(res.visado_administrador).toBe(false);
  });

  it('2. Rechaza registro con observaciones menores a 50 caracteres', async () => {
    await expect(
      bitacoraService.submitBitacora(11, {
        temas_cubiertos: ['Tema'],
        observaciones: 'Muy corto',
        nivel_dificultad: 'Bajo',
      })
    ).rejects.toThrow(/al menos 50 caracteres/i);
  });

  it('3. Lista bitácoras pedagógicas para la bandeja administrativa', async () => {
    const list = await bitacoraService.getBitacoras();
    expect(list.length).toBeGreaterThanOrEqual(3);

    const pendientes = await bitacoraService.getBitacoras('PENDIENTES');
    expect(pendientes.every((b) => !b.visado_administrador)).toBe(true);
  });

  it('4. Visa administrativamente una bitácora conmutando a HORAS_VISADAS', async () => {
    vi.spyOn(authService, 'getCurrentUser').mockReturnValue({
      email: 'admin.epis@upt.pe',
    });

    const res = await bitacoraService.visar(1);
    expect(res.visado_administrador).toBe(true);
    expect(res.estado_sesion).toBe('HORAS_VISADAS');
    expect(res.horas_declaradas).toBe(2.0);
  });

  it('5. Formula observación técnica exigiendo al menos 15 caracteres', async () => {
    vi.spyOn(authService, 'getCurrentUser').mockReturnValue({
      email: 'admin.epis@upt.pe',
    });

    // Rechaza observación muy corta
    await expect(bitacoraService.observar(1, 'Corta')).rejects.toThrow(/mínimo 15 caracteres/i);

    // Acepta observación válida
    const res = await bitacoraService.observar(
      1,
      'Se requiere adjuntar mayor evidencia de asistencia presencial.'
    );
    expect(res.estado_sesion).toBe('OBSERVADA');
    expect(res.motivo_observacion).toContain('mayor evidencia');
  });
});
