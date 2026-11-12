/**
 * Layout Principal de la Aplicación (Shell)
 * Sistema Web P2P de Mentorías Académicas — EPIS UPT
 *
 * Integra el encabezado institucional, la barra de flujo guiado, la barra de navegación RBAC,
 * el contenedor principal y el pie de página institucional.
 */

import React from 'react';
import { type AuthUser, type UserRole } from '../../context/AuthContext';
import { type NavTab } from '../../navigation/navigationConfig';
import { Header } from './Header';
import { RoleNavigation } from './RoleNavigation';
import { Footer } from './Footer';

export interface AppLayoutProps {
  user: AuthUser | null;
  token: string | null;
  activeRole: UserRole;
  hasConsented: boolean;
  activeTab: NavTab;
  onSelectTab: (tab: NavTab) => void;
  onRoleSwitch: (role: UserRole) => void;
  onLogout: () => void;
  children: React.ReactNode;
}

export const AppLayout: React.FC<AppLayoutProps> = ({
  user,
  token,
  activeRole,
  hasConsented,
  activeTab,
  onSelectTab,
  onRoleSwitch,
  onLogout,
  children,
}) => {
  const isAuthenticated = Boolean(token && user);

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#F8FAFC',
        fontFamily: "'Segoe UI', -apple-system, BlinkMacSystemFont, Roboto, sans-serif",
        color: '#1E293B',
        display: 'flex',
        flexDirection: 'column',
      }}
    >
      {/* 1. Encabezado Institucional */}
      <Header
        user={user}
        token={token}
        activeRole={activeRole}
        hasConsented={hasConsented}
        onRoleSwitch={onRoleSwitch}
        onLogout={onLogout}
        onLoginClick={() => onSelectTab('auth')}
      />

      {/* 2. Barra de Rutas Guiadas por Rol Activo */}
      {isAuthenticated && (
        <div
          style={{
            backgroundColor: '#0F172A',
            color: '#F8FAFC',
            padding: '0.5rem 2rem',
            borderBottom: '1px solid #334155',
          }}
        >
          <div
            style={{
              maxWidth: '1200px',
              margin: '0 auto',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              flexWrap: 'wrap',
              gap: '0.5rem',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', fontSize: '0.8rem' }}>
              <span style={{ color: '#B99451', fontWeight: 700 }}>
                Flujo Guiado{' '}
                {activeRole === 'mentoreado'
                  ? 'Mentoreado'
                  : activeRole === 'mentor'
                  ? 'Mentor'
                  : 'Administrador'}
                :
              </span>
              {activeRole === 'mentoreado' && (
                <div style={{ display: 'flex', gap: '0.4rem' }}>
                  <button
                    type="button"
                    onClick={() => onSelectTab('recommendations')}
                    style={{
                      background: activeTab === 'recommendations' ? '#B99451' : 'transparent',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '0.25rem 0.6rem',
                      fontSize: '0.78rem',
                      cursor: 'pointer',
                      fontWeight: 600,
                    }}
                  >
                    1. 🎯 Explorar mentorías
                  </button>
                  <span style={{ color: '#64748B' }}>→</span>
                  <button
                    type="button"
                    onClick={() => onSelectTab('bookings')}
                    style={{
                      background: activeTab === 'bookings' ? '#B99451' : 'transparent',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '0.25rem 0.6rem',
                      fontSize: '0.78rem',
                      cursor: 'pointer',
                      fontWeight: 600,
                    }}
                  >
                    2. 📅 Mis reservas
                  </button>
                  <span style={{ color: '#64748B' }}>→</span>
                  <button
                    type="button"
                    onClick={() => onSelectTab('profile')}
                    style={{
                      background: activeTab === 'profile' ? '#B99451' : 'transparent',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '0.25rem 0.6rem',
                      fontSize: '0.78rem',
                      cursor: 'pointer',
                      fontWeight: 600,
                    }}
                  >
                    3. 👤 Mi perfil
                  </button>
                </div>
              )}
              {activeRole === 'mentor' && (
                <div style={{ display: 'flex', gap: '0.4rem' }}>
                  <button
                    type="button"
                    onClick={() => onSelectTab('sessions')}
                    style={{
                      background: activeTab === 'sessions' ? '#B99451' : 'transparent',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '0.25rem 0.6rem',
                      fontSize: '0.78rem',
                      cursor: 'pointer',
                      fontWeight: 600,
                    }}
                  >
                    1. 📋 Mis sesiones
                  </button>
                  <span style={{ color: '#64748B' }}>→</span>
                  <button
                    type="button"
                    onClick={() => onSelectTab('offers')}
                    style={{
                      background: activeTab === 'offers' ? '#B99451' : 'transparent',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '0.25rem 0.6rem',
                      fontSize: '0.78rem',
                      cursor: 'pointer',
                      fontWeight: 600,
                    }}
                  >
                    2. 🏷️ Publicar mentoría
                  </button>
                  <span style={{ color: '#64748B' }}>→</span>
                  <button
                    type="button"
                    onClick={() => onSelectTab('certificates')}
                    style={{
                      background: activeTab === 'certificates' ? '#B99451' : 'transparent',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '0.25rem 0.6rem',
                      fontSize: '0.78rem',
                      cursor: 'pointer',
                      fontWeight: 600,
                    }}
                  >
                    3. 📜 Mis constancias
                  </button>
                  <span style={{ color: '#64748B' }}>→</span>
                  <button
                    type="button"
                    onClick={() => onSelectTab('profile')}
                    style={{
                      background: activeTab === 'profile' ? '#B99451' : 'transparent',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '0.25rem 0.6rem',
                      fontSize: '0.78rem',
                      cursor: 'pointer',
                      fontWeight: 600,
                    }}
                  >
                    4. 👤 Mi disponibilidad
                  </button>
                </div>
              )}
              {activeRole === 'administrador' && (
                <div style={{ display: 'flex', gap: '0.4rem' }}>
                  <button
                    type="button"
                    onClick={() => onSelectTab('admin')}
                    style={{
                      background: activeTab === 'admin' ? '#B99451' : 'transparent',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '0.25rem 0.6rem',
                      fontSize: '0.78rem',
                      cursor: 'pointer',
                      fontWeight: 600,
                    }}
                  >
                    1. 🛡️ Gestión de mentores
                  </button>
                  <span style={{ color: '#64748B' }}>→</span>
                  <button
                    type="button"
                    onClick={() => onSelectTab('services')}
                    style={{
                      background: activeTab === 'services' ? '#B99451' : 'transparent',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '4px',
                      padding: '0.25rem 0.6rem',
                      fontSize: '0.78rem',
                      cursor: 'pointer',
                      fontWeight: 600,
                    }}
                  >
                    2. 🛰️ Estado del sistema
                  </button>
                </div>
              )}
            </div>
          </div>
        </div>
      )}

      {/* 3. Selector Contextual de Módulos (RBAC) */}
      <RoleNavigation
        activeTab={activeTab}
        activeRole={isAuthenticated ? activeRole : null}
        isAuthenticated={isAuthenticated}
        onSelectTab={onSelectTab}
      />

      {/* 4. Contenedor Principal */}
      <main
        style={{
          flex: 1,
          maxWidth: '1200px',
          width: '100%',
          margin: '0 auto',
          padding: '2rem 1.5rem',
        }}
      >
        {children}
      </main>

      {/* 5. Pie de Página */}
      <Footer />
    </div>
  );
};
