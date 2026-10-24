import React, { useState, useEffect } from 'react';
import { profileService } from '../services/profileService';
import type { AcademicProfile, AvailabilitySlot } from '../services/profileService';
import { fetchCourses } from '../services/apiClient';
import type { Course } from '../services/apiClient';

export interface ProfileAvailabilityViewProps {
  userEmail?: string;
  onSaved?: () => void;
}

const DAYS_OF_WEEK = [
  { id: 1, name: 'Lunes' },
  { id: 2, name: 'Martes' },
  { id: 3, name: 'Miércoles' },
  { id: 4, name: 'Jueves' },
  { id: 5, name: 'Viernes' },
  { id: 6, name: 'Sábado' },
];

const TIME_SLOTS = [
  { start: '08:00', end: '09:00', label: '08:00 - 09:00' },
  { start: '09:00', end: '10:00', label: '09:00 - 10:00' },
  { start: '10:00', end: '11:00', label: '10:00 - 11:00' },
  { start: '11:00', end: '12:00', label: '11:00 - 12:00' },
  { start: '12:00', end: '13:00', label: '12:00 - 13:00' },
  { start: '14:00', end: '15:00', label: '14:00 - 15:00' },
  { start: '15:00', end: '16:00', label: '15:00 - 16:00' },
  { start: '16:00', end: '17:00', label: '16:00 - 17:00' },
  { start: '17:00', end: '18:00', label: '17:00 - 18:00' },
  { start: '18:00', end: '19:00', label: '18:00 - 19:00' },
  { start: '19:00', end: '20:00', label: '19:00 - 20:00' },
];

