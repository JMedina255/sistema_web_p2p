/**
 * Componente Guard de Protección de Vistas por Rol (RBAC)
 * Sistema Web P2P de Mentorías Académicas — EPIS UPT
 *
 * Impide el montaje y renderizado de componentes privados cuando el usuario no cuenta
 * con autenticación institucional o no posee el rol autorizado correspondiente.
 * Evita la fuga de datos y llamadas no autorizadas a endpoints backend.
 */

import React from 'react';
import { type UserRole } from '../../context/AuthContext';
import { type NavTab, NAVIGATION_ITEMS } from '../../navigation/navigationConfig';
import { canAccessTab, isTabProtected } from '../../navigation/navigationPermissions';

export interface ProtectedViewProps {
  tab: NavTab;
  activeRole: UserRole | null;
  isAuthenticated: boolean;
  userEmail?: string | null;
  hasConsented?: boolean;
  onNavigateToAuth: () => void;
  onNavigateToDefault: () => void;
  onSwitchRole?: (role: UserRole) => void;
  availableRoles?: UserRole[];
  children: React.ReactNode;
}

export const ProtectedView: React.FC<ProtectedViewProps> = ({
  tab,
  activeRole,
  isAuthenticated,
  userEmail,
  onNavigateToAuth,
  onNavigateToDefault,
  onSwitchRole,
  availableRoles = [],
  children,
}) => {
  const item = NAVIGATION_ITEMS[tab];
  const tabLabel = item?.label ?? tab;

  // 1. Pestañas públicas que no requieren autenticación (ej. Catálogo de Cursos)
  if (!isTabProtected(tab)) {
    return <>{children}</>;
  }

  // 2. Pestaña de autenticación: accesible para visitantes, o informativa si ya está autenticado
  if (tab === 'auth') {
    if (!isAuthenticated) {
      return <>{children}</>;
    }
    return (
      <div
        role="region"
        aria-label="Sesión Activa"
        style={{
          maxWidth: '560px',
          margin: '2rem auto',
          padding: '2rem',
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #E2E8F0',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
          textAlign: 'center',
        }}
      >
        <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>✅</div>
        <h3 style={{ color: '#1C2A59', fontSize: '1.25rem', fontWeight: 700, margin: '0 0 0.5rem 0' }}>
          Sesión Institucional Activa
        </h3>
        <p style={{ color: '#64748B', fontSize: '0.9rem', marginBottom: '1.5rem', lineHeight: 1.5 }}>
          Ya has iniciado sesión con la cuenta <strong>{userEmail}</strong>. Tu perfil activo actual es{' '}
          <strong style={{ textTransform: 'capitalize' }}>{activeRole}</strong>.
        </p>
        <button
          type="button"
          onClick={onNavigateToDefault}
          style={{
            backgroundColor: '#1C2A59',
            color: '#FFFFFF',
            border: 'none',
            borderRadius: '6px',
            padding: '0.65rem 1.25rem',
            fontSize: '0.88rem',
            fontWeight: 600,
            cursor: 'pointer',
          }}
        >
          Ir a mi panel principal
        </button>
      </div>
    );
  }

  // 3. Caso: Usuario NO autenticado intentando acceder a una vista privada
  if (!isAuthenticated) {
    return (
      <div
        role="region"
        aria-label="Acceso Restringido"
        style={{
          maxWidth: '580px',
          margin: '2rem auto',
          padding: '2.5rem 2rem',
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #E2E8F0',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
          textAlign: 'center',
        }}
      >
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🔒</div>
        <h2
          style={{
            color: '#1C2A59',
            fontSize: '1.35rem',
            fontWeight: 700,
            margin: '0 0 0.75rem 0',
          }}
        >
          Acceso Restringido a {tabLabel}
        </h2>
        <p
          style={{
            color: '#64748B',
            fontSize: '0.92rem',
            lineHeight: 1.6,
            maxWidth: '480px',
            margin: '0 auto 1.75rem auto',
          }}
        >
          Para consultar este módulo institucional, debes iniciar sesión con tu cuenta institucional de la{' '}
          <strong>Universidad Privada de Tacna (@upt.pe)</strong>.
        </p>
        <button
          type="button"
          onClick={onNavigateToAuth}
          style={{
            backgroundColor: '#1C2A59',
            color: '#FFFFFF',
            border: 'none',
            borderRadius: '8px',
            padding: '0.75rem 1.5rem',
            fontSize: '0.9rem',
            fontWeight: 600,
            cursor: 'pointer',
            transition: 'background-color 0.2s',
          }}
        >
          Iniciar Sesión Institucional
        </button>
      </div>
    );
  }

  // 4. Caso: Usuario autenticado pero NO autorizado para este rol activo
  const hasAccess = canAccessTab(tab, activeRole, true);
  if (!hasAccess) {
    // Verificar si el usuario cuenta con algún otro rol asignado que sí tenga acceso
    const eligibleRole = availableRoles.find((r) => item?.allowedRoles.includes(r));

    return (
      <div
        role="alert"
        aria-label="Acceso No Autorizado"
        style={{
          maxWidth: '600px',
          margin: '2rem auto',
          padding: '2.5rem 2rem',
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #FED7AA',
          boxShadow: '0 4px 6px -1px rgba(0, 0, 0, 0.05)',
          textAlign: 'center',
        }}
      >
        <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>🛡️</div>
        <h2
          style={{
            color: '#9A3412',
            fontSize: '1.35rem',
            fontWeight: 700,
            margin: '0 0 0.75rem 0',
          }}
        >
          Acceso No Autorizado
        </h2>
        <p
          style={{
            color: '#475569',
            fontSize: '0.92rem',
            lineHeight: 1.6,
            maxWidth: '500px',
            margin: '0 auto 1.5rem auto',
          }}
        >
          Tu perfil activo actual (
          <strong style={{ textTransform: 'capitalize' }}>{activeRole ?? 'Sin rol'}</strong>
          ) no cuenta con permisos para acceder a la sección <strong>{tabLabel}</strong>.
        </p>

        {eligibleRole && onSwitchRole && (
          <div
            style={{
              backgroundColor: '#FFF7ED',
              border: '1px dashed #FDBA74',
              borderRadius: '8px',
              padding: '1rem',
              marginBottom: '1.5rem',
            }}
          >
            <p style={{ margin: '0 0 0.75rem 0', fontSize: '0.85rem', color: '#9A3412' }}>
              Tu cuenta tiene asignado el perfil de{' '}
              <strong style={{ textTransform: 'capitalize' }}>{eligibleRole}</strong>, el cual dispone de acceso a este módulo.
            </p>
            <button
              type="button"
              onClick={() => onSwitchRole(eligibleRole)}
              style={{
                backgroundColor: '#B99451',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '6px',
                padding: '0.55rem 1.1rem',
                fontSize: '0.85rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Cambiar a perfil {eligibleRole}
            </button>
          </div>
        )}

        <div>
          <button
            type="button"
            onClick={onNavigateToDefault}
            style={{
              backgroundColor: '#1C2A59',
              color: '#FFFFFF',
              border: 'none',
              borderRadius: '8px',
              padding: '0.7rem 1.4rem',
              fontSize: '0.88rem',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Volver a mi panel principal
          </button>
        </div>
      </div>
    );
  }

  // 5. Usuario autenticado y con permisos válidos: renderizar la vista protegida
  return <>{children}</>;
};
