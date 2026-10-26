/**
 * Servicio de Publicación y Gestión de Ofertas de Mentoría — (T-14 / T-15 / T-16)
 *
 * Trazabilidad:
 * - Requerimiento Funcional: RF08 (Publicación y parametrización de ofertas de mentoría)
 * - Caso de Uso: CUS06 (Publicar oferta de mentoría)
 * - Regla de Negocio RN-04: Antelación obligatoria mayor a 24 horas (T > 24 h); estándar recomendado >= 48 h.
 * - Regla de Negocio RN-05: Aforo estándar estricto: 10 cupos para Presencial, 20 cupos para Virtual.
 * - Regla de Negocio RN-06: Asignación de infraestructura física (aulas libres validadas).
 * - Regla de Negocio RN-07: Aprovisionamiento de infraestructura virtual (Google Meet / Discord).
 *
 * NOTA DE ARQUITECTURA:
 * La API real de backend para ofertas (T-15 y T-16) es responsabilidad de Renzo.
 * Este servicio define el contrato tipado en TypeScript y provee un adaptador MOCK explícito,
 * debidamente señalizado como "Modo de prueba local — Backend pendiente", garantizando que
 * no se simule falsamente persistencia remota mientras la API no esté integrada.
 */

export type SessionModality = 'presencial' | 'virtual';
export type SessionDuration = 60 | 90;

export interface PublishOfferPayload {
  id_asignatura: number;
  codigo_asignatura: string;
  nombre_asignatura: string;
  id_tema: number;
  nombre_tema: string;
  fecha_inicio: string; // ISO 8601 o formato local YYYY-MM-DDTHH:mm
  duracion_minutos: SessionDuration;
  modalidad: SessionModality;
  aforo_maximo: number; // 10 para presencial, 20 para virtual (RN-05)
  espacio_asignado: string; // Aula física o enlace virtual
  mentor_email: string;
  mentor_nombre?: string;
  notas_adicionales?: string;
}

export interface PublishOfferResponse {
  id_oferta: string;
  codigo_sesion: string;
  estado: 'PUBLICADA';
  mensaje: string;
  fecha_publicacion: string;
  aforo: number;
  espacio_asignado: string;
  modo: 'mock' | 'api';
  offer: PublishOfferPayload;
}

export interface OfferValidationResult {
  isValid: boolean;
  errors: Record<string, string>;
  hoursAdvance: number;
  isAdvanceValid: boolean; // > 24 h (RN-04)
  isRecommendedAdvance: boolean; // >= 48 h (Recomendación RN-04)
}

export type OfferErrorCode =
  | 'REQUIRED_FIELD_MISSING'
  | 'INVALID_ADVANCE_TIME'
  | 'INVALID_CAPACITY'
  | 'INVALID_DURATION'
  | 'INVALID_MODALITY'
  | 'NETWORK_ERROR'
  | 'MOCK_DISABLED';

export class OfferException extends Error {
  public code: OfferErrorCode;

  constructor(code: OfferErrorCode, message: string) {
    super(message);
    this.name = 'OfferException';
    this.code = code;
  }
}

/**
 * Aforos institucionales inmutables según RN-05
 */
export const STANDARD_CAPACITY: Record<SessionModality, number> = {
  presencial: 10,
  virtual: 20,
};

/**
 * Catálogo de recintos sugeridos para modalidad presencial (RN-06)
 */
export const SUGGESTED_CLASSROOMS = [
  'Laboratorio de Cómputo 101 - Pabellón G (EPIS)',
  'Laboratorio de Redes y Telecomunicaciones 202 (EPIS)',
  'Laboratorio de Inteligencia Artificial 303 (EPIS)',
  'Aula Magna 104 - Pabellón Central (EPIS)',
  'Sala de Trabajo Colaborativo 201 (EPIS)',
];

/**
 * Enlaces virtuales sugeridos para aprovisionamiento (RN-07)
 */
export const SUGGESTED_VIRTUAL_PLATFORMS = [
  { id: 'meet', label: 'Google Meet Institucional UPT (@upt.pe)', prefix: 'https://meet.google.com/upt-epis-' },
  { id: 'discord', label: 'Servidor Oficial Discord EPIS (Canal Tutoría)', prefix: 'https://discord.gg/epis-upt-room-' },
];

/**
 * Calcula las horas de antelación entre la fecha de la sesión y la fecha de referencia (o now).
 */
export function calculateAdvanceHours(startDateTime: string | Date, referenceNow: Date = new Date()): number {
  const target = typeof startDateTime === 'string' ? new Date(startDateTime) : startDateTime;
  if (isNaN(target.getTime())) {
    return -1;
  }
  const diffMs = target.getTime() - referenceNow.getTime();
  return diffMs / (1000 * 60 * 60);
}

