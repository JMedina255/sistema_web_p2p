import { useState } from 'react';
import { Navigation } from './components/Navigation';
import { LateralDocks } from './components/LateralDocks';
import { ConsentModal } from './components/ConsentModal';
import { LoginView } from './components/LoginView';
import { AdminView } from './components/AdminView';
import { MentorFlowView } from './components/MentorFlowView';
import { MenteeFlowView } from './components/MenteeFlowView';
import { HomeView } from './components/HomeView';
import { RecommendationView } from './components/RecommendationView';
import { BookingView } from './components/BookingView';
import { GamificationView } from './components/GamificationView';
import {
  INITIAL_BOOKINGS,
  INITIAL_LOGS,
  INITIAL_CERTIFICATES,
  MOCK_USERS
} from './data/mockData';
import type {
  Mentor,
  SessionBooking,
  UserAccount,
  PedagogicalLog,
  DigitalCertificate
} from './data/mockData';

export function App() {
  // Estado de Autenticación Institucional (CUS01 / RF02)
  // Iniciamos con null para que el usuario pueda usar el Login o entrar con 1 clic
  const [currentUser, setCurrentUser] = useState<UserAccount | null>(() => {
    const saved = localStorage.getItem('upt_p2p_active_user');
    if (saved) {
      const found = MOCK_USERS.find(u => u.username === saved);
      if (found) return found;
    }
    return null;
  });

  const [currentTab, setCurrentTab] = useState<string>('home');
  const [isConsentModalOpen, setIsConsentModalOpen] = useState<boolean>(false);
  const [hasAcceptedConsent, setHasAcceptedConsent] = useState<boolean>(false);

  // Estados Globales Sincronizados entre Roles
  const [bookings, setBookings] = useState<SessionBooking[]>(INITIAL_BOOKINGS);
  const [logs, setLogs] = useState<PedagogicalLog[]>(INITIAL_LOGS);
  const [certificates, setCertificates] = useState<DigitalCertificate[]>(INITIAL_CERTIFICATES);
  const [selectedMentorForBooking, setSelectedMentorForBooking] = useState<Mentor | null>(null);
  const [selectedTopicForBooking, setSelectedTopicForBooking] = useState<string>('');

  // Login
  const handleLoginSuccess = (user: UserAccount) => {
    setCurrentUser(user);
    setHasAcceptedConsent(user.hasAcceptedConsent);
    localStorage.setItem('upt_p2p_active_user', user.username);
    if (user.role === 'admin') setCurrentTab('admin');
    else if (user.role === 'mentor') setCurrentTab('mentor');
    else setCurrentTab('mentee');
  };

  // Logout
  const handleLogout = () => {
    setCurrentUser(null);
    localStorage.removeItem('upt_p2p_active_user');
  };

  // Cambio rápido entre cuentas de prueba (admin, mentor, mentoreado)
  const handleSwitchUser = (username: string) => {
    const targetUser = MOCK_USERS.find(u => u.username === username);
    if (targetUser) {
      setCurrentUser(targetUser);
      setHasAcceptedConsent(targetUser.hasAcceptedConsent);
      localStorage.setItem('upt_p2p_active_user', targetUser.username);
      if (targetUser.role === 'admin') setCurrentTab('admin');
      else if (targetUser.role === 'mentor') setCurrentTab('mentor');
      else setCurrentTab('mentee');
    }
  };

  // Acciones de Agendamiento y Mentorías
  const handleSelectMentorForBooking = (mentor: Mentor, topic: string) => {
    setSelectedMentorForBooking(mentor);
    setSelectedTopicForBooking(topic);
    setCurrentTab('booking');
  };

  const handleAddBooking = (newBooking: SessionBooking) => {
    setBookings([newBooking, ...bookings]);
  };

  const handleConfirmBooking = (sessionId: string) => {
    setBookings(bookings.map(b => b.id === sessionId ? { ...b, status: 'CONFIRMADA' } : b));
  };

  const handleUpdateBookingStatus = (sessionId: string, newStatus: SessionBooking['status']) => {
    setBookings(bookings.map(b => b.id === sessionId ? { ...b, status: newStatus } : b));
  };

  // Ratificación de asistencia en T-24h (CUS24 / RN-08)
  const handleRatifyAttendance = (sessionId: string) => {
    setBookings(bookings.map(b => b.id === sessionId ? { ...b, ratifiedT24: true } : b));
  };

  // Agregar Bitácora (CUS10)
  const handleAddLog = (newLog: PedagogicalLog) => {
    setLogs([newLog, ...logs]);
  };

  // Si no ha iniciado sesión, desplegamos la pantalla institucional de Login
  if (!currentUser) {
    return <LoginView onLoginSuccess={handleLoginSuccess} />;
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* Navegación Dual Institucional */}
      <Navigation
        currentUser={currentUser}
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        onSwitchUser={handleSwitchUser}
        onLogout={handleLogout}
        onOpenConsentModal={() => setIsConsentModalOpen(true)}
      />

      {/* Docks Flotantes Laterales */}
      <LateralDocks />

      {/* Notificación Superior si aún no ha firmado el Consentimiento Ley 29733 (RF01) */}
      {!hasAcceptedConsent && (
        <div
          style={{
            backgroundColor: '#1C2A59',
            color: '#FFFFFF',
            padding: '0.55rem 1.5rem',
            textAlign: 'center',
            fontSize: '0.82rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.75rem',
            borderBottom: '2px solid var(--accent-gold)'
          }}
        >
          <span>⚖️ <strong>Ley N° 29733:</strong> Como estudiante institucional, debes autorizar el uso académico de tus datos para el algoritmo de emparejamiento.</span>
          <button
            onClick={() => setIsConsentModalOpen(true)}
            style={{
              background: 'var(--accent-gold)',
              color: '#FFFFFF',
              border: 'none',
              padding: '0.25rem 0.8rem',
              borderRadius: 'var(--radius-pill)',
              fontSize: '0.76rem',
              fontWeight: 700,
              cursor: 'pointer'
            }}
          >
            Firmar Consentimiento
          </button>
        </div>
      )}

      {/* Contenido Principal de las Vistas según Rol y Pestaña */}
      <main className="main-content">
        {/* VISTA ADMINISTRADOR (CUS14, CUS22, CUS13, CUS12) */}
        {currentTab === 'admin' && (
          <AdminView
            certificates={certificates}
            onAddCertificate={(newCert) => setCertificates([newCert, ...certificates])}
          />
        )}

        {/* VISTA MENTOR (CUS09, CUS23, CUS07, CUS11, CUS10, CUS16) */}
        {currentTab === 'mentor' && (
          <MentorFlowView
            bookings={bookings}
            onConfirmBooking={handleConfirmBooking}
            onUpdateBookingStatus={handleUpdateBookingStatus}
            onAddNewOffer={() => {}}
            onAddLog={handleAddLog}
            certificates={certificates}
          />
        )}

        {/* VISTA MENTOREADO (CUS02, CUS03, CUS04, CUS24, CUS11, CUS05) */}
        {currentTab === 'mentee' && (
          <MenteeFlowView
            bookings={bookings}
            onRatifyAttendance={handleRatifyAttendance}
            onOpenConsentModal={() => setIsConsentModalOpen(true)}
            hasAcceptedConsent={hasAcceptedConsent}
            onSelectMentorForBooking={handleSelectMentorForBooking}
          />
        )}

        {/* VISTA CATÁLOGO GENERAL / INICIO */}
        {currentTab === 'home' && (
          <HomeView
            onStartMatching={() => {
              if (currentUser.role === 'mentee') setCurrentTab('mentee');
              else setCurrentTab('recommendation');
            }}
            onOpenBookings={() => {
              if (currentUser.role === 'mentor') setCurrentTab('mentor');
              else if (currentUser.role === 'mentee') setCurrentTab('mentee');
              else setCurrentTab('booking');
            }}
            onSelectMentorForBooking={handleSelectMentorForBooking}
          />
        )}

        {/* VISTA RECOMENDADOR TRADICIONAL */}
        {currentTab === 'recommendation' && (
          <RecommendationView
            onSelectMentorForBooking={handleSelectMentorForBooking}
          />
        )}

        {/* VISTA AGENDAMIENTO TRADICIONAL */}
        {currentTab === 'booking' && (
          <BookingView
            selectedMentorForBooking={selectedMentorForBooking}
            selectedTopicForBooking={selectedTopicForBooking}
            bookings={bookings}
            onAddBooking={handleAddBooking}
            onConfirmBooking={handleConfirmBooking}
            userRole={currentUser.role === 'mentor' ? 'mentor' : 'mentee'}
          />
        )}

        {/* VISTA GAMIFICACIÓN GENERAL */}
        {currentTab === 'gamification' && (
          <GamificationView />
        )}
      </main>

      {/* Pie de Página Institucional */}
      <footer
        style={{
          backgroundColor: 'var(--primary-navy-dark)',
          color: 'rgba(255, 255, 255, 0.7)',
          fontSize: '0.82rem',
          padding: '1.5rem',
          textAlign: 'center',
          marginTop: 'auto',
          borderTop: '1px solid rgba(255, 255, 255, 0.08)'
        }}
      >
        <div style={{ maxWidth: '1100px', margin: '0 auto', display: 'flex', flexDirection: 'column', gap: '0.35rem' }}>
          <p style={{ color: '#FFFFFF', fontWeight: 600 }}>
            Universidad Privada de Tacna • Escuela Profesional de Ingeniería de Sistemas (EPIS)
          </p>
          <p style={{ fontSize: '0.75rem', color: 'rgba(255, 255, 255, 0.5)' }}>
            Sistema Web P2P de Mentorías Académicas • Convalidación oficial de horas extracurriculares
          </p>
        </div>
      </footer>

      {/* Modal de Consentimiento Informado (RF01) */}
      <ConsentModal
        isOpen={isConsentModalOpen}
        onClose={() => setIsConsentModalOpen(false)}
        onAccept={() => setHasAcceptedConsent(true)}
      />
    </div>
  );
}

export default App;
