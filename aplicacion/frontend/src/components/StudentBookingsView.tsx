/**
 * Componente: Bandeja de Reservas Personales y Ratificación de Asistencia (T-25)
 * Módulo MOD-05: Quórum, Confirmación y Cancelaciones.
 *
 * Trazabilidad:
 * - Requerimiento Funcional: RF13 / CUS24 (Confirmación anticipada de asistencia a mentoría)
 * - Compromiso de Participación: PB-014 (Compromiso formativo del mentoreado)
 * - Regla de Negocio RN-08: Ventana de confirmación de asistencia hasta T-24 horas
 * - Regla de Negocio RN-09: Cómputo del quórum regulatorio del 50%
 * - Regla de Negocio RN-10: Política de desistimiento antes de T-24 horas
 * - Requerimiento No Funcional: RNF05 (Accesibilidad WAI-ARIA y diseño responsive)
 * - Requerimiento No Funcional: RNF09 (Mantenibilidad y cobertura de pruebas)
 */

import React, { useState, useEffect, useCallback, useId, useRef } from 'react';
import {
  bookingService,
  type BookingDetailResponse,
  type BookingStatus,
  BookingException,
} from '../services/bookingService';
import { authService } from '../services/authService';

/**
 * Propiedades del componente StudentBookingsView (T-25 / RF13 / CUS24).
 */
export interface StudentBookingsViewProps {
  /** Correo institucional del estudiante mentoreado (se resuelve desde JWT si se omite) */
  studentEmail?: string;
  /** Timestamp simulado opcional para pruebas deterministas de ventanas temporales */
  currentTime?: number;
  /** Callback para navegar a la cartelera de recomendaciones cuando no hay reservas */
  onExploreRecommendations?: () => void;
  /** Callback para redirigir al login institucional cuando no existe sesión activa */
  onLoginRedirect?: () => void;
}

/**
 * Resuelve la identidad institucional activa a partir de props o decodificación de JWT.
 */
function resolveEffectiveStudentEmail(propEmail?: string): string | null {
  if (propEmail && propEmail.trim().endsWith('@upt.pe')) {
    return propEmail.trim().toLowerCase();
  }
  const token = authService.getToken();
  if (token) {
    try {
      const parts = token.split('.');
      if (parts.length === 3) {
        const payloadJson = atob(parts[1].replace(/-/g, '+').replace(/_/g, '/'));
        const payload = JSON.parse(payloadJson);
        if (typeof payload.sub === 'string' && payload.sub.includes('@upt.pe')) {
          return payload.sub.trim().toLowerCase();
        }
        if (typeof payload.email === 'string' && payload.email.includes('@upt.pe')) {
          return payload.email.trim().toLowerCase();
        }
      }
    } catch {
      // Ignorar fallos de decodificación
    }
  }
  return null;
}

/**
 * Formatea una fecha ISO 8601 a un formato comprensible en español peruano (es-PE).
 */
function formatDateTime(isoString?: string | null): string {
  if (!isoString) return 'Por coordinar';
  try {
    const date = new Date(isoString);
    if (isNaN(date.getTime())) return isoString;
    return new Intl.DateTimeFormat('es-PE', {
      weekday: 'short',
      day: 'numeric',
      month: 'short',
      year: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: true,
    }).format(date);
  } catch {
    return isoString;
  }
}

/**
 * Evalúa preventivamente en cliente la regla de negocio RN-08 (corte a T-24h).
 */
function evaluateT24Window(
  sessionStartIso?: string | null,
  referenceTimeMs?: number
): {
  isOpen: boolean;
  isPast: boolean;
  hoursRemaining: number;
  cutoffIso: string | null;
  message: string;
} {
  if (!sessionStartIso) {
    return {
      isOpen: false,
      isPast: false,
      hoursRemaining: 0,
      cutoffIso: null,
      message: 'Fecha de inicio no disponible',
    };
  }

  const startTime = new Date(sessionStartIso).getTime();
  if (isNaN(startTime)) {
    return {
      isOpen: false,
      isPast: false,
      hoursRemaining: 0,
      cutoffIso: null,
      message: 'Formato de fecha de sesión inválido',
    };
  }

  const now = referenceTimeMs ?? Date.now();
  const diffMs = startTime - now;
  const hoursRemaining = Math.floor(diffMs / (3600 * 1000));
  const cutoffTime = startTime - 24 * 3600 * 1000;
  const cutoffIso = new Date(cutoffTime).toISOString();

  if (diffMs <= 0) {
    return {
      isOpen: false,
      isPast: true,
      hoursRemaining: 0,
      cutoffIso,
      message: 'La sesión de mentoría ya se encuentra en curso o concluida.',
    };
  }

  // Estricto: mayor a 24 horas (diffMs > 24 * 3600 * 1000)
  if (diffMs <= 24 * 3600 * 1000) {
    return {
      isOpen: false,
      isPast: false,
      hoursRemaining,
      cutoffIso,
      message:
        'Ventana de ratificación cerrada (RN-08): El corte perentorio se cumplió a las 24 horas previas al inicio.',
    };
  }

  return {
    isOpen: true,
    isPast: false,
    hoursRemaining,
    cutoffIso,
    message: `Ventana de ratificación abierta: Restan aproximadamente ${hoursRemaining} horas para el inicio de la clase.`,
  };
}

