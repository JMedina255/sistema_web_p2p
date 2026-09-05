import React, { useState, useMemo } from 'react';
import { MOCK_MENTORS } from '../data/mockData';
import type { Mentor, SessionBooking } from '../data/mockData';

interface BookingViewProps {
  selectedMentorForBooking: Mentor | null;
  selectedTopicForBooking: string;
  bookings: SessionBooking[];
  onAddBooking: (booking: SessionBooking) => void;
  onConfirmBooking: (sessionId: string) => void;
  userRole: 'mentee' | 'mentor';
}

export const BookingView: React.FC<BookingViewProps> = ({
  selectedMentorForBooking,
  selectedTopicForBooking,
  bookings,
  onAddBooking,
  onConfirmBooking,
  userRole
}) => {
  const [activeMentor, setActiveMentor] = useState<Mentor>(selectedMentorForBooking || MOCK_MENTORS[0]);
  const [chosenTopic, setChosenTopic] = useState<string>(selectedTopicForBooking || 'Estructuras de Datos y Recursividad');
  const [selectedSlotId, setSelectedSlotId] = useState<string>(
    (selectedMentorForBooking || MOCK_MENTORS[0]).availabilitySlots[0]?.id || ''
  );
  const [bookingSuccessMessage, setBookingSuccessMessage] = useState<string | null>(null);

  // Buscador de mentor por escritura (sin selector tradicional)
  const [isSearchingMentor, setIsSearchingMentor] = useState<boolean>(false);
  const [mentorSearchText, setMentorSearchText] = useState<string>('');

  // Sincronizar reactivamente si cambia la selección desde Home o Recomendador
  const [prevPropMentor, setPrevPropMentor] = useState<Mentor | null>(selectedMentorForBooking);
  const [prevPropTopic, setPrevPropTopic] = useState<string>(selectedTopicForBooking);

  if (selectedMentorForBooking && selectedMentorForBooking !== prevPropMentor) {
    setPrevPropMentor(selectedMentorForBooking);
    setActiveMentor(selectedMentorForBooking);
    if (selectedMentorForBooking.availabilitySlots.length > 0) {
      setSelectedSlotId(selectedMentorForBooking.availabilitySlots[0].id);
    }
  }

  if (selectedTopicForBooking && selectedTopicForBooking !== prevPropTopic) {
    setPrevPropTopic(selectedTopicForBooking);
    setChosenTopic(selectedTopicForBooking);
  }

  const filteredMentors = useMemo(() => {
    if (!mentorSearchText.trim()) return MOCK_MENTORS;
    const q = mentorSearchText.toLowerCase().trim();
    return MOCK_MENTORS.filter(m =>
      m.name.toLowerCase().includes(q) ||
      m.subjectSpecialties.some(s => s.toLowerCase().includes(q)) ||
      m.cycle.toLowerCase().includes(q)
    );
  }, [mentorSearchText]);

  const handleBookSession = () => {
    const slot = activeMentor.availabilitySlots.find(s => s.id === selectedSlotId) || activeMentor.availabilitySlots[0];
    const newSession: SessionBooking = {
      id: `ses-${Date.now().toString().slice(-4)}`,
      mentorName: activeMentor.name,
      studentName: 'Estudiante Mentoreado Demo (II Ciclo)',
      subjectName: activeMentor.subjectSpecialties[0] || 'Asignatura Crítica',
      topic: chosenTopic,
      day: slot?.day || 'Viernes',
      time: slot?.time || '10:00 - 11:30 AM',
      status: 'PENDIENTE',
      dateFormatted: `Próximo ${slot?.day || 'Viernes'}, ${slot?.time || '10:00 AM'}`
    };

    onAddBooking(newSession);
    setBookingSuccessMessage(`¡Solicitud de mentoría enviada a ${activeMentor.name}!`);
    setTimeout(() => setBookingSuccessMessage(null), 3500);
  };

  return (
    <div className="fade-in">
      <div style={{ marginBottom: '1.75rem' }}>
        <div style={{ display: 'inline-flex', alignItems: 'center', gap: '0.4rem', marginBottom: '0.35rem' }}>
          <span className="badge badge-gold">Agendamiento P2P</span>
          <span className="badge badge-navy">Horarios Verificados</span>
        </div>
        <h2 style={{ fontSize: '1.65rem', color: 'var(--primary-navy)' }}>
          Reserva y Coordinación de Citas
        </h2>
        <p style={{ color: 'var(--text-body)', fontSize: '0.9rem', maxWidth: '750px' }}>
          Selecciona tu mentor, tema y bloque de horario disponible para coordinar tu sesión.
        </p>
      </div>

      {bookingSuccessMessage && (
        <div
          style={{
            backgroundColor: '#E6F4EA',
            color: '#137333',
            padding: '0.85rem 1.25rem',
            borderRadius: '12px',
            marginBottom: '1.5rem',
            border: '1px solid #CEEAD6',
            fontWeight: 600,
            display: 'flex',
            alignItems: 'center',
            gap: '0.6rem',
            boxShadow: '0 2px 8px rgba(19, 115, 51, 0.08)'
          }}
        >
          <span>✓</span>
          <span>{bookingSuccessMessage}</span>
        </div>
      )}

      <div style={{ display: 'grid', gridTemplateColumns: '1.2fr 1.8fr', gap: '1.75rem' }}>
        {/* Columna 1: Formulario de Reserva */}
        <div className="upt-card">
          <h3 style={{ fontSize: '1rem', color: 'var(--primary-navy)', marginBottom: '1rem' }}>
            Nueva Solicitud de Mentoría
          </h3>

          {/* Mentor Seleccionado (Tarjeta interactiva con opción de búsqueda por escritura) */}
          <div style={{ marginBottom: '1.25rem' }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.4rem' }}>
              <label style={{ fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-heading)' }}>
                Estudiante Mentor:
              </label>
              <button
                type="button"
                onClick={() => setIsSearchingMentor(!isSearchingMentor)}
                style={{
                  background: 'none',
                  border: 'none',
                  color: 'var(--primary-blue)',
                  fontSize: '0.78rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                  padding: 0
                }}
              >
                {isSearchingMentor ? 'Cerrar búsqueda ✕' : 'Cambiar mentor por búsqueda 🔍'}
              </button>
            </div>

            {/* Cuadro de Búsqueda por Escritura si el usuario desea cambiar de mentor */}
            {isSearchingMentor ? (
              <div style={{ background: 'var(--bg-page)', padding: '0.75rem', borderRadius: '12px', border: '1.5px solid var(--accent-gold)', marginBottom: '0.75rem' }}>
                <input
                  type="text"
                  value={mentorSearchText}
                  onChange={(e) => setMentorSearchText(e.target.value)}
                  placeholder="Escribe el nombre o materia del mentor..."
                  style={{
                    width: '100%',
                    padding: '0.5rem 0.75rem',
                    borderRadius: '8px',
                    border: '1px solid var(--border-color)',
                    fontSize: '0.85rem',
                    marginBottom: '0.5rem',
                    outline: 'none'
                  }}
                  autoFocus
                />
                <div style={{ maxHeight: '180px', overflowY: 'auto', display: 'flex', flexDirection: 'column', gap: '0.4rem' }}>
                  {filteredMentors.map((m) => (
                    <div
                      key={m.id}
                      onClick={() => {
                        setActiveMentor(m);
                        if (m.availabilitySlots.length > 0) {
                          setSelectedSlotId(m.availabilitySlots[0].id);
                        }
                        setIsSearchingMentor(false);
                      }}
                      style={{
                        padding: '0.45rem 0.6rem',
                        borderRadius: '8px',
                        backgroundColor: activeMentor.id === m.id ? 'rgba(185, 148, 81, 0.15)' : '#FFFFFF',
                        border: '1px solid var(--border-color)',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.6rem'
                      }}
                    >
                      <img src={m.avatar} alt={m.name} style={{ width: '28px', height: '28px', borderRadius: '50%' }} />
                      <div style={{ flex: 1, minWidth: 0 }}>
                        <div style={{ fontSize: '0.8rem', fontWeight: 700, color: 'var(--primary-navy)' }}>{m.name}</div>
                        <div style={{ fontSize: '0.7rem', color: 'var(--text-muted)' }}>{m.cycle} • {m.subjectSpecialties.slice(0, 2).join(', ')}</div>
                      </div>
                      <span style={{ fontSize: '0.75rem', color: 'var(--accent-gold-dark)', fontWeight: 700 }}>★ {m.rating}</span>
                    </div>
                  ))}
                </div>
              </div>
            ) : (
              /* Tarjeta del Mentor Activo */
              <div
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.85rem',
                  padding: '0.75rem 1rem',
                  backgroundColor: 'var(--bg-page)',
                  borderRadius: '12px',
                  border: '1.5px solid var(--border-color)'
                }}
              >
                <img
                  src={activeMentor.avatar}
                  alt={activeMentor.name}
                  style={{ width: '48px', height: '48px', borderRadius: '50%', border: '2px solid var(--accent-gold)' }}
                />
                <div style={{ flex: 1 }}>
                  <div style={{ fontSize: '0.92rem', fontWeight: 700, color: 'var(--primary-navy)' }}>
                    {activeMentor.name}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: 'var(--text-muted)' }}>
                    {activeMentor.cycle} • Código: <code>{activeMentor.code}</code>
                  </div>
                  <div style={{ fontSize: '0.74rem', color: 'var(--text-gold)', fontWeight: 600, marginTop: '0.2rem' }}>
                    ★ {activeMentor.rating} ({activeMentor.reviewsCount} valoraciones) • {activeMentor.totalHours} hrs
                  </div>
                </div>
              </div>
            )}
          </div>

          {/* Tema a Reforzar */}
          <div style={{ marginBottom: '1.25rem' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.4rem' }}>
              Tema o Consulta a Resolver:
            </label>
            <input
              type="text"
              value={chosenTopic}
              onChange={(e) => setChosenTopic(e.target.value)}
              placeholder="Ej: Recursividad y punteros en C++..."
              style={{
                width: '100%',
                padding: '0.6rem 0.8rem',
                borderRadius: '8px',
                border: '1.5px solid var(--border-color)',
                fontFamily: 'inherit',
                fontSize: '0.88rem',
                backgroundColor: 'var(--bg-page)',
                color: 'var(--text-heading)',
                outline: 'none'
              }}
            />
          </div>

          {/* Franjas Horarias Disponibles */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: 'var(--text-heading)', marginBottom: '0.5rem' }}>
              Selecciona el Horario Disponible:
            </label>
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.45rem' }}>
              {activeMentor.availabilitySlots.map((slot) => (
                <div
                  key={slot.id}
                  onClick={() => setSelectedSlotId(slot.id)}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'space-between',
                    padding: '0.65rem 0.9rem',
                    borderRadius: '10px',
                    border: selectedSlotId === slot.id ? '2px solid var(--accent-gold)' : '1px solid var(--border-color)',
                    backgroundColor: selectedSlotId === slot.id ? 'rgba(185, 148, 81, 0.08)' : 'var(--bg-page)',
                    cursor: 'pointer',
                    transition: 'all 0.15s ease'
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                    <span>📅</span>
                    <div>
                      <strong style={{ fontSize: '0.84rem', color: 'var(--primary-navy)' }}>{slot.day}</strong>
                      <div style={{ fontSize: '0.76rem', color: 'var(--text-muted)' }}>{slot.time}</div>
                    </div>
                  </div>
                  <span className="badge badge-success" style={{ fontSize: '0.68rem' }}>Disponible</span>
                </div>
              ))}
            </div>
          </div>

          <button
            className="btn-gold"
            onClick={handleBookSession}
            style={{ width: '100%', padding: '0.7rem' }}
          >
            Confirmar Reserva de Sesión
          </button>
        </div>

        {/* Columna 2: Bandeja de Sesiones */}
        <div>
          <div className="upt-card">
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1.25rem' }}>
              <h3 style={{ fontSize: '1rem', color: 'var(--primary-navy)', margin: 0 }}>
                Agenda de Sesiones
              </h3>
              <div style={{ display: 'flex', gap: '0.4rem' }}>
                <span className="badge badge-gold" style={{ fontSize: '0.68rem' }}>
                  {userRole === 'mentor' ? 'Vista: Mentor' : 'Vista: Mentoreado'}
                </span>
                <span className="badge badge-navy" style={{ fontSize: '0.68rem' }}>
                  {bookings.length} Sesiones
                </span>
              </div>
            </div>

            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem' }}>
              {bookings.map((booking) => {
                const isPending = booking.status === 'PENDIENTE';
                return (
                  <div
                    key={booking.id}
                    style={{
                      border: '1px solid var(--border-color)',
                      borderRadius: '12px',
                      padding: '1rem',
                      backgroundColor: isPending ? 'rgba(255, 248, 230, 0.35)' : '#FFFFFF',
                      display: 'flex',
                      flexDirection: 'column',
                      gap: '0.6rem',
                      boxShadow: '0 2px 6px rgba(0,0,0,0.02)'
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
                      <div>
                        <span className="badge badge-navy" style={{ fontSize: '0.68rem', marginBottom: '0.25rem' }}>
                          {booking.subjectName}
                        </span>
                        <h4 style={{ fontSize: '0.98rem', color: 'var(--primary-navy)', margin: '0.15rem 0' }}>
                          {booking.topic}
                        </h4>
                      </div>

                      <span
                        className="badge"
                        style={{
                          backgroundColor: isPending ? 'rgba(185, 148, 81, 0.15)' : '#E6F4EA',
                          color: isPending ? 'var(--accent-gold-dark)' : '#137333',
                          border: isPending ? '1px solid rgba(185, 148, 81, 0.3)' : '1px solid #CEEAD6',
                          fontSize: '0.72rem'
                        }}
                      >
                        ● {booking.status}
                      </span>
                    </div>

                    <div style={{ display: 'grid', gridTemplateColumns: 'repeat(3, 1fr)', gap: '0.4rem', fontSize: '0.78rem', color: 'var(--text-body)', borderTop: '1px dashed var(--border-color)', paddingTop: '0.6rem' }}>
                      <div>
                        <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.68rem' }}>Mentor:</span>
                        <strong>{booking.mentorName}</strong>
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.68rem' }}>Estudiante:</span>
                        <span>{booking.studentName}</span>
                      </div>
                      <div>
                        <span style={{ color: 'var(--text-muted)', display: 'block', fontSize: '0.68rem' }}>Horario:</span>
                        <strong>{booking.dateFormatted}</strong>
                      </div>
                    </div>

                    {isPending && (
                      <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '0.2rem' }}>
                        <button
                          className="btn-gold btn-sm"
                          onClick={() => onConfirmBooking(booking.id)}
                          style={{ fontSize: '0.75rem', padding: '0.35rem 0.75rem' }}
                        >
                          ✓ Confirmar Sesión
                        </button>
                      </div>
                    )}
                  </div>
                );
              })}
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};
