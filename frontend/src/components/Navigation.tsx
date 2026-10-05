import React from 'react';
import type { UserAccount } from '../data/mockData';
import { MOCK_USERS } from '../data/mockData';

interface NavigationProps {
  currentUser: UserAccount;
  currentTab: string;
  setCurrentTab: (tab: string) => void;
  onSwitchUser: (username: string) => void;
  onLogout: () => void;
  onOpenConsentModal: () => void;
}

export const Navigation: React.FC<NavigationProps> = ({
  currentUser,
  currentTab,
  setCurrentTab,
  onSwitchUser,
  onLogout,
  onOpenConsentModal
}) => {
  const roleConfig = {
    admin: { label: 'Administrador (Comité)', color: '#B99451', icon: '🛡️', bg: '#FFF8E6' },
    mentor: { label: 'Mentor (Ciclos VII-X)', color: '#1C2A59', icon: '🎓', bg: '#EEF3FF' },
    mentee: { label: 'Mentoreado (Ciclos I-IV)', color: '#0066CC', icon: '📚', bg: '#E8F5E9' }
  }[currentUser.role];

  return (
    <header className="header-wrapper" style={{ width: '100%' }}>
      {/* 1. Top Utility Bar (docs/diseño.md - 3.1) */}
      <div className="top-utility-bar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <span style={{ opacity: 0.9, fontWeight: 500, fontSize: '0.78rem' }}>
            Universidad Privada de Tacna — Facultad de Ingeniería (EPIS)
          </span>
          <span style={{ opacity: 0.4 }}>|</span>
          <button
            onClick={onOpenConsentModal}
            style={{
              background: 'none',
              border: 'none',
              color: 'var(--accent-gold)',
              cursor: 'pointer',
              fontSize: '0.75rem',
              fontWeight: 600,
              display: 'flex',
              alignItems: 'center',
              gap: '0.3rem'
            }}
          >
            ⚖️ Ley N° 29733: Consentimiento Académico
          </button>
        </div>

        <div className="utility-links" style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <span style={{ fontSize: '0.75rem', opacity: 0.8 }}>Sesión Segura (JWT Active)</span>
          <a href="#portal">Portal UPT</a>
          <a href="#campus">Campus Virtual</a>
        </div>
      </div>

      {/* 2. Main Header con Identidad Visual UPT */}
      <nav className="main-header" style={{ flexWrap: 'wrap', gap: '0.75rem' }}>
        <div className="brand-container" style={{ cursor: 'pointer' }} onClick={() => setCurrentTab('home')}>
          <div className="brand-badge">
            UPT
          </div>
          <div className="brand-text">
            <h1>SISTEMA WEB P2P</h1>
            <span>Mentorías Académicas EPIS • 2026</span>
          </div>
        </div>

        {/* Pestañas Contextuales según Rol */}
        <div className="nav-links" style={{ flexWrap: 'wrap', gap: '0.35rem' }}>
          {currentUser.role === 'admin' && (
            <>
              <button
                className={`nav-item-btn ${currentTab === 'admin' ? 'active' : ''}`}
                onClick={() => setCurrentTab('admin')}
              >
                📊 Panel Administrador (CUS14 / CUS22)
              </button>
              <button
                className={`nav-item-btn ${currentTab === 'home' ? 'active' : ''}`}
                onClick={() => setCurrentTab('home')}
              >
                🌐 Vista Catálogo
              </button>
            </>
          )}

          {currentUser.role === 'mentor' && (
            <>
              <button
                className={`nav-item-btn ${currentTab === 'mentor' ? 'active' : ''}`}
                onClick={() => setCurrentTab('mentor')}
              >
                🎓 Mi Panel Mentor (CUS09 / CUS10 / CUS11)
              </button>
              <button
                className={`nav-item-btn ${currentTab === 'home' ? 'active' : ''}`}
                onClick={() => setCurrentTab('home')}
              >
                🌐 Explorar Clases
              </button>
            </>
          )}

          {currentUser.role === 'mentee' && (
            <>
              <button
                className={`nav-item-btn ${currentTab === 'home' ? 'active' : ''}`}
                onClick={() => setCurrentTab('home')}
              >
                🏠 Inicio & Clases
              </button>
              <button
                className={`nav-item-btn ${currentTab === 'mentee' ? 'active' : ''}`}
                onClick={() => setCurrentTab('mentee')}
              >
                🎯 Recomendador & Reservas (CUS02 / CUS24)
              </button>
            </>
          )}
        </div>

        {/* Acciones de Usuario: Perfil Activo, Switcher Rápido de Roles y Cerrar Sesión */}
        <div className="header-actions" style={{ display: 'flex', alignItems: 'center', gap: '0.75rem' }}>
          {/* Tarjeta Perfil Activo */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              gap: '0.6rem',
              background: 'var(--bg-page)',
              padding: '0.3rem 0.65rem',
              borderRadius: '9999px',
              border: '1px solid var(--border-color)'
            }}
          >
            <img
              src={currentUser.avatar}
              alt={currentUser.name}
              style={{
                width: '32px',
                height: '32px',
                borderRadius: '50%',
                border: '1.5px solid var(--accent-gold)',
                objectFit: 'cover'
              }}
            />
            <div style={{ textAlign: 'left', lineHeight: 1.2 }}>
              <strong style={{ fontSize: '0.8rem', color: 'var(--primary-navy)', display: 'block' }}>
                {currentUser.name.split(' ')[0]} {currentUser.name.split(' ')[1] || ''}
              </strong>
              <span
                style={{
                  fontSize: '0.68rem',
                  color: roleConfig.color,
                  fontWeight: 700,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.2rem'
                }}
              >
                {roleConfig.icon} {currentUser.role.toUpperCase()}
              </span>
            </div>
          </div>

          {/* Selector Rápido para Alternar entre las 3 Cuentas en 1 Clic */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              background: '#FFFFFF',
              border: '1px solid var(--border-color)',
              borderRadius: '9999px',
              padding: '2px',
              fontSize: '0.72rem'
            }}
          >
            {MOCK_USERS.map((u) => {
              const isSelected = u.username === currentUser.username;
              return (
                <button
                  key={u.username}
                  onClick={() => onSwitchUser(u.username)}
                  title={`Cambiar a ${u.title}`}
                  style={{
                    border: 'none',
                    background: isSelected ? 'var(--primary-navy)' : 'transparent',
                    color: isSelected ? '#FFFFFF' : 'var(--text-body)',
                    fontWeight: isSelected ? 700 : 500,
                    padding: '0.25rem 0.55rem',
                    borderRadius: '9999px',
                    cursor: 'pointer',
                    fontSize: '0.72rem'
                  }}
                >
                  {u.username === 'admin' ? '🛡️ Admin' : u.username === 'mentor' ? '🎓 Mentor' : '📚 Mentoreado'}
                </button>
              );
            })}
          </div>

          {/* Botón Salir / Logout */}
          <button
            onClick={onLogout}
            title="Cerrar Sesión Institucional"
            style={{
              background: 'transparent',
              border: '1.5px solid #CBD5E0',
              color: '#4A5568',
              padding: '0.35rem 0.75rem',
              borderRadius: '9999px',
              fontSize: '0.75rem',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.3rem'
            }}
          >
            🚪 Salir
          </button>
        </div>
      </nav>
    </header>
  );
};