/**
 * Configuración visual de etiquetas y estilos por cada estado del ciclo de vida (MOD-05).
 */
interface StatusConfig {
  label: string;
  badgeBg: string;
  badgeText: string;
  badgeBorder: string;
  description: string;
}

function getStatusConfig(status: BookingStatus | string): StatusConfig {
  switch (status) {
    case 'PENDIENTE_CONFIRMACION':
      return {
        label: 'Pendiente de Ratificación',
        badgeBg: '#FEF3C7',
        badgeText: '#92400E',
        badgeBorder: '#F59E0B',
        description:
          'Cupo provisional. Debes ratificar tu asistencia antes de T-24h para ser contabilizado en el quórum (RN-08).',
      };
    case 'CONFIRMADA':
      return {
        label: 'Asistencia Ratificada',
        badgeBg: '#D1FAE5',
        badgeText: '#065F46',
        badgeBorder: '#10B981',
        description:
          'Has ratificado tu asistencia. Tu cupo está asegurado en la evaluación del quórum regulatorio (RN-09).',
      };
    case 'NO_CONFIRMADA':
      return {
        label: 'No Confirmada (Expirada)',
        badgeBg: '#FEE2E2',
        badgeText: '#991B1B',
        badgeBorder: '#EF4444',
        description:
          'La reserva no fue ratificada antes del corte de 24 horas y el cupo fue liberado automáticamente.',
      };
    case 'CANCELADA_USUARIO':
      return {
        label: 'Desistimiento Voluntario',
        badgeBg: '#F3F4F6',
        badgeText: '#374151',
        badgeBorder: '#9CA3AF',
        description: 'Cancelada voluntariamente por el estudiante conforme a la política RN-10.',
      };
    case 'CANCELADA_SISTEMA':
      return {
        label: 'Cancelada por el Sistema',
        badgeBg: '#FEE2E2',
        badgeText: '#7F1D1D',
        badgeBorder: '#DC2626',
        description:
          'Sesión suspendida por el sistema al no alcanzar el quórum del 50% reglamentario (RN-09).',
      };
    case 'ASISTIDA':
      return {
        label: 'Asistencia Cumplida',
        badgeBg: '#DBEAFE',
        badgeText: '#1E40AF',
        badgeBorder: '#3B82F6',
        description: 'Asistencia registrada satisfactoriamente por el mentor en la bitácora.',
      };
    case 'INASISTENCIA':
      return {
        label: 'Inasistencia Registrada',
        badgeBg: '#FCE7F3',
        badgeText: '#831843',
        badgeBorder: '#EC4899',
        description: 'Inasistencia no justificada reportada al culminar la sesión.',
      };
    default:
      return {
        label: String(status),
        badgeBg: '#F1F5F9',
        badgeText: '#334155',
        badgeBorder: '#CBD5E1',
        description: 'Estado registrado en el sistema.',
      };
  }
}

