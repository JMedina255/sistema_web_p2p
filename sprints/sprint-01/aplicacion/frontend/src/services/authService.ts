/**
 * Servicio de Autenticación y Desafío OTP (T-02 / CUS01 / RF01 / RNF01)
 *
 * NOTA DE ARQUITECTURA:
 * La API real de backend para emisión de OTP y validación (T-03) es responsabilidad de Renzo.
 * Este módulo define el contrato formal de comunicación y provee un adaptador MOCK explícito,
 * activado únicamente en entorno de desarrollo ('development') para permitir las pruebas de interfaz
 * de Joan sin depender de la infraestructura de correo SMTP institucional.
 */

export type AuthErrorCode =
  | 'INVALID_EMAIL'
  | 'NON_UPT_DOMAIN'
  | 'CHALLENGE_NOT_FOUND'
  | 'OTP_EXPIRED'
  | 'OTP_INVALID'
  | 'OTP_ALREADY_USED'
  | 'COOLDOWN_ACTIVE'
  | 'NETWORK_ERROR'
  | 'MOCK_DISABLED';

export class AuthException extends Error {
  public code: AuthErrorCode;

  constructor(code: AuthErrorCode, message: string) {
    super(message);
    this.name = 'AuthException';
    this.code = code;
  }
}

export interface RequestOtpPayload {
  email: string;
}

export interface RequestOtpResponse {
  challengeId: string;
  email: string;
  expiresAt: string; // ISO 8601
  cooldownSeconds: number;
  message: string;
  isMock: boolean;
  mockCodeHint?: string; // Código de prueba visible solo en desarrollo
}

export interface VerifyOtpPayload {
  challengeId: string;
  otp: string;
}

export interface VerifyOtpResponse {
  success: boolean;
  email: string;
  verifiedAt: string;
  mode: 'mock' | 'api';
  message: string;
  token?: string;
  tokenType?: string;
}

export interface ResendOtpPayload {
  challengeId: string;
}

// ============================================================================
// Adaptador MOCK en Memoria (Exclusivo para Desarrollo Local - Hito 3)
// ============================================================================

interface MockChallenge {
  id: string;
  email: string;
  code: string;
  createdAt: number;
  expiresAt: number; // Vigencia de 5 minutos (RNF01)
  resendAvailableAt: number; // Cooldown de 60 segundos (CUS01)
  consumed: boolean;
}

class MockAuthAdapter {
  private activeChallenge: MockChallenge | null = null;
  private challengeCounter: number = 100;

  private isDev(): boolean {
    const globalProcess = (globalThis as unknown as { process?: { env?: Record<string, string> } }).process;
    if (globalProcess?.env?.NODE_ENV === 'production') {
      return false;
    }
    if (typeof import.meta !== 'undefined' && import.meta.env) {
      return Boolean(import.meta.env.DEV);
    }
    return true;
  }

  public async requestOtp(email: string): Promise<RequestOtpResponse> {
    if (!this.isDev()) {
      throw new AuthException(
        'MOCK_DISABLED',
        'El adaptador mock de autenticación está estrictamente deshabilitado fuera de desarrollo.'
      );
    }

    const trimmedEmail = email.trim().toLowerCase();

    // Validación de dominio institucional exacto @upt.pe (CUS01 / RN-01)
    if (!trimmedEmail.endsWith('@upt.pe')) {
      throw new AuthException(
        'NON_UPT_DOMAIN',
        'El correo debe pertenecer estrictamente al dominio institucional oficial @upt.pe.'
      );
    }

    const emailRegex = /^[a-zA-Z0-9._%+-]+@upt\.pe$/;
    if (!emailRegex.test(trimmedEmail)) {
      throw new AuthException(
        'INVALID_EMAIL',
        'El formato del correo electrónico institucional es inválido.'
      );
    }

    // Simulación de latencia de red (250ms)
    await new Promise((resolve) => setTimeout(resolve, 250));

    this.challengeCounter += 1;
    const challengeId = `CHAL-DEV-${this.challengeCounter}-${Date.now().toString().slice(-4)}`;
    const now = Date.now();
    const expiresAt = now + 5 * 60 * 1000; // 5 minutos de vigencia (RNF01)
    const resendAvailableAt = now + 60 * 1000; // 60 segundos de cooldown (CUS01)

    // Código de prueba reproducible: 123456 por defecto (conservado como string de 6 dígitos)
    const mockCode = '123456';

    // Se descarta cualquier desafío anterior: cada nueva solicitud invalida el anterior
    this.activeChallenge = {
      id: challengeId,
      email: trimmedEmail,
      code: mockCode,
      createdAt: now,
      expiresAt,
      resendAvailableAt,
      consumed: false,
    };

    return {
      challengeId,
      email: trimmedEmail,
      expiresAt: new Date(expiresAt).toISOString(),
      cooldownSeconds: 60,
      message: 'Código de acceso de prueba generado satisfactoriamente.',
      isMock: true,
      mockCodeHint: mockCode,
    };
  }

