/**
 * Servicio de Perfiles Académicos y Disponibilidad Horaria — (T-11 / T-12)
 * Maneja la captura de intereses, debilidades/fortalezas y agenda semanal (RF04 / CUS15 / RN-03).
 */

export interface AvailabilitySlot {
  dia_semana: number; // 1: Lunes, 2: Martes, 3: Miércoles, 4: Jueves, 5: Viernes, 6: Sábado
  hora_inicio: string; // ej. "08:00"
  hora_fin: string; // ej. "09:00"
}

export interface AcademicProfile {
  email: string;
  codigo_estudiante?: string;
  nombres?: string;
  apellidos?: string;
  ciclo_actual: number; // 1 a 10
  rol_postulacion: 'mentoreado' | 'mentor';
  materias_interes: number[]; // IDs de asignaturas seleccionadas
  temas_seleccionados: number[]; // IDs de temas silábicos de refuerzo o fortaleza
  biografia: string;
  modalidad_preferida: 'presencial' | 'virtual' | 'hibrida';
  updated_at?: string;
}

const STORAGE_PROFILE_KEY = 'p2p_profile_';
const STORAGE_AVAILABILITY_KEY = 'p2p_availability_';

class ProfileService {
  private mode: 'mock' | 'api' = 'mock';

  public getMode(): 'mock' | 'api' {
    return this.mode;
  }

  public setMode(mode: 'mock' | 'api'): void {
    this.mode = mode;
  }

  /**
   * Valida la regla de mérito y ciclo mínimo institucional (RN-03)
   * Los mentores deben pertenecer estrictamente a ciclos avanzados (VII a X).
   */
  public validateMentorEligibility(ciclo: number): { eligible: boolean; reason?: string } {
    if (ciclo < 7) {
      return {
        eligible: false,
        reason:
          'Conforme a la regla institucional RN-03, la postulación al rol de Mentor está reservada para estudiantes de ciclos superiores (VII al X ciclo).',
      };
    }
    return { eligible: true };
  }

  /**
   * Obtiene el perfil formativo del estudiante.
   */
  public async getProfile(email: string): Promise<AcademicProfile> {
    if (!email) {
      return this.getDefaultProfile('');
    }

    if (this.mode === 'mock') {
      try {
        const stored = typeof window !== 'undefined' ? window.localStorage.getItem(STORAGE_PROFILE_KEY + email) : null;
        if (stored) {
          return JSON.parse(stored) as AcademicProfile;
        }
      } catch {
        // Fallback en pruebas
      }

      // Perfil inicial sugerido para Joan o Renzo en dev
      const defaultProfile = this.getDefaultProfile(email);
      if (email.startsWith('2022074255')) {
        defaultProfile.codigo_estudiante = '2022074255';
        defaultProfile.nombres = 'Joan Cristian';
        defaultProfile.apellidos = 'Medina Quispe';
        defaultProfile.ciclo_actual = 6;
      } else if (email.startsWith('2022073504')) {
        defaultProfile.codigo_estudiante = '2022073504';
        defaultProfile.nombres = 'Renzo Antonio';
        defaultProfile.apellidos = 'Antayhua Mamani';
        defaultProfile.ciclo_actual = 7;
        defaultProfile.rol_postulacion = 'mentor';
      }
      return defaultProfile;
    }

    // Modo API (T-12 de Renzo)
    try {
      const baseUrl = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
      const res = await fetch(`${baseUrl}/api/v1/profiles/me?email=${encodeURIComponent(email)}`);
      if (res.ok) {
        return (await res.json()) as AcademicProfile;
      }
    } catch {
      // Fallback a default
    }

    return this.getDefaultProfile(email);
  }