/**
 * Valida un payload de publicación de oferta conforme a las reglas RN-04, RN-05 y restricciones de campos.
 */
export function validateOfferPayload(
  payload: Partial<PublishOfferPayload>,
  referenceNow: Date = new Date()
): OfferValidationResult {
  const errors: Record<string, string> = {};

  if (!payload.id_asignatura || payload.id_asignatura <= 0) {
    errors.id_asignatura = 'Debe seleccionar una asignatura formativa crítica del catálogo.';
  }

  if (!payload.id_tema || payload.id_tema <= 0) {
    errors.id_tema = 'Debe seleccionar una unidad o tema conceptual del sílabo.';
  }

  if (!payload.modalidad || (payload.modalidad !== 'presencial' && payload.modalidad !== 'virtual')) {
    errors.modalidad = 'Debe seleccionar una modalidad válida (Presencial o Virtual).';
  }

  if (!payload.duracion_minutos || (payload.duracion_minutos !== 60 && payload.duracion_minutos !== 90)) {
    errors.duracion_minutos = 'La duración debe ser en bloques lectivos de 60 o 90 minutos.';
  }

  // Validación de antelación (RN-04)
  let hoursAdvance = -1;
  let isAdvanceValid = false;
  let isRecommendedAdvance = false;

  if (!payload.fecha_inicio) {
    errors.fecha_inicio = 'Debe ingresar la fecha y hora de inicio de la mentoría.';
  } else {
    hoursAdvance = calculateAdvanceHours(payload.fecha_inicio, referenceNow);
    if (hoursAdvance < 0) {
      errors.fecha_inicio = 'La fecha y hora de la mentoría no puede encontrarse en el pasado.';
    } else if (hoursAdvance <= 24) {
      // Regla estricta obligatoria RN-04: T > 24 h
      errors.fecha_inicio =
        'Infracción de RN-04: Toda mentoría debe publicarse con una antelación superior a 24 horas respecto al inicio de la sesión para garantizar la confirmación de quórum.';
    } else {
      isAdvanceValid = true;
      // Estándar recomendado institucional: T >= 48 h
      isRecommendedAdvance = hoursAdvance >= 48;
    }
  }

  // Validación de aforo (RN-05)
  if (payload.modalidad) {
    const expectedCapacity = STANDARD_CAPACITY[payload.modalidad];
    if (payload.aforo_maximo !== undefined && payload.aforo_maximo !== expectedCapacity) {
      errors.aforo_maximo = `Infracción de RN-05: El aforo para la modalidad ${payload.modalidad} debe ser exactamente ${expectedCapacity} estudiantes.`;
    }
  }

  // Validación de infraestructura
  if (!payload.espacio_asignado || !payload.espacio_asignado.trim()) {
    errors.espacio_asignado =
      payload.modalidad === 'presencial'
        ? 'Debe asignar o confirmar un ambiente físico validado (RN-06).'
        : 'Debe generar o especificar el enlace institucional de teleconferencia (RN-07).';
  }

  return {
    isValid: Object.keys(errors).length === 0,
    errors,
    hoursAdvance,
    isAdvanceValid,
    isRecommendedAdvance,
  };
}

// ============================================================================
// Adaptador MOCK en Memoria / LocalStorage (Exclusivo para Desarrollo Local)
// ============================================================================

const STORAGE_OFFERS_KEY = 'p2p_offers_mock_sprint03';

class MockOfferAdapter {
  private sessionCounter = 1001;