  public async resendOtp(challengeId: string): Promise<RequestOtpResponse> {
    if (!this.isDev()) {
      throw new AuthException('MOCK_DISABLED', 'Mock deshabilitado fuera de desarrollo.');
    }

    await new Promise((resolve) => setTimeout(resolve, 250));

    if (!this.activeChallenge || this.activeChallenge.id !== challengeId) {
      throw new AuthException(
        'CHALLENGE_NOT_FOUND',
        'El desafío anterior ha caducado o fue descartado. Por favor, reinicia el acceso.'
      );
    }

    const now = Date.now();
    if (now < this.activeChallenge.resendAvailableAt && now < this.activeChallenge.expiresAt) {
      const remainingSeconds = Math.ceil((this.activeChallenge.resendAvailableAt - now) / 1000);
      throw new AuthException(
        'COOLDOWN_ACTIVE',
        `Debes esperar ${remainingSeconds} segundos antes de solicitar un nuevo reenvío.`
      );
    }

    // Nuevo desafío que invalida el código previo
    this.challengeCounter += 1;
    const newChallengeId = `CHAL-DEV-${this.challengeCounter}-${Date.now().toString().slice(-4)}`;
    const expiresAt = now + 5 * 60 * 1000;
    const resendAvailableAt = now + 60 * 1000;
    const newMockCode = '654321'; // Código rotativo para distinguir el reenvío

    this.activeChallenge = {
      id: newChallengeId,
      email: this.activeChallenge.email,
      code: newMockCode,
      createdAt: now,
      expiresAt,
      resendAvailableAt,
      consumed: false,
    };

    return {
      challengeId: newChallengeId,
      email: this.activeChallenge.email,
      expiresAt: new Date(expiresAt).toISOString(),
      cooldownSeconds: 60,
      message: 'Se ha reenviado un nuevo código OTP de prueba. El anterior ha sido invalidado.',
      isMock: true,
      mockCodeHint: newMockCode,
    };
  }

  public async verifyOtp(challengeId: string, otp: string): Promise<VerifyOtpResponse> {
    if (!this.isDev()) {
      throw new AuthException('MOCK_DISABLED', 'Mock deshabilitado fuera de desarrollo.');
    }

    await new Promise((resolve) => setTimeout(resolve, 250));

    const cleanOtp = otp.trim();

    // El OTP debe ser exactamente de 6 dígitos numéricos
    if (!/^\d{6}$/.test(cleanOtp)) {
      throw new AuthException(
        'OTP_INVALID',
        'El código OTP debe estar compuesto estrictamente por 6 dígitos numéricos.'
      );
    }

    if (!this.activeChallenge || this.activeChallenge.id !== challengeId) {
      throw new AuthException(
        'CHALLENGE_NOT_FOUND',
        'El código ingresado corresponde a un desafío anterior que ha sido invalidado.'
      );
    }

    const now = Date.now();

    // Caso de prueba especial para expiración inmediata sin esperar 5 minutos: código "000000"
    if (cleanOtp === '000000' || now > this.activeChallenge.expiresAt) {
      throw new AuthException(
        'OTP_EXPIRED',
        'El código de verificación ha expirado (plazo máximo de 5 minutos según RNF01). Solicita uno nuevo.'
      );
    }

    // Verificar si ya fue consumido
    if (this.activeChallenge.consumed) {
      throw new AuthException(
        'OTP_ALREADY_USED',
        'Este código OTP ya ha sido utilizado previamente. Solicita un nuevo código.'
      );
    }

    // Validación de coincidencia de código
    if (cleanOtp !== this.activeChallenge.code) {
      throw new AuthException(
        'OTP_INVALID',
        'Código OTP incorrecto. Verifica los 6 dígitos remitidos.'
      );
    }

    // Código verificado exitosamente -> se marca como consumido
    this.activeChallenge.consumed = true;
    const verifiedEmail = this.activeChallenge.email;

    return {
      success: true,
      email: verifiedEmail,
      verifiedAt: new Date().toISOString(),
      mode: 'mock',
      message: 'Autenticación de prueba validada correctamente.',
    };
  }

