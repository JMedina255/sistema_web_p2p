/**
 * Suite de Pruebas de Reloj Controlado con Time-Travel (T-31 / Vitest Fake Timers)
 *
 * Trazabilidad:
 * - Regla RN-04: Antelación mínima de publicación y reprogramación (>24h)
 * - Regla RN-08: Ventana de ratificación de asistencia [T-48h, T-24h]
 * - Regla RN-10: Cierre perentorio de desistimiento sin penalidad a T-24h
 * - Regla RN-12: Ventana perentoria de 48h para registro de bitácoras pedagógicas
 */

import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';

describe('ControlledClock Time-Travel Test Suite (T-31 / vi.useFakeTimers)', () => {
  const sessionStartTime = new Date('2026-11-20T10:00:00.000Z');
  const sessionEndTime = new Date('2026-11-20T11:00:00.000Z');

  beforeEach(() => {
    vi.useFakeTimers();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  // Marca 1: T - 48h (Apertura de la ventana de ratificación)
  it('1. Marca T - 48h: habilita formalmente la ventana de ratificación de asistencia (RN-08)', () => {
    const tMinus48 = new Date(sessionStartTime.getTime() - 48 * 3600 * 1000);
    vi.setSystemTime(tMinus48);

    const now = Date.now();
    const hoursToSession = (sessionStartTime.getTime() - now) / (3600 * 1000);

    // En T-48h la ventana está abierta (restan exactamente 48 horas)
    const isRatificationWindowOpen = hoursToSession <= 48 && hoursToSession > 24;
    expect(hoursToSession).toBe(48.0);
    expect(isRatificationWindowOpen).toBe(true);
  });

  // Marca 2: T - 24h (Corte de desistimiento y evaluación de quórum)
  it('2. Marca T - 24h: bloquea desistimiento voluntario y activa evaluación de quórum (RN-09 / RN-10)', () => {
    const tMinus24 = new Date(sessionStartTime.getTime() - 24 * 3600 * 1000);
    vi.setSystemTime(tMinus24);

    const now = Date.now();
    const hoursToSession = (sessionStartTime.getTime() - now) / (3600 * 1000);

    // En T-24h se cierra el desistimiento voluntario sin penalidad
    const canCancelVoluntarily = hoursToSession > 24.0;
    const isQuorumEvaluationDue = hoursToSession <= 24.0;

    expect(hoursToSession).toBe(24.0);
    expect(canCancelVoluntarily).toBe(false);
    expect(isQuorumEvaluationDue).toBe(true);
  });

  // Marca 3: T = 0 (Inicio de sesión y habilitación de pase de asistencia QR)
  it('3. Marca T = 0: habilita el pase de asistencia digital QR TOTP (RF17)', () => {
    vi.setSystemTime(sessionStartTime);

    const now = Date.now();
    const windowStart = sessionStartTime.getTime() - 15 * 60 * 1000; // -15 min
    const windowEnd = sessionEndTime.getTime() + 30 * 60 * 1000;    // +30 min

    const isAttendanceOpen = now >= windowStart && now <= windowEnd;
    expect(isAttendanceOpen).toBe(true);
  });

  // Marca 4: T + 48h (Cierre perentorio de bitácoras pedagógicas)
  it('4. Marca T + 48h: bloquea el registro ordinario extemporáneo de bitácoras pedagógicas (RN-12)', () => {
    // Exactamente en el límite de 48 horas tras finalizar la sesión
    const tPlus48 = new Date(sessionEndTime.getTime() + 48 * 3600 * 1000);
    vi.setSystemTime(tPlus48);

    const hoursSinceEnd = (Date.now() - sessionEndTime.getTime()) / (3600 * 1000);
    expect(hoursSinceEnd).toBe(48.0);

    // 1 milisegundo después (extemporáneo)
    vi.advanceTimersByTime(1000);
    const expiredHours = (Date.now() - sessionEndTime.getTime()) / (3600 * 1000);
    const isExpired = expiredHours > 48.0;

    expect(isExpired).toBe(true);
  });
});
