/**
 * Vista: Mis Mentorías Publicadas, Supervisión de Quórum y Resolución de Contingencias (T-32 / Sprint 6)
 *
 * Trazabilidad:
 * - Requerimiento Funcional: RF08 (Gestión de ofertas), RF16 (Gestión resolutiva ante quórum insuficiente)
 * - Casos de Uso: CUS06, CUS07, CUS23
 * - Regla de Negocio RN-04: Antelación mínima de 24 horas para reprogramación
 * - Regla de Negocio RN-05: Aforo inmutable (10 presencial / 20 virtual) y mínimo 3 confirmados
 * - Regla de Negocio RN-10: Decisión resolutiva del mentor ante quórum insuficiente
 * - Requerimiento No Funcional: RNF05 (Accesibilidad WCAG 2.1 AA / WAI-ARIA)
 */

import React, { useState, useEffect, useCallback } from 'react';
import {
  offerService,
  type PublishOfferResponse,
  type QuorumDecisionPayload,
} from '../services/offerService';
import { authService } from '../services/authService';
import { SessionAttendanceView } from './SessionAttendanceView';
import { BitacoraFormView } from './BitacoraFormView';

export interface MentorSessionsViewProps {
  mentorEmail: string;
  onNavigateToPublish?: () => void;
  onPublishNewOffer?: () => void;
}

interface EnrolledStudent {
  id_reserva: number;
  codigo_reserva: string;
  estudiante_email: string;
  estado: string;
  fecha_reserva: string;
  fecha_ratificacion?: string | null;
}