  public cancelChallenge(): void {
    this.activeChallenge = null;
  }
}

const mockAdapter = new MockAuthAdapter();

// ============================================================================
// Adaptador de API Real (T-03 / Renzo / FASTAPI REST)
// ============================================================================

export class ApiAuthAdapter {
  private apiBaseUrl: string;

  constructor(apiBaseUrl?: string) {
    const globalProcess = (globalThis as unknown as { process?: { env?: Record<string, string> } }).process;
    const envUrl = typeof import.meta !== 'undefined' && import.meta.env?.VITE_API_BASE_URL
      ? (import.meta.env.VITE_API_BASE_URL as string)
      : globalProcess?.env?.VITE_API_BASE_URL;

    this.apiBaseUrl = apiBaseUrl || envUrl || 'http://localhost:8000';
  }

  public async requestOtp(email: string): Promise<RequestOtpResponse> {
    const trimmedEmail = email.trim().toLowerCase();

    // Validación previa de dominio institucional exacto @upt.pe
    if (!trimmedEmail.endsWith('@upt.pe')) {
      throw new AuthException(
        'NON_UPT_DOMAIN',
        'El correo debe pertenecer estrictamente al dominio institucional oficial @upt.pe.'
      );
    }

    try {
      const response = await fetch(`${this.apiBaseUrl}/api/v1/auth/otp/request`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ email: trimmedEmail }),
      });

      const data = await response.json();

      if (!response.ok) {
        let code: AuthErrorCode = 'NETWORK_ERROR';
        let message = 'Error en solicitud OTP';

        if (response.status === 429) {
          code = 'COOLDOWN_ACTIVE';
        } else if (response.status === 422) {
          code = 'INVALID_EMAIL';
        }

        if (data && typeof data.detail === 'object') {
          code = (data.detail.code as AuthErrorCode) || code;
          message = data.detail.message || message;
        } else if (data && typeof data.detail === 'string') {
          message = data.detail;
        }

        throw new AuthException(code, message);
      }

      return data as RequestOtpResponse;
    } catch (err: unknown) {
      if (err instanceof AuthException) throw err;
      throw new AuthException(
        'NETWORK_ERROR',
        'No fue posible comunicar con el servidor API de autenticación. Verifica que el backend esté ejecutándose.'
      );
    }
  }

  public async resendOtp(challengeId: string): Promise<RequestOtpResponse> {
    try {
      const response = await fetch(`${this.apiBaseUrl}/api/v1/auth/otp/resend`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ challengeId }),
      });

      const data = await response.json();

      if (!response.ok) {
        let code: AuthErrorCode = 'CHALLENGE_NOT_FOUND';
        let message = 'Error al reenviar código OTP';

        if (response.status === 429) {
          code = 'COOLDOWN_ACTIVE';
        }

        if (data && typeof data.detail === 'object') {
          code = (data.detail.code as AuthErrorCode) || code;
          message = data.detail.message || message;
        } else if (data && typeof data.detail === 'string') {
          message = data.detail;
        }

        throw new AuthException(code, message);
      }

      return data as RequestOtpResponse;
    } catch (err: unknown) {
      if (err instanceof AuthException) throw err;
      throw new AuthException('NETWORK_ERROR', 'No fue posible comunicar con el servidor para reenvío de código.');
    }
  }

  public async verifyOtp(challengeId: string, otp: string): Promise<VerifyOtpResponse> {
    const cleanOtp = otp.trim();
    if (!/^\d{6}$/.test(cleanOtp)) {
      throw new AuthException(
        'OTP_INVALID',
        'El código OTP debe estar compuesto estrictamente por 6 dígitos numéricos.'
      );
    }

    try {
      const response = await fetch(`${this.apiBaseUrl}/api/v1/auth/otp/verify`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify({ challengeId, otp: cleanOtp }),
      });

      const data = await response.json();

      if (!response.ok) {
        let code: AuthErrorCode = 'OTP_INVALID';
        let message = 'Error en verificación OTP';

        if (response.status === 404) {
          code = 'CHALLENGE_NOT_FOUND';
        }

        if (data && typeof data.detail === 'object') {
          code = (data.detail.code as AuthErrorCode) || code;
          message = data.detail.message || message;
        } else if (data && typeof data.detail === 'string') {
          message = data.detail;
        }

        throw new AuthException(code, message);
      }

      return data as VerifyOtpResponse;
    } catch (err: unknown) {
      if (err instanceof AuthException) throw err;
      throw new AuthException('NETWORK_ERROR', 'No fue posible validar el código OTP contra la API de backend.');
    }
  }
}