  /**
   * Guarda o actualiza el perfil académico.
   */
  public async saveProfile(
    profile: AcademicProfile
  ): Promise<{ success: boolean; profile: AcademicProfile; message: string }> {
    if (!profile.email) {
      throw new Error('El correo institucional es obligatorio para guardar el perfil.');
    }

    // Validación de RN-03 si postula a mentor
    if (profile.rol_postulacion === 'mentor') {
      const check = this.validateMentorEligibility(profile.ciclo_actual);
      if (!check.eligible) {
        throw new Error(check.reason);
      }
    }

    const updatedProfile: AcademicProfile = {
      ...profile,
      updated_at: new Date().toISOString(),
    };

    if (this.mode === 'mock') {
      try {
        if (typeof window !== 'undefined') {
          window.localStorage.setItem(STORAGE_PROFILE_KEY + profile.email, JSON.stringify(updatedProfile));
        }
      } catch {
        // Ignorar en test
      }

      return {
        success: true,
        profile: updatedProfile,
        message: 'Perfil formativo actualizado exitosamente (Modo Mock).',
      };
    }

    // Modo API real
    const baseUrl = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
    const res = await fetch(`${baseUrl}/api/v1/profiles/me`, {
      method: 'PUT',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
      },
      body: JSON.stringify(updatedProfile),
    });

    if (!res.ok) {
      throw new Error(`Error HTTP ${res.status} al guardar perfil.`);
    }

    const data = await res.json();
    return {
      success: true,
      profile: data,
      message: 'Perfil formativo persistido en base de datos.',
    };
  }

  /**
   * Consulta los bloques horarios de disponibilidad semanal.
   */
  public async getAvailability(email: string): Promise<AvailabilitySlot[]> {
    if (!email) return [];

    if (this.mode === 'mock') {
      try {
        const stored = typeof window !== 'undefined' ? window.localStorage.getItem(STORAGE_AVAILABILITY_KEY + email) : null;
        if (stored) {
          return JSON.parse(stored) as AvailabilitySlot[];
        }
      } catch {
        // Fallback
      }

      // Slots predeterminados de prueba (Lunes y Miércoles 14:00 - 16:00)
      return [
        { dia_semana: 1, hora_inicio: '14:00', hora_fin: '15:00' },
        { dia_semana: 1, hora_inicio: '15:00', hora_fin: '16:00' },
        { dia_semana: 3, hora_inicio: '14:00', hora_fin: '15:00' },
        { dia_semana: 3, hora_inicio: '15:00', hora_fin: '16:00' },
      ];
    }

    // Modo API real
    try {
      const baseUrl = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
      const res = await fetch(`${baseUrl}/api/v1/profiles/availability?email=${encodeURIComponent(email)}`);
      if (res.ok) {
        const data = await res.json();
        return data.slots as AvailabilitySlot[];
      }
    } catch {
      // Fallback
    }

    return [];
  }

  /**
   * Guarda la matriz de disponibilidad semanal.
   */
  public async saveAvailability(
    email: string,
    slots: AvailabilitySlot[]
  ): Promise<{ success: boolean; totalSlots: number; message: string }> {
    if (!email) {
      throw new Error('El correo es requerido para registrar disponibilidad.');
    }

    if (this.mode === 'mock') {
      try {
        if (typeof window !== 'undefined') {
          window.localStorage.setItem(STORAGE_AVAILABILITY_KEY + email, JSON.stringify(slots));
        }
      } catch {
        // En entorno test
      }

      return {
        success: true,
        totalSlots: slots.length,
        message: `Disponibilidad horaria guardada (${slots.length} horas semanales registradas).`,
      };
    }

    // Modo API
    const baseUrl = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
    const res = await fetch(`${baseUrl}/api/v1/profiles/availability`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ email, slots }),
    });

    if (!res.ok) {
      throw new Error(`Error HTTP ${res.status} al guardar disponibilidad.`);
    }

    return {
      success: true,
      totalSlots: slots.length,
      message: 'Disponibilidad horaria persistida en base de datos.',
    };
  }

  private getDefaultProfile(email: string): AcademicProfile {
    return {
      email,
      codigo_estudiante: email.split('@')[0] || '',
      nombres: '',
      apellidos: '',
      ciclo_actual: 3,
      rol_postulacion: 'mentoreado',
      materias_interes: [1, 3], // Cálculo I y Algoritmos por defecto
      temas_seleccionados: [1, 2],
      biografia: 'Estudiante de la EPIS-UPT buscando asesoría académica en materias filtro.',
      modalidad_preferida: 'presencial',
    };
  }
}

export const profileService = new ProfileService();
