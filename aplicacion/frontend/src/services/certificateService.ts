/**
 * Servicio de Acreditación de Horas y Emisión de Constancias PDF Oficiales DEMO
 * T-42 / T-43 / T-44 / RF22 / RF23 / RN-14
 * Sistema Web P2P de Mentorías Académicas — EPIS UPT
 */

import { authService } from './authService';

export interface CertificateMetaResponse {
  id_certificado: number;
  id_mentor: string;
  codigo_folio: string;
  periodo_academico: string;
  horas_acreditadas: number;
  hash_firma: string;
  estado: string;
  created_at: string;
  verification_url: string;
}

export interface HoursSummaryResponse {
  mentor_email: string;
  horas_visadas: number;
  horas_pendientes: number;
  umbral_requerido: number;
  porcentaje_progreso: number;
  es_elegible: boolean;
  horas_faltantes: number;
  certificado_emitido: CertificateMetaResponse | null;
}

export interface CertificateVerifyResponse {
  valido: boolean;
  codigo_folio: string;
  id_mentor: string;
  periodo_academico: string;
  horas_acreditadas: number;
  hash_firma: string;
  estado: string;
  fecha_emision: string;
  institucion: string;
  mensaje: string;
}

class ApiCertificateAdapter {
  private getBaseUrl(): string {
    return (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
  }

  private getAuthHeaders(custom: Record<string, string> = {}): Record<string, string> {
    const headers: Record<string, string> = {
      Accept: 'application/json',
      ...custom,
    };
    const token = authService.getToken();
    if (token) {
      headers['Authorization'] = `Bearer ${token}`;
    }
    return headers;
  }

  public async getHoursSummary(
    mentorEmail?: string,
    academicPeriod: string = '2026-II'
  ): Promise<HoursSummaryResponse> {
    const email = mentorEmail || authService.getCurrentUser()?.email || '';
    const url = `${this.getBaseUrl()}/api/v1/certificates/summary?mentor_email=${encodeURIComponent(
      email
    )}&periodo_academico=${encodeURIComponent(academicPeriod)}`;
    const res = await fetch(url, {
      method: 'GET',
      headers: this.getAuthHeaders(),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => null);
      throw new Error(err?.detail || `Error HTTP ${res.status}: ${res.statusText}`);
    }
    return res.json();
  }

  public async generateCertificate(params?: {
    mentorEmail?: string;
    academicPeriod?: string;
  }): Promise<CertificateMetaResponse> {
    const url = `${this.getBaseUrl()}/api/v1/certificates/generate`;
    const res = await fetch(url, {
      method: 'POST',
      headers: this.getAuthHeaders({ 'Content-Type': 'application/json' }),
      body: JSON.stringify({
        periodo_academico: params?.academicPeriod || '2026-II',
        mentor_email: params?.mentorEmail || undefined,
      }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => null);
      throw new Error(err?.detail || `Error HTTP ${res.status}: ${res.statusText}`);
    }
    return res.json();
  }

  public async getCertificate(certificateId: number): Promise<CertificateMetaResponse> {
    const url = `${this.getBaseUrl()}/api/v1/certificates/${certificateId}`;
    const res = await fetch(url, {
      method: 'GET',
      headers: this.getAuthHeaders(),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => null);
      throw new Error(err?.detail || `Error HTTP ${res.status}: ${res.statusText}`);
    }
    return res.json();
  }

  public async downloadPdf(certificateId: number): Promise<Blob> {
    const url = `${this.getBaseUrl()}/api/v1/certificates/${certificateId}/download`;
    const res = await fetch(url, {
      method: 'GET',
      headers: this.getAuthHeaders({ Accept: 'application/pdf' }),
    });
    if (!res.ok) {
      const err = await res.json().catch(() => null);
      throw new Error(err?.detail || `Error HTTP ${res.status}: ${res.statusText}`);
    }
    return res.blob();
  }

  public async verifyCertificate(folio: string): Promise<CertificateVerifyResponse> {
    const url = `${this.getBaseUrl()}/api/v1/certificates/verificar?folio=${encodeURIComponent(
      folio
    )}`;
    const res = await fetch(url, { method: 'GET' });
    if (!res.ok) {
      const err = await res.json().catch(() => null);
      throw new Error(err?.detail || `Error HTTP ${res.status}: ${res.statusText}`);
    }
    return res.json();
  }
}

class MockCertificateAdapter {
  private mockSummaries: Record<string, HoursSummaryResponse> = {
    'mentor@upt.pe': {
      mentor_email: 'mentor@upt.pe',
      horas_visadas: 22.0,
      horas_pendientes: 2.0,
      umbral_requerido: 20.0,
      porcentaje_progreso: 100.0,
      es_elegible: true,
      horas_faltantes: 0.0,
      certificado_emitido: null,
    },
    '2022073504@upt.pe': {
      mentor_email: '2022073504@upt.pe',
      horas_visadas: 22.0,
      horas_pendientes: 0.0,
      umbral_requerido: 20.0,
      porcentaje_progreso: 100.0,
      es_elegible: true,
      horas_faltantes: 0.0,
      certificado_emitido: null,
    },
    'mentor.insuficiente@upt.pe': {
      mentor_email: 'mentor.insuficiente@upt.pe',
      horas_visadas: 16.0,
      horas_pendientes: 4.0,
      umbral_requerido: 20.0,
      porcentaje_progreso: 80.0,
      es_elegible: false,
      horas_faltantes: 4.0,
      certificado_emitido: null,
    },
  };

  private mockCertificates: Record<number, CertificateMetaResponse> = {};
  private mockFolioMap: Record<string, CertificateMetaResponse> = {};
  private certIdCounter = 1;

  public resetMockState() {
    this.mockCertificates = {};
    this.mockFolioMap = {};
    this.certIdCounter = 1;
    this.mockSummaries = {
      'mentor@upt.pe': {
        mentor_email: 'mentor@upt.pe',
        horas_visadas: 22.0,
        horas_pendientes: 2.0,
        umbral_requerido: 20.0,
        porcentaje_progreso: 100.0,
        es_elegible: true,
        horas_faltantes: 0.0,
        certificado_emitido: null,
      },
      '2022073504@upt.pe': {
        mentor_email: '2022073504@upt.pe',
        horas_visadas: 22.0,
        horas_pendientes: 0.0,
        umbral_requerido: 20.0,
        porcentaje_progreso: 100.0,
        es_elegible: true,
        horas_faltantes: 0.0,
        certificado_emitido: null,
      },
      'mentor.insuficiente@upt.pe': {
        mentor_email: 'mentor.insuficiente@upt.pe',
        horas_visadas: 16.0,
        horas_pendientes: 4.0,
        umbral_requerido: 20.0,
        porcentaje_progreso: 80.0,
        es_elegible: false,
        horas_faltantes: 4.0,
        certificado_emitido: null,
      },
    };
  }

  public setMockHours(email: string, visadas: number, pendientes: number = 0) {
    const cleanEmail = email.trim().toLowerCase();
    const progreso = Math.min(100.0, Math.round((visadas / 20.0) * 1000) / 10);
    const faltantes = Math.max(0, Math.round((20.0 - visadas) * 100) / 100);
    this.mockSummaries[cleanEmail] = {
      mentor_email: cleanEmail,
      horas_visadas: visadas,
      horas_pendientes: pendientes,
      umbral_requerido: 20.0,
      porcentaje_progreso: progreso,
      es_elegible: visadas >= 20.0,
      horas_faltantes: faltantes,
      certificado_emitido: this.mockSummaries[cleanEmail]?.certificado_emitido || null,
    };
  }

  public async getHoursSummary(
    mentorEmail?: string,
    academicPeriod: string = '2026-II'
  ): Promise<HoursSummaryResponse> {
    void academicPeriod;
    const email = (mentorEmail || authService.getCurrentUser()?.email || 'mentor@upt.pe').trim().toLowerCase();
    if (!this.mockSummaries[email]) {
      this.mockSummaries[email] = {
        mentor_email: email,
        horas_visadas: 0.0,
        horas_pendientes: 0.0,
        umbral_requerido: 20.0,
        porcentaje_progreso: 0.0,
        es_elegible: false,
        horas_faltantes: 20.0,
        certificado_emitido: null,
      };
    }
    return { ...this.mockSummaries[email] };
  }

  public async generateCertificate(params?: {
    mentorEmail?: string;
    academicPeriod?: string;
  }): Promise<CertificateMetaResponse> {
    const email = (params?.mentorEmail || authService.getCurrentUser()?.email || 'mentor@upt.pe').trim().toLowerCase();
    const summary = await this.getHoursSummary(email, params?.academicPeriod);

    if (!summary.es_elegible) {
      throw new Error(
        `INSUFFICIENT_ACCREDITED_HOURS: No cumples con el umbral mínimo de 20 horas visadas para emitir la constancia (acumulas ${summary.horas_visadas} h).`
      );
    }

    if (summary.certificado_emitido) {
      throw new Error(
        'DUPLICATE_CERTIFICATE_ISSUANCE: Ya se encuentra emitida tu constancia institucional para este período académico.'
      );
    }

    const cId = this.certIdCounter++;
    const period = params?.academicPeriod || '2026-II';
    const folio = `CERT-${period}-${String(cId).padStart(4, '0')}`;
    const hash = `sha256-mock-cert-${cId}-${Date.now()}`;
    const cert: CertificateMetaResponse = {
      id_certificado: cId,
      id_mentor: email,
      codigo_folio: folio,
      periodo_academico: period,
      horas_acreditadas: summary.horas_visadas,
      hash_firma: hash,
      estado: 'EMITIDO_DEMO',
      created_at: new Date().toISOString(),
      verification_url: `https://epis.upt.edu.pe/p2p/certificados/verificar?folio=${folio}`,
    };

    this.mockCertificates[cId] = cert;
    this.mockFolioMap[folio] = cert;
    summary.certificado_emitido = cert;
    this.mockSummaries[email] = summary;

    return cert;
  }

  public async getCertificate(certificateId: number): Promise<CertificateMetaResponse> {
    const c = this.mockCertificates[certificateId];
    if (!c) {
      throw new Error('CERTIFICATE_NOT_FOUND: La constancia solicitada no fue encontrada.');
    }
    return c;
  }

  public async downloadPdf(certificateId: number): Promise<Blob> {
    const c = this.mockCertificates[certificateId];
    const folio = c ? c.codigo_folio : 'CERT-2026-II-0001';
    const mockContent = `%PDF-1.4\nDEMO - FINES ACADÉMICOS\nConstancia de Mentoría EPIS-UPT\nFolio: ${folio}\n`;
    return new Blob([mockContent], { type: 'application/pdf' });
  }

  public async verifyCertificate(folio: string): Promise<CertificateVerifyResponse> {
    const clean = folio.trim().toUpperCase();
    const c = this.mockFolioMap[clean];
    if (!c) {
      throw new Error(`CERTIFICATE_NOT_FOUND: El folio '${clean}' no corresponde a ninguna constancia.`);
    }
    return {
      valido: true,
      codigo_folio: c.codigo_folio,
      id_mentor: c.id_mentor,
      periodo_academico: c.periodo_academico,
      horas_acreditadas: c.horas_acreditadas,
      hash_firma: c.hash_firma,
      estado: c.estado,
      fecha_emision: c.created_at,
      institucion: 'Universidad Privada de Tacna - Escuela Profesional de Ingeniería de Sistemas',
      mensaje: 'Constancia de mentoría auténtica, vigente y acreditada por la EPIS-UPT.',
    };
  }
}

const apiAdapter = new ApiCertificateAdapter();
const mockAdapter = new MockCertificateAdapter();

function resolveServiceMode(): 'mock' | 'api' {
  if (import.meta.env.PROD) return 'api';
  if (import.meta.env.VITE_SERVICE_MODE === 'api') return 'api';
  return 'mock';
}

let activeMode = resolveServiceMode();

export const certificateService = {
  setMode(mode: 'mock' | 'api') {
    if (import.meta.env.PROD && mode === 'mock') {
      throw new Error('El modo mock no está permitido en producción.');
    }
    activeMode = mode;
  },

  getMode(): 'mock' | 'api' {
    return activeMode;
  },

  setMockHours(email: string, visadas: number, pendientes: number = 0) {
    mockAdapter.setMockHours(email, visadas, pendientes);
  },

  resetMockState() {
    mockAdapter.resetMockState();
  },

  async getHoursSummary(params?: {
    mentorEmail?: string;
    academicPeriod?: string;
  }): Promise<HoursSummaryResponse> {
    if (activeMode === 'api') {
      return apiAdapter.getHoursSummary(params?.mentorEmail, params?.academicPeriod);
    }
    return mockAdapter.getHoursSummary(params?.mentorEmail, params?.academicPeriod);
  },

  async generateCertificate(params?: {
    mentorEmail?: string;
    academicPeriod?: string;
  }): Promise<CertificateMetaResponse> {
    if (activeMode === 'api') {
      return apiAdapter.generateCertificate(params);
    }
    return mockAdapter.generateCertificate(params);
  },

  async getCertificate(certificateId: number): Promise<CertificateMetaResponse> {
    if (activeMode === 'api') {
      return apiAdapter.getCertificate(certificateId);
    }
    return mockAdapter.getCertificate(certificateId);
  },

  async downloadPdf(certificateId: number, folio?: string): Promise<Blob> {
    let blob: Blob;
    if (activeMode === 'api') {
      blob = await apiAdapter.downloadPdf(certificateId);
    } else {
      blob = await mockAdapter.downloadPdf(certificateId);
    }

    // Si estamos en entorno navegador, disparar descarga automática
    if (typeof window !== 'undefined' && typeof document !== 'undefined') {
      try {
        const url = window.URL.createObjectURL(blob);
        const a = document.createElement('a');
        a.style.display = 'none';
        a.href = url;
        const folioStr = folio || `CERT-${certificateId}`;
        a.download = `Constancia_Mentoria_EPIS_2026_II_${folioStr}.pdf`;
        document.body.appendChild(a);
        a.click();
        setTimeout(() => {
          document.body.removeChild(a);
          window.URL.revokeObjectURL(url);
        }, 150);
      } catch {
        // En entorno test / headless puede no existir createObjectURL completo
      }
    }

    return blob;
  },

  async downloadCertificatePdf(certificateId: number, folio?: string): Promise<Blob> {
    return this.downloadPdf(certificateId, folio);
  },

  async verifyCertificate(folio: string): Promise<CertificateVerifyResponse> {
    if (activeMode === 'api') {
      return apiAdapter.verifyCertificate(folio);
    }
    return mockAdapter.verifyCertificate(folio);
  },
};