export const MentorSessionsView: React.FC<MentorSessionsViewProps> = ({
  mentorEmail,
  onNavigateToPublish,
  onPublishNewOffer,
}) => {
  const handlePublish = onNavigateToPublish || onPublishNewOffer;
  const [sessions, setSessions] = useState<PublishOfferResponse[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [error, setError] = useState<string | null>(null);

  // Vistas activas de Asistencia y Bitácora
  const [selectedAttendanceSession, setSelectedAttendanceSession] = useState<PublishOfferResponse | null>(null);
  const [selectedBitacoraSession, setSelectedBitacoraSession] = useState<PublishOfferResponse | null>(null);

  // Mapa de nóminas de estudiantes por ID de sesión
  const [rosters, setRosters] = useState<Record<string, EnrolledStudent[]>>({});
  const [loadingRosterId, setLoadingRosterId] = useState<string | null>(null);
  const [expandedSessionId, setExpandedSessionId] = useState<string | null>(null);
  const [now] = useState(() => Date.now());

  // Estado del Diálogo Modal de Contingencia de Quórum (T-32 / WCAG 2.1 AA)
  const [contingencySession, setContingencySession] = useState<PublishOfferResponse | null>(null);
  const [contingencyDecision, setContingencyDecision] = useState<'PROCEED' | 'RESCHEDULE' | 'CANCEL'>('PROCEED');
  const [rescheduleDate, setRescheduleDate] = useState<string>('');
  const [cancelReason, setCancelReason] = useState<string>('');
  const [isSubmittingContingency, setIsSubmittingContingency] = useState<boolean>(false);
  const [contingencyError, setContingencyError] = useState<string | null>(null);
  const [statusMessage, setStatusMessage] = useState<string | null>(null);

  const fetchSessions = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const data = await offerService.getOffers(mentorEmail);
      setSessions(data);
    } catch {
      setError('No fue posible cargar las sesiones publicadas del mentor.');
    } finally {
      setIsLoading(false);
    }
  }, [mentorEmail]);

  useEffect(() => {
    fetchSessions();
  }, [fetchSessions]);

  // Manejo de tecla Escape para cerrar modal de accesibilidad
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && contingencySession) {
        setContingencySession(null);
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [contingencySession]);

  // Consultar nómina de inscritos de una sesión específica
  const loadRoster = async (sessionId: string) => {
    if (expandedSessionId === sessionId) {
      setExpandedSessionId(null);
      return;
    }

    setExpandedSessionId(sessionId);
    if (rosters[sessionId]) return;

    setLoadingRosterId(sessionId);
    try {
      const baseUrl = (import.meta.env.VITE_API_BASE_URL as string) || 'http://localhost:8000';
      const token = authService.getToken();
      const headers: Record<string, string> = { Accept: 'application/json' };
      if (token) headers['Authorization'] = `Bearer ${token}`;

      const res = await fetch(`${baseUrl}/api/v1/bookings/session/${sessionId}`, { headers });
      if (res.ok) {
        const list = await res.json();
        setRosters((prev) => ({ ...prev, [sessionId]: list }));
      } else {
        setRosters((prev) => ({ ...prev, [sessionId]: [] }));
      }
    } catch {
      setRosters((prev) => ({ ...prev, [sessionId]: [] }));
    } finally {
      setLoadingRosterId(null);
    }
  };

  const computeQuorumInfo = (session: PublishOfferResponse, enrolledList?: EnrolledStudent[]) => {
    const aforo = session.aforo || (session.offer.modalidad === 'presencial' ? 10 : 20);
    const quorumTarget = Math.ceil(aforo * 0.5); // RN-09: 50%
    const confirmedCount = (enrolledList || []).filter((e) => e.estado === 'CONFIRMADA').length;
    const totalEnrolled = (enrolledList || []).filter(
      (e) => e.estado !== 'CANCELADA_USUARIO' && e.estado !== 'CANCELADA_SISTEMA'
    ).length;

    const startDate = new Date(session.offer.fecha_inicio.replace('Z', '+00:00'));
    const hoursRemaining = (startDate.getTime() - now) / (3600 * 1000);

    const isQuorumReached = confirmedCount >= (session.offer.modalidad === 'presencial' ? 3 : 5) || confirmedCount >= quorumTarget;
    const isPastDeadline = hoursRemaining <= 24;
    const isInsufficient = session.estado === 'QUORUM_INSUFICIENTE' || (isPastDeadline && !isQuorumReached);

    return {
      aforo,
      quorumTarget,
      confirmedCount,
      totalEnrolled,
      hoursRemaining,
      isQuorumReached,
      isPastDeadline,
      isInsufficient,
    };
  };

  const openContingencyModal = (session: PublishOfferResponse) => {
    setContingencySession(session);
    setContingencyDecision('PROCEED');
    setRescheduleDate('');
    setCancelReason('');
    setContingencyError(null);
  };

  const closeContingencyModal = () => {
    setContingencySession(null);
    setContingencyError(null);
  };

  const handleContingencySubmit = async () => {
    if (!contingencySession) return;
    setContingencyError(null);

    // Validación en cliente para RESCHEDULE
    if (contingencyDecision === 'RESCHEDULE') {
      if (!rescheduleDate) {
        setContingencyError('Debe ingresar una nueva fecha y hora para la mentoría.');
        return;
      }
      const targetTime = new Date(rescheduleDate).getTime();
      const diffHours = (targetTime - Date.now()) / (3600 * 1000);
      if (diffHours <= 24) {
        setContingencyError('La reprogramación exige una antelación mayor a 24 horas.');
        return;
      }
    }

    // Validación en cliente para CANCEL
    if (contingencyDecision === 'CANCEL') {
      if (!cancelReason.trim()) {
        setContingencyError('Debe ingresar obligatoriamente una justificación académica de cancelación.');
        return;
      }
    }

    setIsSubmittingContingency(true);
    try {
      const sId = contingencySession.id_oferta || contingencySession.codigo_sesion;
      const payload: QuorumDecisionPayload = {
        decision: contingencyDecision,
        new_start_time: contingencyDecision === 'RESCHEDULE' ? new Date(rescheduleDate).toISOString() : undefined,
        reason: contingencyDecision === 'CANCEL' ? cancelReason.trim() : undefined,
      };

      const resp = await offerService.resolveQuorum(sId, payload);
      setStatusMessage(`Decisión registrada exitosamente: ${resp.mensaje || 'Sesión actualizada'}`);

      // Actualizar estado local de la sesión
      setSessions((prev) =>
        prev.map((s) => {
          if ((s.id_oferta || s.codigo_sesion) === sId) {
            return {
              ...s,
              estado: resp.estado_nuevo || (contingencyDecision === 'PROCEED' ? 'CONFIRMADA' : contingencyDecision === 'RESCHEDULE' ? 'PUBLICADA' : 'CANCELADA_QUORUM'),
              offer: {
                ...s.offer,
                fecha_inicio: resp.nueva_fecha_inicio || s.offer.fecha_inicio,
              },
            };
          }
          return s;
        })
      );

      closeContingencyModal();
    } catch (err: unknown) {
      setContingencyError(err instanceof Error ? err.message : 'Error al procesar la resolución de contingencia.');
    } finally {
      setIsSubmittingContingency(false);
    }
  };

  if (selectedAttendanceSession) {
    const sId = selectedAttendanceSession.id_oferta || selectedAttendanceSession.codigo_sesion;
    return (
      <SessionAttendanceView
        sessionId={sId}
        sessionTitle={`${selectedAttendanceSession.offer.nombre_asignatura} (${selectedAttendanceSession.codigo_sesion})`}
        isMentor={true}
        onBack={() => setSelectedAttendanceSession(null)}
      />
    );
  }

  if (selectedBitacoraSession) {
    const sId = selectedBitacoraSession.id_oferta || selectedBitacoraSession.codigo_sesion;
    const startMs = new Date(selectedBitacoraSession.offer.fecha_inicio).getTime();
    const endMs = startMs + (selectedBitacoraSession.offer.duracion_minutos || 60) * 60 * 1000;
    return (
      <BitacoraFormView
        sessionId={sId}
        sessionTitle={`${selectedBitacoraSession.offer.nombre_asignatura} (${selectedBitacoraSession.codigo_sesion})`}
        sessionEndDate={new Date(endMs)}
        subjectName={selectedBitacoraSession.offer.nombre_asignatura}
        onBack={() => setSelectedBitacoraSession(null)}
      />
    );
  }

  return (
    <div style={{ width: '100%', maxWidth: '980px', margin: '0 auto' }}>
      {/* Banner accesible de estado */}
      <div aria-live="polite" style={{ position: 'relative' }}>
        {statusMessage && (
          <div
            style={{
              backgroundColor: '#DEF7EC',
              border: '1px solid #31C48D',
              borderRadius: '8px',
              padding: '0.85rem 1.25rem',
              color: '#03543F',
              marginBottom: '1rem',
              display: 'flex',
              justifyContent: 'space-between',
              alignItems: 'center',
            }}
          >
            <span>✅ {statusMessage}</span>
            <button
              type="button"
              onClick={() => setStatusMessage(null)}
              style={{ background: 'none', border: 'none', cursor: 'pointer', fontSize: '1rem', color: '#03543F' }}
            >
              ✕
            </button>
          </div>
        )}
      </div>

      {/* Cabecera del Portal de Mentor */}
      <div
        style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '1.5rem',
          flexWrap: 'wrap',
          gap: '1rem',
        }}
      >
        <div>
          <h2 style={{ fontSize: '1.5rem', fontWeight: 800, color: '#1C2A59', margin: '0 0 0.35rem 0' }}>
            📋 Mis Mentorías Académicas Programadas
          </h2>
          <p style={{ margin: 0, fontSize: '0.88rem', color: '#64748B' }}>
            Supervisión de aforo, ratificación de estudiantes y quórum institucional.
          </p>
        </div>
        {handlePublish && (
          <button
            type="button"
            onClick={handlePublish}
            style={{
              backgroundColor: '#1C2A59',
              color: '#FFFFFF',
              border: 'none',
              borderRadius: '8px',
              padding: '0.65rem 1.25rem',
              fontSize: '0.88rem',
              fontWeight: 700,
              cursor: 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              boxShadow: '0 2px 6px rgba(28, 42, 89, 0.2)',
            }}
          >
            <span>➕</span> Publicar Nueva Oferta
          </button>
        )}
      </div>

      {/* Estados de carga y error */}
      {isLoading && (
        <div style={{ textAlign: 'center', padding: '3rem', color: '#64748B' }}>
          <div style={{ fontSize: '1.5rem', marginBottom: '0.5rem' }}>⏳</div>
          <p>Consultando sesiones de mentoría en base de datos...</p>
        </div>
      )}

      {error && (
        <div
          style={{
            backgroundColor: '#FEF2F2',
            border: '1px solid #F87171',
            borderRadius: '8px',
            padding: '1rem',
            color: '#991B1B',
            marginBottom: '1.5rem',
          }}
        >
          {error}
        </div>
      )}

      {!isLoading && !error && sessions.length === 0 && (
        <div
          style={{
            backgroundColor: '#FFFFFF',
            border: '1px dashed #CBD5E1',
            borderRadius: '12px',
            padding: '3rem 2rem',
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: '2.5rem', marginBottom: '1rem' }}>🎓</div>
          <h3 style={{ fontSize: '1.2rem', color: '#1C2A59', marginBottom: '0.5rem' }}>
            No tienes sesiones de mentoría publicadas actualmente
          </h3>
          <p style={{ color: '#64748B', fontSize: '0.88rem', maxWidth: '500px', margin: '0 auto 1.5rem auto' }}>
            Como mentor académico de la EPIS-UPT, puedes abrir plazas para asignaturas filtro (Cálculo I, Algoritmos,
            POO, Base de Datos) con al menos 24 horas de antelación.
          </p>
          {handlePublish && (
            <button
              type="button"
              onClick={handlePublish}
              style={{
                backgroundColor: '#B99451',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '8px',
                padding: '0.65rem 1.5rem',
                fontSize: '0.9rem',
                fontWeight: 700,
                cursor: 'pointer',
              }}
            >
              Publicar Mi Primera Sesión
            </button>
          )}
        </div>
      )}

      {/* Cuadrícula de Sesiones */}
      <div style={{ display: 'flex', flexDirection: 'column', gap: '1rem' }}>
        {sessions.map((session) => {
          const sId = session.id_oferta || session.codigo_sesion;
          const enrolled = rosters[sId];
          const qInfo = computeQuorumInfo(session, enrolled);

          return (
            <div
              key={sId}
              style={{
                backgroundColor: '#FFFFFF',
                borderRadius: '12px',
                border: qInfo.isInsufficient ? '2px solid #F59E0B' : '1px solid #E2E8F0',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
                overflow: 'hidden',
                transition: 'border-color 0.2s',
              }}
            >
              <div style={{ padding: '1.25rem 1.5rem' }}>
                <div
                  style={{
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                    flexWrap: 'wrap',
                    gap: '0.75rem',
                    marginBottom: '0.75rem',
                  }}
                >
                  <div>
                    <span
                      style={{
                        backgroundColor: '#F1F5F9',
                        color: '#1C2A59',
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        padding: '0.2rem 0.5rem',
                        borderRadius: '4px',
                        marginRight: '0.5rem',
                      }}
                    >
                      {session.offer.codigo_asignatura}
                    </span>
                    <span style={{ fontSize: '0.75rem', color: '#64748B' }}>
                      Código: <strong>{session.codigo_sesion}</strong>
                    </span>
                    <h3 style={{ fontSize: '1.15rem', fontWeight: 800, color: '#1C2A59', margin: '0.4rem 0 0.2rem 0' }}>
                      {session.offer.nombre_asignatura}
                    </h3>
                    <div style={{ fontSize: '0.88rem', color: '#475569', fontWeight: 500 }}>
                      📌 Tema: <em>{session.offer.nombre_tema}</em>
                    </div>
                  </div>

                  {/* Insignia de Quórum Reactivo */}
                  <div style={{ textAlign: 'right' }}>
                    {session.estado === 'CONFIRMADA' || qInfo.isQuorumReached ? (
                      <span
                        style={{
                          backgroundColor: '#DEF7EC',
                          color: '#03543F',
                          padding: '0.35rem 0.75rem',
                          borderRadius: '20px',
                          fontSize: '0.8rem',
                          fontWeight: 700,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '0.35rem',
                        }}
                      >
                        ✅ Quórum Alcanzado (≥ 50%)
                      </span>
                    ) : qInfo.isInsufficient ? (
                      <span
                        style={{
                          backgroundColor: '#FEF3C7',
                          color: '#92400E',
                          padding: '0.35rem 0.75rem',
                          borderRadius: '20px',
                          fontSize: '0.8rem',
                          fontWeight: 700,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '0.35rem',
                        }}
                      >
                        ⚠️ Quórum Insuficiente (&lt; 3 alumnos confirmados)
                      </span>
                    ) : (
                      <span
                        style={{
                          backgroundColor: '#E0F2FE',
                          color: '#075985',
                          padding: '0.35rem 0.75rem',
                          borderRadius: '20px',
                          fontSize: '0.8rem',
                          fontWeight: 700,
                          display: 'inline-flex',
                          alignItems: 'center',
                          gap: '0.35rem',
                        }}
                      >
                        🔵 Inscripción en Curso
                      </span>
                    )}
                  </div>
                </div>

                {/* Fila de Metadatos */}
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))',
                    gap: '0.75rem',
                    backgroundColor: '#F8FAFC',
                    borderRadius: '8px',
                    padding: '0.75rem 1rem',
                    fontSize: '0.82rem',
                    marginBottom: '1rem',
                  }}
                >
                  <div>
                    <span style={{ color: '#64748B', display: 'block' }}>Fecha y Hora:</span>
                    <strong>{new Date(session.offer.fecha_inicio.replace('Z', '+00:00')).toLocaleString()}</strong>
                  </div>
                  <div>
                    <span style={{ color: '#64748B', display: 'block' }}>Modalidad & Aforo:</span>
                    <strong>
                      {session.offer.modalidad === 'presencial' ? '🏫 Presencial (10 plazas)' : '💻 Virtual (20 plazas)'}
                    </strong>
                  </div>
                  <div>
                    <span style={{ color: '#64748B', display: 'block' }}>Duración:</span>
                    <strong>{session.offer.duracion_minutos} minutos</strong>
                  </div>
                  <div>
                    <span style={{ color: '#64748B', display: 'block' }}>Espacio / Recinto:</span>
                    <strong style={{ wordBreak: 'break-all' }}>{session.offer.espacio_asignado}</strong>
                  </div>
                </div>

                {/* Barra de progreso de Aforo */}
                <div style={{ marginBottom: '1rem' }}>
                  <div
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      fontSize: '0.78rem',
                      marginBottom: '0.3rem',
                    }}
                  >
                    <span style={{ color: '#475569', fontWeight: 600 }}>
                      Plazas ocupadas: {enrolled ? qInfo.totalEnrolled : '?'} / {qInfo.aforo} (Meta Quórum: {qInfo.quorumTarget})
                    </span>
                    <span style={{ color: qInfo.isQuorumReached ? '#059669' : '#D97706', fontWeight: 700 }}>
                      {enrolled ? `${qInfo.confirmedCount} confirmados` : 'Clic en Ver Nómina'}
                    </span>
                  </div>
                  <div style={{ width: '100%', height: '8px', backgroundColor: '#E2E8F0', borderRadius: '4px', overflow: 'hidden' }}>
                    <div
                      style={{
                        width: enrolled ? `${Math.min(100, (qInfo.confirmedCount / qInfo.aforo) * 100)}%` : '0%',
                        height: '100%',
                        backgroundColor: qInfo.isQuorumReached ? '#10B981' : '#F59E0B',
                        transition: 'width 0.3s ease',
                      }}
                    />
                  </div>
                </div>

                {/* Acciones */}
                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem', flexWrap: 'wrap' }}>
                  {qInfo.isInsufficient && (
                    <button
                      type="button"
                      onClick={() => openContingencyModal(session)}
                      style={{
                        backgroundColor: '#F59E0B',
                        color: '#FFFFFF',
                        border: 'none',
                        borderRadius: '6px',
                        padding: '0.45rem 1rem',
                        fontSize: '0.82rem',
                        fontWeight: 700,
                        cursor: 'pointer',
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.35rem',
                      }}
                    >
                      ⚡ Resolver Contingencia
                    </button>
                  )}

                  <button
                    type="button"
                    onClick={() => setSelectedAttendanceSession(session)}
                    style={{
                      backgroundColor: '#1C2A59',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '6px',
                      padding: '0.45rem 0.85rem',
                      fontSize: '0.82rem',
                      fontWeight: 600,
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.35rem',
                    }}
                  >
                    📱 Asistencia
                  </button>

                  <button
                    type="button"
                    onClick={() => setSelectedBitacoraSession(session)}
                    style={{
                      backgroundColor: '#B99451',
                      color: '#FFFFFF',
                      border: 'none',
                      borderRadius: '6px',
                      padding: '0.45rem 0.85rem',
                      fontSize: '0.82rem',
                      fontWeight: 600,
                      cursor: 'pointer',
                      display: 'flex',
                      alignItems: 'center',
                      gap: '0.35rem',
                    }}
                  >
                    📝 Bitácora
                  </button>

                  <button
                    type="button"
                    onClick={() => loadRoster(sId)}
                    style={{
                      backgroundColor: '#FFFFFF',
                      border: '1px solid #CBD5E1',
                      borderRadius: '6px',
                      padding: '0.45rem 1rem',
                      fontSize: '0.82rem',
                      fontWeight: 600,
                      color: '#1C2A59',
                      cursor: 'pointer',
                    }}
                  >
                    {expandedSessionId === sId ? '▲ Ocultar Nómina' : '▼ Ver Nómina de Inscritos'}
                  </button>
                </div>
              </div>

              {/* Acordeón de Nómina de Estudiantes */}
              {expandedSessionId === sId && (
                <div style={{ backgroundColor: '#F8FAFC', borderTop: '1px solid #E2E8F0', padding: '1rem 1.5rem' }}>
                  <h4 style={{ fontSize: '0.88rem', fontWeight: 700, color: '#1C2A59', margin: '0 0 0.5rem 0' }}>
                    👥 Estudiantes Inscritos en la Sesión ({enrolled ? enrolled.length : 0})
                  </h4>

                  {loadingRosterId === sId && <p style={{ fontSize: '0.8rem', color: '#64748B' }}>Cargando nómina...</p>}

                  {!loadingRosterId && enrolled && enrolled.length === 0 && (
                    <p style={{ fontSize: '0.82rem', color: '#94A3B8', fontStyle: 'italic', margin: 0 }}>
                      Aún no hay estudiantes inscritos en esta sesión de mentoría.
                    </p>
                  )}

                  {!loadingRosterId && enrolled && enrolled.length > 0 && (
                    <div style={{ overflowX: 'auto' }}>
                      <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.8rem' }}>
                        <thead>
                          <tr style={{ borderBottom: '1px solid #CBD5E1', color: '#475569', textAlign: 'left' }}>
                            <th style={{ padding: '0.4rem 0.5rem' }}>Código Reserva</th>
                            <th style={{ padding: '0.4rem 0.5rem' }}>Correo Institucional</th>
                            <th style={{ padding: '0.4rem 0.5rem' }}>Estado</th>
                            <th style={{ padding: '0.4rem 0.5rem' }}>Fecha de Registro</th>
                          </tr>
                        </thead>
                        <tbody>
                          {enrolled.map((stu) => (
                            <tr key={stu.id_reserva} style={{ borderBottom: '1px solid #E2E8F0' }}>
                              <td style={{ padding: '0.4rem 0.5rem', fontFamily: 'monospace', fontWeight: 600 }}>
                                {stu.codigo_reserva}
                              </td>
                              <td style={{ padding: '0.4rem 0.5rem' }}>{stu.estudiante_email}</td>
                              <td style={{ padding: '0.4rem 0.5rem' }}>
                                <span
                                  style={{
                                    backgroundColor:
                                      stu.estado === 'CONFIRMADA'
                                        ? '#DEF7EC'
                                        : stu.estado === 'PENDIENTE_CONFIRMACION'
                                        ? '#FEF3C7'
                                        : '#FEE2E2',
                                    color:
                                      stu.estado === 'CONFIRMADA'
                                        ? '#03543F'
                                        : stu.estado === 'PENDIENTE_CONFIRMACION'
                                        ? '#92400E'
                                        : '#991B1B',
                                    padding: '0.15rem 0.4rem',
                                    borderRadius: '4px',
                                    fontSize: '0.72rem',
                                    fontWeight: 700,
                                  }}
                                >
                                  {stu.estado}
                                </span>
                              </td>
                              <td style={{ padding: '0.4rem 0.5rem', color: '#64748B' }}>
                                {new Date(stu.fecha_reserva).toLocaleString()}
                              </td>
                            </tr>
                          ))}
                        </tbody>
                      </table>
                    </div>
                  )}
                </div>
              )}
            </div>
          );
        })}
      </div>

      {/* Modal Accesible de Resolución de Contingencia (T-32 / WCAG 2.1 AA) */}
      {contingencySession && (
        <div
          role="dialog"
          aria-modal="true"
          aria-labelledby="contingency-modal-title"
          style={{
            position: 'fixed',
            inset: 0,
            backgroundColor: 'rgba(15, 23, 42, 0.6)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            padding: '1rem',
            zIndex: 1000,
          }}
        >
          <div
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '16px',
              maxWidth: '560px',
              width: '100%',
              padding: '1.75rem',
              boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.2)',
              maxHeight: '90vh',
              overflowY: 'auto',
            }}
          >
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <h3 id="contingency-modal-title" style={{ fontSize: '1.25rem', fontWeight: 800, color: '#1C2A59', margin: 0 }}>
                ⚡ Resolución de Quórum Insuficiente
              </h3>
              <button
                type="button"
                onClick={closeContingencyModal}
                style={{ background: 'none', border: 'none', fontSize: '1.25rem', cursor: 'pointer', color: '#64748B' }}
                aria-label="Cerrar modal"
              >
                ✕
              </button>
            </div>

            <p style={{ fontSize: '0.88rem', color: '#475569', marginBottom: '1.25rem' }}>
              La sesión <strong>{contingencySession.codigo_sesion}</strong> ({contingencySession.offer.nombre_asignatura})
              no alcanzó el quórum mínimo requerido a 24 horas del inicio. Seleccione una acción resolutiva:
            </p>

            {contingencyError && (
              <div
                style={{
                  backgroundColor: '#FEF2F2',
                  border: '1px solid #F87171',
                  borderRadius: '8px',
                  padding: '0.75rem 1rem',
                  color: '#991B1B',
                  fontSize: '0.82rem',
                  marginBottom: '1rem',
                }}
              >
                ⚠️ {contingencyError}
              </div>
            )}

            {/* Opciones Resolutivas */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: '0.85rem', marginBottom: '1.5rem' }}>
              {/* Opción A: PROCEED */}
              <label
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.75rem',
                  padding: '0.75rem 1rem',
                  borderRadius: '8px',
                  border: contingencyDecision === 'PROCEED' ? '2px solid #1C2A59' : '1px solid #CBD5E1',
                  backgroundColor: contingencyDecision === 'PROCEED' ? '#F8FAFC' : '#FFFFFF',
                  cursor: 'pointer',
                }}
              >
                <input
                  type="radio"
                  name="decision"
                  value="PROCEED"
                  checked={contingencyDecision === 'PROCEED'}
                  onChange={() => setContingencyDecision('PROCEED')}
                  style={{ marginTop: '0.2rem' }}
                />
                <div>
                  <strong style={{ color: '#1C2A59', display: 'block', fontSize: '0.9rem' }}>
                    Dictar de Todas Formas
                  </strong>
                  <span style={{ fontSize: '0.8rem', color: '#64748B' }}>
                    Confirmar el dictado de la mentoría con el aforo reducido de estudiantes que ratificaron a tiempo.
                  </span>
                </div>
              </label>

              {/* Opción B: RESCHEDULE */}
              <label
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.75rem',
                  padding: '0.75rem 1rem',
                  borderRadius: '8px',
                  border: contingencyDecision === 'RESCHEDULE' ? '2px solid #1C2A59' : '1px solid #CBD5E1',
                  backgroundColor: contingencyDecision === 'RESCHEDULE' ? '#F8FAFC' : '#FFFFFF',
                  cursor: 'pointer',
                }}
              >
                <input
                  type="radio"
                  name="decision"
                  value="RESCHEDULE"
                  checked={contingencyDecision === 'RESCHEDULE'}
                  onChange={() => setContingencyDecision('RESCHEDULE')}
                  style={{ marginTop: '0.2rem' }}
                />
                <div style={{ width: '100%' }}>
                  <strong style={{ color: '#1C2A59', display: 'block', fontSize: '0.9rem' }}>
                    Reprogramar Sesión
                  </strong>
                  <span style={{ fontSize: '0.8rem', color: '#64748B', display: 'block', marginBottom: '0.5rem' }}>
                    Postergar la fecha y hora de la mentoría con al menos 24 horas de antelación.
                  </span>
                  {contingencyDecision === 'RESCHEDULE' && (
                    <div>
                      <input
                        type="datetime-local"
                        aria-label="Nueva Fecha y Hora"
                        value={rescheduleDate}
                        onChange={(e) => setRescheduleDate(e.target.value)}
                        style={{
                          width: '100%',
                          padding: '0.5rem',
                          borderRadius: '6px',
                          border: '1px solid #94A3B8',
                          fontSize: '0.85rem',
                        }}
                      />
                    </div>
                  )}
                </div>
              </label>

              {/* Opción C: CANCEL */}
              <label
                style={{
                  display: 'flex',
                  alignItems: 'flex-start',
                  gap: '0.75rem',
                  padding: '0.75rem 1rem',
                  borderRadius: '8px',
                  border: contingencyDecision === 'CANCEL' ? '2px solid #DC2626' : '1px solid #CBD5E1',
                  backgroundColor: contingencyDecision === 'CANCEL' ? '#FEF2F2' : '#FFFFFF',
                  cursor: 'pointer',
                }}
              >
                <input
                  type="radio"
                  name="decision"
                  value="CANCEL"
                  checked={contingencyDecision === 'CANCEL'}
                  onChange={() => setContingencyDecision('CANCEL')}
                  style={{ marginTop: '0.2rem' }}
                />
                <div style={{ width: '100%' }}>
                  <strong style={{ color: '#991B1B', display: 'block', fontSize: '0.9rem' }}>
                    Cancelar Sesión Definitivamente
                  </strong>
                  <span style={{ fontSize: '0.8rem', color: '#64748B', display: 'block', marginBottom: '0.5rem' }}>
                    Anular la sesión liberando a los estudiantes inscritos sin penalidad alguna.
                  </span>
                  {contingencyDecision === 'CANCEL' && (
                    <div>
                      <textarea
                        aria-label="Motivo de Cancelación"
                        placeholder="Ingrese la justificación académica de cancelación obligatoria..."
                        value={cancelReason}
                        onChange={(e) => setCancelReason(e.target.value)}
                        rows={3}
                        style={{
                          width: '100%',
                          padding: '0.5rem',
                          borderRadius: '6px',
                          border: '1px solid #94A3B8',
                          fontSize: '0.85rem',
                          resize: 'vertical',
                        }}
                      />
                    </div>
                  )}
                </div>
              </label>
            </div>

            {/* Botones de acción */}
            <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
              <button
                type="button"
                onClick={closeContingencyModal}
                disabled={isSubmittingContingency}
                style={{
                  backgroundColor: '#FFFFFF',
                  border: '1px solid #CBD5E1',
                  borderRadius: '8px',
                  padding: '0.6rem 1.25rem',
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  color: '#475569',
                  cursor: 'pointer',
                }}
              >
                Cerrar
              </button>
              <button
                type="button"
                onClick={handleContingencySubmit}
                disabled={isSubmittingContingency}
                style={{
                  backgroundColor: '#1C2A59',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '8px',
                  padding: '0.6rem 1.5rem',
                  fontSize: '0.88rem',
                  fontWeight: 700,
                  cursor: isSubmittingContingency ? 'not-allowed' : 'pointer',
                  opacity: isSubmittingContingency ? 0.7 : 1,
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                }}
              >
                {isSubmittingContingency && <span>⏳</span>}
                <span>Confirmar Decisión</span>
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