const apiAdapter = new ApiAuthAdapter();

// Modo activo del servicio ('mock' por defecto para preservar compatibilidad con pruebas de H3)
let currentMode: 'mock' | 'api' = 'mock';
const SESSION_TOKEN_KEY = 'p2p_epis_jwt_token';

// ============================================================================
// Fachada del Servicio de Autenticación
// ============================================================================

export const authService = {
  /**
   * Indica si la API real de T-03 está seleccionada como activa.
   * Por defecto en las pruebas de Sprint 1 reporta false al estar en modo mock.
   */
  hasRealApi(): boolean {
    return currentMode === 'api';
  },

  getMode(): 'mock' | 'api' {
    return currentMode;
  },

  setMode(mode: 'mock' | 'api'): void {
    currentMode = mode;
  },

  async requestOtp(payload: RequestOtpPayload): Promise<RequestOtpResponse> {
    if (currentMode === 'api') {
      return apiAdapter.requestOtp(payload.email);
    }
    return mockAdapter.requestOtp(payload.email);
  },

  async resendOtp(payload: ResendOtpPayload): Promise<RequestOtpResponse> {
    if (currentMode === 'api') {
      return apiAdapter.resendOtp(payload.challengeId);
    }
    return mockAdapter.resendOtp(payload.challengeId);
  },

  async verifyOtp(payload: VerifyOtpPayload): Promise<VerifyOtpResponse> {
    let result: VerifyOtpResponse;
    if (currentMode === 'api') {
      result = await apiAdapter.verifyOtp(payload.challengeId, payload.otp);
    } else {
      result = await mockAdapter.verifyOtp(payload.challengeId, payload.otp);
    }

    if (result.success && result.token) {
      this.saveToken(result.token);
    }

    return result;
  },

  cancelChallenge(): void {
    mockAdapter.cancelChallenge();
  },

  saveToken(token: string): void {
    try {
      sessionStorage.setItem(SESSION_TOKEN_KEY, token);
    } catch {
      // Entornos sin sessionStorage
    }
  },

  getToken(): string | null {
    try {
      return sessionStorage.getItem(SESSION_TOKEN_KEY);
    } catch {
      return null;
    }
  },

  clearToken(): void {
    try {
      sessionStorage.removeItem(SESSION_TOKEN_KEY);
    } catch {
      // Ignore
    }
  },

  isAuthenticated(): boolean {
    return Boolean(this.getToken());
  },
};
