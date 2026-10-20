import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { ApiAuthAdapter, authService } from '../authService';

describe('ApiAuthAdapter & Real API Integration (T-03 / RNF01 / RNF02)', () => {
  let adapter: ApiAuthAdapter;

  beforeEach(() => {
    adapter = new ApiAuthAdapter('http://localhost:8000');
    authService.clearToken();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    authService.clearToken();
    authService.setMode('mock');
  });

  describe('1. Solicitud de OTP vía API', () => {
    it('rechaza en el cliente correos que no pertenezcan al dominio @upt.pe', async () => {
      await expect(adapter.requestOtp('estudiante@gmail.com')).rejects.toThrowError(
        expect.objectContaining({ code: 'NON_UPT_DOMAIN' })
      );
    });

    it('procesa respuesta exitosa del backend REST', async () => {
      const mockFetchResponse = {
        challengeId: 'CHAL-API-1234567890AB',
        email: '2022074255@upt.pe',
        expiresAt: new Date(Date.now() + 5 * 60 * 1000).toISOString(),
        cooldownSeconds: 60,
        message: 'Código emitido',
        isMock: false,
        mockCodeHint: '654321',
      };

      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockFetchResponse,
      } as Response);

      const result = await adapter.requestOtp('2022074255@upt.pe');
      expect(result.challengeId).toBe('CHAL-API-1234567890AB');
      expect(result.email).toBe('2022074255@upt.pe');
      expect(result.isMock).toBe(false);
    });

    it('mapea respuesta HTTP 429 a excepción COOLDOWN_ACTIVE', async () => {
      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: false,
        status: 429,
        json: async () => ({
          detail: { code: 'COOLDOWN_ACTIVE', message: 'Debes esperar 45 segundos' },
        }),
      } as Response);

      await expect(adapter.requestOtp('2022074255@upt.pe')).rejects.toThrowError(
        expect.objectContaining({ code: 'COOLDOWN_ACTIVE' })
      );
    });

    it('maneja fallos de red retornando NETWORK_ERROR', async () => {
      vi.spyOn(globalThis, 'fetch').mockRejectedValueOnce(new Error('Failed to fetch'));

      await expect(adapter.requestOtp('2022074255@upt.pe')).rejects.toThrowError(
        expect.objectContaining({ code: 'NETWORK_ERROR' })
      );
    });
  });

  describe('2. Verificación de OTP y Gestión de Tokens JWT', () => {
    it('rechaza en el cliente códigos que no tengan 6 dígitos numéricos', async () => {
      await expect(adapter.verifyOtp('CHAL-123', '12')).rejects.toThrowError(
        expect.objectContaining({ code: 'OTP_INVALID' })
      );
    });

    it('emite y almacena token JWT de sesión tras verificación exitosa', async () => {
      const mockVerifyResponse = {
        success: true,
        email: '2022074255@upt.pe',
        verifiedAt: new Date().toISOString(),
        mode: 'api',
        message: 'Autenticado',
        token: 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIyMDIyMDc0MjU1QHVwdC5wZSJ9.fake_sig',
        tokenType: 'bearer',
      };

      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockVerifyResponse,
      } as Response);

      authService.setMode('api');
      const verifyResult = await authService.verifyOtp({
        challengeId: 'CHAL-API-123',
        otp: '123456',
      });

      expect(verifyResult.success).toBe(true);
      expect(verifyResult.token).toBe(mockVerifyResponse.token);
      expect(authService.getToken()).toBe(mockVerifyResponse.token);
      expect(authService.isAuthenticated()).toBe(true);

      // Limpieza de sesión
      authService.clearToken();
      expect(authService.isAuthenticated()).toBe(false);
    });

    it('mapea código inválido o expirado desde la API', async () => {
      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: false,
        status: 400,
        json: async () => ({
          detail: { code: 'OTP_EXPIRED', message: 'Código expirado' },
        }),
      } as Response);

      await expect(adapter.verifyOtp('CHAL-123', '000000')).rejects.toThrowError(
        expect.objectContaining({ code: 'OTP_EXPIRED' })
      );
    });
  });

  describe('3. Reenvío de OTP vía API', () => {
    it('procesa reenvío exitoso desde la API', async () => {
      const mockResend = {
        challengeId: 'CHAL-API-NEW',
        email: '2022074255@upt.pe',
        expiresAt: new Date().toISOString(),
        cooldownSeconds: 60,
        message: 'Nuevo código emitido',
        isMock: false,
      };

      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: true,
        status: 200,
        json: async () => mockResend,
      } as Response);

      const res = await adapter.resendOtp('CHAL-API-OLD');
      expect(res.challengeId).toBe('CHAL-API-NEW');
    });

    it('mapea desafío inexistente a CHALLENGE_NOT_FOUND', async () => {
      vi.spyOn(globalThis, 'fetch').mockResolvedValueOnce({
        ok: false,
        status: 404,
        json: async () => ({
          detail: { code: 'CHALLENGE_NOT_FOUND', message: 'Desafío no encontrado' },
        }),
      } as Response);

      await expect(adapter.resendOtp('NONEXISTENT')).rejects.toThrowError(
        expect.objectContaining({ code: 'CHALLENGE_NOT_FOUND' })
      );
    });
  });
});
