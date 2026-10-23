import { describe, it, expect, beforeEach } from 'vitest';
import { consentService } from '../consentService';

describe('consentService (T-04 / RF02 / RN-02)', () => {
  const testEmail = '2022074255@upt.pe';

  beforeEach(async () => {
    consentService.setMode('mock');
    await consentService.revokeConsent(testEmail);
  });

  it('1. Retorna hasConsented=false por defecto para un usuario no registrado', async () => {
    const status = await consentService.getConsentStatus(testEmail);
    expect(status.hasConsented).toBe(false);
    expect(status.consentedAt).toBeNull();
    expect(status.termsVersion).toBe(consentService.getTermsVersion());
  });

  it('2. Registra exitosamente la aceptación de términos bajo la Ley N° 29733', async () => {
    const res = await consentService.acceptConsent(testEmail);
    expect(res.success).toBe(true);
    expect(res.email).toBe(testEmail);
    expect(res.consentedAt).toBeTruthy();

    const status = await consentService.getConsentStatus(testEmail);
    expect(status.hasConsented).toBe(true);
    expect(status.consentedAt).toBe(res.consentedAt);
  });

  it('3. Rechaza el registro con correos que no pertenecen al dominio @upt.pe', async () => {
    await expect(consentService.acceptConsent('usuario@gmail.com')).rejects.toThrow(
      'Se requiere un correo institucional válido con dominio @upt.pe'
    );
  });

  it('4. Permite revocar o desestimar el consentimiento previamente otorgado', async () => {
    await consentService.acceptConsent(testEmail);
    let status = await consentService.getConsentStatus(testEmail);
    expect(status.hasConsented).toBe(true);

    const revokeRes = await consentService.revokeConsent(testEmail);
    expect(revokeRes.success).toBe(true);

    status = await consentService.getConsentStatus(testEmail);
    expect(status.hasConsented).toBe(false);
  });

  it('5. Maneja consultas con correo vacío retornando false sin excepciones', async () => {
    const status = await consentService.getConsentStatus('');
    expect(status.hasConsented).toBe(false);
  });
});
