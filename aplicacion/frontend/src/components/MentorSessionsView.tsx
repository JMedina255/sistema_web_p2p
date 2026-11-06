/**
 * Vista: Mis Mentorías Publicadas y Supervisión de Quórum (Sprint 5 / Sprint 6 Pre-Requisito)
 *
 * Trazabilidad:
 * - Requerimiento Funcional: RF08 (Gestión y catálogo de ofertas de mentoría)
 * - Regla de Negocio RN-05: Aforo inmutable (10 presencial / 20 virtual)
 * - Regla de Negocio RN-08: Corte perentorio a T-24h para confirmaciones
 * - Regla de Negocio RN-09: Cómputo del quórum regulatorio del 50% (5 presencial / 10 virtual)
 * - Requerimiento No Funcional: RNF05 (Accesibilidad WAI-ARIA)
 */

import React, { useState, useEffect, useCallback } from 'react';
import { offerService, type PublishOfferResponse } from '../services/offerService';
import { authService } from '../services/authService';

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

  // Mapa de nóminas de estudiantes por ID de sesión
  const [rosters, setRosters] = useState<Record<string, EnrolledStudent[]>>({});
  const [loadingRosterId, setLoadingRosterId] = useState<string | null>(null);
  const [expandedSessionId, setExpandedSessionId] = useState<string | null>(null);

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
    const totalEnrolled = (enrolledList || []).filter((e) => e.estado !== 'CANCELADA_USUARIO' && e.estado !== 'CANCELADA_SISTEMA').length;

    const startDate = new Date(session.offer.fecha_inicio.replace('Z', '+00:00'));
    const hoursRemaining = (startDate.getTime() - Date.now()) / (3600 * 1000);

    const isQuorumReached = confirmedCount >= quorumTarget;
    const isPastDeadline = hoursRemaining <= 24;

    return {
      aforo,
      quorumTarget,
      confirmedCount,
      totalEnrolled,
      hoursRemaining,
      isQuorumReached,
      isPastDeadline,
    };
  };

  return (
    <div style={{ width: '100%', maxWidth: '980px', margin: '0 auto' }}>
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
            Supervisión pedagógica de aforo, ratificación de estudiantes y quórum institucional (RN-05 / RN-08 / RN-09).
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
                border: '1px solid #E2E8F0',
                boxShadow: '0 2px 8px rgba(0, 0, 0, 0.04)',
                overflow: 'hidden',
                transition: 'border-color 0.2s',
              }}
            >
              <div style={{ padding: '1.25rem 1.5rem' }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', flexWrap: 'wrap', gap: '0.75rem', marginBottom: '0.75rem' }}>
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
                    {qInfo.isQuorumReached ? (
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
                    ) : qInfo.isPastDeadline ? (
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
                        ⚠️ Quórum Insuficiente (Corte T-24h)
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
                  <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: '0.78rem', marginBottom: '0.3rem' }}>
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
                <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
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
    </div>
  );
};
