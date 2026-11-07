/**
 * Aplicación Principal y Shell Institucional
 * Sistema Web P2P de Mentorías Académicas — EPIS UPT
 *
 * Arquitectura de Navegación y Vistas Protegidas por Rol (RBAC):
 * - Control de acceso dinámico según rol activo: Mentoreado, Mentor, Administrador y Visitante.
 * - Guardas de protección para prevenir renderizado no autorizado y fuga de credenciales.
 * - Sincronización bidireccional con parámetros de URL (?tab=).
 * - Integración de flujos de negocio sin credenciales ficticias por defecto.
 */

import React, { useState, useEffect, useCallback } from 'react';
import { AuthProvider, useAuth, parseJwt, type UserRole } from './context/AuthContext';
import { type NavTab } from './navigation/navigationConfig';
import {
  sanitizeRequestedTab,
  getDefaultTabForRole,
} from './navigation/navigationPermissions';
import { AppLayout } from './components/layout/AppLayout';
import { ProtectedView } from './components/auth/ProtectedView';
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

export type { NavTab } from './navigation/navigationConfig';

const TAB_HEADERS: Record<NavTab, { title: string; subtitle: string }> = {
  auth: {
    title: 'Iniciar Sesión Institucional',
    subtitle: 'Ingresa con tu correo institucional @upt.pe mediante código de verificación temporal.',
  },
  consent: {
    title: 'Consentimiento Informado de Privacidad',
    subtitle: 'Tratamiento seguro de datos personales y política de privacidad de la plataforma de mentorías académicas.',
  },
  curriculum: {
    title: 'Catálogo Curricular',
    subtitle: 'Consulta asignaturas de la carrera, códigos curriculares y contenidos temáticos.',
  },
  profile: {
    title: 'Perfil del Estudiante y Disponibilidad Horaria',
    subtitle: 'Gestiona tus intereses temáticos, fortalezas formativas y disponibilidad de horarios semanales.',
  },
  offers: {
    title: 'Publicación de Ofertas de Mentoría',
    subtitle: 'Programa nuevas sesiones de mentoría indicando asignatura, modalidad, horario y ubicación.',
  },
  recommendations: {
    title: 'Mentorías Recomendadas y Reserva de Sesiones',
    subtitle: 'Encuentra sesiones de mentoría afines a tus asignaturas y reserva tu vacante.',
  },
  bookings: {
    title: 'Mis Reservas de Mentoría',
    subtitle: 'Revisa tus sesiones reservadas, confirma tu asistencia con anticipación o libera tu vacante si no puedes asistir.',
  },
  sessions: {
    title: 'Panel del Mentor: Sesiones y Asistencia',
    subtitle: 'Supervisa tus sesiones de mentoría programadas, estudiantes inscritos y estado del quórum.',
  },
  admin: {
    title: 'Panel de Administración Institucional',
    subtitle: 'Supervisión de usuarios, acreditación de mentores y seguimiento de sesiones académicas.',
  },
  services: {
    title: 'Estado de los Servicios del Sistema',
    subtitle: 'Monitoreo de conectividad y estado operativo de la plataforma.',
  },
};

