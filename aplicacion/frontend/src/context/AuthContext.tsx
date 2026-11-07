/**
 * Contexto Global de Autenticación, Sesión y Consentimiento Informado (Ley N° 29733 / RN-02)
 *
 * Administra el ciclo de vida del estudiante/mentor/administrador institucional:
 * - Token JWT institucional y resolución reactiva de claims.
 * - Lista de roles asignados y conmutación de rol activo (Mentoreado / Mentor / Administrador).
 * - Estado de consentimiento legal digital conforme a la Ley N° 29733 (RF02 / RN-02).
 */

import React, { createContext, useContext, useState, useEffect, useCallback, useMemo } from 'react';
import { authService, type VerifyOtpResponse } from '../services/authService';
import { consentService } from '../services/consentService';

export type UserRole = 'mentoreado' | 'mentor' | 'administrador';

export interface AuthUser {
  email: string;
  roles: UserRole[];
  codigo?: string;
  nombres?: string;
  apellidos?: string;
}

export interface AuthContextType {
  user: AuthUser | null;
  token: string | null;
  activeRole: UserRole;
  hasConsented: boolean;
  isCheckingConsent: boolean;
  login: (data: VerifyOtpResponse) => Promise<void>;
  logout: () => void;
  switchRole: (role: UserRole) => void;
  setHasConsented: (status: boolean) => void;
  refreshSession: () => Promise<void>;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

const ACTIVE_ROLE_KEY = 'p2p_active_role';

// eslint-disable-next-line react-refresh/only-export-components
export function parseJwt(token: string): { sub?: string; email?: string; roles?: string[]; role?: string } | null {
  try {
    const parts = token.split('.');
    if (parts.length !== 3) return null;
    let base64 = parts[1].replace(/-/g, '+').replace(/_/g, '/');
    while (base64.length % 4 !== 0) {
      base64 += '=';
    }
    const jsonStr = atob(base64);
    return JSON.parse(jsonStr);
  } catch {
    return null;
  }
}

// Inicialización o reconstrucción del usuario a partir del token JWT
// eslint-disable-next-line react-refresh/only-export-components
export function initUserFromToken(jwtToken: string | null): AuthUser | null {
  if (!jwtToken) return null;
  const payload = parseJwt(jwtToken);
  if (!payload) return null;

  const email = (payload.sub || payload.email || '').trim().toLowerCase();
  if (!email || !email.includes('@')) return null;

  const rawRoles: string[] =
    Array.isArray(payload.roles) && payload.roles.length > 0
      ? payload.roles
      : payload.role
      ? [payload.role]
      : email.startsWith('admin')
      ? ['administrador', 'mentoreado']
      : ['mentoreado'];

  const roles: UserRole[] = rawRoles.map((r) => r.toLowerCase() as UserRole);
  if (!roles.includes('mentoreado')) {
    roles.push('mentoreado');
  }

  const codigo = email.split('@')[0];
  return {
    email,
    roles,
    codigo,
  };
}

function resolveInitialRole(user: AuthUser | null): UserRole {
  if (!user) return 'mentoreado';
  const savedRole = (typeof window !== 'undefined' ? sessionStorage.getItem(ACTIVE_ROLE_KEY) : null) as UserRole | null;
  if (savedRole && user.roles.includes(savedRole)) {
    return savedRole;
  }
  if (user.roles.includes('administrador')) {
    return 'administrador';
  }
  if (user.roles.includes('mentor')) {
    return 'mentor';
  }
  return 'mentoreado';
}

export const AuthProvider: React.FC<{ children: React.ReactNode }> = ({ children }) => {
  const initialToken = authService.getToken();
  const initialUser = initUserFromToken(initialToken);
  const [token, setToken] = useState<string | null>(initialToken);
  const [user, setUser] = useState<AuthUser | null>(initialUser);
  const [activeRole, setActiveRole] = useState<UserRole>(() => resolveInitialRole(initialUser));
  const [hasConsented, setHasConsentedState] = useState<boolean>(true);
  const [isCheckingConsent, setIsCheckingConsent] = useState<boolean>(false);

  // Verificar consentimiento digital en base de datos (RN-02 / Ley 29733)
  const verifyConsent = useCallback(async (email: string) => {
    setIsCheckingConsent(true);
    try {
      const status = await consentService.getConsentStatus(email);
      setHasConsentedState(status.hasConsented);
    } catch {
      // En caso de fallo de red, se mantiene el estado seguro
      setHasConsentedState(false);
    } finally {
      setIsCheckingConsent(false);
    }
  }, []);

  // Sincronizar estado al cambiar el token
  useEffect(() => {
    const currentUser = initUserFromToken(token);
    setUser(currentUser);

    if (currentUser) {
      // Resolver rol activo
      const savedRole = (typeof window !== 'undefined' ? sessionStorage.getItem(ACTIVE_ROLE_KEY) : null) as UserRole | null;
      if (savedRole && currentUser.roles.includes(savedRole)) {
        setActiveRole(savedRole);
      } else if (currentUser.roles.includes('administrador')) {
        setActiveRole('administrador');
      } else if (currentUser.roles.includes('mentor')) {
        setActiveRole('mentor');
      } else {
        setActiveRole('mentoreado');
      }

      verifyConsent(currentUser.email);
    } else {
      setActiveRole('mentoreado');
      setHasConsentedState(true);
    }
  }, [token, verifyConsent]);

  const login = useCallback(
    async (data: VerifyOtpResponse) => {
      if (data.token) {
        authService.saveToken(data.token);
        setToken(data.token);
      } else {
        // En modo mock sin token, emitir token simulado con claims estándar
        const mockPayload = {
          sub: data.email,
          email: data.email,
          roles: data.email.startsWith('admin')
            ? ['administrador', 'mentoreado']
            : data.email.startsWith('2022073504') || data.email.startsWith('mentor.')
            ? ['mentor', 'mentoreado']
            : ['mentoreado'],
          role: data.email.startsWith('admin') ? 'administrador' : 'estudiante',
        };
        const mockJwt = `mock.${btoa(JSON.stringify(mockPayload))}.sig`;
        authService.saveToken(mockJwt);
        setToken(mockJwt);
      }
    },
    []
  );

  const logout = useCallback(() => {
    authService.clearToken();
    if (typeof window !== 'undefined') {
      sessionStorage.removeItem(ACTIVE_ROLE_KEY);
    }
    setToken(null);
    setUser(null);
    setActiveRole('mentoreado');
    setHasConsentedState(true);
  }, []);

  const switchRole = useCallback(
    (newRole: UserRole) => {
      if (user && user.roles.includes(newRole)) {
        setActiveRole(newRole);
        if (typeof window !== 'undefined') {
          sessionStorage.setItem(ACTIVE_ROLE_KEY, newRole);
        }
      }
    },
    [user]
  );

  const setHasConsented = useCallback((status: boolean) => {
    setHasConsentedState(status);
  }, []);

  const refreshSession = useCallback(async () => {
    const currentToken = authService.getToken();
    setToken(currentToken);
    if (user) {
      await verifyConsent(user.email);
    }
  }, [user, verifyConsent]);

  const value = useMemo(
    () => ({
      user,
      token,
      activeRole,
      hasConsented,
      isCheckingConsent,
      login,
      logout,
      switchRole,
      setHasConsented,
      refreshSession,
    }),
    [user, token, activeRole, hasConsented, isCheckingConsent, login, logout, switchRole, setHasConsented, refreshSession]
  );

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
};

// eslint-disable-next-line react-refresh/only-export-components
export const useAuth = (): AuthContextType => {
  const context = useContext(AuthContext);
  if (!context) {
    throw new Error('useAuth debe ser utilizado dentro de un AuthProvider');
  }
  return context;
};
