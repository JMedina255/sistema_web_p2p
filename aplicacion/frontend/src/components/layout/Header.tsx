/**
 * Encabezado Institucional del Sistema Web P2P (UPT)
 * Muestra identidad corporativa, sesión del usuario, selector de roles y estado de consentimiento.
 */

import React from 'react';
import { type AuthUser, type UserRole } from '../../context/AuthContext';

export interface HeaderProps {
  user: AuthUser | null;
  token: string | null;
  activeRole: UserRole;
  hasConsented: boolean;
  onRoleSwitch: (role: UserRole) => void;
  onLogout: () => void;
  onLoginClick?: () => void;
}

export const Header: React.FC<HeaderProps> = ({
  user,
  token,
  activeRole,
  hasConsented,
  onRoleSwitch,
  onLogout,
  onLoginClick,
}) => {
  return (
    <header
      style={{
        backgroundColor: '#1C2A59',
        color: '#FFFFFF',
        padding: '0.9rem 2rem',
        boxShadow: '0 2px 8px rgba(0, 0, 0, 0.15)',
        borderBottom: '3px solid #B99451',
      }}
    >
      <div
        style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem',
        }}
      >
        {/* Logotipo e Identidad Institucional */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem' }}>
          <div
            style={{
              background: '#B99451',
              color: '#FFFFFF',
              fontWeight: 900,
              fontSize: '1rem',
              padding: '0.35rem 0.65rem',
              borderRadius: '6px',
              letterSpacing: '0.05em',
            }}
          >
            UPT
          </div>
          <div>
            <h1 style={{ margin: 0, fontSize: '1.15rem', fontWeight: 700, letterSpacing: '-0.01em' }}>
              SISTEMA WEB P2P DE MENTORÍAS ACADÉMICAS
            </h1>
            <p style={{ margin: 0, fontSize: '0.75rem', opacity: 0.85 }}>
              Escuela Profesional de Ingeniería de Sistemas • Facultad de Ingeniería
            </p>
          </div>
        </div>

        {/* Bloque de Sesión y Conmutación de Rol Reactivo */}
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.85rem', flexWrap: 'wrap', fontSize: '0.8rem' }}>
          {token && user ? (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
                background: 'rgba(255, 255, 255, 0.1)',
                padding: '0.35rem 0.85rem',
                borderRadius: '8px',
                border: '1px solid rgba(255, 255, 255, 0.2)',
              }}
            >
              <div>
                <span style={{ opacity: 0.8, fontSize: '0.72rem', display: 'block' }}>Usuario Institucional:</span>
                <span style={{ color: '#F8FAFC', fontSize: '0.82rem', fontWeight: 600 }}>
                  Sesión: {user.email}
                </span>
              </div>

              {/* Conmutador de Roles Disponibles */}
              {user.roles && user.roles.length > 1 ? (
                <div style={{ display: 'flex', alignItems: 'center', gap: '0.35rem', marginLeft: '0.5rem' }}>
                  <span style={{ fontSize: '0.72rem', opacity: 0.8 }}>Rol:</span>
                  {user.roles.map((r) => (
                    <button
                      key={r}
                      type="button"
                      onClick={() => onRoleSwitch(r)}
                      aria-pressed={activeRole === r}
                      data-testid={`role-switch-${r}`}
                      style={{
                        border: 'none',
                        borderRadius: '4px',
                        padding: '0.2rem 0.5rem',
                        fontSize: '0.72rem',
                        fontWeight: 700,
                        cursor: 'pointer',
                        textTransform: 'uppercase',
                        backgroundColor: activeRole === r ? '#B99451' : 'rgba(255, 255, 255, 0.2)',
                        color: '#FFFFFF',
                        transition: 'all 0.2s',
                      }}
                    >
                      {r}
                    </button>
                  ))}
                </div>
              ) : (
                <span
                  style={{
                    background: '#B99451',
                    color: '#FFFFFF',
                    fontSize: '0.72rem',
                    fontWeight: 700,
                    padding: '0.2rem 0.5rem',
                    borderRadius: '4px',
                    textTransform: 'uppercase',
                  }}
                >
                  {activeRole}
                </span>
              )}

              {/* Estado del consentimiento */}
              <span
                style={{
                  fontSize: '0.72rem',
                  padding: '0.2rem 0.5rem',
                  borderRadius: '4px',
                  background: hasConsented ? 'rgba(16, 185, 129, 0.25)' : 'rgba(239, 68, 68, 0.3)',
                  color: hasConsented ? '#A7F3D0' : '#FCA5A5',
                  border: `1px solid ${hasConsented ? '#059669' : '#DC2626'}`,
                }}
              >
                {hasConsented ? '⚖️ Consentimiento OK' : '⚠️ Sin Consentimiento'}
              </span>

              {/* Botón Cerrar Sesión */}
              <button
                type="button"
                onClick={onLogout}
                style={{
                  background: 'transparent',
                  border: '1px solid rgba(255, 255, 255, 0.3)',
                  color: '#F8FAFC',
                  padding: '0.2rem 0.55rem',
                  borderRadius: '4px',
                  fontSize: '0.72rem',
                  cursor: 'pointer',
                  fontWeight: 600,
                }}
              >
                Cerrar Sesión
              </button>
            </div>
          ) : (
            <div
              style={{
                display: 'flex',
                alignItems: 'center',
                gap: '0.75rem',
              }}
            >
              <div
                style={{
                  background: 'rgba(255, 255, 255, 0.1)',
                  padding: '0.35rem 0.75rem',
                  borderRadius: '6px',
                  color: '#CBD5E1',
                  fontSize: '0.78rem',
                }}
              >
                🔒 Sin sesión institucional activa
              </div>
              {onLoginClick && (
                <button
                  type="button"
                  onClick={onLoginClick}
                  style={{
                    backgroundColor: '#B99451',
                    color: '#FFFFFF',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '0.35rem 0.75rem',
                    fontSize: '0.78rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                  }}
                >
                  Iniciar sesión
                </button>
              )}
            </div>
          )}
        </div>
      </div>
    </header>
  );
};