export const StudentBookingsView: React.FC<StudentBookingsViewProps> = ({
  studentEmail: propEmail,
  currentTime,
  onExploreRecommendations,
  onLoginRedirect,
}) => {
  const componentId = useId();

  // Resolución de identidad del estudiante
  const effectiveEmail = resolveEffectiveStudentEmail(propEmail);

  // Estados principales de la vista
  const [bookings, setBookings] = useState<BookingDetailResponse[]>([]);
  const [isLoading, setIsLoading] = useState<boolean>(true);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [statusFilter, setStatusFilter] = useState<string>('TODAS');

  // Estado del diálogo modal de confirmación pedagógica (T-25 / RF13 / CUS24)
  const [confirmingBooking, setConfirmingBooking] = useState<BookingDetailResponse | null>(null);
  const [isSubmittingConfirm, setIsSubmittingConfirm] = useState<boolean>(false);
  const [confirmError, setConfirmError] = useState<string | null>(null);
  const [notificationMessage, setNotificationMessage] = useState<{
    type: 'success' | 'info' | 'error';
    text: string;
  } | null>(null);

  // Referencias para accesibilidad y focus trap en el diálogo
  const dialogRef = useRef<HTMLDivElement>(null);
  const cancelBtnRef = useRef<HTMLButtonElement>(null);

  /**
   * Carga las reservas del estudiante autenticado desde el servicio activo.
   */
  const loadBookings = useCallback(async () => {
    if (!effectiveEmail) {
      setIsLoading(false);
      return;
    }

    try {
      setIsLoading(true);
      setErrorMessage(null);

      // Si se definió un tiempo simulado en props, sincronizarlo en el mockAdapter para pruebas
      if (typeof currentTime === 'number') {
        bookingService.setCurrentTime(currentTime);
      }

      const list = await bookingService.getMyReservations(undefined, effectiveEmail);
      // Garantizar que solo se visualicen reservas del estudiante autenticado
      const studentOnly = list.filter(
        (b) => b.estudiante_email.trim().toLowerCase() === effectiveEmail.trim().toLowerCase()
      );
      setBookings(studentOnly);
    } catch (err: unknown) {
      if (err instanceof BookingException) {
        setErrorMessage(err.message);
      } else {
        setErrorMessage('Ocurrió un error inesperado al cargar tus reservas de mentoría.');
      }
    } finally {
      setIsLoading(false);
    }
  }, [effectiveEmail, currentTime]);

  useEffect(() => {
    loadBookings();
  }, [loadBookings]);

  /**
   * Cierra el diálogo de ratificación descartando cambios.
   */
  const handleCloseDialog = useCallback(() => {
    setConfirmingBooking(null);
    setConfirmError(null);
    setIsSubmittingConfirm(false);
  }, []);

  /**
   * Abre el diálogo accesible de ratificación pedagógica.
   */
  const handleOpenConfirmDialog = (booking: BookingDetailResponse) => {
    setConfirmingBooking(booking);
    setConfirmError(null);
  };

  // Manejo de foco accesible cuando se abre el diálogo
  useEffect(() => {
    if (confirmingBooking) {
      setTimeout(() => {
        cancelBtnRef.current?.focus();
      }, 50);
    }
  }, [confirmingBooking]);

  // Manejo de tecla Escape para cerrar el diálogo
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape' && confirmingBooking && !isSubmittingConfirm) {
        handleCloseDialog();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [confirmingBooking, isSubmittingConfirm, handleCloseDialog]);

  /**
   * Ejecuta la ratificación de asistencia consumiendo bookingService.confirmAttendance (T-25 / RF13).
   */
  const handleExecuteConfirmation = async () => {
    if (!confirmingBooking) return;

    try {
      setIsSubmittingConfirm(true);
      setConfirmError(null);

      const updated = await bookingService.confirmAttendance(
        confirmingBooking.id_reserva,
        effectiveEmail ?? undefined
      );

      // Éxito en la ratificación
      setNotificationMessage({
        type: 'success',
        text: `¡Asistencia ratificada con éxito para ${updated.nombre_asignatura || 'la sesión'}! Tu cupo está asegurado en la evaluación de quórum.`,
      });

      handleCloseDialog();
      // Recargar lista para refrescar estados desde la fuente de datos activa
      await loadBookings();
    } catch (err: unknown) {
      if (err instanceof BookingException) {
        if (err.code === 'ENDPOINT_NOT_IMPLEMENTED') {
          // Explicación pedagógica cuando el backend de Renzo (T-26) está en desarrollo
          setConfirmError(
            'ℹ️ Integración pendiente en backend (T-26): El servicio de ratificación en el servidor FastAPI está en desarrollo por Renzo. La interfaz está lista y conectada contractualmente.'
          );
        } else if (err.code === 'WINDOW_CLOSED_T24H') {
          setConfirmError(
            'Infracción de RN-08: El plazo perentorio de ratificación cerró a las 24 horas previas al inicio de la sesión.'
          );
        } else if (err.code === 'INVALID_STATUS_TRANSITION') {
          setConfirmError('Esta reserva ya fue confirmada o se encuentra en un estado incompatible.');
        } else if (err.code === 'FORBIDDEN') {
          setConfirmError('No tienes autorización para ratificar una reserva de otro estudiante.');
        } else if (err.code === 'NETWORK_ERROR') {
          setConfirmError('No fue posible contactar al servidor. Verifica tu conectividad institucional.');
        } else {
          setConfirmError(err.message);
        }
      } else {
        setConfirmError('Error imprevisto al procesar la ratificación de asistencia.');
      }
    } finally {
      setIsSubmittingConfirm(false);
    }
  };

  // Filtrado reactivo de reservas
  const filteredBookings = bookings.filter((b) => {
    if (statusFilter === 'TODAS') return true;
    if (statusFilter === 'PENDIENTES') return b.estado === 'PENDIENTE_CONFIRMACION';
    if (statusFilter === 'CONFIRMADAS') return b.estado === 'CONFIRMADA';
    if (statusFilter === 'HISTORICO') {
      return (
        b.estado === 'CANCELADA_USUARIO' ||
        b.estado === 'CANCELADA_SISTEMA' ||
        b.estado === 'NO_CONFIRMADA' ||
        b.estado === 'ASISTIDA' ||
        b.estado === 'INASISTENCIA'
      );
    }
    return true;
  });

  // ==========================================================================
  // Renderizado: Caso sin autenticación institucional
  // ==========================================================================
  if (!effectiveEmail) {
    return (
      <section
        className="student-bookings-container"
        aria-labelledby={`${componentId}-unauth-title`}
        style={{
          maxWidth: '1000px',
          margin: '0 auto',
          padding: '24px 16px',
          fontFamily: 'system-ui, -apple-system, sans-serif',
        }}
      >
        <div
          style={{
            backgroundColor: '#FFFBEB',
            border: '1px solid #FCD34D',
            borderRadius: '8px',
            padding: '24px',
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: '36px', marginBottom: '12px' }}>🔒</div>
          <h2
            id={`${componentId}-unauth-title`}
            style={{ color: '#002147', fontSize: '20px', fontWeight: 700, margin: '0 0 8px 0' }}
          >
            Acceso Restringido a Mis Reservas (RN-01)
          </h2>
          <p style={{ color: '#4B5563', fontSize: '14px', maxWidth: '520px', margin: '0 auto 20px auto' }}>
            Para consultar tus cupos inscritos y ratificar formalmente tu asistencia, debes iniciar sesión
            con tu cuenta institucional de la <strong>Universidad Privada de Tacna (@upt.pe)</strong>.
          </p>
          {onLoginRedirect && (
            <button
              onClick={onLoginRedirect}
              style={{
                backgroundColor: '#002147',
                color: '#FFFFFF',
                border: 'none',
                padding: '10px 22px',
                borderRadius: '6px',
                fontSize: '14px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Iniciar Sesión Institucional
            </button>
          )}
        </div>
      </section>
    );
  }

  // ==========================================================================
  // Renderizado Principal
  // ==========================================================================
  return (
    <section
      className="student-bookings-view"
      aria-labelledby={`${componentId}-header-title`}
      style={{
        maxWidth: '1050px',
        margin: '0 auto',
        padding: '20px 16px',
        fontFamily: 'system-ui, -apple-system, sans-serif',
      }}
    >
      {/* Encabezado Institucional EPIS-UPT */}
      <header
        style={{
          borderBottom: '2px solid #002147',
          paddingBottom: '16px',
          marginBottom: '20px',
          display: 'flex',
          flexWrap: 'wrap',
          justifyContent: 'space-between',
          alignItems: 'center',
          gap: '12px',
        }}
      >
        <div>
          <div style={{ display: 'flex', alignItems: 'center', gap: '8px', marginBottom: '4px' }}>
            <span
              style={{
                backgroundColor: '#002147',
                color: '#F59E0B',
                fontSize: '11px',
                fontWeight: 800,
                padding: '3px 8px',
                borderRadius: '4px',
                letterSpacing: '0.5px',
              }}
            >
              EPIS · UPT
            </span>
            <span style={{ fontSize: '12px', color: '#64748B', fontWeight: 600 }}>
              Módulo MOD-05: Quórum & Confirmación
            </span>
          </div>
          <h1
            id={`${componentId}-header-title`}
            style={{
              color: '#002147',
              fontSize: '24px',
              fontWeight: 800,
              margin: '0 0 4px 0',
            }}
          >
            Mis Reservas de Mentoría
          </h1>
          <p style={{ color: '#475569', fontSize: '13px', margin: 0 }}>
            Estudiante autenticado: <strong>{effectiveEmail}</strong>
          </p>
        </div>

        {/* Acciones de cabecera */}
        <div style={{ display: 'flex', gap: '8px', alignItems: 'center' }}>
          <button
            onClick={loadBookings}
            disabled={isLoading}
            aria-label="Actualizar nómina de reservas personales"
            style={{
              backgroundColor: '#FFFFFF',
              color: '#002147',
              border: '1px solid #CBD5E1',
              borderRadius: '6px',
              padding: '8px 14px',
              fontSize: '13px',
              fontWeight: 600,
              cursor: isLoading ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '6px',
            }}
          >
            <span aria-hidden="true">🔄</span> {isLoading ? 'Actualizando...' : 'Actualizar'}
          </button>
          {onExploreRecommendations && (
            <button
              onClick={onExploreRecommendations}
              style={{
                backgroundColor: '#002147',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '6px',
                padding: '8px 14px',
                fontSize: '13px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              + Buscar Mentorías
            </button>
          )}
        </div>
      </header>

      {/* Notificaciones globales */}
      {notificationMessage && (
        <div
          role="alert"
          style={{
            backgroundColor: notificationMessage.type === 'success' ? '#ECFDF5' : '#EFF6FF',
            border: `1px solid ${notificationMessage.type === 'success' ? '#10B981' : '#3B82F6'}`,
            borderRadius: '6px',
            padding: '12px 16px',
            marginBottom: '16px',
            color: notificationMessage.type === 'success' ? '#065F46' : '#1E40AF',
            fontSize: '14px',
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
          }}
        >
          <div>
            <strong>{notificationMessage.type === 'success' ? '✓ ' : 'ℹ️ '}</strong>
            {notificationMessage.text}
          </div>
          <button
            onClick={() => setNotificationMessage(null)}
            aria-label="Cerrar notificación"
            style={{
              background: 'none',
              border: 'none',
              color: 'inherit',
              cursor: 'pointer',
              fontSize: '16px',
              padding: '0 4px',
            }}
          >
            ✕
          </button>
        </div>
      )}

      {/* Barra de Filtros */}
      <nav
        aria-label="Filtro de reservas por estado"
        style={{
          display: 'flex',
          flexWrap: 'wrap',
          gap: '8px',
          marginBottom: '20px',
          borderBottom: '1px solid #E2E8F0',
          paddingBottom: '10px',
        }}
      >
        {[
          { id: 'TODAS', label: `Todas (${bookings.length})` },
          {
            id: 'PENDIENTES',
            label: `Por Ratificar (${bookings.filter((b) => b.estado === 'PENDIENTE_CONFIRMACION').length})`,
          },
          {
            id: 'CONFIRMADAS',
            label: `Ratificadas (${bookings.filter((b) => b.estado === 'CONFIRMADA').length})`,
          },
          {
            id: 'HISTORICO',
            label: `Histórico / Otras (${
              bookings.filter(
                (b) =>
                  b.estado !== 'PENDIENTE_CONFIRMACION' && b.estado !== 'CONFIRMADA'
              ).length
            })`,
          },
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => setStatusFilter(tab.id)}
            style={{
              backgroundColor: statusFilter === tab.id ? '#002147' : '#F8FAFC',
              color: statusFilter === tab.id ? '#FFFFFF' : '#475569',
              border: '1px solid',
              borderColor: statusFilter === tab.id ? '#002147' : '#CBD5E1',
              borderRadius: '20px',
              padding: '6px 14px',
              fontSize: '12px',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.15s ease-in-out',
            }}
          >
            {tab.label}
          </button>
        ))}
      </nav>

      {/* Contenido según estados de carga / error / lista */}
      {isLoading ? (
        <div
          role="status"
          aria-live="polite"
          style={{
            padding: '48px 16px',
            textAlign: 'center',
            backgroundColor: '#F8FAFC',
            borderRadius: '8px',
            border: '1px dashed #CBD5E1',
          }}
        >
          <div
            style={{
              display: 'inline-block',
              width: '28px',
              height: '28px',
              border: '3px solid #CBD5E1',
              borderTopColor: '#002147',
              borderRadius: '50%',
              animation: 'spin 1s linear infinite',
              marginBottom: '12px',
            }}
          />
          <p style={{ color: '#475569', fontSize: '14px', margin: 0, fontWeight: 500 }}>
            Consultando nómina de reservas de mentoría...
          </p>
        </div>
      ) : errorMessage ? (
        <div
          role="alert"
          style={{
            backgroundColor: '#FEF2F2',
            border: '1px solid #FCA5A5',
            borderRadius: '8px',
            padding: '24px',
            textAlign: 'center',
          }}
        >
          <div style={{ fontSize: '32px', marginBottom: '8px' }}>⚠️</div>
          <h2 style={{ color: '#991B1B', fontSize: '18px', margin: '0 0 8px 0' }}>
            No fue posible cargar tus reservas
          </h2>
          <p style={{ color: '#7F1D1D', fontSize: '13px', margin: '0 auto 16px auto', maxWidth: '500px' }}>
            {errorMessage}
          </p>
          <button
            onClick={loadBookings}
            style={{
              backgroundColor: '#991B1B',
              color: '#FFFFFF',
              border: 'none',
              padding: '8px 18px',
              borderRadius: '6px',
              fontSize: '13px',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Reintentar Consulta
          </button>
        </div>
      ) : filteredBookings.length === 0 ? (
        <div
          style={{
            padding: '48px 16px',
            textAlign: 'center',
            backgroundColor: '#F8FAFC',
            borderRadius: '8px',
            border: '1px dashed #CBD5E1',
          }}
        >
          <div style={{ fontSize: '36px', marginBottom: '10px' }}>📋</div>
          <h2 style={{ color: '#002147', fontSize: '18px', fontWeight: 700, margin: '0 0 6px 0' }}>
            No se encontraron reservas
          </h2>
          <p style={{ color: '#64748B', fontSize: '13px', margin: '0 auto 18px auto', maxWidth: '480px' }}>
            {statusFilter === 'TODAS'
              ? 'Aún no te has inscrito en ninguna sesión de mentoría académica. Explora el catálogo de recomendaciones para reservar tu cupo.'
              : 'No cuentas con reservas que coincidan con el filtro seleccionado.'}
          </p>
          {onExploreRecommendations && (
            <button
              onClick={onExploreRecommendations}
              style={{
                backgroundColor: '#002147',
                color: '#FFFFFF',
                border: 'none',
                padding: '10px 20px',
                borderRadius: '6px',
                fontSize: '13px',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              Explorar Clases Recomendadas
            </button>
          )}
        </div>
      ) : (
        <div
          role="region"
          aria-label="Listado de reservas de mentoría"
          style={{ display: 'grid', gridTemplateColumns: '1fr', gap: '16px' }}
        >
          {filteredBookings.map((booking) => {
            const statusConfig = getStatusConfig(booking.estado);
            const timeCheck = evaluateT24Window(booking.fecha_inicio, currentTime);
            const isPending = booking.estado === 'PENDIENTE_CONFIRMACION';
            const isConfirmed = booking.estado === 'CONFIRMADA';
            const canConfirm = isPending && timeCheck.isOpen;

            return (
              <article
                key={booking.id_reserva}
                aria-labelledby={`booking-card-title-${booking.id_reserva}`}
                style={{
                  backgroundColor: '#FFFFFF',
                  border: '1px solid #E2E8F0',
                  borderRadius: '8px',
                  padding: '20px',
                  boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
                  transition: 'box-shadow 0.2s ease',
                  borderLeft: `5px solid ${statusConfig.badgeBorder}`,
                }}
              >
                {/* Cabecera de la Tarjeta */}
                <div
                  style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    justifyContent: 'space-between',
                    alignItems: 'flex-start',
                    gap: '12px',
                    marginBottom: '12px',
                  }}
                >
                  <div>
                    <div style={{ display: 'flex', gap: '8px', alignItems: 'center', marginBottom: '4px' }}>
                      <span
                        style={{
                          backgroundColor: '#F1F5F9',
                          color: '#0F172A',
                          fontSize: '11px',
                          fontWeight: 700,
                          padding: '2px 8px',
                          borderRadius: '4px',
                        }}
                      >
                        {booking.codigo_reserva}
                      </span>
                      {booking.codigo_sesion && (
                        <span style={{ fontSize: '11px', color: '#64748B' }}>
                          Clase: {booking.codigo_sesion}
                        </span>
                      )}
                    </div>
                    <h2
                      id={`booking-card-title-${booking.id_reserva}`}
                      style={{
                        color: '#002147',
                        fontSize: '18px',
                        fontWeight: 700,
                        margin: '0 0 4px 0',
                      }}
                    >
                      {booking.nombre_asignatura || 'Asignatura Formativa EPIS'}
                    </h2>
                    <p style={{ color: '#475569', fontSize: '13px', margin: 0, fontWeight: 500 }}>
                      Tema: {booking.nombre_tema || 'Temario Académico Silábico'}
                    </p>
                  </div>

                  {/* Insignia de Estado */}
                  <span
                    style={{
                      backgroundColor: statusConfig.badgeBg,
                      color: statusConfig.badgeText,
                      border: `1px solid ${statusConfig.badgeBorder}`,
                      fontSize: '12px',
                      fontWeight: 700,
                      padding: '4px 10px',
                      borderRadius: '12px',
                      whiteSpace: 'nowrap',
                    }}
                  >
                    {statusConfig.label}
                  </span>
                </div>

                {/* Grid de Metadatos de la Reserva */}
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
                    gap: '12px',
                    backgroundColor: '#F8FAFC',
                    padding: '12px',
                    borderRadius: '6px',
                    marginBottom: '14px',
                    fontSize: '13px',
                  }}
                >
                  <div>
                    <span style={{ color: '#64748B', display: 'block', fontSize: '11px' }}>
                      Fecha y Hora de Sesión:
                    </span>
                    <strong style={{ color: '#0F172A' }}>{formatDateTime(booking.fecha_inicio)}</strong>
                  </div>
                  <div>
                    <span style={{ color: '#64748B', display: 'block', fontSize: '11px' }}>
                      Modalidad & Espacio:
                    </span>
                    <strong style={{ color: '#0F172A' }}>
                      {booking.modalidad === 'virtual' ? '🌐 Virtual' : '🏛️ Presencial'}
                      {booking.espacio_asignado ? ` · ${booking.espacio_asignado}` : ''}
                    </strong>
                  </div>
                  <div>
                    <span style={{ color: '#64748B', display: 'block', fontSize: '11px' }}>
                      Mentor Responsable:
                    </span>
                    <strong style={{ color: '#0F172A' }}>{booking.mentor_email || 'Por asignar'}</strong>
                  </div>
                  <div>
                    <span style={{ color: '#64748B', display: 'block', fontSize: '11px' }}>
                      Fecha de Reserva:
                    </span>
                    <span style={{ color: '#334155' }}>{formatDateTime(booking.fecha_reserva)}</span>
                  </div>
                </div>

                {/* Explicación Pedagógica del Estado y Plazos */}
                <div style={{ marginBottom: '14px', fontSize: '12px' }}>
                  <p style={{ color: '#475569', margin: '0 0 6px 0' }}>{statusConfig.description}</p>
                  {isPending && (
                    <div
                      style={{
                        backgroundColor: timeCheck.isOpen ? '#FFFBEB' : '#FEF2F2',
                        color: timeCheck.isOpen ? '#92400E' : '#991B1B',
                        padding: '8px 12px',
                        borderRadius: '6px',
                        fontWeight: 500,
                      }}
                    >
                      <span aria-hidden="true">{timeCheck.isOpen ? '⏳ ' : '⛔ '}</span>
                      <strong>Límite RN-08:</strong> {timeCheck.message}
                      {timeCheck.cutoffIso && (
                        <div style={{ marginTop: '2px', fontSize: '11px' }}>
                          Corte definitivo: <strong>{formatDateTime(timeCheck.cutoffIso)}</strong>
                        </div>
                      )}
                    </div>
                  )}
                  {isConfirmed && booking.fecha_ratificacion && (
                    <div
                      style={{
                        backgroundColor: '#ECFDF5',
                        color: '#065F46',
                        padding: '6px 12px',
                        borderRadius: '6px',
                        fontSize: '11px',
                        marginTop: '4px',
                      }}
                    >
                      ✓ Ratificación registrada el: <strong>{formatDateTime(booking.fecha_ratificacion)}</strong>
                    </div>
                  )}
                  {booking.motivo_cancelacion && (
                    <div
                      style={{
                        backgroundColor: '#F1F5F9',
                        color: '#475569',
                        padding: '6px 12px',
                        borderRadius: '6px',
                        fontSize: '11px',
                        marginTop: '4px',
                      }}
                    >
                      Motivo registrado: <em>«{booking.motivo_cancelacion}»</em>
                    </div>
                  )}
                </div>

                {/* Barra de Acciones de la Tarjeta */}
                <div
                  style={{
                    display: 'flex',
                    flexWrap: 'wrap',
                    justifyContent: 'flex-end',
                    gap: '10px',
                    borderTop: '1px solid #F1F5F9',
                    paddingTop: '12px',
                  }}
                >
                  {isPending ? (
                    canConfirm ? (
                      <button
                        onClick={() => handleOpenConfirmDialog(booking)}
                        style={{
                          backgroundColor: '#002147',
                          color: '#FFFFFF',
                          border: 'none',
                          borderRadius: '6px',
                          padding: '9px 18px',
                          fontSize: '13px',
                          fontWeight: 700,
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '6px',
                          boxShadow: '0 1px 2px rgba(0,0,0,0.1)',
                        }}
                      >
                        <span aria-hidden="true">✓</span> Confirmar Asistencia
                      </button>
                    ) : (
                      <button
                        disabled
                        aria-disabled="true"
                        title={timeCheck.message}
                        style={{
                          backgroundColor: '#E2E8F0',
                          color: '#94A3B8',
                          border: 'none',
                          borderRadius: '6px',
                          padding: '9px 18px',
                          fontSize: '13px',
                          fontWeight: 600,
                          cursor: 'not-allowed',
                        }}
                      >
                        Plazo Vencido (T-24h cerrado)
                      </button>
                    )
                  ) : isConfirmed ? (
                    <span
                      style={{
                        fontSize: '12px',
                        color: '#059669',
                        fontWeight: 600,
                        padding: '8px 12px',
                        backgroundColor: '#ECFDF5',
                        borderRadius: '6px',
                      }}
                    >
                      ✓ Asistencia Confirmada
                    </span>
                  ) : (
                    <span
                      style={{
                        fontSize: '12px',
                        color: '#64748B',
                        padding: '8px 12px',
                      }}
                    >
                      Reserva no activa
                    </span>
                  )}
                </div>
              </article>
            );
          })}
        </div>
      )}

      {/* ====================================================================== */}
      {/* Diálogo Modal Accesible: Ratificación Pedagógica (T-25 / RF13 / CUS24) */}
      {/* ====================================================================== */}
      {confirmingBooking && (
        <div
          role="presentation"
          style={{
            position: 'fixed',
            top: 0,
            left: 0,
            right: 0,
            bottom: 0,
            backgroundColor: 'rgba(15, 23, 42, 0.65)',
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            zIndex: 1000,
            padding: '16px',
          }}
          onClick={(e) => {
            if (e.target === e.currentTarget && !isSubmittingConfirm) {
              handleCloseDialog();
            }
          }}
        >
          <div
            ref={dialogRef}
            role="dialog"
            aria-modal="true"
            aria-labelledby={`${componentId}-modal-title`}
            aria-describedby={`${componentId}-modal-desc`}
            style={{
              backgroundColor: '#FFFFFF',
              borderRadius: '10px',
              maxWidth: '540px',
              width: '100%',
              boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.2)',
              overflow: 'hidden',
              animation: 'fadeIn 0.15s ease-out',
            }}
          >
            {/* Cabecera del Diálogo */}
            <div
              style={{
                backgroundColor: '#002147',
                color: '#FFFFFF',
                padding: '18px 24px',
                display: 'flex',
                justifyContent: 'space-between',
                alignItems: 'center',
              }}
            >
              <div>
                <span
                  style={{
                    backgroundColor: '#F59E0B',
                    color: '#002147',
                    fontSize: '11px',
                    fontWeight: 800,
                    padding: '2px 6px',
                    borderRadius: '4px',
                    marginRight: '8px',
                  }}
                >
                  T-25 · CUS24
                </span>
                <span style={{ fontSize: '13px', color: '#CBD5E1' }}>
                  {confirmingBooking.codigo_reserva}
                </span>
                <h3
                  id={`${componentId}-modal-title`}
                  style={{
                    fontSize: '18px',
                    fontWeight: 700,
                    margin: '4px 0 0 0',
                    color: '#FFFFFF',
                  }}
                >
                  Ratificar Asistencia a Mentoría
                </h3>
              </div>
              <button
                onClick={handleCloseDialog}
                disabled={isSubmittingConfirm}
                aria-label="Cerrar diálogo de ratificación"
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: '#FFFFFF',
                  fontSize: '20px',
                  cursor: isSubmittingConfirm ? 'not-allowed' : 'pointer',
                  padding: '4px 8px',
                  lineHeight: 1,
                }}
              >
                ✕
              </button>
            </div>

            {/* Cuerpo del Diálogo con Información Pedagógica */}
            <div style={{ padding: '24px' }}>
              <div
                id={`${componentId}-modal-desc`}
                style={{
                  backgroundColor: '#F8FAFC',
                  border: '1px solid #E2E8F0',
                  borderRadius: '6px',
                  padding: '14px',
                  marginBottom: '16px',
                  fontSize: '13px',
                }}
              >
                <div style={{ color: '#002147', fontWeight: 700, fontSize: '15px', marginBottom: '4px' }}>
                  {confirmingBooking.nombre_asignatura || 'Asignatura Formativa'}
                </div>
                <div style={{ color: '#475569', marginBottom: '8px' }}>
                  Tema: <strong>{confirmingBooking.nombre_tema || 'Contenido curricular'}</strong>
                </div>
                <div style={{ color: '#0F172A', fontSize: '12px' }}>
                  📅 Horario: <strong>{formatDateTime(confirmingBooking.fecha_inicio)}</strong>
                </div>
                <div style={{ color: '#0F172A', fontSize: '12px' }}>
                  Modalidad: <strong>{confirmingBooking.modalidad === 'virtual' ? '🌐 Virtual' : '🏛️ Presencial'}</strong>
                </div>
              </div>

              {/* Mensajes de Compromiso Formativo (PB-014 / RN-08 / RN-09) */}
              <div
                style={{
                  backgroundColor: '#FFFBEB',
                  borderLeft: '4px solid #F59E0B',
                  padding: '12px 14px',
                  borderRadius: '0 6px 6px 0',
                  marginBottom: '16px',
                  fontSize: '12px',
                  color: '#78350F',
                }}
              >
                <p style={{ margin: '0 0 6px 0', fontWeight: 700 }}>
                  📜 Compromiso de Asistencia y Quórum (RN-08 / RN-09 / PB-014):
                </p>
                <ul style={{ margin: 0, paddingLeft: '18px', lineHeight: 1.4 }}>
                  <li>
                    Al ratificar, tu cupo pasa a estado <strong>CONFIRMADA</strong> y se contabiliza en el quórum
                    mínimo del 50% requerido para habilitar el dictado de la clase.
                  </li>
                  <li>
                    Recuerda que si surge algún inconveniente, tienes la opción de desistir voluntariamente
                    hasta 24 horas antes del inicio sin penalización (RN-10).
                  </li>
                  <li>
                    <em>Aviso institucional:</em> La ratificación individual no asegura el dictado definitivo si la
                    sesión general no alcanza el 50% de cupos confirmados al corte de T-24h (RN-09).
                  </li>
                </ul>
              </div>

              {/* Errores dentro del Diálogo */}
              {confirmError && (
                <div
                  role="alert"
                  style={{
                    backgroundColor: confirmError.includes('ℹ️') ? '#EFF6FF' : '#FEF2F2',
                    border: `1px solid ${confirmError.includes('ℹ️') ? '#93C5FD' : '#FCA5A5'}`,
                    borderRadius: '6px',
                    padding: '10px 14px',
                    marginBottom: '16px',
                    color: confirmError.includes('ℹ️') ? '#1E40AF' : '#991B1B',
                    fontSize: '12px',
                  }}
                >
                  {confirmError}
                </div>
              )}

              {/* Botones de Acción */}
              <div
                style={{
                  display: 'flex',
                  justifyContent: 'flex-end',
                  gap: '12px',
                  marginTop: '10px',
                }}
              >
                <button
                  ref={cancelBtnRef}
                  type="button"
                  onClick={handleCloseDialog}
                  disabled={isSubmittingConfirm}
                  style={{
                    backgroundColor: '#FFFFFF',
                    color: '#475569',
                    border: '1px solid #CBD5E1',
                    borderRadius: '6px',
                    padding: '9px 18px',
                    fontSize: '13px',
                    fontWeight: 600,
                    cursor: isSubmittingConfirm ? 'not-allowed' : 'pointer',
                  }}
                >
                  Cancelar
                </button>
                <button
                  type="button"
                  onClick={handleExecuteConfirmation}
                  disabled={isSubmittingConfirm}
                  style={{
                    backgroundColor: isSubmittingConfirm ? '#64748B' : '#002147',
                    color: '#FFFFFF',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '9px 20px',
                    fontSize: '13px',
                    fontWeight: 700,
                    cursor: isSubmittingConfirm ? 'not-allowed' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                  }}
                >
                  {isSubmittingConfirm ? 'Ratificando asistencia...' : '✓ Confirmar Asistencia'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </section>
  );
};
