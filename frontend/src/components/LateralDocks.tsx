import React from 'react';

export const LateralDocks: React.FC = () => {
  return (
    <>
      {/* Dock Izquierdo (docs/diseño.md - 3.2: Accesos Rápidos Universitarios) */}
      <aside className="dock-left" aria-label="Accesos Rápidos UPT">
        <button className="dock-item" title="Campus Virtual">
          🎓
          <span className="tooltip">Campus Virtual UPT</span>
        </button>
        <button className="dock-item" title="Avisos y Matrícula">
          📋
          <span className="tooltip">Matrícula & Notas</span>
        </button>
        <button className="dock-item" title="Biblioteca Central">
          📚
          <span className="tooltip">Biblioteca Virtual</span>
        </button>
        <button className="dock-item" title="Horarios de Clases">
          ⏱️
          <span className="tooltip">Horarios Académicos</span>
        </button>
        <button className="dock-item" title="Trámites EPIS">
          🏛️
          <span className="tooltip">Trámites Dirección EPIS</span>
        </button>
      </aside>

      {/* Dock Derecho (docs/diseño.md - 3.2: Redes Sociales e Interacción) */}
      <aside className="dock-right" aria-label="Canales Institucionales">
        <button className="dock-item" title="Facebook UPT">
          🌐
          <span className="tooltip">Facebook Institucional</span>
        </button>
        <button className="dock-item" title="LinkedIn EPIS">
          💼
          <span className="tooltip">Red Profesional EPIS</span>
        </button>
        <button className="dock-item" title="Soporte y Mesa de Ayuda">
          💬
          <span className="tooltip">Mesa de Ayuda P2P</span>
        </button>
      </aside>
    </>
  );
};
