import React from 'react';

interface NavigationProps {
  currentTab: 'home' | 'recommendation' | 'booking' | 'gamification';
  setCurrentTab: (tab: 'home' | 'recommendation' | 'booking' | 'gamification') => void;
  userRole: 'mentee' | 'mentor';
  setUserRole: (role: 'mentee' | 'mentor') => void;
  onOpenConsentModal: () => void;
}

export const Navigation: React.FC<NavigationProps> = ({
  currentTab,
  setCurrentTab,
  userRole,
  setUserRole,
  onOpenConsentModal
}) => {
  return (
    <header className="header-wrapper" style={{ width: '100%' }}>
      {/* 1. Top Utility Bar (docs/diseño.md - 3.1) */}
      <div className="top-utility-bar">
        <div style={{ display: 'flex', alignItems: 'center', gap: '1rem' }}>
          <span style={{ opacity: 0.9, fontWeight: 500 }}>
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
            ⚖️ Ley 29733: Consentimiento
          </button>
        </div>

        <div className="utility-links">
          <a href="#inicio">Portal UPT</a>
          <a href="#campus">Campus Virtual</a>
          <a href="#calidad">UPT Calidad</a>
          <a href="#alumni">GPS Alumni</a>
        </div>
      </div>

      {/* 2. Main Header con Identidad Visual UPT */}
      <nav className="main-header">
        <div className="brand-container" style={{ cursor: 'pointer' }} onClick={() => setCurrentTab('home')}>
          <div className="brand-badge">
            UPT
          </div>
          <div className="brand-text">
            <h1>SISTEMA WEB P2P</h1>
            <span>Mentorías Académicas EPIS • 2026</span>
          </div>
        </div>

        {/* Pestañas de Navegación del Sistema */}
        <div className="nav-links">
          <button
            className={`nav-item-btn ${currentTab === 'home' ? 'active' : ''}`}
            onClick={() => setCurrentTab('home')}
          >
            🏠 Inicio
          </button>
          <button
            className={`nav-item-btn ${currentTab === 'recommendation' ? 'active' : ''}`}
            onClick={() => setCurrentTab('recommendation')}
          >
            🎯 Emparejamiento
          </button>
          <button
            className={`nav-item-btn ${currentTab === 'booking' ? 'active' : ''}`}
            onClick={() => setCurrentTab('booking')}
          >
            📅 Agendamiento
          </button>
          <button
            className={`nav-item-btn ${currentTab === 'gamification' ? 'active' : ''}`}
            onClick={() => setCurrentTab('gamification')}
          >
            🏆 Horas e Insignias
          </button>
        </div>

        {/* Acciones: Switch de Rol y Botón CTA */}
        <div className="header-actions">
          {/* Selector de Rol para la presentación */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              background: 'var(--bg-page)',
              padding: '0.25rem 0.5rem',
              borderRadius: 'var(--radius-pill)',
              border: '1px solid var(--border-color)',
              fontSize: '0.78rem'
            }}
          >
            <span style={{ marginRight: '0.4rem', color: 'var(--text-muted)', fontWeight: 600 }}>
              Rol Activo:
            </span>
            <button
              onClick={() => setUserRole('mentee')}
              style={{
                border: 'none',
                background: userRole === 'mentee' ? 'var(--primary-navy)' : 'transparent',
                color: userRole === 'mentee' ? '#FFFFFF' : 'var(--text-body)',
                fontWeight: 600,
                fontSize: '0.74rem',
                padding: '0.3rem 0.6rem',
                borderRadius: 'var(--radius-pill)',
                cursor: 'pointer'
              }}
            >
              Mentoreado (I-IV)
            </button>
            <button
              onClick={() => setUserRole('mentor')}
              style={{
                border: 'none',
                background: userRole === 'mentor' ? 'var(--accent-gold)' : 'transparent',
                color: userRole === 'mentor' ? '#FFFFFF' : 'var(--text-body)',
                fontWeight: 600,
                fontSize: '0.74rem',
                padding: '0.3rem 0.6rem',
                borderRadius: 'var(--radius-pill)',
                cursor: 'pointer'
              }}
            >
              Mentor (VII-X)
            </button>
          </div>

          <button
            className="btn-gold"
            onClick={() => setCurrentTab('recommendation')}
            style={{ padding: '0.5rem 1.1rem', fontSize: '0.82rem' }}
          >
            <span>Buscar Mentor</span>
            <span>→</span>
          </button>
        </div>
      </nav>
    </header>
  );
};
