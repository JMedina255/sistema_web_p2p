import { useState } from 'react';
import { Navigation } from './components/Navigation';
import { LateralDocks } from './components/LateralDocks';
import { ConsentModal } from './components/ConsentModal';
import { HomeView } from './components/HomeView';
import { RecommendationView } from './components/RecommendationView';
import { BookingView } from './components/BookingView';
import { GamificationView } from './components/GamificationView';
import { INITIAL_BOOKINGS } from './data/mockData';
import type { Mentor, SessionBooking } from './data/mockData';

export function App() {
  const [currentTab, setCurrentTab] = useState<'home' | 'recommendation' | 'booking' | 'gamification'>('home');
  const [userRole, setUserRole] = useState<'mentee' | 'mentor'>('mentee');
  const [isConsentModalOpen, setIsConsentModalOpen] = useState<boolean>(false);
  const [hasAcceptedConsent, setHasAcceptedConsent] = useState<boolean>(false);

  // Estado global de sesiones
  const [bookings, setBookings] = useState<SessionBooking[]>(INITIAL_BOOKINGS);
  const [selectedMentorForBooking, setSelectedMentorForBooking] = useState<Mentor | null>(null);
  const [selectedTopicForBooking, setSelectedTopicForBooking] = useState<string>('');

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

  return (
    <div style={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
      {/* Navegación Dual Institucional */}
      <Navigation
        currentTab={currentTab}
        setCurrentTab={setCurrentTab}
        userRole={userRole}
        setUserRole={setUserRole}
        onOpenConsentModal={() => setIsConsentModalOpen(true)}
      />

      {/* Docks Flotantes Laterales */}
      <LateralDocks />

      {/* Notificación Superior si aún no ha firmado el Consentimiento Ley 29733 */}
      {!hasAcceptedConsent && (
        <div
          style={{
            backgroundColor: '#1C2A59',
            color: '#FFFFFF',
            padding: '0.5rem 1.5rem',
            textAlign: 'center',
            fontSize: '0.8rem',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '0.75rem',
            borderBottom: '2px solid var(--accent-gold)'
          }}
        >
          <span>⚖️ <strong>Ley N° 29733:</strong> Acepta el uso académico de tus datos para el emparejamiento de mentorías.</span>
          <button
            onClick={() => setIsConsentModalOpen(true)}
            style={{
              background: 'var(--accent-gold)',
              color: '#FFFFFF',
              border: 'none',
              padding: '0.25rem 0.75rem',
              borderRadius: 'var(--radius-pill)',
              fontSize: '0.74rem',
              fontWeight: 700,
              cursor: 'pointer'
            }}
          >
            Firmar Consentimiento
          </button>
        </div>
      )}

      {/* Contenido Principal de las Vistas */}
      <main className="main-content">
        {currentTab === 'home' && (
          <HomeView
            onStartMatching={() => setCurrentTab('recommendation')}
            onOpenBookings={() => setCurrentTab('booking')}
            onSelectMentorForBooking={handleSelectMentorForBooking}
          />
        )}

        {currentTab === 'recommendation' && (
          <RecommendationView
            onSelectMentorForBooking={handleSelectMentorForBooking}
          />
        )}

        {currentTab === 'booking' && (
          <BookingView
            selectedMentorForBooking={selectedMentorForBooking}
            selectedTopicForBooking={selectedTopicForBooking}
            bookings={bookings}
            onAddBooking={handleAddBooking}
            onConfirmBooking={handleConfirmBooking}
            userRole={userRole}
          />
        )}

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
