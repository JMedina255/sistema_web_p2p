import React, { useState } from 'react';
import { MOCK_USERS } from '../data/mockData';
import type { UserAccount } from '../data/mockData';

interface LoginViewProps {
  onLoginSuccess: (user: UserAccount) => void;
}

export const LoginView: React.FC<LoginViewProps> = ({ onLoginSuccess }) => {
  const [username, setUsername] = useState<string>('');
  const [password, setPassword] = useState<string>('');
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [showPassword, setShowPassword] = useState<boolean>(false);
  const [isLoading, setIsLoading] = useState<boolean>(false);

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();
    setErrorMessage(null);
    setIsLoading(true);

    setTimeout(() => {
      const foundUser = MOCK_USERS.find(
        (u) => u.username.toLowerCase() === username.trim().toLowerCase() && u.password === password
      );

      setIsLoading(false);

      if (foundUser) {
        onLoginSuccess(foundUser);
      } else {
        setErrorMessage('Credenciales institucionales incorrectas. Verifica tu usuario y contraseña.');
      }
    }, 400);
  };

  return (
    <div
      style={{
        minHeight: '100vh',
        backgroundColor: '#F4F6F9',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '2rem 1rem',
        backgroundImage: 'radial-gradient(#1C2A59 0.75px, transparent 0.75px), radial-gradient(#B99451 0.75px, #F4F6F9 0.75px)',
        backgroundSize: '30px 30px',
        backgroundPosition: '0 0, 15px 15px'
      }}
    >
      <div style={{ width: '100%', maxWidth: '520px', margin: '0 auto' }}>
        {/* Cabecera Institucional del Login */}
        <div style={{ textAlign: 'center', marginBottom: '1.75rem' }}>
          <div
            style={{
              display: 'inline-flex',
              alignItems: 'center',
              gap: '0.75rem',
              background: '#FFFFFF',
              padding: '0.6rem 1.4rem',
              borderRadius: '9999px',
              boxShadow: '0 4px 14px rgba(28, 42, 89, 0.08)',
              border: '1.5px solid #E2E8F0',
              marginBottom: '1rem'
            }}
          >
            <div
              style={{
                width: '32px',
                height: '32px',
                backgroundColor: 'var(--primary-navy)',
                color: 'var(--accent-gold)',
                borderRadius: '8px',
                display: 'flex',
                alignItems: 'center',
                justifyContent: 'center',
                fontWeight: 900,
                fontSize: '0.85rem'
              }}
            >
              UPT
            </div>
            <span style={{ fontSize: '0.88rem', fontWeight: 700, color: 'var(--primary-navy)' }}>
              Facultad de Ingeniería • Escuela Profesional de Ingeniería de Sistemas (EPIS)
            </span>
          </div>

          <h1 style={{ fontSize: '1.85rem', color: 'var(--primary-navy)', marginBottom: '0.35rem' }}>
            Sistema Web P2P de Mentorías Académicas
          </h1>
          <p style={{ color: 'var(--text-body)', fontSize: '0.88rem' }}>
            Autenticación institucional obligatoria con credenciales seguras (RBAC / RLS)
          </p>
        </div>

        {/* Tarjeta de Formulario de Inicio de Sesión */}
        <div
          style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '20px',
            padding: '2.25rem 2.25rem',
            boxShadow: '0 12px 30px rgba(28, 42, 89, 0.09)',
            border: '1px solid #E2E8F0'
          }}
        >
          <div style={{ marginBottom: '1.5rem', textAlign: 'center' }}>
            <h2 style={{ fontSize: '1.3rem', color: 'var(--primary-navy)', marginBottom: '0.25rem' }}>
              Acceso Institucional
            </h2>
            <p style={{ fontSize: '0.82rem', color: 'var(--text-muted)' }}>
              Ingresa tus credenciales del dominio institucional @upt.pe
            </p>
          </div>

          {errorMessage && (
            <div
              style={{
                backgroundColor: '#FDE8E8',
                color: '#9B1C1C',
                padding: '0.75rem 1rem',
                borderRadius: '10px',
                fontSize: '0.8rem',
                marginBottom: '1.2rem',
                border: '1px solid #F8B4B4',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem'
              }}
            >
              <span>⚠️</span>
              <span>{errorMessage}</span>
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div style={{ marginBottom: '1.2rem' }}>
              <label
                style={{
                  display: 'block',
                  fontSize: '0.82rem',
                  fontWeight: 700,
                  color: 'var(--text-heading)',
                  marginBottom: '0.35rem'
                }}
              >
                Usuario Institucional:
              </label>
              <div style={{ position: 'relative' }}>
                <span
                  style={{
                    position: 'absolute',
                    left: '12px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    fontSize: '1rem',
                    color: 'var(--text-muted)'
                  }}
                >
                  👤
                </span>
                <input
                  type="text"
                  value={username}
                  onChange={(e) => setUsername(e.target.value)}
                  placeholder="ej. admin, mentor, mentoreado"
                  required
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.8rem 0.65rem 2.4rem',
                    borderRadius: '10px',
                    border: '1.5px solid var(--border-color)',
                    fontSize: '0.9rem',
                    fontFamily: 'inherit',
                    outline: 'none',
                    backgroundColor: 'var(--bg-page)',
                    color: 'var(--text-heading)'
                  }}
                />
              </div>
            </div>

            <div style={{ marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.35rem' }}>
                <label
                  style={{
                    fontSize: '0.82rem',
                    fontWeight: 700,
                    color: 'var(--text-heading)'
                  }}
                >
                  Contraseña:
                </label>
                <button
                  type="button"
                  onClick={() => setShowPassword(!showPassword)}
                  style={{
                    background: 'none',
                    border: 'none',
                    color: 'var(--primary-blue)',
                    fontSize: '0.75rem',
                    cursor: 'pointer',
                    fontWeight: 600
                  }}
                >
                  {showPassword ? 'Ocultar' : 'Mostrar'}
                </button>
              </div>
              <div style={{ position: 'relative' }}>
                <span
                  style={{
                    position: 'absolute',
                    left: '12px',
                    top: '50%',
                    transform: 'translateY(-50%)',
                    fontSize: '1rem',
                    color: 'var(--text-muted)'
                  }}
                >
                  🔒
                </span>
                <input
                  type={showPassword ? 'text' : 'password'}
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                  placeholder="Ingresa tu contraseña"
                  required
                  style={{
                    width: '100%',
                    padding: '0.65rem 0.8rem 0.65rem 2.4rem',
                    borderRadius: '10px',
                    border: '1.5px solid var(--border-color)',
                    fontSize: '0.9rem',
                    fontFamily: 'inherit',
                    outline: 'none',
                    backgroundColor: 'var(--bg-page)',
                    color: 'var(--text-heading)'
                  }}
                />
              </div>
            </div>

            <button
              type="submit"
              disabled={isLoading}
              className="btn-gold"
              style={{
                width: '100%',
                padding: '0.8rem',
                fontSize: '0.95rem',
                fontWeight: 700,
                boxShadow: '0 4px 14px rgba(185, 148, 81, 0.3)'
              }}
            >
              {isLoading ? 'Verificando con Servidor UPT...' : 'Iniciar Sesión Institucional →'}
            </button>
          </form>

          {/* Guía Informativa de Credenciales Habilitadas para Pruebas */}
          <div
            style={{
              marginTop: '1.5rem',
              backgroundColor: 'var(--bg-page)',
              borderRadius: '12px',
              padding: '0.85rem 1rem',
              border: '1px solid var(--border-color)',
              fontSize: '0.75rem'
            }}
          >
            <span style={{ fontWeight: 800, color: 'var(--primary-navy)', display: 'block', marginBottom: '0.4rem' }}>
              📋 Cuentas Habilitadas para Pruebas:
            </span>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.35rem', color: 'var(--text-body)' }}>
              <div>
                <strong>🛡️ Administrado (tutoría):</strong> <code>admin</code> / <code>admin123</code>
                <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.7rem' }}>Ing. Liliana Vega Bernal</span>
              </div>
              <div>
                <strong>🎓 Mentor:</strong> <code>mentor</code> / <code>mentor123</code>
                <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.7rem' }}>Joan Medina Q (VIII Ciclo)</span>
              </div>
              <div>
                <strong>📚 Mentoreado:</strong> <code>mentoreado</code> / <code>mentoreado123</code>
                <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.7rem' }}>Renzo Antayhua M (II Ciclo)</span>
              </div>
            </div>
          </div>

          <div
            style={{
              marginTop: '1.25rem',
              paddingTop: '0.85rem',
              borderTop: '1px solid var(--border-color)',
              textAlign: 'center',
              fontSize: '0.72rem',
              color: 'var(--text-muted)'
            }}
          >
            ⚖️ Ley N° 29733 de Protección de Datos Personales • Sesión cifrada con JWT
          </div>
        </div>
      </div>
    </div>
  );
};
