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
import { HealthStatus } from './HealthStatus';

export interface AdminDashboardViewProps {
  adminEmail?: string;
}

export const AdminDashboardView: React.FC<AdminDashboardViewProps> = ({
  adminEmail = 'admin.epis@upt.pe',
}) => {
  const [activeTab, setActiveTab] = useState<'roles' | 'quorum' | 'health'>('roles');

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

  useEffect(() => {
    if (activeTab === 'quorum') {
      loadOffers();
    }
  }, [activeTab, loadOffers]);

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
                Asignación y Validación de Mérito de Mentores (RN-03 / RF03)
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
                2022074255 (Joan - Ciclo 7)
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
                2022073504 (Renzo - Ciclo 8 / Mentor)
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
                2023079999 (Novato - Ciclo 2)
              </button>
            </div>

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
                      ⭐ Promover a Mentor (Verificar Mérito RN-03)
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
                  Supervisión de Quórum y Sesiones EPIS (RN-09)
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

        {/* SECCIÓN 3: SALUD DEL SISTEMA */}
        {activeTab === 'health' && (
          <div>
            <HealthStatus />
          </div>
        )}
      </div>
    </div>
  );
};
