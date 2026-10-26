import { describe, it, expect, beforeEach } from 'vitest';
import { profileService } from '../profileService';
import type { AcademicProfile, AvailabilitySlot } from '../profileService';

describe('profileService (T-11 / RF04 / CUS15 / RN-03)', () => {
  const testEmail = '2022074255@upt.pe';

  beforeEach(() => {
    profileService.setMode('mock');
  });

  it('1. Valida la regla de mérito RN-03: ciclo >= 7 para mentores', () => {
    expect(profileService.validateMentorEligibility(6).eligible).toBe(false);
    expect(profileService.validateMentorEligibility(7).eligible).toBe(true);
    expect(profileService.validateMentorEligibility(10).eligible).toBe(true);
  });

  it('2. Obtiene un perfil por defecto para un correo institucional', async () => {
    const profile = await profileService.getProfile(testEmail);
    expect(profile.email).toBe(testEmail);
    expect(profile.materias_interes.length).toBeGreaterThan(0);
    expect(profile.modalidad_preferida).toBe('presencial');
  });

  it('3. Guarda y recupera exitosamente un perfil modificado', async () => {
    const customProfile: AcademicProfile = {
      email: testEmail,
      codigo_estudiante: '2022074255',
      nombres: 'Joan',
      apellidos: 'Medina',
      ciclo_actual: 6,
      rol_postulacion: 'mentoreado',
      materias_interes: [1, 2, 3],
      temas_seleccionados: [1],
      biografia: 'Prueba de perfil',
      modalidad_preferida: 'virtual',
    };

    const res = await profileService.saveProfile(customProfile);
    expect(res.success).toBe(true);
    expect(res.profile.biografia).toBe('Prueba de perfil');

    const loaded = await profileService.getProfile(testEmail);
    expect(loaded.modalidad_preferida).toBe('virtual');
    expect(loaded.materias_interes).toEqual([1, 2, 3]);
  });

  it('4. Bloquea el guardado si postula a mentor con ciclo inferior a VII', async () => {
    const invalidMentorProfile: AcademicProfile = {
      email: testEmail,
      ciclo_actual: 5,
      rol_postulacion: 'mentor',
      materias_interes: [1],
      temas_seleccionados: [],
      biografia: 'Postulante',
      modalidad_preferida: 'presencial',
    };

    await expect(profileService.saveProfile(invalidMentorProfile)).rejects.toThrow(
      /RN-03/
    );
  });

  it('5. Guarda y recupera bloques de disponibilidad horaria semanal', async () => {
    const slots: AvailabilitySlot[] = [
      { dia_semana: 1, hora_inicio: '08:00', hora_fin: '09:00' },
      { dia_semana: 2, hora_inicio: '10:00', hora_fin: '11:00' },
    ];

    const saveRes = await profileService.saveAvailability(testEmail, slots);
    expect(saveRes.success).toBe(true);
    expect(saveRes.totalSlots).toBe(2);

    const loadedSlots = await profileService.getAvailability(testEmail);
    expect(loadedSlots).toHaveLength(2);
    expect(loadedSlots[0].dia_semana).toBe(1);
    expect(loadedSlots[1].hora_inicio).toBe('10:00');
  });
});
