/**
 * Panel de Administración Institucional EPIS-UPT (RF03 / CUS10 / RN-03 / RN-09)
 *
 * Funcionalidades:
 * 1. Gestión de Roles: Consulta, promoción a mentor con verificación de mérito (RN-03: Ciclo ≥ VII) y revocación.
 * 2. Monitoreo Institucional de Quórum: Supervisión de sesiones y tasa de ratificación (RN-09).
 * 3. Salud y Telemetría de Servicios: Estado en tiempo real de FastAPI y base de datos Supabase.
 */

import React, { useState, useEffect, useCallback } from 'react';
import { roleService } from '../services/roleService';
import { offerService, type PublishOfferResponse } from '../services/offerService';
import { bitacoraService, type BitacoraItem } from '../services/bitacoraService';
import { HealthStatus } from './HealthStatus';
import { CurriculumCatalogView } from './CurriculumCatalogView';
import { AdminScheduleUploadView } from './AdminScheduleUploadView';

export interface AdminDashboardViewProps {
  adminEmail?: string;
  showDevControls?: boolean;
}

export const AdminDashboardView: React.FC<AdminDashboardViewProps> = ({
  adminEmail = '',
  showDevControls = false,
}) => {
  const isDev = showDevControls && !import.meta.env.PROD;
  const [activeTab, setActiveTab] = useState<
    'roles' | 'quorum' | 'health' | 'bitacoras' | 'curriculum' | 'schedule'
  >('roles');

  // Estado para gestión de roles
  const [searchEmail, setSearchEmail] = useState('');
  const [queriedRoles, setQueriedRoles] = useState<string[] | null>(null);
  const [queriedEmail, setQueriedEmail] = useState<string | null>(null);
  const [roleLoading, setRoleLoading] = useState(false);
  const [roleMessage, setRoleMessage] = useState<{ text: string; type: 'success' | 'error' | 'info' } | null>(null);

  // Estado para monitoreo de quórum
  const [offers, setOffers] = useState<PublishOfferResponse[]>([]);
  const [offersLoading, setOffersLoading] = useState(false);
  const [offersError, setOffersError] = useState<string | null>(null);

  // Estado para auditoría y fiscalización de bitácoras (T-40 / T-41 / RF26 / RN-14)
  const [bitacoras, setBitacoras] = useState<BitacoraItem[]>([]);
  const [bitacorasLoading, setBitacorasLoading] = useState(false);
  const [bitacorasError, setBitacorasError] = useState<string | null>(null);
  const [bitacoraFiltro, setBitacoraFiltro] = useState<'TODAS' | 'PENDIENTES' | 'VISADAS' | 'OBSERVADA'>('TODAS');
  const [selectedBitacoraDetail, setSelectedBitacoraDetail] = useState<BitacoraItem | null>(null);
  const [observingBitacora, setObservingBitacora] = useState<BitacoraItem | null>(null);
  const [motivoObservacion, setMotivoObservacion] = useState('');
  const [bitacoraActionLoading, setBitacoraActionLoading] = useState(false);
  const [bitacoraFeedback, setBitacoraFeedback] = useState<{ text: string; type: 'success' | 'error' } | null>(null);

  // Carga inicial de ofertas para supervisión de quórum
  const loadOffers = useCallback(async () => {
    setOffersLoading(true);
    setOffersError(null);
    try {
      const data = await offerService.getOffers();
      setOffers(data);
    } catch (err) {
      setOffersError(err instanceof Error ? err.message : 'Error al cargar ofertas');
    } finally {
      setOffersLoading(false);
    }
  }, []);

  // Carga de bitácoras para fiscalización administrativa
  const loadBitacoras = useCallback(async (filtro?: string) => {
    setBitacorasLoading(true);
    setBitacorasError(null);
    try {
      const data = await bitacoraService.getBitacoras(filtro);
      setBitacoras(data);
    } catch (err) {
      setBitacorasError(err instanceof Error ? err.message : 'Error al cargar bitácoras');
    } finally {
      setBitacorasLoading(false);
    }
  }, []);

  useEffect(() => {
    if (activeTab === 'quorum') {
      loadOffers();
    } else if (activeTab === 'bitacoras') {
      loadBitacoras(bitacoraFiltro);
    }
  }, [activeTab, bitacoraFiltro, loadOffers, loadBitacoras]);

  const handleVisarBitacora = async (b: BitacoraItem) => {
    setBitacoraActionLoading(true);
    setBitacoraFeedback(null);
    try {
      const res = await bitacoraService.visar(b.id_bitacora);
      setBitacoras((prev) =>
        prev.map((item) =>
          item.id_bitacora === b.id_bitacora
            ? { ...item, visado_administrador: true, estado_sesion: 'HORAS_VISADAS' }
            : item
        )
      );
      setBitacoraFeedback({
        text: res.mensaje || 'Horas acreditadas y visadas institucionalmente con éxito.',
        type: 'success',
      });
    } catch (err) {
      setBitacoraFeedback({
        text: err instanceof Error ? err.message : 'Error al visar bitácora.',
        type: 'error',
      });
    } finally {
      setBitacoraActionLoading(false);
    }
  };

  // Cierre accesible de modales con tecla Escape (WCAG 2.1 AA / RNF05)
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (observingBitacora && !bitacoraActionLoading) {
          setObservingBitacora(null);
          setMotivoObservacion('');
        } else if (selectedBitacoraDetail) {
          setSelectedBitacoraDetail(null);
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [observingBitacora, bitacoraActionLoading, selectedBitacoraDetail]);

  const handleObservarSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!observingBitacora) return;
    const clean = motivoObservacion.trim();
    if (clean.length < 15) {
      setBitacoraFeedback({
        text: 'La justificación técnica de la observación debe contener al menos 15 caracteres.',
        type: 'error',
      });
      return;
    }
    setBitacoraActionLoading(true);
    setBitacoraFeedback(null);
    try {
      const res = await bitacoraService.observar(observingBitacora.id_bitacora, clean);
      setBitacoras((prev) =>
        prev.map((item) =>
          item.id_bitacora === observingBitacora.id_bitacora
            ? { ...item, visado_administrador: false, estado_sesion: 'OBSERVADA' }
            : item
        )
      );
      setObservingBitacora(null);
      setMotivoObservacion('');
      setBitacoraFeedback({
        text: res.mensaje || 'Bitácora observada para corrección.',
        type: 'success',
      });
    } catch (err) {
      setBitacoraFeedback({
        text: err instanceof Error ? err.message : 'Error al observar bitácora.',
        type: 'error',
      });
    } finally {
      setBitacoraActionLoading(false);
    }
  };

  // Manejadores de Gestión de Roles
  const handleSearchRoles = async (targetEmail: string) => {
    const clean = targetEmail.trim().toLowerCase();
    if (!clean || !clean.includes('@upt.pe')) {
      setRoleMessage({
        text: 'Ingrese un correo institucional válido con dominio @upt.pe.',
        type: 'error',
      });
      return;
    }

    setRoleLoading(true);
    setRoleMessage(null);
    try {
      const res = await roleService.getUserRoles(clean);
      setQueriedEmail(res.email);
      setQueriedRoles(res.roles);
    } catch (err) {
      setRoleMessage({
        text: err instanceof Error ? err.message : 'Error al consultar roles del estudiante',
        type: 'error',
      });
      setQueriedRoles(null);
    } finally {
      setRoleLoading(false);
    }
  };

  const handlePromoteMentor = async () => {
    if (!queriedEmail) return;
    setRoleLoading(true);
    setRoleMessage(null);
    try {
      const res = await roleService.promoteToMentor(queriedEmail, adminEmail);
      setQueriedRoles(res.roles);
      setRoleMessage({
        text: res.message,
        type: 'success',
      });
    } catch (err) {
      setRoleMessage({
        text: err instanceof Error ? err.message : 'Error al promover a mentor.',
        type: 'error',
      });
    } finally {
      setRoleLoading(false);
    }
  };

  const handleRevokeMentor = async () => {
    if (!queriedEmail) return;
    setRoleLoading(true);
    setRoleMessage(null);
    try {
      const res = await roleService.revokeMentor(queriedEmail);
      setQueriedRoles(res.roles);
      setRoleMessage({
        text: res.message,
        type: 'info',
      });
    } catch (err) {
      setRoleMessage({
        text: err instanceof Error ? err.message : 'Error al revocar rol de mentor.',
        type: 'error',
      });
    } finally {
      setRoleLoading(false);
    }
  };

  return (
    <div
      style={{
        maxWidth: '1000px',
        margin: '0 auto',
        backgroundColor: '#FFFFFF',
        borderRadius: '12px',
        border: '1px solid #E2E8F0',
        boxShadow: '0 4px 16px rgba(28, 42, 89, 0.06)',
        overflow: 'hidden',
      }}
    >
      {/* Encabezado */}
      <div
        style={{
          backgroundColor: '#1C2A59',
          color: '#FFFFFF',
          padding: '1.25rem 2rem',
          borderBottom: '3px solid #B99451',
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          flexWrap: 'wrap',
          gap: '1rem',
        }}
      >
        <div>
          <h2 style={{ margin: 0, fontSize: '1.35rem', fontWeight: 800 }}>
            🛡️ Panel de Administración y Supervisión EPIS
          </h2>
          <p style={{ margin: '0.25rem 0 0', fontSize: '0.85rem', opacity: 0.9 }}>
            Administrador en sesión: <strong>{adminEmail}</strong> · Dirección de Escuela
          </p>
        </div>

        {/* Sub-pestañas del panel */}
        <div style={{ display: 'flex', gap: '0.5rem' }}>
          <button
            type="button"
            onClick={() => setActiveTab('roles')}
            style={{
              padding: '0.45rem 0.9rem',
              borderRadius: '6px',
              border: 'none',
              background: activeTab === 'roles' ? '#B99451' : 'rgba(255, 255, 255, 0.15)',
              color: '#FFFFFF',
              fontWeight: 600,
              fontSize: '0.82rem',
              cursor: 'pointer',
            }}
          >
            👥 Gestión de Roles
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('quorum')}
            style={{
              padding: '0.45rem 0.9rem',
              borderRadius: '6px',
              border: 'none',
              background: activeTab === 'quorum' ? '#B99451' : 'rgba(255, 255, 255, 0.15)',
              color: '#FFFFFF',
              fontWeight: 600,
              fontSize: '0.82rem',
              cursor: 'pointer',
            }}
          >
            📊 Monitoreo de Quórum
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('bitacoras')}
            style={{
              padding: '0.45rem 0.9rem',
              borderRadius: '6px',
              border: 'none',
              background: activeTab === 'bitacoras' ? '#B99451' : 'rgba(255, 255, 255, 0.15)',
              color: '#FFFFFF',
              fontWeight: 600,
              fontSize: '0.82rem',
              cursor: 'pointer',
            }}
          >
            📋 Auditoría de Bitácoras
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('curriculum')}
            style={{
              padding: '0.45rem 0.9rem',
              borderRadius: '6px',
              border: 'none',
              background: activeTab === 'curriculum' ? '#B99451' : 'rgba(255, 255, 255, 0.15)',
              color: '#FFFFFF',
              fontWeight: 600,
              fontSize: '0.82rem',
              cursor: 'pointer',
            }}
          >
            📚 Catálogo Curricular (RF05)
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('schedule')}
            style={{
              padding: '0.45rem 0.9rem',
              borderRadius: '6px',
              border: 'none',
              background: activeTab === 'schedule' ? '#B99451' : 'rgba(255, 255, 255, 0.15)',
              color: '#FFFFFF',
              fontWeight: 600,
              fontSize: '0.82rem',
              cursor: 'pointer',
            }}
          >
            📅 Cronograma de Aulas (RF10)
          </button>
          <button
            type="button"
            onClick={() => setActiveTab('health')}
            style={{
              padding: '0.45rem 0.9rem',
              borderRadius: '6px',
              border: 'none',
              background: activeTab === 'health' ? '#B99451' : 'rgba(255, 255, 255, 0.15)',
              color: '#FFFFFF',
              fontWeight: 600,
              fontSize: '0.82rem',
              cursor: 'pointer',
            }}
          >
            🛰️ Salud del Sistema
          </button>
        </div>
      </div>

      <div style={{ padding: '1.75rem 2rem' }}>
        {/* SECCIÓN 1: GESTIÓN DE ROLES */}
        {activeTab === 'roles' && (
          <div>
            <div style={{ marginBottom: '1.5rem' }}>
              <h3 style={{ margin: '0 0 0.5rem', color: '#1C2A59', fontSize: '1.1rem' }}>
                Asignación y Validación de Mérito de Mentores
              </h3>
              <p style={{ margin: 0, color: '#64748B', fontSize: '0.85rem', lineHeight: 1.5 }}>
                Conforme al reglamento de mentorías EPIS-UPT, solo los estudiantes con ciclo académico mayor o igual a
                VII (7) pueden ser promovidos al rol de Mentor. La autopromoción no autorizada se encuentra bloqueada
                en backend.
              </p>
            </div>

            {/* Buscador de usuario */}
            <div
              style={{
                display: 'flex',
                gap: '0.75rem',
                flexWrap: 'wrap',
                marginBottom: '1.25rem',
              }}
            >
              <input
                type="email"
                placeholder="ej. 2022074255@upt.pe"
                value={searchEmail}
                onChange={(e) => setSearchEmail(e.target.value)}
                onKeyDown={(e) => {
                  if (e.key === 'Enter') handleSearchRoles(searchEmail);
                }}
                style={{
                  flex: '1 1 300px',
                  padding: '0.65rem 0.9rem',
                  border: '1px solid #CBD5E1',
                  borderRadius: '6px',
                  fontSize: '0.9rem',
                }}
              />
              <button
                type="button"
                onClick={() => handleSearchRoles(searchEmail)}
                disabled={roleLoading}
                style={{
                  backgroundColor: '#1C2A59',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '6px',
                  padding: '0.65rem 1.25rem',
                  fontWeight: 600,
                  fontSize: '0.85rem',
                  cursor: roleLoading ? 'not-allowed' : 'pointer',
                  opacity: roleLoading ? 0.7 : 1,
                }}
              >
                {roleLoading ? 'Consultando...' : '🔍 Buscar Estudiante'}
              </button>
            </div>

            {/* Accesos rápidos de prueba */}
            {isDev && (
              <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', marginBottom: '1.5rem' }}>
                <span style={{ fontSize: '0.75rem', color: '#64748B', alignSelf: 'center' }}>Cuentas de prueba:</span>
                <button
                  type="button"
                  onClick={() => {
                    setSearchEmail('2022074255@upt.pe');
                    handleSearchRoles('2022074255@upt.pe');
                  }}
                  style={{
                    fontSize: '0.75rem',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '4px',
                    border: '1px solid #CBD5E1',
                    background: '#F8FAFC',
                    cursor: 'pointer',
                  }}
                >
                  2022074255 (Estudiante - Ciclo 7)
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setSearchEmail('2022073504@upt.pe');
                    handleSearchRoles('2022073504@upt.pe');
                  }}
                  style={{
                    fontSize: '0.75rem',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '4px',
                    border: '1px solid #CBD5E1',
                    background: '#F8FAFC',
                    cursor: 'pointer',
                  }}
                >
                  2022073504 (Mentor - Ciclo 8)
                </button>
                <button
                  type="button"
                  onClick={() => {
                    setSearchEmail('2023079999@upt.pe');
                    handleSearchRoles('2023079999@upt.pe');
                  }}
                  style={{
                    fontSize: '0.75rem',
                    padding: '0.25rem 0.5rem',
                    borderRadius: '4px',
                    border: '1px solid #CBD5E1',
                    background: '#F8FAFC',
                    cursor: 'pointer',
                  }}
                >
                  2023079999 (Estudiante - Ciclo 2)
                </button>
              </div>
            )}

            {/* Mensajes de retroalimentación */}
            {roleMessage && (
              <div
                style={{
                  padding: '0.75rem 1rem',
                  borderRadius: '6px',
                  marginBottom: '1.25rem',
                  fontSize: '0.85rem',
                  backgroundColor:
                    roleMessage.type === 'success'
                      ? '#DEF7EC'
                      : roleMessage.type === 'error'
                      ? '#FDE8E8'
                      : '#E1EFFE',
                  color:
                    roleMessage.type === 'success'
                      ? '#03543F'
                      : roleMessage.type === 'error'
                      ? '#9B1C1C'
                      : '#1E429F',
                  border: `1px solid ${
                    roleMessage.type === 'success'
                      ? '#BCF0DA'
                      : roleMessage.type === 'error'
                      ? '#F8B4B4'
                      : '#B4C6FC'
                  }`,
                }}
              >
                {roleMessage.text}
              </div>
            )}

            {/* Ficha de roles del usuario consultado */}
            {queriedEmail && queriedRoles && (
              <div
                style={{
                  background: '#F8FAFC',
                  border: '1px solid #CBD5E1',
                  borderRadius: '8px',
                  padding: '1.25rem',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                  <div>
                    <span style={{ fontSize: '0.75rem', color: '#64748B', fontWeight: 600, textTransform: 'uppercase' }}>
                      Expediente Institucional
                    </span>
                    <h4 style={{ margin: 0, color: '#1C2A59', fontSize: '1.05rem' }}>{queriedEmail}</h4>
                  </div>
                  <div style={{ display: 'flex', gap: '0.5rem' }}>
                    {queriedRoles.map((r) => (
                      <span
                        key={r}
                        style={{
                          fontSize: '0.75rem',
                          fontWeight: 700,
                          padding: '0.25rem 0.6rem',
                          borderRadius: '9999px',
                          textTransform: 'uppercase',
                          backgroundColor:
                            r === 'administrador' ? '#E1EFFE' : r === 'mentor' ? '#FEF3C7' : '#E2E8F0',
                          color:
                            r === 'administrador' ? '#1E429F' : r === 'mentor' ? '#92400E' : '#334155',
                          border: `1px solid ${
                            r === 'administrador' ? '#93C5FD' : r === 'mentor' ? '#FCD34D' : '#CBD5E1'
                          }`,
                        }}
                      >
                        {r}
                      </span>
                    ))}
                  </div>
                </div>

                <div style={{ display: 'flex', gap: '0.75rem', flexWrap: 'wrap' }}>
                  {!queriedRoles.includes('mentor') ? (
                    <button
                      type="button"
                      onClick={handlePromoteMentor}
                      disabled={roleLoading}
                      style={{
                        backgroundColor: '#059669',
                        color: '#FFFFFF',
                        border: 'none',
                        borderRadius: '6px',
                        padding: '0.6rem 1.1rem',
                        fontWeight: 600,
                        fontSize: '0.85rem',
                        cursor: roleLoading ? 'not-allowed' : 'pointer',
                      }}
                    >
                      ⭐ Promover a Mentor (Verificar Mérito Académico)
                    </button>
                  ) : (
                    <button
                      type="button"
                      onClick={handleRevokeMentor}
                      disabled={roleLoading}
                      style={{
                        backgroundColor: '#DC2626',
                        color: '#FFFFFF',
                        border: 'none',
                        borderRadius: '6px',
                        padding: '0.6rem 1.1rem',
                        fontWeight: 600,
                        fontSize: '0.85rem',
                        cursor: roleLoading ? 'not-allowed' : 'pointer',
                      }}
                    >
                      🚫 Revocar Rol de Mentor
                    </button>
                  )}
                </div>
              </div>
            )}
          </div>
        )}

        {/* SECCIÓN 2: MONITOREO DE QUÓRUM */}
        {activeTab === 'quorum' && (
          <div>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
              <div>
                <h3 style={{ margin: 0, color: '#1C2A59', fontSize: '1.1rem' }}>
                  Supervisión de Quórum y Sesiones EPIS
                </h3>
                <p style={{ margin: '0.25rem 0 0', color: '#64748B', fontSize: '0.82rem' }}>
                  Una sesión alcanza quórum viable cuando sus reservas ratificadas son iguales o mayores al 50% de la
                  demanda mínima requerida.
                </p>
              </div>
              <button
                type="button"
                onClick={loadOffers}
                disabled={offersLoading}
                style={{
                  backgroundColor: '#F1F5F9',
                  border: '1px solid #CBD5E1',
                  borderRadius: '6px',
                  padding: '0.4rem 0.8rem',
                  fontSize: '0.8rem',
                  cursor: 'pointer',
                  fontWeight: 600,
                }}
              >
                🔄 Actualizar
              </button>
            </div>

            {offersError && (
              <div
                style={{
                  background: '#FDE8E8',
                  color: '#9B1C1C',
                  padding: '0.75rem',
                  borderRadius: '6px',
                  marginBottom: '1rem',
                  fontSize: '0.85rem',
                }}
              >
                {offersError}
              </div>
            )}

            {offersLoading ? (
              <div style={{ textAlign: 'center', padding: '2rem', color: '#64748B' }}>
                Cargando sesiones y estados de quórum...
              </div>
            ) : offers.length === 0 ? (
              <div style={{ textAlign: 'center', padding: '2rem', color: '#64748B' }}>
                No se registraron ofertas de mentoría activas en la plataforma.
              </div>
            ) : (
              <div style={{ display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                {offers.map((offer) => {
                  const details = offer.offer || (offer as unknown as Record<string, unknown>);
                  const modalidad = details.modalidad || (offer as unknown as { modalidad?: string }).modalidad || 'presencial';
                  const maxCap = offer.aforo || details.aforo_maximo || (modalidad === 'presencial' ? 10 : 20);
                  const enrolled = (offer as unknown as { cupos_ocupados?: number }).cupos_ocupados ?? 0;
                  const ratio = Math.round((enrolled / maxCap) * 100);
                  const meetsQuorum = ratio >= 50;
                  const materia = details.nombre_asignatura || (offer as unknown as { materia?: string }).materia || 'Asignatura';
                  const tema = details.nombre_tema || (offer as unknown as { tema?: string }).tema || 'Tema';
                  const mentor = details.mentor_email || (offer as unknown as { mentor_email?: string }).mentor_email || 'mentor@upt.pe';
                  const horario = details.fecha_inicio || (offer as unknown as { fecha_sesion?: string }).fecha_sesion || '';
                  const lugar = offer.espacio_asignado || details.espacio_asignado || (offer as unknown as { lugar_o_enlace?: string }).lugar_o_enlace || 'EPIS';

                  return (
                    <div
                      key={offer.id_oferta}
                      style={{
                        border: '1px solid #E2E8F0',
                        borderRadius: '8px',
                        padding: '1rem',
                        display: 'flex',
                        justifyContent: 'space-between',
                        alignItems: 'center',
                        flexWrap: 'wrap',
                        gap: '0.75rem',
                        backgroundColor: '#FFFFFF',
                      }}
                    >
                      <div style={{ flex: '1 1 300px' }}>
                        <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          <strong style={{ color: '#1C2A59', fontSize: '0.95rem' }}>{materia}</strong>
                          <span
                            style={{
                              fontSize: '0.7rem',
                              padding: '0.15rem 0.45rem',
                              borderRadius: '4px',
                              background: modalidad === 'presencial' ? '#FEF3C7' : '#E0E7FF',
                              color: modalidad === 'presencial' ? '#92400E' : '#3730A3',
                              fontWeight: 600,
                              textTransform: 'uppercase',
                            }}
                          >
                            {modalidad}
                          </span>
                        </div>
                        <div style={{ fontSize: '0.82rem', color: '#475569', marginTop: '0.2rem' }}>
                          Tema: <strong>{tema}</strong> · Mentor: {mentor}
                        </div>
                        <div style={{ fontSize: '0.75rem', color: '#64748B', marginTop: '0.2rem' }}>
                          Horario: {horario} ({lugar})
                        </div>
                      </div>

                      <div style={{ textAlign: 'right', minWidth: '160px' }}>
                        <div style={{ marginBottom: '0.35rem' }}>
                          <span
                            style={{
                              fontSize: '0.75rem',
                              fontWeight: 700,
                              padding: '0.25rem 0.6rem',
                              borderRadius: '9999px',
                              background: meetsQuorum ? '#DEF7EC' : '#FEF3C7',
                              color: meetsQuorum ? '#03543F' : '#92400E',
                            }}
                          >
                            {meetsQuorum ? '✅ Quórum Viable (≥50%)' : '⏳ En Convocatoria'}
                          </span>
                        </div>
                        <div style={{ fontSize: '0.8rem', color: '#334155' }}>
                          Aforo: <strong>{enrolled}</strong> / {maxCap} inscritos ({ratio}%)
                        </div>
                      </div>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        )}

        {/* SECCIÓN 3: AUDITORÍA DE BITÁCORAS (T-40 / T-41 / RF26 / RN-14) */}
        {activeTab === 'bitacoras' && (
          <div>
            <div style={{ marginBottom: '1.25rem' }}>
              <h3 style={{ margin: '0 0 0.5rem', color: '#1C2A59', fontSize: '1.1rem' }}>
                Bandeja de Auditoría de Bitácoras y Visado Institucional de Horas
              </h3>
              <p style={{ margin: 0, color: '#64748B', fontSize: '0.85rem', lineHeight: 1.5 }}>
                Fiscalización académica y refrendo oficial de horas de acompañamiento pedagógico (<strong>RF26 / RN-14</strong>).
                Solo las bitácoras con visado administrativo conmutan sus horas a formalmente acreditadas para certificación.
              </p>
            </div>

            {/* Filtros de la bandeja */}
            <div style={{ display: 'flex', gap: '0.5rem', marginBottom: '1.25rem', flexWrap: 'wrap' }}>
              {(
                [
                  { key: 'TODAS', label: 'Todas las Bitácoras' },
                  { key: 'PENDIENTES', label: 'Pendientes de Visado' },
                  { key: 'VISADAS', label: 'Horas Visadas y Acreditadas' },
                  { key: 'OBSERVADA', label: 'Observadas para Corrección' },
                ] as const
              ).map((f) => (
                <button
                  key={f.key}
                  type="button"
                  onClick={() => setBitacoraFiltro(f.key)}
                  style={{
                    padding: '0.45rem 0.85rem',
                    borderRadius: '6px',
                    border: '1px solid #CBD5E1',
                    background: bitacoraFiltro === f.key ? '#1C2A59' : '#FFFFFF',
                    color: bitacoraFiltro === f.key ? '#FFFFFF' : '#334155',
                    fontSize: '0.82rem',
                    fontWeight: 600,
                    cursor: 'pointer',
                  }}
                >
                  {f.label}
                </button>
              ))}
            </div>

            {/* Mensajes de feedback */}
            {bitacoraFeedback && (
              <div
                style={{
                  padding: '0.75rem 1rem',
                  borderRadius: '6px',
                  marginBottom: '1rem',
                  fontSize: '0.85rem',
                  background: bitacoraFeedback.type === 'success' ? '#DEF7EC' : '#FDE8E8',
                  color: bitacoraFeedback.type === 'success' ? '#03543F' : '#9B1C1C',
                  border: `1px solid ${bitacoraFeedback.type === 'success' ? '#84E1BC' : '#F8B4B4'}`,
                }}
              >
                {bitacoraFeedback.text}
              </div>
            )}

            {bitacorasError && (
              <div
                style={{
                  padding: '0.75rem 1rem',
                  borderRadius: '6px',
                  marginBottom: '1rem',
                  fontSize: '0.85rem',
                  background: '#FDE8E8',
                  color: '#9B1C1C',
                  border: '1px solid #F8B4B4',
                }}
              >
                {bitacorasError}
              </div>
            )}

            {/* Tabla de bitácoras */}
            {bitacorasLoading ? (
              <div style={{ textAlign: 'center', padding: '2rem', color: '#64748B' }}>
                Cargando bitácoras pedagógicas...
              </div>
            ) : bitacoras.length === 0 ? (
              <div
                style={{
                  textAlign: 'center',
                  padding: '2.5rem',
                  background: '#F8FAFC',
                  borderRadius: '8px',
                  border: '1px dashed #CBD5E1',
                  color: '#64748B',
                }}
              >
                No se registraron bitácoras bajo el filtro seleccionado.
              </div>
            ) : (
              <div style={{ overflowX: 'auto' }}>
                <table
                  style={{
                    width: '100%',
                    borderCollapse: 'collapse',
                    textAlign: 'left',
                    fontSize: '0.85rem',
                  }}
                >
                  <thead>
                    <tr style={{ background: '#F1F5F9', borderBottom: '2px solid #E2E8F0' }}>
                      <th style={{ padding: '0.75rem 1rem', color: '#1C2A59', fontWeight: 700 }}>
                        Código / Sesión
                      </th>
                      <th style={{ padding: '0.75rem 1rem', color: '#1C2A59', fontWeight: 700 }}>
                        Mentor Titular
                      </th>
                      <th style={{ padding: '0.75rem 1rem', color: '#1C2A59', fontWeight: 700 }}>
                        Horas
                      </th>
                      <th style={{ padding: '0.75rem 1rem', color: '#1C2A59', fontWeight: 700 }}>
                        Estado
                      </th>
                      <th style={{ padding: '0.75rem 1rem', color: '#1C2A59', fontWeight: 700 }}>
                        Acciones
                      </th>
                    </tr>
                  </thead>
                  <tbody>
                    {bitacoras.map((b) => {
                      const isVisada = b.visado_administrador || b.estado_sesion === 'HORAS_VISADAS';
                      const isObservada = b.estado_sesion === 'OBSERVADA';

                      return (
                        <tr
                          key={b.id_bitacora}
                          style={{
                            borderBottom: '1px solid #E2E8F0',
                            transition: 'background-color 0.15s ease',
                          }}
                        >
                          <td style={{ padding: '0.85rem 1rem', fontWeight: 600, color: '#1E293B' }}>
                            {b.codigo_sesion || `SES-${b.id_sesion}`}
                          </td>
                          <td style={{ padding: '0.85rem 1rem', color: '#475569' }}>
                            {b.id_mentor}
                          </td>
                          <td style={{ padding: '0.85rem 1rem', color: '#334155', fontWeight: 600 }}>
                            {b.horas_declaradas.toFixed(1)} h
                          </td>
                          <td style={{ padding: '0.85rem 1rem' }}>
                            {isVisada ? (
                              <span
                                style={{
                                  display: 'inline-block',
                                  padding: '0.25rem 0.6rem',
                                  borderRadius: '9999px',
                                  background: '#DEF7EC',
                                  color: '#03543F',
                                  fontWeight: 700,
                                  fontSize: '0.75rem',
                                }}
                              >
                                Horas Acreditadas
                              </span>
                            ) : isObservada ? (
                              <span
                                style={{
                                  display: 'inline-block',
                                  padding: '0.25rem 0.6rem',
                                  borderRadius: '9999px',
                                  background: '#FDE8E8',
                                  color: '#9B1C1C',
                                  fontWeight: 700,
                                  fontSize: '0.75rem',
                                }}
                              >
                                Observada
                              </span>
                            ) : (
                              <span
                                style={{
                                  display: 'inline-block',
                                  padding: '0.25rem 0.6rem',
                                  borderRadius: '9999px',
                                  background: '#FEF3C7',
                                  color: '#92400E',
                                  fontWeight: 700,
                                  fontSize: '0.75rem',
                                }}
                              >
                                Pendiente de Visado
                              </span>
                            )}
                          </td>
                          <td style={{ padding: '0.85rem 1rem' }}>
                            <div style={{ display: 'flex', gap: '0.4rem', flexWrap: 'wrap' }}>
                              <button
                                type="button"
                                onClick={() => setSelectedBitacoraDetail(b)}
                                style={{
                                  padding: '0.35rem 0.65rem',
                                  borderRadius: '5px',
                                  border: '1px solid #CBD5E1',
                                  background: '#FFFFFF',
                                  color: '#334155',
                                  fontSize: '0.78rem',
                                  fontWeight: 600,
                                  cursor: 'pointer',
                                }}
                              >
                                Ver Detalle Pedagógico
                              </button>
                              {!isVisada && (
                                <button
                                  type="button"
                                  onClick={() => handleVisarBitacora(b)}
                                  disabled={bitacoraActionLoading}
                                  style={{
                                    padding: '0.35rem 0.65rem',
                                    borderRadius: '5px',
                                    border: 'none',
                                    background: '#059669',
                                    color: '#FFFFFF',
                                    fontSize: '0.78rem',
                                    fontWeight: 600,
                                    cursor: 'pointer',
                                  }}
                                >
                                  Aprobar y Visar Horas
                                </button>
                              )}
                              <button
                                type="button"
                                onClick={() => {
                                  setObservingBitacora(b);
                                  setMotivoObservacion('');
                                }}
                                disabled={bitacoraActionLoading}
                                style={{
                                  padding: '0.35rem 0.65rem',
                                  borderRadius: '5px',
                                  border: 'none',
                                  background: '#DC2626',
                                  color: '#FFFFFF',
                                  fontSize: '0.78rem',
                                  fontWeight: 600,
                                  cursor: 'pointer',
                                }}
                              >
                                Observar Bitácora
                              </button>
                            </div>
                          </td>
                        </tr>
                      );
                    })}
                  </tbody>
                </table>
              </div>
            )}

            {/* Modal de Detalle Pedagógico e Inspección SHA-256 */}
            {selectedBitacoraDetail && (
              <div
                style={{
                  position: 'fixed',
                  inset: 0,
                  backgroundColor: 'rgba(15, 23, 42, 0.6)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  padding: '1rem',
                  zIndex: 50,
                }}
                role="dialog"
                aria-modal="true"
                aria-label="Detalle Pedagógico de Bitácora"
              >
                <div
                  style={{
                    backgroundColor: '#FFFFFF',
                    borderRadius: '12px',
                    maxWidth: '600px',
                    width: '100%',
                    padding: '1.5rem',
                    boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '1rem' }}>
                    <h4 style={{ margin: 0, color: '#1C2A59', fontSize: '1.1rem', fontWeight: 700 }}>
                      Detalle de Bitácora Pedagógica
                    </h4>
                    <button
                      type="button"
                      onClick={() => setSelectedBitacoraDetail(null)}
                      style={{ border: 'none', background: 'transparent', fontSize: '1.2rem', cursor: 'pointer' }}
                    >
                      ✕
                    </button>
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#475569', display: 'flex', flexDirection: 'column', gap: '0.75rem' }}>
                    <div>
                      <strong>Mentor:</strong> {selectedBitacoraDetail.id_mentor}
                    </div>
                    <div>
                      <strong>Temas Cubiertos:</strong>
                      <ul style={{ margin: '0.25rem 0 0', paddingLeft: '1.25rem' }}>
                        {selectedBitacoraDetail.temas_cubiertos.map((t, idx) => (
                          <li key={idx}>{t}</li>
                        ))}
                      </ul>
                    </div>
                    <div>
                      <strong>Nivel de Dificultad Percibido:</strong> {selectedBitacoraDetail.nivel_dificultad}
                    </div>
                    <div>
                      <strong>Observaciones Docentes:</strong>
                      <p style={{ margin: '0.25rem 0 0', background: '#F8FAFC', padding: '0.6rem', borderRadius: '6px', border: '1px solid #E2E8F0' }}>
                        {selectedBitacoraDetail.observaciones}
                      </p>
                    </div>
                    <div>
                      <strong>Firma Criptográfica SHA-256:</strong>
                      <code
                        style={{
                          display: 'block',
                          margin: '0.25rem 0 0',
                          padding: '0.5rem',
                          background: '#0F172A',
                          color: '#38BDF8',
                          borderRadius: '6px',
                          fontSize: '0.75rem',
                          wordBreak: 'break-all',
                        }}
                      >
                        {selectedBitacoraDetail.hash_firma}
                      </code>
                    </div>
                  </div>
                  <div style={{ marginTop: '1.25rem', textAlign: 'right' }}>
                    <button
                      type="button"
                      onClick={() => setSelectedBitacoraDetail(null)}
                      style={{
                        padding: '0.5rem 1rem',
                        borderRadius: '6px',
                        border: 'none',
                        background: '#1C2A59',
                        color: '#FFFFFF',
                        fontWeight: 600,
                        fontSize: '0.82rem',
                        cursor: 'pointer',
                      }}
                    >
                      Cerrar
                    </button>
                  </div>
                </div>
              </div>
            )}

            {/* Diálogo Modal Accesible de Observación Técnica */}
            {observingBitacora && (
              <div
                style={{
                  position: 'fixed',
                  inset: 0,
                  backgroundColor: 'rgba(15, 23, 42, 0.6)',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  padding: '1rem',
                  zIndex: 50,
                }}
                role="dialog"
                aria-modal="true"
                aria-label="Observar Bitácora Pedagógica"
              >
                <div
                  style={{
                    backgroundColor: '#FFFFFF',
                    borderRadius: '12px',
                    maxWidth: '520px',
                    width: '100%',
                    padding: '1.5rem',
                    boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1)',
                  }}
                >
                  <h4 style={{ margin: '0 0 0.5rem', color: '#B91C1C', fontSize: '1.1rem', fontWeight: 700 }}>
                    Formular Observación Técnica
                  </h4>
                  <p style={{ margin: '0 0 1rem', fontSize: '0.85rem', color: '#64748B' }}>
                    Detalla el motivo técnico o discrepancia detectada para que el mentor titular proceda con su subsanación.
                    (Justificación obligatoria de al menos 15 caracteres).
                  </p>
                  <form onSubmit={handleObservarSubmit}>
                    <textarea
                      role="textbox"
                      required
                      rows={4}
                      value={motivoObservacion}
                      onChange={(e) => setMotivoObservacion(e.target.value)}
                      placeholder="Ingrese los motivos fundamentados de la observación técnica..."
                      style={{
                        width: '100%',
                        padding: '0.65rem 0.85rem',
                        border: '1px solid #CBD5E1',
                        borderRadius: '6px',
                        fontSize: '0.85rem',
                        boxSizing: 'border-box',
                        marginBottom: '0.5rem',
                      }}
                    />
                    <div style={{ fontSize: '0.75rem', color: motivoObservacion.trim().length >= 15 ? '#059669' : '#DC2626', marginBottom: '1rem' }}>
                      {motivoObservacion.trim().length}/15 caracteres mínimos
                    </div>
                    <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.5rem' }}>
                      <button
                        type="button"
                        onClick={() => setObservingBitacora(null)}
                        style={{
                          padding: '0.5rem 1rem',
                          borderRadius: '6px',
                          border: '1px solid #CBD5E1',
                          background: '#FFFFFF',
                          color: '#475569',
                          fontWeight: 600,
                          fontSize: '0.82rem',
                          cursor: 'pointer',
                        }}
                      >
                        Cancelar
                      </button>
                      <button
                        type="submit"
                        disabled={bitacoraActionLoading || motivoObservacion.trim().length < 15}
                        style={{
                          padding: '0.5rem 1rem',
                          borderRadius: '6px',
                          border: 'none',
                          background: '#DC2626',
                          color: '#FFFFFF',
                          fontWeight: 600,
                          fontSize: '0.82rem',
                          cursor: 'pointer',
                          opacity: motivoObservacion.trim().length < 15 ? 0.6 : 1,
                        }}
                      >
                        Confirmar Observación
                      </button>
                    </div>
                  </form>
                </div>
              </div>
            )}
          </div>
        )}

        {/* SECCIÓN 4: GESTIÓN CURRICULAR (RF05 / CUS21) */}
        {activeTab === 'curriculum' && (
          <div>
            <div style={{ marginBottom: '1.5rem' }}>
              <h3 style={{ margin: '0 0 0.5rem', color: '#1C2A59', fontSize: '1.1rem' }}>
                Gestión y Mantenimiento del Catálogo Curricular Oficial (RF05 / CUS21)
              </h3>
              <p style={{ margin: 0, color: '#64748B', fontSize: '0.85rem', lineHeight: 1.5 }}>
                Como Administrador institucional de la EPIS-UPT, puedes registrar nuevas materias críticas de I a IV ciclo,
                actualizar créditos y factores de mérito algorítmico, y mantener la taxonomía jerárquica de temas silábicos oficiales.
              </p>
            </div>
            <CurriculumCatalogView isAdmin={true} />
          </div>
        )}

        {/* SECCIÓN 5: CRONOGRAMAS Y PARSER DE HORARIOS (RF10 / CUS11 / RN-06) */}
        {activeTab === 'schedule' && (
          <AdminScheduleUploadView />
        )}

        {/* SECCIÓN 6: SALUD DEL SISTEMA */}
        {activeTab === 'health' && (
          <div>
            <HealthStatus />
          </div>
        )}
      </div>
    </div>
  );
};
