import { describe, it, expect, beforeEach, vi } from 'vitest';
import {
  offerService,
  validateOfferPayload,
  calculateAdvanceHours,
  STANDARD_CAPACITY,
  OfferException,
  type PublishOfferPayload,
  type SessionDuration,
} from '../offerService';

describe('offerService (T-14 / RF08 / CUS06 / RN-04 / RN-05)', () => {
  const baseNow = new Date('2026-10-26T08:00:00.000Z');

  beforeEach(() => {
    offerService.setMode('mock');
    offerService.clearMockOffers();
    vi.restoreAllMocks();
  });

  describe('CUS06-U01: Validación de campos obligatorios y formato', () => {
    it('1. Rechaza payload vacío o con campos incompletos listando los errores', () => {
      const validation = validateOfferPayload({}, baseNow);
      expect(validation.isValid).toBe(false);
      expect(validation.errors.id_asignatura).toBeDefined();
      expect(validation.errors.id_tema).toBeDefined();
      expect(validation.errors.modalidad).toBeDefined();
      expect(validation.errors.duracion_minutos).toBeDefined();
      expect(validation.errors.fecha_inicio).toBeDefined();
      expect(validation.errors.espacio_asignado).toBeDefined();
    });

    it('2. Rechaza duraciones que no correspondan a bloques lectivos de 60 o 90 minutos', () => {
      const payload: Partial<PublishOfferPayload> = {
        id_asignatura: 1,
        id_tema: 101,
        modalidad: 'presencial',
        duracion_minutos: 45 as unknown as SessionDuration,
        fecha_inicio: '2026-10-29T10:00:00.000Z',
        espacio_asignado: 'Lab EPIS 101',
      };
      const validation = validateOfferPayload(payload, baseNow);
      expect(validation.isValid).toBe(false);
      expect(validation.errors.duracion_minutos).toMatch(/60 o 90 minutos/i);
    });

    it('3. Valida exitosamente un payload completo y bien formado', () => {
      const futureDate = new Date(baseNow.getTime() + 50 * 3600 * 1000).toISOString(); // 50 horas
      const payload: PublishOfferPayload = {
        id_asignatura: 1,
        codigo_asignatura: 'CI-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 101,
        nombre_tema: 'Límites y Continuidad',
        modalidad: 'presencial',
        duracion_minutos: 60,
        aforo_maximo: 10,
        fecha_inicio: futureDate,
        espacio_asignado: 'Laboratorio de Cómputo 101 - Pabellón G (EPIS)',
        mentor_email: '2022074255@upt.pe',
      };

      const validation = validateOfferPayload(payload, baseNow);
      expect(validation.isValid).toBe(true);
      expect(Object.keys(validation.errors).length).toBe(0);
      expect(validation.isAdvanceValid).toBe(true);
      expect(validation.isRecommendedAdvance).toBe(true);
    });
  });

  describe('RN-04: Antelación obligatoria (> 24 h) y estándar recomendado (>= 48 h)', () => {
    it('1. Calcula correctamente las horas de antelación respecto al tiempo presente', () => {
      const in30Hours = new Date(baseNow.getTime() + 30 * 3600 * 1000);
      const hours = calculateAdvanceHours(in30Hours, baseNow);
      expect(hours).toBeCloseTo(30, 1);
    });

    it('2. Bloquea con error de infracción de RN-04 si la antelación es <= 24 horas', () => {
      // 20 horas en el futuro (infracción estricta de RN-04)
      const in20Hours = new Date(baseNow.getTime() + 20 * 3600 * 1000).toISOString();
      const payload: Partial<PublishOfferPayload> = {
        id_asignatura: 1,
        id_tema: 101,
        modalidad: 'presencial',
        duracion_minutos: 60,
        fecha_inicio: in20Hours,
        espacio_asignado: 'Lab 101',
      };

      const validation = validateOfferPayload(payload, baseNow);
      expect(validation.isValid).toBe(false);
      expect(validation.isAdvanceValid).toBe(false);
      expect(validation.errors.fecha_inicio).toMatch(/Infracción de RN-04/i);
    });

    it('3. Rechaza fechas que se encuentren en el pasado', () => {
      const pastDate = new Date(baseNow.getTime() - 2 * 3600 * 1000).toISOString();
      const payload: Partial<PublishOfferPayload> = {
        id_asignatura: 1,
        id_tema: 101,
        modalidad: 'presencial',
        duracion_minutos: 60,
        fecha_inicio: pastDate,
        espacio_asignado: 'Lab 101',
      };

      const validation = validateOfferPayload(payload, baseNow);
      expect(validation.isValid).toBe(false);
      expect(validation.errors.fecha_inicio).toMatch(/en el pasado/i);
    });

    it('4. Permite publicación si antelación > 24 h pero señala recomendación pendiente si < 48 h', () => {
      // 36 horas en el futuro
      const in36Hours = new Date(baseNow.getTime() + 36 * 3600 * 1000).toISOString();
      const payload: PublishOfferPayload = {
        id_asignatura: 1,
        codigo_asignatura: 'CI-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 101,
        nombre_tema: 'Límites',
        modalidad: 'virtual',
        duracion_minutos: 90,
        aforo_maximo: 20,
        fecha_inicio: in36Hours,
        espacio_asignado: 'https://meet.google.com/upt-ci101-demo',
        mentor_email: '2022074255@upt.pe',
      };

      const validation = validateOfferPayload(payload, baseNow);
      expect(validation.isValid).toBe(true);
      expect(validation.isAdvanceValid).toBe(true);
      expect(validation.isRecommendedAdvance).toBe(false); // No llega a las 48 h recomendadas
    });

    it('5. Reconoce antelación óptima recomendada cuando es >= 48 h', () => {
      // 49 horas en el futuro
      const in49Hours = new Date(baseNow.getTime() + 49 * 3600 * 1000).toISOString();
      const payload: PublishOfferPayload = {
        id_asignatura: 1,
        codigo_asignatura: 'CI-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 101,
        nombre_tema: 'Límites',
        modalidad: 'virtual',
        duracion_minutos: 90,
        aforo_maximo: 20,
        fecha_inicio: in49Hours,
        espacio_asignado: 'https://meet.google.com/upt-ci101-demo',
        mentor_email: '2022074255@upt.pe',
      };

      const validation = validateOfferPayload(payload, baseNow);
      expect(validation.isValid).toBe(true);
      expect(validation.isAdvanceValid).toBe(true);
      expect(validation.isRecommendedAdvance).toBe(true);
    });
  });

  describe('CUS06-U02: Aforos automáticos por modalidad (RN-05)', () => {
    it('1. Valida que el aforo presencial reglamentario sea estrictamente 10 estudiantes', () => {
      expect(STANDARD_CAPACITY.presencial).toBe(10);

      const in50Hours = new Date(baseNow.getTime() + 50 * 3600 * 1000).toISOString();
      const invalidPresencialPayload: PublishOfferPayload = {
        id_asignatura: 1,
        codigo_asignatura: 'CI-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 101,
        nombre_tema: 'Límites',
        modalidad: 'presencial',
        duracion_minutos: 60,
        aforo_maximo: 15, // Inválido para presencial
        fecha_inicio: in50Hours,
        espacio_asignado: 'Lab 101',
        mentor_email: '2022074255@upt.pe',
      };

      const validation = validateOfferPayload(invalidPresencialPayload, baseNow);
      expect(validation.isValid).toBe(false);
      expect(validation.errors.aforo_maximo).toMatch(/Infracción de RN-05.*10 estudiantes/i);
    });

    it('2. Valida que el aforo virtual reglamentario sea estrictamente 20 estudiantes', () => {
      expect(STANDARD_CAPACITY.virtual).toBe(20);

      const in50Hours = new Date(baseNow.getTime() + 50 * 3600 * 1000).toISOString();
      const invalidVirtualPayload: PublishOfferPayload = {
        id_asignatura: 1,
        codigo_asignatura: 'CI-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 101,
        nombre_tema: 'Límites',
        modalidad: 'virtual',
        duracion_minutos: 60,
        aforo_maximo: 30, // Inválido para virtual
        fecha_inicio: in50Hours,
        espacio_asignado: 'https://meet.google.com/upt-test',
        mentor_email: '2022074255@upt.pe',
      };

      const validation = validateOfferPayload(invalidVirtualPayload, baseNow);
      expect(validation.isValid).toBe(false);
      expect(validation.errors.aforo_maximo).toMatch(/Infracción de RN-05.*20 estudiantes/i);
    });
  });

  describe('Adaptador Mock y Publicación (T-14)', () => {
    it('1. Publica una oferta válida, genera código de sesión SES-XXXX y modo mock', async () => {
      const in72Hours = new Date(Date.now() + 72 * 3600 * 1000).toISOString();
      const validPayload: PublishOfferPayload = {
        id_asignatura: 2,
        codigo_asignatura: 'CI-201',
        nombre_asignatura: 'Cálculo II',
        id_tema: 201,
        nombre_tema: 'Integrales Impropias',
        modalidad: 'presencial',
        duracion_minutos: 90,
        aforo_maximo: 10,
        fecha_inicio: in72Hours,
        espacio_asignado: 'Laboratorio de Cómputo 101 - Pabellón G (EPIS)',
        mentor_email: '2022074255@upt.pe',
        mentor_nombre: 'Joan Medina Quispe',
      };

      const res = await offerService.publishOffer(validPayload);
      expect(res.estado).toBe('PUBLICADA');
      expect(res.codigo_sesion).toMatch(/^SES-\d+$/);
      expect(res.modo).toBe('mock');
      expect(res.aforo).toBe(10);
      expect(res.offer.nombre_asignatura).toBe('Cálculo II');

      const stored = await offerService.getOffers('2022074255@upt.pe');
      expect(stored.length).toBe(1);
      expect(stored[0].codigo_sesion).toBe(res.codigo_sesion);
    });

    it('2. Lanza OfferException ante payload inválido en publishOffer', async () => {
      const invalidPayload = {} as PublishOfferPayload;
      await expect(offerService.publishOffer(invalidPayload)).rejects.toThrow(OfferException);
    });

    it('3. Genera enlaces virtuales y aulas sugeridas coherentes', () => {
      const link = offerService.generateVirtualLink('CI-101');
      expect(link).toMatch(/^https:\/\/meet\.google\.com\/upt-ci101-[a-z0-9]+/);

      const room = offerService.suggestClassroom();
      expect(room).toContain('EPIS');
    });
  });

  describe('Integración API (T-15/T-16 Pendiente)', () => {
    it('1. Maneja de forma controlada el modo API cuando el endpoint no está disponible', async () => {
      offerService.setMode('api');
      expect(offerService.getMode()).toBe('api');

      // Mock de fetch fallido
      vi.stubGlobal('fetch', vi.fn().mockRejectedValue(new Error('Connection refused')));

      const in72Hours = new Date(Date.now() + 72 * 3600 * 1000).toISOString();
      const payload: PublishOfferPayload = {
        id_asignatura: 1,
        codigo_asignatura: 'CI-101',
        nombre_asignatura: 'Cálculo I',
        id_tema: 101,
        nombre_tema: 'Límites',
        modalidad: 'virtual',
        duracion_minutos: 60,
        aforo_maximo: 20,
        fecha_inicio: in72Hours,
        espacio_asignado: 'https://meet.google.com/test',
        mentor_email: '2022074255@upt.pe',
      };

      await expect(offerService.publishOffer(payload)).rejects.toThrow(/backend real \(T-15 \/ T-16\) puede encontrarse pendiente/i);
    });
  });
});
