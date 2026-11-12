/**
 * Políticas y Verificación de Permisos de Navegación RBAC
 * Sistema Web P2P de Mentorías Académicas — EPIS UPT
 */

import { type UserRole } from '../context/AuthContext';
import {
  type NavTab,
  NAVIGATION_ITEMS,
  ROLE_DEFAULT_TAB,
  VISITOR_DEFAULT_TAB,
} from './navigationConfig';

/**
 * Determina si una pestaña requiere autenticación institucional
 */
export function isTabProtected(tab: NavTab): boolean {
  return NAVIGATION_ITEMS[tab]?.requiresAuth ?? true;
}

/**
 * Valida si un usuario (con un rol activo dado y estado de autenticación) tiene permiso para acceder a una pestaña
 */
export function canAccessTab(
  tab: NavTab,
  activeRole: UserRole | null,
  isAuthenticated: boolean
): boolean {
  const item = NAVIGATION_ITEMS[tab];
  if (!item) return false;

  // Caso 1: Pestaña de autenticación
  if (tab === 'auth') {
    // Solo disponible si el usuario no tiene sesión iniciada
    return !isAuthenticated;
  }

  // Caso 2: Pestaña pública (Cursos)
  if (!item.requiresAuth) {
    return true;
  }

  // Caso 3: Pestañas protegidas que requieren autenticación
  if (!isAuthenticated || !activeRole) {
    return false;
  }

  // Comprobar si el rol activo tiene autorización explícita para la pestaña
  return item.allowedRoles.includes(activeRole);
}

/**
 * Retorna la pestaña por defecto recomendada según el estado del usuario
 */
export function getDefaultTabForRole(role: UserRole | null): NavTab {
  if (!role) {
    return VISITOR_DEFAULT_TAB;
  }
  return ROLE_DEFAULT_TAB[role] ?? VISITOR_DEFAULT_TAB;
}

/**
 * Determina si una cadena corresponde a un identificador canónico de pestaña
 */
export function isValidTab(tab: unknown): tab is NavTab {
  const validTabs: NavTab[] = [
    'auth',
    'consent',
    'curriculum',
    'profile',
    'offers',
    'recommendations',
    'bookings',
    'sessions',
    'certificates',
    'admin',
    'services',
  ];
  return typeof tab === 'string' && validTabs.includes(tab as NavTab);
}

/**
 * Sanitiza y valida un parámetro de pestaña recibido por URL o navegación directa
 * Si la pestaña no es válida, redirige a la vista por defecto correspondiente al rol.
 * Si strictAuthorization es true, también verifica que el rol tenga acceso autorizado.
 */
export function sanitizeRequestedTab(
  requestedTab: string | null,
  activeRole: UserRole | null = null,
  isAuthenticated: boolean = false,
  strictAuthorization: boolean = false
): NavTab {
  if (!requestedTab || !isValidTab(requestedTab)) {
    return getDefaultTabForRole(isAuthenticated ? activeRole : null);
  }

  if (strictAuthorization && !canAccessTab(requestedTab, activeRole, isAuthenticated)) {
    return getDefaultTabForRole(isAuthenticated ? activeRole : null);
  }

  return requestedTab;
}
