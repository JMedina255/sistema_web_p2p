/**
 * Servicio de Consentimiento Informado Digital — Ley N° 29733 (T-04 / T-05)
 * Gobierna el registro de conformidad para tratamiento de datos personales y algoritmos de emparejamiento.
 */

export interface ConsentStatus {
  hasConsented: boolean;
  consentedAt: string | null;
  version: string;
  termsVersion: string;
  email: string;
  mode: 'mock' | 'api';
}

export interface ConsentPayload {
  email: string;
  accepted: boolean;
  termsVersion: string;
  ipAddress?: string;
  userAgent?: string;
}

export interface ConsentResponse {
  success: boolean;
  consentedAt: string;
  email: string;
  message: string;
}

const STORAGE_KEY_PREFIX = 'p2p_consent_';
const CURRENT_TERMS_VERSION = '2026-II-v1.0';

class ConsentService {
  private mode: 'mock' | 'api' = 'mock';

  constructor() {
    // Si existe VITE_API_BASE_URL y no estamos en DEV forzado, podría usar api
    this.mode = 'mock';
  }

  public getMode(): 'mock' | 'api' {
    return this.mode;
  }

  public setMode(mode: 'mock' | 'api'): void {
    this.mode = mode;
  }

  public getTermsVersion(): string {
    return CURRENT_TERMS_VERSION;
  }

  /**
   * Consulta el estado del consentimiento para un correo institucional dado.
   */
  public async getConsentStatus(email: string): Promise<ConsentStatus> {
    if (!email) {
      return {
        hasConsented: false,
        consentedAt: null,
        version: '1.0',
        termsVersion: CURRENT_TERMS_VERSION,
        email: '',
        mode: this.mode,
      };
    }

    if (this.mode === 'mock') {
      try {
        const stored = typeof window !== 'undefined' ? window.localStorage.getItem(STORAGE_KEY_PREFIX + email) : null;
        if (stored) {
          const parsed = JSON.parse(stored);
          return {
            hasConsented: Boolean(parsed.accepted),
            consentedAt: parsed.consentedAt || null,
            version: '1.0',
            termsVersion: parsed.termsVersion || CURRENT_TERMS_VERSION,
            email,
            mode: 'mock',
          };
        }
      } catch {
        // Fallback seguro si localStorage falla o está bloqueado
      }

      // Por defecto para nuevos usuarios en mock: no consentido
      return {
        hasConsented: false,
        consentedAt: null,
        version: '1.0',
        termsVersion: CURRENT_TERMS_VERSION,
        email,
        mode: 'mock',
      };
    }

    // Modo API real (T-05)
    try {
      const baseUrl = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
      const res = await fetch(`${baseUrl}/api/v1/consent/status?email=${encodeURIComponent(email)}`);
      if (res.ok) {
        const data = await res.json();
        return {
          hasConsented: Boolean(data.has_consented),
          consentedAt: data.consented_at || null,
          version: '1.0',
          termsVersion: data.terms_version || CURRENT_TERMS_VERSION,
          email,
          mode: 'api',
        };
      }
    } catch {
      // Fallback a mock en caso de indisponibilidad en desarrollo
    }

    return {
      hasConsented: false,
      consentedAt: null,
      version: '1.0',
      termsVersion: CURRENT_TERMS_VERSION,
      email,
      mode: this.mode,
    };
  }

  /**
   * Registra la aceptación expresa del consentimiento informado digital.
   */
  public async acceptConsent(email: string, termsVersion: string = CURRENT_TERMS_VERSION): Promise<ConsentResponse> {
    if (!email || !email.endsWith('@upt.pe')) {
      throw new Error('Se requiere un correo institucional válido con dominio @upt.pe');
    }

    const consentedAt = new Date().toISOString();

    if (this.mode === 'mock') {
      try {
        if (typeof window !== 'undefined') {
          window.localStorage.setItem(
            STORAGE_KEY_PREFIX + email,
            JSON.stringify({
              accepted: true,
              consentedAt,
              termsVersion,
              email,
            })
          );
        }
      } catch {
        // En caso de entornos de prueba sin localStorage
      }

      return {
        success: true,
        consentedAt,
        email,
        message: 'Consentimiento informado registrado exitosamente conforme a la Ley N° 29733 (Modo Mock).',
      };
    }

    // Modo API real (T-05 de Renzo)
    const baseUrl = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
    const res = await fetch(`${baseUrl}/api/v1/consent/accept`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify({
        email,
        accepted: true,
        terms_version: termsVersion,
      }),
    });

    if (!res.ok) {
      throw new Error(`Error en servidor al registrar consentimiento: HTTP ${res.status}`);
    }

    const data = await res.json();
    return {
      success: true,
      consentedAt: data.consented_at || consentedAt,
      email,
      message: 'Consentimiento informado registrado exitosamente en base de datos.',
    };
  }

  /**
   * Revoca o rechaza el consentimiento informado, bloqueando el acceso al sistema (RN-02).
   */
  public async revokeConsent(email: string): Promise<{ success: boolean; message: string }> {
    if (this.mode === 'mock') {
      try {
        if (typeof window !== 'undefined') {
          window.localStorage.removeItem(STORAGE_KEY_PREFIX + email);
        }
      } catch {
        // Manejo silencioso en test
      }

      return {
        success: true,
        message: 'Consentimiento no otorgado o revocado. Acceso a la plataforma bloqueado preventivamente.',
      };
    }

    // Modo API real
    const baseUrl = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
    try {
      await fetch(`${baseUrl}/api/v1/consent/revoke`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ email }),
      });
    } catch {
      // Ignorar error de red si se revoca offline
    }

    return {
      success: true,
      message: 'Consentimiento revocado. Sesión abortada.',
    };
  }
}

export const consentService = new ConsentService();
