/**
 * Barra de Navegación Contextual por Rol (RBAC)
 * Sistema Web P2P de Mentorías Académicas — EPIS UPT
 *
 * Despliega exclusivamente las pestañas autorizadas según el rol activo o estado de visitante.
 * Cumple con los estándares de accesibilidad WAI-ARIA para navegación por pestañas.
 */

import React from 'react';
import { type UserRole } from '../../context/AuthContext';
import { type NavTab, getNavigationItemsForRole } from '../../navigation/navigationConfig';

export interface RoleNavigationProps {
  activeTab: NavTab;
  activeRole: UserRole | null;
  isAuthenticated: boolean;
  onSelectTab: (tab: NavTab) => void;
}

export const RoleNavigation: React.FC<RoleNavigationProps> = ({
  activeTab,
  activeRole,
  isAuthenticated,
  onSelectTab,
}) => {
  const navItems = getNavigationItemsForRole(isAuthenticated ? activeRole : null);

  return (
    <nav
      aria-label="Navegación principal por rol"
      style={{
        backgroundColor: '#FFFFFF',
        borderBottom: '1px solid #E2E8F0',
        padding: '0.6rem 2rem',
      }}
    >
      <div
        role="tablist"
        aria-label="Módulos del sistema"
        style={{
          maxWidth: '1200px',
          margin: '0 auto',
          display: 'flex',
          gap: '0.5rem',
          flexWrap: 'wrap',
        }}
      >
        {navItems.map((item) => {
          const isActive = activeTab === item.tab;
          return (
            <button
              key={item.tab}
              id={`nav-tab-${item.tab}`}
              aria-pressed={isActive}
              type="button"
              onClick={() => onSelectTab(item.tab)}
              style={{
                background: isActive ? '#1C2A59' : '#F1F5F9',
                color: isActive ? '#FFFFFF' : '#475569',
                border: 'none',
                borderRadius: '6px',
                padding: '0.5rem 1rem',
                fontSize: '0.82rem',
                fontWeight: 600,
                cursor: 'pointer',
                transition: 'all 0.2s ease-in-out',
                display: 'inline-flex',
                alignItems: 'center',
                gap: '0.4rem',
              }}
            >
              <span>{item.icon}</span>
              {' '}
              <span>{item.label}</span>
            </button>
          );
        })}
      </div>
    </nav>
  );
};
