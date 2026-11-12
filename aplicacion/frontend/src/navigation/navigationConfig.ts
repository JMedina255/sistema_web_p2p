/**
 * Configuración Centralizada de Navegación y Perfiles RBAC
 * Sistema Web P2P de Mentorías Académicas — EPIS UPT
 */

import { type UserRole } from '../context/AuthContext';

export type NavTab =
  | 'auth'
  | 'consent'
  | 'curriculum'
  | 'profile'
  | 'offers'
  | 'recommendations'
  | 'bookings'
  | 'sessions'
  | 'certificates'
  | 'admin'
  | 'services';

export interface NavigationItem {
  tab: NavTab;
  label: string;
  icon: string;
  shortLabel?: string;
  allowedRoles: (UserRole | 'visitor')[];
  requiresAuth: boolean;
  description: string;
}

/**
 * Matriz canónica de pestañas y permisos asociados
 */
export const NAVIGATION_ITEMS: Record<NavTab, NavigationItem> = {
  auth: {
    tab: 'auth',
    label: 'Iniciar sesión',
    icon: '🔐',
    allowedRoles: ['visitor'],
    requiresAuth: false,
    description: 'Acceso institucional mediante correo @upt.pe y código OTP.',
  },
  consent: {
    tab: 'consent',
    label: 'Consentimiento',
    icon: '⚖️',
    allowedRoles: ['mentoreado', 'mentor', 'administrador'],
    requiresAuth: true,
    description: 'Consentimiento informado de tratamiento de datos personales (Ley N.º 29733).',
  },
  curriculum: {
    tab: 'curriculum',
    label: 'Cursos',
    icon: '📚',
    allowedRoles: ['visitor', 'mentoreado', 'mentor', 'administrador'],
    requiresAuth: false,
    description: 'Catálogo de asignaturas formativas y contenidos silábicos oficiales.',
  },
  recommendations: {
    tab: 'recommendations',
    label: 'Explorar mentorías',
    icon: '🎯',
    allowedRoles: ['mentoreado'],
    requiresAuth: true,
    description: 'Cartelera de mentorías recomendadas según afinidad curricular y horarios.',
  },
  bookings: {
    tab: 'bookings',
    label: 'Mis reservas',
    icon: '📅',
    allowedRoles: ['mentoreado'],
    requiresAuth: true,
    description: 'Bandeja personal de reservas de mentoría, confirmación de asistencia y desistimiento.',
  },
  profile: {
    tab: 'profile',
    label: 'Mi perfil',
    icon: '👤',
    allowedRoles: ['mentoreado', 'mentor'],
    requiresAuth: true,
    description: 'Ficha académica del estudiante y disponibilidad horaria semanal.',
  },
  sessions: {
    tab: 'sessions',
    label: 'Mis sesiones',
    icon: '📋',
    allowedRoles: ['mentor'],
    requiresAuth: true,
    description: 'Supervisión de sesiones programadas, aforos, quórum y pase de asistencia.',
  },
  offers: {
    tab: 'offers',
    label: 'Publicar mentoría',
    icon: '🏷️',
    allowedRoles: ['mentor'],
    requiresAuth: true,
    description: 'Convocatoria y programación de nuevas sesiones de mentoría académica.',
  },
  certificates: {
    tab: 'certificates',
    label: 'Mis constancias',
    icon: '📜',
    allowedRoles: ['mentor'],
    requiresAuth: true,
    description: 'Acreditación de horas de mentoría y descarga de constancias oficiales DEMO.',
  },
  admin: {
    tab: 'admin',
    label: 'Administración',
    icon: '🛡️',
    allowedRoles: ['administrador'],
    requiresAuth: true,
    description: 'Gestión institucional de roles, verificación de mérito y supervisión de quórum.',
  },
  services: {
    tab: 'services',
    label: 'Estado del sistema',
    icon: '🛰️',
    allowedRoles: ['administrador'],
    requiresAuth: true,
    description: 'Monitor de telemetría, conectividad con base de datos y latencias.',
  },
};

/**
 * Pestaña inicial por defecto según el rol activo o estado de visitante
 */
export const ROLE_DEFAULT_TAB: Record<UserRole, NavTab> = {
  mentoreado: 'recommendations',
  mentor: 'sessions',
  administrador: 'admin',
};

export const VISITOR_DEFAULT_TAB: NavTab = 'auth';

/**
 * Retorna la lista ordenada de elementos de navegación visibles en el menú según el rol activo
 */
export function getNavigationItemsForRole(role: UserRole | null): NavigationItem[] {
  if (!role) {
    // Visitante no autenticado: solo Login y Catálogo de Cursos
    return [NAVIGATION_ITEMS.auth, NAVIGATION_ITEMS.curriculum];
  }

  switch (role) {
    case 'mentoreado':
      return [
        NAVIGATION_ITEMS.recommendations,
        NAVIGATION_ITEMS.bookings,
        NAVIGATION_ITEMS.curriculum,
        NAVIGATION_ITEMS.profile,
      ];
    case 'mentor':
      return [
        NAVIGATION_ITEMS.sessions,
        NAVIGATION_ITEMS.offers,
        NAVIGATION_ITEMS.certificates,
        NAVIGATION_ITEMS.curriculum,
        NAVIGATION_ITEMS.profile,
      ];
    case 'administrador':
      return [
        NAVIGATION_ITEMS.admin,
        NAVIGATION_ITEMS.curriculum,
        NAVIGATION_ITEMS.services,
      ];
    default:
      return [NAVIGATION_ITEMS.auth, NAVIGATION_ITEMS.curriculum];
  }
}
