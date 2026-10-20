import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { authService } from '../authService';

describe('authService & MockAuthAdapter (T-02 / PB-002 / RNF01 / RNF09)', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    authService.cancelChallenge();
  });

  afterEach(() => {
    vi.useRealTimers();
    authService.cancelChallenge();
  });

  // Helper para resolver promesas con setTimeout en timers simulados
  async function resolveWithTimer<T>(promise: Promise<T>): Promise<T> {
    const resPromise = promise;
    await vi.advanceTimersByTimeAsync(300);
    return resPromise;
  }

  // Helper para verificar rechazos con setTimeout en timers simulados
  async function expectRejection<T>(promise: Promise<T>, expectedCode: string): Promise<void> {
    const assertion = expect(promise).rejects.toThrowError(
      expect.objectContaining({ code: expectedCode })
    );
    await vi.advanceTimersByTimeAsync(300);
    await assertion;
  }

  describe('1. Validación de Correo Institucional', () => {
    it('permite correos con dominio exacto @upt.pe', async () => {
      const res = await resolveWithTimer(
        authService.requestOtp({ email: '2022074255@upt.pe' })
      );

      expect(res.challengeId).toMatch(/^CHAL-DEV-/);
      expect(res.email).toBe('2022074255@upt.pe');
      expect(res.isMock).toBe(true);
      expect(res.cooldownSeconds).toBe(60);
      expect(new Date(res.expiresAt).getTime()).toBeGreaterThan(Date.now());
    });

    it('rechaza dominios que no sean @upt.pe (ej. @gmail.com)', async () => {
      await expectRejection(
        authService.requestOtp({ email: 'estudiante@gmail.com' }),
        'NON_UPT_DOMAIN'
      );
    });

    it('rechaza formatos de correo inválidos aun cuando terminen en @upt.pe', async () => {
      await expectRejection(
        authService.requestOtp({ email: '@upt.pe' }),
        'INVALID_EMAIL'
      );

      await expectRejection(
        authService.requestOtp({ email: 'usuario invalido@upt.pe' }),
        'INVALID_EMAIL'
      );
    });
  });

  describe('2. Verificación de OTP y Conservación de Ceros Iniciales', () => {
    it('verifica exitosamente el código válido por defecto (123456)', async () => {
      const challenge = await resolveWithTimer(
        authService.requestOtp({ email: '2022073504@upt.pe' })
      );

      const verifyRes = await resolveWithTimer(
        authService.verifyOtp({
          challengeId: challenge.challengeId,
          otp: '123456',
        })
      );

      expect(verifyRes.success).toBe(true);
      expect(verifyRes.email).toBe('2022073504@upt.pe');
      expect(verifyRes.mode).toBe('mock');
    });

    it('rechaza códigos con longitud distinta de 6 dígitos', async () => {
      const challenge = await resolveWithTimer(
        authService.requestOtp({ email: '2022074255@upt.pe' })
      );

      await expectRejection(
        authService.verifyOtp({ challengeId: challenge.challengeId, otp: '123' }),
        'OTP_INVALID'
      );

      await expectRejection(
        authService.verifyOtp({ challengeId: challenge.challengeId, otp: '1234567' }),
        'OTP_INVALID'
      );
    });

    it('rechaza código incorrecto de 6 dígitos', async () => {
      const challenge = await resolveWithTimer(
        authService.requestOtp({ email: '2022074255@upt.pe' })
      );

      await expectRejection(
        authService.verifyOtp({
          challengeId: challenge.challengeId,
          otp: '999999',
        }),
        'OTP_INVALID'
      );
    });

    it('rechaza un código que ya fue consumido previamente', async () => {
      const challenge = await resolveWithTimer(
        authService.requestOtp({ email: '2022074255@upt.pe' })
      );

      // Primera verificación exitosa
      await resolveWithTimer(
        authService.verifyOtp({
          challengeId: challenge.challengeId,
          otp: '123456',
        })
      );

      // Segundo intento con el mismo código consumido
      await expectRejection(
        authService.verifyOtp({
          challengeId: challenge.challengeId,
          otp: '123456',
        }),
        'OTP_ALREADY_USED'
      );
    });
  });

  describe('3. Expiración Temporal con Reloj Controlado (RNF01: 5 Minutos)', () => {
    it('permite verificar antes del límite de 5 minutos (ej. a los 4m 50s)', async () => {
      const challenge = await resolveWithTimer(
        authService.requestOtp({ email: '2022074255@upt.pe' })
      );

      // Avanzar reloj 4 minutos y 50 segundos
      vi.advanceTimersByTime(4 * 60 * 1000 + 50 * 1000);

      const res = await resolveWithTimer(
        authService.verifyOtp({
          challengeId: challenge.challengeId,
          otp: '123456',
        })
      );

      expect(res.success).toBe(true);
    });

    it('rechaza con OTP_EXPIRED cuando el tiempo sobrepasa los 5 minutos', async () => {
      const challenge = await resolveWithTimer(
        authService.requestOtp({ email: '2022074255@upt.pe' })
      );

      // Avanzar 5 minutos y 1 segundo
      vi.advanceTimersByTime(5 * 60 * 1000 + 1000);

      await expectRejection(
        authService.verifyOtp({
          challengeId: challenge.challengeId,
          otp: '123456',
        }),
        'OTP_EXPIRED'
      );
    });

    it('el código especial 000000 fuerza la simulación de expiración inmediata para demostraciones', async () => {
      const challenge = await resolveWithTimer(
        authService.requestOtp({ email: '2022074255@upt.pe' })
      );

      await expectRejection(
        authService.verifyOtp({
          challengeId: challenge.challengeId,
          otp: '000000',
        }),
        'OTP_EXPIRED'
      );
    });
  });

  describe('4. Cooldown de Reenvío e Invalidación de Desafíos (CUS01)', () => {
    it('bloquea el reenvío si se solicita antes de 60 segundos con COOLDOWN_ACTIVE', async () => {
      const challenge = await resolveWithTimer(
        authService.requestOtp({ email: '2022074255@upt.pe' })
      );

      // Intentar reenvío inmediato (0 segundos transcurridos)
      await expectRejection(
        authService.resendOtp({ challengeId: challenge.challengeId }),
        'COOLDOWN_ACTIVE'
      );
    });

    it('permite el reenvío tras transcurrir 60 segundos y genera un nuevo desafío', async () => {
      const challenge = await resolveWithTimer(
        authService.requestOtp({ email: '2022074255@upt.pe' })
      );

      // Avanzar 61 segundos para superar el cooldown
      vi.advanceTimersByTime(61 * 1000);

      const newChallenge = await resolveWithTimer(
        authService.resendOtp({ challengeId: challenge.challengeId })
      );

      expect(newChallenge.challengeId).not.toBe(challenge.challengeId);
      expect(newChallenge.mockCodeHint).toBe('654321');

      // El código rotativo 654321 es válido para el nuevo desafío
      const verifyRes = await resolveWithTimer(
        authService.verifyOtp({
          challengeId: newChallenge.challengeId,
          otp: '654321',
        })
      );
      expect(verifyRes.success).toBe(true);

      // El desafío antiguo queda invalidado
      await expectRejection(
        authService.verifyOtp({
          challengeId: challenge.challengeId,
          otp: '123456',
        }),
        'CHALLENGE_NOT_FOUND'
      );
    });
  });

  describe('5. Cancelación y Cambio de Correo', () => {
    it('descarta el desafío en memoria al llamar cancelChallenge', async () => {
      const challenge = await resolveWithTimer(
        authService.requestOtp({ email: '2022074255@upt.pe' })
      );

      authService.cancelChallenge();

      await expectRejection(
        authService.verifyOtp({
          challengeId: challenge.challengeId,
          otp: '123456',
        }),
        'CHALLENGE_NOT_FOUND'
      );
    });
  });

  describe('6. Bloqueo del Mock Fuera de Desarrollo', () => {
    it('rechaza solicitudes cuando no está en entorno de desarrollo', async () => {
      const originalEnv = process.env.NODE_ENV;

      try {
        process.env.NODE_ENV = 'production';

        await expectRejection(
          authService.requestOtp({ email: '2022074255@upt.pe' }),
          'MOCK_DISABLED'
        );
      } finally {
        process.env.NODE_ENV = originalEnv;
      }
    });

    it('hasRealApi reporta false en Sprint 1 al estar T-03 en desarrollo por Renzo', () => {
      expect(authService.hasRealApi()).toBe(false);
    });
  });
});
