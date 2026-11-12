import { describe, it, expect, beforeEach, vi } from 'vitest';
import { certificateService } from '../certificateService';

describe('certificateService (T-42 / T-43 / T-44 / RF22 / RF23 / RN-14)', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    certificateService.setMode('mock');
  });

  describe('1. Consulta de Resumen de Horas (RN-14)', () => {
    it('retorna resumen con horas visadas, pendientes y porcentaje de progreso', async () => {
      certificateService.setMockHours('mentor@upt.pe', 16.0, 4.0);
      const summary = await certificateService.getHoursSummary({ mentorEmail: 'mentor@upt.pe' });

      expect(summary.mentor_email).toBe('mentor@upt.pe');
      expect(summary.horas_visadas).toBe(16.0);
      expect(summary.horas_pendientes).toBe(4.0);
      expect(summary.umbral_requerido).toBe(20.0);
      expect(summary.porcentaje_progreso).toBe(80.0);
      expect(summary.es_elegible).toBe(false);
      expect(summary.horas_faltantes).toBe(4.0);
    });

    it('reporta es_elegible = true cuando horas_visadas >= 20.0', async () => {
      certificateService.setMockHours('mentor.completo@upt.pe', 22.0, 0.0);
      const summary = await certificateService.getHoursSummary({ mentorEmail: 'mentor.completo@upt.pe' });

      expect(summary.horas_visadas).toBe(22.0);
      expect(summary.porcentaje_progreso).toBe(100.0);
      expect(summary.es_elegible).toBe(true);
      expect(summary.horas_faltantes).toBe(0.0);
    });
  });

  describe('2. Emisión y Descarga de Constancia Oficial DEMO', () => {
    it('bloquea la emisión si el mentor acumula menos de 20.0 horas visadas (RN-14)', async () => {
      certificateService.setMockHours('mentor.insuficiente@upt.pe', 14.0, 2.0);

      await expect(
        certificateService.generateCertificate({ mentorEmail: 'mentor.insuficiente@upt.pe' })
      ).rejects.toThrow(/INSUFFICIENT_ACCREDITED_HOURS/);
    });

    it('emite constancia con folio único, hash SHA-256 y marca DEMO cuando horas >= 20.0', async () => {
      certificateService.setMockHours('mentor.aprobado@upt.pe', 20.0, 0.0);

      const cert = await certificateService.generateCertificate({
        mentorEmail: 'mentor.aprobado@upt.pe',
        academicPeriod: '2026-II',
      });

      expect(cert.id_certificado).toBeGreaterThan(0);
      expect(cert.id_mentor).toBe('mentor.aprobado@upt.pe');
      expect(cert.codigo_folio).toMatch(/^CERT-2026-II-\d{4}$/);
      expect(cert.horas_acreditadas).toBe(20.0);
      expect(cert.estado).toBe('EMITIDO_DEMO');
      expect(cert.hash_firma).toContain('sha256-mock');
      expect(cert.verification_url).toContain(`folio=${cert.codigo_folio}`);

      // Comprobar que una segunda solicitud es rechazada por duplicidad
      await expect(
        certificateService.generateCertificate({ mentorEmail: 'mentor.aprobado@upt.pe' })
      ).rejects.toThrow(/DUPLICATE_CERTIFICATE_ISSUANCE/);
    });

    it('genera y descarga el archivo binario PDF correctamente', async () => {
      certificateService.setMockHours('mentor.descarga@upt.pe', 24.0, 0.0);
      const cert = await certificateService.generateCertificate({
        mentorEmail: 'mentor.descarga@upt.pe',
      });

      const blob = await certificateService.downloadPdf(cert.id_certificado, cert.codigo_folio);
      expect(blob).toBeInstanceOf(Blob);
      expect(blob.type).toBe('application/pdf');

      const text = await blob.text();
      expect(text).toContain('DEMO - FINES ACADÉMICOS');
      expect(text).toContain(cert.codigo_folio);
    });
  });

  describe('3. Verificación de Constancia Institucional QR', () => {
    it('valida un folio existente retornando dictamen auténtico', async () => {
      certificateService.setMockHours('mentor.qr@upt.pe', 20.0);
      const cert = await certificateService.generateCertificate({
        mentorEmail: 'mentor.qr@upt.pe',
      });

      const verification = await certificateService.verifyCertificate(cert.codigo_folio);
      expect(verification.valido).toBe(true);
      expect(verification.codigo_folio).toBe(cert.codigo_folio);
      expect(verification.horas_acreditadas).toBe(20.0);
      expect(verification.estado).toBe('EMITIDO_DEMO');
    });

    it('rechaza un folio inexistente con error 404', async () => {
      await expect(
        certificateService.verifyCertificate('CERT-2026-II-9999')
      ).rejects.toThrow(/CERTIFICATE_NOT_FOUND/);
    });
  });

  describe('4. Modo API y Seguridad en Producción', () => {
    it('impide activar modo mock si se detecta entorno de producción', () => {
      const originalProd = import.meta.env.PROD;
      try {
        (import.meta.env as unknown as { PROD: boolean }).PROD = true;
        expect(() => certificateService.setMode('mock')).toThrow(
          /El modo mock no está permitido en producción/
        );
      } finally {
        (import.meta.env as unknown as { PROD: boolean }).PROD = originalProd;
      }
    });
  });
});