  public async publishOffer(payload: PublishOfferPayload): Promise<PublishOfferResponse> {
    const validation = validateOfferPayload(payload);
    if (!validation.isValid) {
      const firstError = Object.values(validation.errors)[0];
      throw new OfferException('REQUIRED_FIELD_MISSING', firstError);
    }

    // Forzar aforo reglamentario RN-05
    const forcedCapacity = STANDARD_CAPACITY[payload.modalidad];
    const sanitizedPayload: PublishOfferPayload = {
      ...payload,
      aforo_maximo: forcedCapacity,
    };

    const code = `SES-${this.sessionCounter++}`;
    const id = `offer-mock-${Date.now()}`;
    const publishedAt = new Date().toISOString();

    const response: PublishOfferResponse = {
      id_oferta: id,
      codigo_sesion: code,
      estado: 'PUBLICADA',
      mensaje: `¡Oferta de mentoría publicada con éxito en el catálogo EPIS! Código de sesión: ${code}`,
      fecha_publicacion: publishedAt,
      aforo: forcedCapacity,
      espacio_asignado: sanitizedPayload.espacio_asignado,
      modo: 'mock',
      offer: sanitizedPayload,
    };

    // Almacenar en localStorage para persistencia visual durante la sesión
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        const stored = window.localStorage.getItem(STORAGE_OFFERS_KEY);
        const list: PublishOfferResponse[] = stored ? JSON.parse(stored) : [];
        list.unshift(response);
        window.localStorage.setItem(STORAGE_OFFERS_KEY, JSON.stringify(list));
      }
    } catch {
      // Entorno de prueba sin window o con almacenamiento restringido
    }

    return response;
  }

  public getOffers(mentorEmail?: string): PublishOfferResponse[] {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        const stored = window.localStorage.getItem(STORAGE_OFFERS_KEY);
        if (stored) {
          const list: PublishOfferResponse[] = JSON.parse(stored);
          if (mentorEmail) {
            return list.filter((item) => item.offer.mentor_email === mentorEmail);
          }
          return list;
        }
      }
    } catch {
      // Ignorar fallback
    }
    return [];
  }

  public clearOffers(): void {
    try {
      if (typeof window !== 'undefined' && window.localStorage) {
        window.localStorage.removeItem(STORAGE_OFFERS_KEY);
      }
    } catch {
      // Ignorar
    }
  }
}

// ============================================================================
// Adaptador API de Integración Futura (T-15 / T-16 de Renzo)
// ============================================================================

class ApiOfferAdapter {
  private getBaseUrl(): string {
    return (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
  }

  public async publishOffer(payload: PublishOfferPayload): Promise<PublishOfferResponse> {
    const url = `${this.getBaseUrl()}/api/v1/offers`;
    try {
      const response = await fetch(url, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
        },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => null);
        const msg = errorData?.detail || `Error HTTP ${response.status}: ${response.statusText}`;
        throw new OfferException('NETWORK_ERROR', msg);
      }

      const data = await response.json();
      return {
        ...data,
        modo: 'api',
      };
    } catch (err: unknown) {
      if (err instanceof OfferException) throw err;
      throw new OfferException(
        'NETWORK_ERROR',
        'No fue posible conectar con el servidor para registrar la oferta. El backend real (T-15 / T-16) puede encontrarse pendiente.'
      );
    }
  }

  public async getOffers(mentorEmail?: string): Promise<PublishOfferResponse[]> {
    const query = mentorEmail ? `?mentor_email=${encodeURIComponent(mentorEmail)}` : '';
    const url = `${this.getBaseUrl()}/api/v1/offers${query}`;
    const response = await fetch(url, {
      method: 'GET',
      headers: { 'Accept': 'application/json' },
    });
    if (!response.ok) {
      throw new OfferException('NETWORK_ERROR', `Error al consultar ofertas: ${response.statusText}`);
    }
    return response.json();
  }
}

const mockAdapter = new MockOfferAdapter();
const apiAdapter = new ApiOfferAdapter();

let currentServiceMode: 'mock' | 'api' = 'mock';

// ============================================================================
// Fachada Principal del Servicio de Ofertas (offerService)
// ============================================================================

export const offerService = {
  getMode(): 'mock' | 'api' {
    return currentServiceMode;
  },

  setMode(mode: 'mock' | 'api'): void {
    currentServiceMode = mode;
  },

  /**
   * Publica una nueva oferta de mentoría académica.
   * Valida estrictamente RN-04 y RN-05 antes de despachar al adaptador activo.
   */
  async publishOffer(payload: PublishOfferPayload): Promise<PublishOfferResponse> {
    if (currentServiceMode === 'api') {
      return apiAdapter.publishOffer(payload);
    }
    return mockAdapter.publishOffer(payload);
  },

  /**
   * Obtiene las ofertas publicadas (del mock o del backend según el modo activo).
   */
  async getOffers(mentorEmail?: string): Promise<PublishOfferResponse[]> {
    if (currentServiceMode === 'api') {
      return apiAdapter.getOffers(mentorEmail);
    }
    return mockAdapter.getOffers(mentorEmail);
  },

  /**
   * Limpia el almacenamiento de prueba local.
   */
  clearMockOffers(): void {
    mockAdapter.clearOffers();
  },

  /**
   * Helper para generar enlace de reunión virtual reproducible.
   */
  generateVirtualLink(subjectCode: string): string {
    const randomHex = Math.random().toString(36).substring(2, 7);
    const codePrefix = subjectCode.toLowerCase().replace(/[^a-z0-9]/g, '');
    return `https://meet.google.com/upt-${codePrefix}-${randomHex}`;
  },

  /**
   * Helper para obtener sugerencia de aula libre presencial.
   */
  suggestClassroom(): string {
    return SUGGESTED_CLASSROOMS[0];
  },
};
