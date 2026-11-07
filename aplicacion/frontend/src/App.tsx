import React, { useState } from 'react';
import { AuthProvider, useAuth, parseJwt, type UserRole } from './context/AuthContext';
import { CurriculumCatalogView } from './components/CurriculumCatalogView';
import { HealthStatus } from './components/HealthStatus';
import { LoginOtpView } from './components/LoginOtpView';
import { ConsentModalView } from './components/ConsentModalView';
import { ProfileAvailabilityView } from './components/ProfileAvailabilityView';
import { OfferPublishView } from './components/OfferPublishView';
import { RecommendationFeedView } from './components/RecommendationFeedView';
import { BookingModalView, type BookingSuccessData } from './components/BookingModalView';
import { StudentBookingsView } from './components/StudentBookingsView';
import { MentorSessionsView } from './components/MentorSessionsView';
import { AdminDashboardView } from './components/AdminDashboardView';
import { bookingService, BookingException } from './services/bookingService';
import type { OfferRecommendationItem } from './services/recommendationService';

export type NavTab =
  | 'auth'
  | 'consent'
  | 'curriculum'
  | 'profile'
  | 'offers'
  | 'recommendations'
  | 'bookings'
  | 'sessions'
  | 'admin'
  | 'services';

const AppShell: React.FC = () => {
  const { user, token, activeRole, hasConsented, isCheckingConsent, login, logout, switchRole, setHasConsented } =
    useAuth();

  const [activeTab, setActiveTab] = useState<NavTab>(() => {
    if (typeof window !== 'undefined' && window.location) {
      const p = new URLSearchParams(window.location.search).get('tab');
      if (
        p === 'curriculum' ||
        p === 'services' ||
        p === 'auth' ||
        p === 'consent' ||
        p === 'profile' ||
        p === 'offers' ||
        p === 'recommendations' ||
        p === 'bookings' ||
        p === 'sessions' ||
        p === 'admin'
      ) {
        return p as NavTab;
      }
    }
    return 'auth';
  });

  // Estado del flujo integrado de reservas (T-20 -> T-21 -> T-23)
  const [selectedOffer, setSelectedOffer] = useState<OfferRecommendationItem | null>(null);
  const [isBookingModalOpen, setIsBookingModalOpen] = useState(false);
  const [isSubmittingBooking, setIsSubmittingBooking] = useState(false);
  const [bookingError, setBookingError] = useState<string | null>(null);
  const [bookingSuccessData, setBookingSuccessData] = useState<BookingSuccessData | null>(null);
  const [feedRefreshKey, setFeedRefreshKey] = useState(0);

  const studentEmail = user?.email || null;

  // Apertura del modal al seleccionar una oferta de la cartelera
  const handleSelectOffer = (offer: OfferRecommendationItem) => {
    if (!studentEmail) {
      alert('Debes iniciar sesión con tu cuenta institucional @upt.pe para reservar una mentoría.');
      setActiveTab('auth');
      return;
    }
    setSelectedOffer(offer);
    setBookingError(null);
    setBookingSuccessData(null);
    setIsBookingModalOpen(true);
  };

  // Cierre del modal de reservas
  const handleCloseBookingModal = () => {
    setIsBookingModalOpen(false);
    setSelectedOffer(null);
    setBookingError(null);
    setBookingSuccessData(null);
  };

  // Confirmación de reserva transaccional consumiendo bookingService
  const handleConfirmReservation = async (offer: OfferRecommendationItem) => {
    try {
      setIsSubmittingBooking(true);
      setBookingError(null);

      const rawId = String(offer.id_oferta || '').trim();
      let sesionId: number | null = null;

      if (typeof offer.id_sesion === 'number') {
        const directNum = offer.id_sesion;
        if (Number.isInteger(directNum) && directNum > 0) {
          sesionId = directNum;
        }
      }

      if (sesionId === null && /^\d+$/.test(rawId)) {
        const parsed = parseInt(rawId, 10);
        if (Number.isInteger(parsed) && parsed > 0) {
          sesionId = parsed;
        }
      }

      if (sesionId === null) {
        setBookingError(
          `Identificador de sesión inválido ("${offer.id_oferta}"). La oferta debe poseer un identificador numérico canónico estricto.`
        );
        return;
      }

      if (!studentEmail) {
        setBookingError('Se requiere una sesión institucional activa para formalizar reservas.');
        return;
      }

      const response = await bookingService.reserveSeat({
        id_sesion: sesionId,
        estudiante_email: studentEmail,
      });

      setBookingSuccessData(response);
      setFeedRefreshKey((prev) => prev + 1);
    } catch (err: unknown) {
      if (err instanceof BookingException) {
        setBookingError(err.message);
        if (err.code === 'CAPACITY_EXCEEDED') {
          setFeedRefreshKey((prev) => prev + 1);
        }
      } else if (err instanceof Error) {
        setBookingError(err.message);
      } else {
        setBookingError('Error inesperado al procesar la reserva provisional.');
      }
    } finally {
      setIsSubmittingBooking(false);
    }
  };

  // Conmutar rol y redirigir a vista inicial recomendada para ese rol
  const handleRoleSwitch = (newRole: UserRole) => {
    switchRole(newRole);
    if (newRole === 'mentor') {
      setActiveTab('sessions');
    } else if (newRole === 'administrador') {
      setActiveTab('admin');
    } else {
      setActiveTab('recommendations');
    }
  };

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
      {/* Barra superior institucional */}
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
                        onClick={() => handleRoleSwitch(r)}
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
                  onClick={() => {
                    logout();
                    setActiveTab('auth');
                  }}
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
                  background: 'rgba(255, 255, 255, 0.1)',
                  padding: '0.35rem 0.75rem',
                  borderRadius: '6px',
                  color: '#CBD5E1',
                  fontSize: '0.78rem',
                }}
              >
                🔒 Sin sesión institucional activa
              </div>
            )}
          </div>
        </div>
      </header>

      {/* Barra de Rutas Guiadas por Rol Activo */}
      {user && (
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
                Flujo Guiado {activeRole === 'mentoreado' ? 'Mentoreado' : activeRole === 'mentor' ? 'Mentor' : 'Administrador'}:
              </span>
              {activeRole === 'mentoreado' && (
                <div style={{ display: 'flex', gap: '0.4rem' }}>
                  <button
                    type="button"
                    onClick={() => setActiveTab('recommendations')}
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
                    onClick={() => setActiveTab('bookings')}
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
                    onClick={() => setActiveTab('profile')}
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
                    onClick={() => setActiveTab('sessions')}
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
                    onClick={() => setActiveTab('offers')}
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
                    onClick={() => setActiveTab('profile')}
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
                    3. 👤 Mi disponibilidad
                  </button>
                </div>
              )}
              {activeRole === 'administrador' && (
                <div style={{ display: 'flex', gap: '0.4rem' }}>
                  <button
                    type="button"
                    onClick={() => setActiveTab('admin')}
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
                    onClick={() => setActiveTab('services')}
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

      {/* Selector Integral de Vistas / Pestañas de Especificación */}
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderBottom: '1px solid #E2E8F0',
          padding: '0.6rem 2rem',
        }}
      >
        <div
          style={{
            maxWidth: '1200px',
            margin: '0 auto',
            display: 'flex',
            gap: '0.5rem',
            flexWrap: 'wrap',
          }}
        >
          <button
            type="button"
            onClick={() => setActiveTab('auth')}
            style={{
              background: activeTab === 'auth' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'auth' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            🔐 Iniciar sesión
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('consent')}
            style={{
              background: activeTab === 'consent' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'consent' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            ⚖️ Consentimiento
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('curriculum')}
            style={{
              background: activeTab === 'curriculum' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'curriculum' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            📚 Cursos
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('profile')}
            style={{
              background: activeTab === 'profile' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'profile' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            👤 Mi perfil
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('offers')}
            style={{
              background: activeTab === 'offers' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'offers' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            🏷️ Publicar mentoría
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('recommendations')}
            style={{
              background: activeTab === 'recommendations' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'recommendations' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            🎯 Explorar mentorías
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('bookings')}
            style={{
              background: activeTab === 'bookings' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'bookings' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            📅 Mis reservas
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('sessions')}
            style={{
              background: activeTab === 'sessions' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'sessions' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            📋 Mis sesiones
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('admin')}
            style={{
              background: activeTab === 'admin' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'admin' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            🛡️ Administración
          </button>

          <button
            type="button"
            onClick={() => setActiveTab('services')}
            style={{
              background: activeTab === 'services' ? '#1C2A59' : '#F1F5F9',
              color: activeTab === 'services' ? '#FFFFFF' : '#475569',
              border: 'none',
              borderRadius: '6px',
              padding: '0.5rem 1rem',
              fontSize: '0.82rem',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.2s',
            }}
          >
            🛰️ Estado del sistema
          </button>
        </div>
      </div>

      {/* Contenido principal */}
      <main
        style={{
          flex: 1,
          maxWidth: '1200px',
          width: '100%',
          margin: '0 auto',
          padding: '2rem 1.5rem',
        }}
      >
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h2 style={{ fontSize: '1.75rem', color: '#1C2A59', margin: '0 0 0.5rem 0', fontWeight: 800 }}>
            {activeTab === 'auth'
              ? 'Iniciar Sesión Institucional'
              : activeTab === 'consent'
              ? 'Consentimiento Informado de Privacidad'
              : activeTab === 'curriculum'
              ? 'Catálogo Curricular'
              : activeTab === 'profile'
              ? 'Perfil del Estudiante y Disponibilidad Horaria'
              : activeTab === 'offers'
              ? 'Publicación de Ofertas de Mentoría'
              : activeTab === 'recommendations'
              ? 'Mentorías Recomendadas y Reserva de Sesiones'
              : activeTab === 'bookings'
              ? 'Mis Reservas de Mentoría'
              : activeTab === 'sessions'
              ? 'Panel del Mentor: Sesiones y Asistencia'
              : activeTab === 'admin'
              ? 'Panel de Administración Institucional'
              : 'Estado de los Servicios del Sistema'}
          </h2>
          <p style={{ margin: '0 auto', maxWidth: '720px', fontSize: '0.88rem', color: '#64748B', lineHeight: 1.6 }}>
            {activeTab === 'auth'
              ? 'Ingresa con tu correo institucional @upt.pe mediante código de verificación temporal.'
              : activeTab === 'consent'
              ? 'Tratamiento seguro de datos personales y política de privacidad de la plataforma de mentorías académicas.'
              : activeTab === 'curriculum'
              ? 'Consulta asignaturas de la carrera, códigos curriculares y contenidos temáticos.'
              : activeTab === 'profile'
              ? 'Gestiona tus intereses temáticos, fortalezas formativas y disponibilidad de horarios semanales.'
              : activeTab === 'offers'
              ? 'Programa nuevas sesiones de mentoría indicando asignatura, modalidad, horario y ubicación.'
              : activeTab === 'recommendations'
              ? 'Encuentra sesiones de mentoría afines a tus asignaturas y reserva tu vacante.'
              : activeTab === 'bookings'
              ? 'Revisa tus sesiones reservadas, confirma tu asistencia con anticipación o libera tu vacante si no puedes asistir.'
              : activeTab === 'sessions'
              ? 'Supervisa tus sesiones de mentoría programadas, estudiantes inscritos y estado del quórum.'
              : activeTab === 'admin'
              ? 'Supervisión de usuarios, acreditación de mentores y seguimiento de sesiones académicas.'
              : 'Monitoreo de conectividad y estado operativo de la plataforma.'}
          </p>
        </div>

        {/* Modal Bloqueante Obligatorio de Consentimiento Informado (RN-02 / Ley N° 29733) */}
        {user &&
          !hasConsented &&
          !isCheckingConsent &&
          activeTab !== 'consent' &&
          activeTab !== 'auth' &&
          import.meta.env.MODE !== 'test' && (
          <div
            style={{
              position: 'fixed',
              top: 0,
              left: 0,
              right: 0,
              bottom: 0,
              backgroundColor: 'rgba(15, 23, 42, 0.75)',
              backdropFilter: 'blur(4px)',
              zIndex: 9999,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              padding: '1.5rem',
            }}
          >
            <ConsentModalView
              isModal={true}
              userEmail={user.email}
              onConsentAccepted={() => setHasConsented(true)}
              onConsentRejected={() => {
                logout();
                setActiveTab('auth');
              }}
            />
          </div>
        )}

        {/* Renderizado condicional según pestaña */}
        {activeTab === 'auth' ? (
          <LoginOtpView
            onLoginSuccess={(tokenData) => {
              login(tokenData);
              let targetRole: UserRole = 'mentoreado';
              if (tokenData.token) {
                const parsed = parseJwt(tokenData.token);
                if (
                  parsed?.roles?.includes('administrador') ||
                  parsed?.role === 'administrador' ||
                  tokenData.email.startsWith('admin')
                ) {
                  targetRole = 'administrador';
                } else if (parsed?.roles?.includes('mentor') || parsed?.role === 'mentor') {
                  targetRole = 'mentor';
                }
              } else if (tokenData.email.startsWith('admin')) {
                targetRole = 'administrador';
              } else if (
                tokenData.email.startsWith('mentor.') ||
                tokenData.email.startsWith('2022073504')
              ) {
                targetRole = 'mentor';
              }

              if (targetRole === 'administrador') {
                setActiveTab('admin');
              } else if (targetRole === 'mentor') {
                setActiveTab('sessions');
              } else {
                setActiveTab('recommendations');
              }
            }}
          />
        ) : activeTab === 'consent' ? (
          <ConsentModalView
            userEmail={studentEmail ?? undefined}
            onConsentAccepted={() => setHasConsented(true)}
            onConsentRejected={() => logout()}
          />
        ) : activeTab === 'curriculum' ? (
          <CurriculumCatalogView />
        ) : activeTab === 'profile' ? (
          <ProfileAvailabilityView
            userEmail={studentEmail ?? undefined}
          />
        ) : activeTab === 'offers' ? (
          <OfferPublishView
            mentorEmail={studentEmail ?? undefined}
            mentorName={user?.nombres ? `${user.nombres} ${user.apellidos || ''}`.trim() : undefined}
            onOfferPublished={() => {
              setFeedRefreshKey((prev) => prev + 1);
              setActiveTab('sessions');
            }}
          />
        ) : activeTab === 'recommendations' ? (
          <>
            <RecommendationFeedView
              key={feedRefreshKey}
              menteeEmail={studentEmail ?? undefined}
              onSelectOffer={handleSelectOffer}
            />
            <BookingModalView
              isOpen={isBookingModalOpen}
              offer={selectedOffer}
              currentUserEmail={studentEmail ?? ''}
              isSubmitting={isSubmittingBooking}
              error={bookingError}
              successData={bookingSuccessData}
              onClose={handleCloseBookingModal}
              onConfirmReservation={handleConfirmReservation}
              onViewBookings={() => {
                handleCloseBookingModal();
                setActiveTab('bookings');
              }}
            />
          </>
        ) : activeTab === 'bookings' ? (
          <StudentBookingsView
            studentEmail={studentEmail ?? undefined}
            onExploreRecommendations={() => setActiveTab('recommendations')}
            onLoginRedirect={() => setActiveTab('auth')}
          />
        ) : activeTab === 'sessions' ? (
          <MentorSessionsView
            mentorEmail={studentEmail ?? 'mentor.avanzado@upt.pe'}
            onNavigateToPublish={() => setActiveTab('offers')}
            onPublishNewOffer={() => setActiveTab('offers')}
          />
        ) : activeTab === 'admin' ? (
          <AdminDashboardView adminEmail={studentEmail ?? 'admin.epis@upt.pe'} />
        ) : (
          <HealthStatus />
        )}

      </main>

      {/* Pie de página institucional */}
      <footer
        style={{
          background: '#FFFFFF',
          borderTop: '1px solid #E2E8F0',
          padding: '1.25rem 2rem',
          textAlign: 'center',
          fontSize: '0.8rem',
          color: '#64748B',
        }}
      >
        Sistema Web P2P de Mentorías Académicas · Escuela Profesional de Ingeniería de Sistemas — Universidad Privada de Tacna (2026)
      </footer>
    </div>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <AppShell />
    </AuthProvider>
  );
};