export const ProfileAvailabilityView: React.FC<ProfileAvailabilityViewProps> = ({
  userEmail = '2022074255@upt.pe',
  onSaved,
}) => {
  const [email, setEmail] = useState<string>(userEmail);
  const [profile, setProfile] = useState<AcademicProfile | null>(null);
  const [slots, setSlots] = useState<AvailabilitySlot[]>([]);
  const [courses, setCourses] = useState<Course[]>([]);
  const [activeSection, setActiveSection] = useState<'profile' | 'schedule'>(() => {
    if (typeof window !== 'undefined' && window.location) {
      const s = new URLSearchParams(window.location.search).get('section');
      if (s === 'schedule' || s === 'profile') return s;
    }
    return 'profile';
  });
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [isSaving, setIsSaving] = useState<boolean>(false);
  const [notification, setNotification] = useState<{ text: string; type: 'success' | 'error' | 'warning' } | null>(null);

  useEffect(() => {
    setEmail(userEmail);
  }, [userEmail]);

  // Carga inicial de datos
  useEffect(() => {
    let isMounted = true;
    const loadData = async () => {
      setIsLoading(true);
      try {
        const [profData, slotsData, coursesData] = await Promise.all([
          profileService.getProfile(email),
          profileService.getAvailability(email),
          fetchCourses(true).catch(() => []),
        ]);

        if (isMounted) {
          const urlParams = typeof window !== 'undefined' ? new URLSearchParams(window.location.search) : null;
          const initialRole = urlParams?.get('role');
          if (profData && (initialRole === 'mentor' || initialRole === 'mentoreado')) {
            setProfile({ ...profData, rol_postulacion: initialRole });
          } else {
            setProfile(profData);
          }
          setSlots(slotsData);
          setCourses(coursesData);
        }
      } catch (err: unknown) {
        if (isMounted) {
          setNotification({
            text: err instanceof Error ? err.message : 'Error al cargar perfil y disponibilidad.',
            type: 'error',
          });
        }
      } finally {
        if (isMounted) setIsLoading(false);
      }
    };

    if (email) {
      loadData();
    }

    return () => {
      isMounted = false;
    };
  }, [email]);

  // Manejador de cambio de campos del perfil
  const handleProfileChange = <K extends keyof AcademicProfile>(field: K, value: AcademicProfile[K]) => {
    if (!profile) return;
    setProfile({
      ...profile,
      [field]: value,
    });
    setNotification(null);
  };

  // Alternar selección de una asignatura filtro
  const handleToggleCourse = (courseId: number) => {
    if (!profile) return;
    const current = profile.materias_interes || [];
    const exists = current.includes(courseId);
    const updated = exists ? current.filter((id) => id !== courseId) : [...current, courseId];
    handleProfileChange('materias_interes', updated);
  };

  // Alternar una celda en la grilla semanal
  const handleToggleSlot = (dia_semana: number, hora_inicio: string, hora_fin: string) => {
    const isSlotSelected = slots.some(
      (s) => s.dia_semana === dia_semana && s.hora_inicio === hora_inicio
    );

    if (isSlotSelected) {
      setSlots(slots.filter((s) => !(s.dia_semana === dia_semana && s.hora_inicio === hora_inicio)));
    } else {
      setSlots([...slots, { dia_semana, hora_inicio, hora_fin }]);
    }
  };

  // Atajos rápidos para marcar horarios comunes
  const handleQuickSelect = (type: 'mornings' | 'afternoons' | 'clear') => {
    if (type === 'clear') {
      setSlots([]);
      return;
    }

    const filteredSlots = TIME_SLOTS.filter((ts) => {
      const hour = parseInt(ts.start.split(':')[0], 10);
      return type === 'mornings' ? hour >= 8 && hour < 12 : hour >= 14 && hour < 18;
    });

    const newSlots: AvailabilitySlot[] = [];
    DAYS_OF_WEEK.slice(0, 5).forEach((day) => {
      filteredSlots.forEach((slot) => {
        newSlots.push({
          dia_semana: day.id,
          hora_inicio: slot.start,
          hora_fin: slot.end,
        });
      });
    });

    setSlots(newSlots);
  };

  // Guardado general de perfil y disponibilidad
  const handleSaveAll = async () => {
    if (!profile) return;
    setIsSaving(true);
    setNotification(null);

    try {
      // Validar RN-03 si postula a mentor
      if (profile.rol_postulacion === 'mentor') {
        const check = profileService.validateMentorEligibility(profile.ciclo_actual);
        if (!check.eligible) {
          setNotification({
            text: check.reason || 'No cumple con el requisito de mérito para ser mentor.',
            type: 'warning',
          });
          setIsSaving(false);
          return;
        }
      }

      await Promise.all([
        profileService.saveProfile(profile),
        profileService.saveAvailability(email, slots),
      ]);

      setNotification({
        text: `Perfil formativo y agenda semanal (${slots.length} horas) guardados exitosamente conforme a RF04 / CUS15.`,
        type: 'success',
      });

      if (onSaved) onSaved();
    } catch (err: unknown) {
      setNotification({
        text: err instanceof Error ? err.message : 'Error al guardar los datos.',
        type: 'error',
      });
    } finally {
      setIsSaving(false);
    }
  };

  if (isLoading || !profile) {
    return (
      <div style={{ padding: '3rem', textAlign: 'center', color: '#64748B' }}>
        Cargando perfil formativo y agenda semanal...
      </div>
    );
  }

  const isMentorEligible = profile.ciclo_actual >= 7;

  return (
    <div style={{ width: '100%', maxWidth: '1000px', margin: '0 auto' }}>
      {/* Selector de Usuario para Pruebas en Dev */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          padding: '0.85rem 1.25rem',
          border: '1px solid #E2E8F0',
          marginBottom: '1.25rem',
          flexWrap: 'wrap',
          gap: '0.75rem',
        }}
      >
        <div style={{ fontSize: '0.82rem' }}>
          <span style={{ color: '#64748B' }}>Configurando perfil para: </span>
          <strong style={{ color: '#1C2A59' }}>{email}</strong>
          <span style={{ marginLeft: '0.5rem', color: '#B99451', fontWeight: 600 }}>
            ({profile.rol_postulacion === 'mentor' ? '🌟 Mentor' : '🎯 Mentoreado'} · Ciclo {profile.ciclo_actual})
          </span>
        </div>

        <div style={{ display: 'flex', gap: '0.4rem' }}>
          <button
            type="button"
            onClick={() => setEmail('2022074255@upt.pe')}
            style={{
              fontSize: '0.72rem',
              padding: '0.25rem 0.6rem',
              borderRadius: '6px',
              border: '1px solid #CBD5E1',
              background: email.includes('2022074255') ? '#1C2A59' : '#FFFFFF',
              color: email.includes('2022074255') ? '#FFFFFF' : '#334155',
              cursor: 'pointer',
            }}
          >
            Joan (VI Ciclo)
          </button>
          <button
            type="button"
            onClick={() => setEmail('2022073504@upt.pe')}
            style={{
              fontSize: '0.72rem',
              padding: '0.25rem 0.6rem',
              borderRadius: '6px',
              border: '1px solid #CBD5E1',
              background: email.includes('2022073504') ? '#1C2A59' : '#FFFFFF',
              color: email.includes('2022073504') ? '#FFFFFF' : '#334155',
              cursor: 'pointer',
            }}
          >
            Renzo (VII Ciclo Mentor)
          </button>
        </div>
      </div>

      {/* Pestañas de Navegación Interna */}
      <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem' }}>
        <button
          type="button"
          onClick={() => setActiveSection('profile')}
          style={{
            flex: 1,
            padding: '0.75rem 1rem',
            borderRadius: '10px',
            border: activeSection === 'profile' ? '2px solid #1C2A59' : '1px solid #E2E8F0',
            backgroundColor: activeSection === 'profile' ? '#FFFFFF' : '#F8FAFC',
            color: activeSection === 'profile' ? '#1C2A59' : '#64748B',
            fontWeight: 700,
            fontSize: '0.88rem',
            cursor: 'pointer',
            boxShadow: activeSection === 'profile' ? '0 4px 12px rgba(28, 42, 89, 0.08)' : 'none',
          }}
        >
          👤 1. Perfil Formativo Académico
        </button>
        <button
          type="button"
          onClick={() => setActiveSection('schedule')}
          style={{
            flex: 1,
            padding: '0.75rem 1rem',
            borderRadius: '10px',
            border: activeSection === 'schedule' ? '2px solid #1C2A59' : '1px solid #E2E8F0',
            backgroundColor: activeSection === 'schedule' ? '#FFFFFF' : '#F8FAFC',
            color: activeSection === 'schedule' ? '#1C2A59' : '#64748B',
            fontWeight: 700,
            fontSize: '0.88rem',
            cursor: 'pointer',
            boxShadow: activeSection === 'schedule' ? '0 4px 12px rgba(28, 42, 89, 0.08)' : 'none',
          }}
        >
          📅 2. Matriz Semanal de Disponibilidad ({slots.length} horas)
        </button>
      </div>

      {/* Notificaciones */}
      {notification && (
        <div
          role="alert"
          style={{
            padding: '0.85rem 1.25rem',
            borderRadius: '8px',
            marginBottom: '1.25rem',
            fontSize: '0.84rem',
            backgroundColor:
              notification.type === 'success'
                ? '#F0FDF4'
                : notification.type === 'error'
                ? '#FEF2F2'
                : '#FFFBEB',
            color:
              notification.type === 'success'
                ? '#166534'
                : notification.type === 'error'
                ? '#991B1B'
                : '#92400E',
            border: `1px solid ${
              notification.type === 'success'
                ? '#BBF7D0'
                : notification.type === 'error'
                ? '#FECACA'
                : '#FDE68A'
            }`,
          }}
        >
          {notification.text}
        </div>
      )}

      {/* SECCIÓN 1: PERFIL FORMATIVO */}
      {activeSection === 'profile' && (
        <div
          style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '16px',
            padding: '1.75rem',
            border: '1px solid #E2E8F0',
            boxShadow: '0 4px 12px rgba(28, 42, 89, 0.05)',
          }}
        >
          <div style={{ borderBottom: '1px solid #E2E8F0', paddingBottom: '0.75rem', marginBottom: '1.25rem' }}>
            <h3 style={{ margin: '0 0 0.25rem 0', color: '#1C2A59', fontSize: '1.15rem', fontWeight: 800 }}>
              Configuración del Perfil Académico (CUS15 / RF04)
            </h3>
            <p style={{ margin: 0, fontSize: '0.82rem', color: '#64748B' }}>
              Define tu avance curricular, materias filtro prioritarias y modalidad de aprendizaje preferida.
            </p>
          </div>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))', gap: '1.25rem', marginBottom: '1.5rem' }}>
            {/* Ciclo Formativo Actual */}
            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.35rem' }}>
                Ciclo Académico Actual (EPIS):
              </label>
              <select
                value={profile.ciclo_actual}
                onChange={(e) => handleProfileChange('ciclo_actual', Number(e.target.value))}
                style={{
                  width: '100%',
                  padding: '0.55rem 0.85rem',
                  borderRadius: '8px',
                  border: '1px solid #CBD5E1',
                  fontSize: '0.85rem',
                  color: '#1E293B',
                  backgroundColor: '#FFFFFF',
                }}
              >
                {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map((c) => (
                  <option key={c} value={c}>
                    Ciclo {c} {c >= 7 ? '• Habilitado para Mentoría' : '• Ciclo Inicial/Intermedio'}
                  </option>
                ))}
              </select>
            </div>

            {/* Rol de Participación / Intención */}
            <div>
              <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.35rem' }}>
                Rol de Participación en la Plataforma:
              </label>
              <div style={{ display: 'flex', gap: '0.5rem' }}>
                <button
                  type="button"
                  onClick={() => handleProfileChange('rol_postulacion', 'mentoreado')}
                  style={{
                    flex: 1,
                    padding: '0.55rem',
                    borderRadius: '8px',
                    border: profile.rol_postulacion === 'mentoreado' ? '2px solid #1C2A59' : '1px solid #CBD5E1',
                    background: profile.rol_postulacion === 'mentoreado' ? '#EFF6FF' : '#FFFFFF',
                    color: profile.rol_postulacion === 'mentoreado' ? '#1C2A59' : '#64748B',
                    fontWeight: 700,
                    fontSize: '0.82rem',
                    cursor: 'pointer',
                  }}
                >
                  🎯 Mentoreado (Solicitar Asesoría)
                </button>
                <button
                  type="button"
                  onClick={() => handleProfileChange('rol_postulacion', 'mentor')}
                  style={{
                    flex: 1,
                    padding: '0.55rem',
                    borderRadius: '8px',
                    border: profile.rol_postulacion === 'mentor' ? '2px solid #B99451' : '1px solid #CBD5E1',
                    background: profile.rol_postulacion === 'mentor' ? '#FEFCE8' : '#FFFFFF',
                    color: profile.rol_postulacion === 'mentor' ? '#854D0E' : '#64748B',
                    fontWeight: 700,
                    fontSize: '0.82rem',
                    cursor: 'pointer',
                  }}
                >
                  🌟 Postulante a Mentor (Enseñar)
                </button>
              </div>
            </div>
          </div>

          {/* Advertencia de la Regla de Negocio RN-03 */}
          {profile.rol_postulacion === 'mentor' && !isMentorEligible && (
            <div
              style={{
                backgroundColor: '#FEF2F2',
                border: '1px solid #FECACA',
                borderRadius: '8px',
                padding: '0.75rem 1rem',
                marginBottom: '1.25rem',
                fontSize: '0.82rem',
                color: '#991B1B',
              }}
            >
              ⚠️ <strong>Regla de Mérito RN-03:</strong> Tu ciclo actual ({profile.ciclo_actual}) es menor al VII ciclo. La acreditación oficial como Mentor requiere estar cursando del VII al X ciclo y haber aprobado las asignaturas críticas.
            </div>
          )}

          {/* Modalidad de Preferencia */}
          <div style={{ marginBottom: '1.25rem' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.35rem' }}>
              Modalidad de Mentoría Preferida:
            </label>
            <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
              {[
                { id: 'presencial', label: '🏫 Presencial (Laboratorios EPIS / Aulas UPT)' },
                { id: 'virtual', label: '💻 Virtual (Google Meet / Discord Oficial)' },
                { id: 'hibrida', label: '🔄 Híbrida (Flexible)' },
              ].map((mod) => (
                <label
                  key={mod.id}
                  style={{
                    display: 'flex',
                    alignItems: 'center',
                    gap: '0.4rem',
                    fontSize: '0.82rem',
                    color: '#334155',
                    cursor: 'pointer',
                    background: profile.modalidad_preferida === mod.id ? '#F0FDF4' : '#F8FAFC',
                    padding: '0.45rem 0.85rem',
                    borderRadius: '6px',
                    border: `1px solid ${profile.modalidad_preferida === mod.id ? '#86EFAC' : '#E2E8F0'}`,
                  }}
                >
                  <input
                    type="radio"
                    name="modalidad"
                    checked={profile.modalidad_preferida === mod.id}
                    onChange={() => handleProfileChange('modalidad_preferida', mod.id as 'presencial' | 'virtual' | 'hibrida')}
                    style={{ accentColor: '#1C2A59' }}
                  />
                  {mod.label}
                </label>
              ))}
            </div>
          </div>

          {/* Selección de Asignaturas Filtro de Interés / Fortaleza */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.35rem' }}>
              {profile.rol_postulacion === 'mentor'
                ? 'Asignaturas filtro que dominas y puedes asesorar (Fortalezas):'
                : 'Asignaturas filtro en las que requieres mentoría académica (Necesidades):'}
            </label>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '0.65rem' }}>
              {courses.length > 0 ? (
                courses.map((c) => {
                  const isChecked = (profile.materias_interes || []).includes(c.id_asignatura);
                  return (
                    <div
                      key={c.id_asignatura}
                      onClick={() => handleToggleCourse(c.id_asignatura)}
                      style={{
                        padding: '0.65rem 0.85rem',
                        borderRadius: '8px',
                        border: isChecked ? '2px solid #1C2A59' : '1px solid #CBD5E1',
                        backgroundColor: isChecked ? '#EFF6FF' : '#FFFFFF',
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.5rem',
                      }}
                    >
                      <input
                        type="checkbox"
                        checked={isChecked}
                        onChange={() => {}} // Manejado por div
                        style={{ accentColor: '#1C2A59' }}
                      />
                      <div>
                        <span style={{ fontSize: '0.72rem', color: '#B99451', fontWeight: 700, display: 'block' }}>
                          {c.codigo_curso} · Ciclo {c.ciclo_plan}
                        </span>
                        <strong style={{ fontSize: '0.84rem', color: '#1E293B' }}>{c.nombre_curso}</strong>
                      </div>
                    </div>
                  );
                })
              ) : (
                <div style={{ fontSize: '0.8rem', color: '#64748B' }}>Cargando catálogo formativo...</div>
              )}
            </div>
          </div>

          {/* Breve semblanza / Biografía académica */}
          <div style={{ marginBottom: '1.5rem' }}>
            <label style={{ display: 'block', fontSize: '0.82rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.35rem' }}>
              Semblanza y Temas de Enfoque Específico:
            </label>
            <textarea
              rows={3}
              value={profile.biografia}
              onChange={(e) => handleProfileChange('biografia', e.target.value)}
              placeholder="Indica temas específicos del sílabo donde tienes mayores dudas o fortalezas (ej. Punteros en C++, Derivadas parciales, Normalización Boyce-Codd)..."
              style={{
                width: '100%',
                padding: '0.65rem',
                borderRadius: '8px',
                border: '1px solid #CBD5E1',
                fontSize: '0.82rem',
                fontFamily: 'inherit',
                resize: 'vertical',
              }}
            />
          </div>
        </div>
      )}

      {/* SECCIÓN 2: MATRIZ SEMANAL DE DISPONIBILIDAD */}
      {activeSection === 'schedule' && (
        <div
          style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '16px',
            padding: '1.75rem',
            border: '1px solid #E2E8F0',
            boxShadow: '0 4px 12px rgba(28, 42, 89, 0.05)',
          }}
        >
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap', gap: '0.75rem', borderBottom: '1px solid #E2E8F0', paddingBottom: '0.75rem', marginBottom: '1.25rem' }}>
            <div>
              <h3 style={{ margin: '0 0 0.25rem 0', color: '#1C2A59', fontSize: '1.15rem', fontWeight: 800 }}>
                Agenda Semanal de Disponibilidad (RF04 / CUS15)
              </h3>
              <p style={{ margin: 0, fontSize: '0.82rem', color: '#64748B' }}>
                Haz clic sobre las franjas horarias en las que tienes disponibilidad para recibir o brindar mentorías.
              </p>
            </div>

            <div style={{ display: 'flex', gap: '0.4rem' }}>
              <button
                type="button"
                onClick={() => handleQuickSelect('mornings')}
                style={{
                  fontSize: '0.75rem',
                  padding: '0.3rem 0.65rem',
                  borderRadius: '6px',
                  border: '1px solid #CBD5E1',
                  background: '#FFFFFF',
                  cursor: 'pointer',
                  color: '#334155',
                }}
              >
                🌅 Mañanas (08:00-12:00)
              </button>
              <button
                type="button"
                onClick={() => handleQuickSelect('afternoons')}
                style={{
                  fontSize: '0.75rem',
                  padding: '0.3rem 0.65rem',
                  borderRadius: '6px',
                  border: '1px solid #CBD5E1',
                  background: '#FFFFFF',
                  cursor: 'pointer',
                  color: '#334155',
                }}
              >
                🌇 Tardes (14:00-18:00)
              </button>
              <button
                type="button"
                onClick={() => handleQuickSelect('clear')}
                style={{
                  fontSize: '0.75rem',
                  padding: '0.3rem 0.65rem',
                  borderRadius: '6px',
                  border: '1px solid #FECACA',
                  background: '#FEF2F2',
                  cursor: 'pointer',
                  color: '#991B1B',
                }}
              >
                🗑️ Limpiar
              </button>
            </div>
          </div>

          {/* Grilla Semanal */}
          <div style={{ overflowX: 'auto', marginBottom: '1.25rem' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', textAlign: 'center', fontSize: '0.78rem' }}>
              <thead>
                <tr style={{ backgroundColor: '#1C2A59', color: '#FFFFFF' }}>
                  <th style={{ padding: '0.65rem', border: '1px solid #1C2A59', width: '110px' }}>Horario</th>
                  {DAYS_OF_WEEK.map((d) => (
                    <th key={d.id} style={{ padding: '0.65rem', border: '1px solid #2B3D75' }}>
                      {d.name}
                    </th>
                  ))}
                </tr>
              </thead>
              <tbody>
                {TIME_SLOTS.map((ts) => (
                  <tr key={ts.start}>
                    <td style={{ padding: '0.5rem', backgroundColor: '#F8FAFC', fontWeight: 600, color: '#475569', border: '1px solid #E2E8F0' }}>
                      {ts.label}
                    </td>
                    {DAYS_OF_WEEK.map((day) => {
                      const isSelected = slots.some(
                        (s) => s.dia_semana === day.id && s.hora_inicio === ts.start
                      );
                      return (
                        <td
                          key={day.id}
                          onClick={() => handleToggleSlot(day.id, ts.start, ts.end)}
                          style={{
                            border: '1px solid #E2E8F0',
                            padding: '0.4rem',
                            cursor: 'pointer',
                            backgroundColor: isSelected ? '#10B981' : '#FFFFFF',
                            color: isSelected ? '#FFFFFF' : 'transparent',
                            transition: 'background-color 0.15s ease',
                          }}
                          title={`${day.name} ${ts.label}: ${isSelected ? 'Disponible (clic para quitar)' : 'No disponible (clic para marcar)'}`}
                        >
                          {isSelected ? '✓' : '·'}
                        </td>
                      );
                    })}
                  </tr>
                ))}
              </tbody>
            </table>
          </div>

          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', fontSize: '0.8rem', color: '#64748B' }}>
            <span>
              Total comprometido: <strong style={{ color: '#1C2A59' }}>{slots.length} bloques de 1 hora</strong> ({slots.length} h semanales).
            </span>
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
              <span style={{ width: '12px', height: '12px', backgroundColor: '#10B981', display: 'inline-block', borderRadius: '2px' }}></span>
              <span>Disponible</span>
              <span style={{ width: '12px', height: '12px', backgroundColor: '#FFFFFF', border: '1px solid #CBD5E1', display: 'inline-block', borderRadius: '2px', marginLeft: '0.5rem' }}></span>
              <span>No disponible</span>
            </div>
          </div>
        </div>
      )}

      {/* Botón de Guardado General */}
      <div style={{ display: 'flex', justifyContent: 'flex-end', marginTop: '1.5rem', gap: '0.75rem' }}>
        <button
          type="button"
          onClick={handleSaveAll}
          disabled={isSaving}
          style={{
            backgroundColor: isSaving ? '#94A3B8' : '#1C2A59',
            color: '#FFFFFF',
            border: 'none',
            borderRadius: '8px',
            padding: '0.75rem 2rem',
            fontSize: '0.9rem',
            fontWeight: 700,
            cursor: isSaving ? 'not-allowed' : 'pointer',
            boxShadow: '0 4px 12px rgba(28, 42, 89, 0.15)',
            transition: 'background-color 0.2s',
          }}
        >
          {isSaving ? 'Guardando datos...' : '💾 Guardar Perfil y Disponibilidad'}
        </button>
      </div>
    </div>
  );
};