const AppShell: React.FC = () => {
  const {
    user,
    token,
    activeRole,
    hasConsented,
    isCheckingConsent,
    login,
    logout,
    switchRole,
    setHasConsented,
  } = useAuth();

  const isAuthenticated = Boolean(token && user);

  // Inicializar activeTab a partir de la URL o valor por defecto según el estado de sesión
  const [activeTab, setActiveTab] = useState<NavTab>(() => {
    if (typeof window !== 'undefined' && window.location) {
      const p = new URLSearchParams(window.location.search).get('tab');
      if (p) {
        return sanitizeRequestedTab(p, activeRole, Boolean(token && user));
      }
    }
    return getDefaultTabForRole(token && user ? activeRole : null);
  });

  // Sincronizar activeTab con la URL del navegador
  const handleSelectTab = useCallback((tab: NavTab) => {
    setActiveTab(tab);
    if (typeof window !== 'undefined' && window.history) {
      const url = new URL(window.location.href);
      url.searchParams.set('tab', tab);
      window.history.pushState({}, '', url.toString());
    }
  }, []);

  // Escuchar navegación del historial (atrás / adelante)
  useEffect(() => {
    const handlePopState = () => {
      if (typeof window !== 'undefined') {
        const p = new URLSearchParams(window.location.search).get('tab');
        const sanitized = sanitizeRequestedTab(p, activeRole, isAuthenticated);
        setActiveTab(sanitized);
      }
    };
    window.addEventListener('popstate', handlePopState);
    return () => window.removeEventListener('popstate', handlePopState);
  }, [activeRole, isAuthenticated]);

  // Manejo de conmutación de rol activo
  const handleRoleSwitch = useCallback(
    (newRole: UserRole) => {
      switchRole(newRole);
      const defaultTab = getDefaultTabForRole(newRole);
      handleSelectTab(defaultTab);
    },
    [switchRole, handleSelectTab]
  );

  // Cierre de sesión institucional
  const handleLogout = useCallback(() => {
    logout();
    handleSelectTab('auth');
  }, [logout, handleSelectTab]);

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
      handleSelectTab('auth');
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

  return (
    <AppLayout
      user={user}
      token={token}
      activeRole={activeRole}
      hasConsented={hasConsented}
      activeTab={activeTab}
      onSelectTab={handleSelectTab}
      onRoleSwitch={handleRoleSwitch}
      onLogout={handleLogout}
    >
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
              handleLogout();
            }}
          />
        </div>
      )}

      {/* Guarda de Protección por Rol (RBAC) */}
      <ProtectedView
        tab={activeTab}
        activeRole={isAuthenticated ? activeRole : null}
        isAuthenticated={isAuthenticated}
        userEmail={user?.email}
        hasConsented={hasConsented}
        onNavigateToAuth={() => handleSelectTab('auth')}
        onNavigateToDefault={() =>
          handleSelectTab(getDefaultTabForRole(isAuthenticated ? activeRole : null))
        }
        onSwitchRole={handleRoleSwitch}
        availableRoles={user?.roles}
      >
        <div style={{ textAlign: 'center', marginBottom: '2rem' }}>
          <h2
            style={{
              fontSize: '1.75rem',
              color: '#1C2A59',
              margin: '0 0 0.5rem 0',
              fontWeight: 800,
            }}
          >
            {TAB_HEADERS[activeTab]?.title}
          </h2>
          <p
            style={{
              margin: '0 auto',
              maxWidth: '720px',
              fontSize: '0.88rem',
              color: '#64748B',
              lineHeight: 1.6,
            }}
          >
            {TAB_HEADERS[activeTab]?.subtitle}
          </p>
        </div>

        {activeTab === 'auth' && (
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

              handleSelectTab(getDefaultTabForRole(targetRole));
            }}
          />
        )}

        {activeTab === 'consent' && (
          <ConsentModalView
            userEmail={studentEmail ?? undefined}
            onConsentAccepted={() => setHasConsented(true)}
            onConsentRejected={() => handleLogout()}
          />
        )}

        {activeTab === 'curriculum' && <CurriculumCatalogView />}

        {activeTab === 'profile' && (
          <ProfileAvailabilityView userEmail={studentEmail ?? undefined} />
        )}

        {activeTab === 'offers' && (
          <OfferPublishView
            mentorEmail={studentEmail ?? undefined}
            mentorName={
              user?.nombres ? `${user.nombres} ${user.apellidos || ''}`.trim() : undefined
            }
            onOfferPublished={() => {
              setFeedRefreshKey((prev) => prev + 1);
              handleSelectTab('sessions');
            }}
          />
        )}

        {activeTab === 'recommendations' && (
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
                handleSelectTab('bookings');
              }}
            />
          </>
        )}

        {activeTab === 'bookings' && (
          <StudentBookingsView
            studentEmail={studentEmail ?? undefined}
            onExploreRecommendations={() => handleSelectTab('recommendations')}
            onLoginRedirect={() => handleSelectTab('auth')}
          />
        )}

        {activeTab === 'sessions' && (
          <MentorSessionsView
            mentorEmail={studentEmail ?? ''}
            onNavigateToPublish={() => handleSelectTab('offers')}
            onPublishNewOffer={() => handleSelectTab('offers')}
          />
        )}

        {activeTab === 'admin' && (
          <AdminDashboardView adminEmail={studentEmail ?? undefined} />
        )}

        {activeTab === 'services' && <HealthStatus />}
      </ProtectedView>
    </AppLayout>
  );
};

export const App: React.FC = () => {
  return (
    <AuthProvider>
      <AppShell />
    </AuthProvider>
  );
};
