/**
 * Componente: Bandeja de Reservas Personales, Ratificación y Desistimiento Voluntario (T-25 / T-27)
 * Módulo MOD-05: Quórum, Confirmación y Cancelaciones.
 *
 * Trazabilidad:
 * - Requerimiento Funcional: RF13 / CUS24 (Confirmación anticipada de asistencia a mentoría)
 * - Requerimiento Funcional: RF14 / CUS17 (Desistimiento voluntario y liberación anticipada de cupos)
 * - Compromiso de Participación: PB-014 (Compromiso formativo de asistencia)
 * - Compromiso Formativo: PB-015 (Conducta ética de liberación responsable del cupo)
 * - Regla de Negocio RN-05: Aforos estándar inmutables (10 presencial / 20 virtual)
 * - Regla de Negocio RN-08: Ventana de confirmación de asistencia hasta T-24 horas
 * - Regla de Negocio RN-09: Cómputo del quórum regulatorio del 50% (5 presencial / 10 virtual)
 * - Regla de Negocio RN-10: Política de desistimiento antes de T-24 horas sin penalización
 * - Requerimiento No Funcional: RNF05 (Accesibilidad WAI-ARIA y diseño responsive)
 * - Requerimiento No Funcional: RNF07 (Integridad y concurrencia transaccional en backend)
 * - Requerimiento No Funcional: RNF09 (Mantenibilidad y cobertura de pruebas automatizadas)
 */

import React, { useState, useEffect, useCallback, useId, useRef } from 'react';
import {
  bookingService,
  type BookingDetailResponse,
  type BookingStatus,
  BookingException,
} from '../services/bookingService';
import { authService } from '../services/authService';
import { PostSessionSurveyModal } from './PostSessionSurveyModal';

/**
 * Propiedades del componente StudentBookingsView (T-25 / T-27 / RF13 / RF14).
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
 * Evalúa preventivamente en cliente las reglas de negocio temporales RN-08 y RN-10 (corte a T-24h).
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
        'Ventana de ratificación y desistimiento cerrada: El corte perentorio se cumplió a las 24 horas previas al inicio.',
    };
  }

  return {
    isOpen: true,
    isPast: false,
    hoursRemaining,
    cutoffIso,
    message: `Ventana abierta: Restan aproximadamente ${hoursRemaining} horas para el inicio de la clase.`,
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
          'Cupo provisional. Debes ratificar tu asistencia antes de 24 horas para ser contabilizado en el quórum.',
      };
    case 'CONFIRMADA':
      return {
        label: 'Asistencia Ratificada',
        badgeBg: '#D1FAE5',
        badgeText: '#065F46',
        badgeBorder: '#10B981',
        description:
          'Has ratificado tu asistencia. Tu cupo está asegurado en la evaluación del quórum institucional.',
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
        description: 'Cancelada voluntariamente por el estudiante conforme a la política de desistimiento.',
      };
    case 'CANCELADA_SISTEMA':
      return {
        label: 'Cancelada por el Sistema',
        badgeBg: '#FEE2E2',
        badgeText: '#7F1D1D',
        badgeBorder: '#DC2626',
        description:
          'Sesión suspendida por el sistema al no alcanzar el quórum del 50% reglamentario.',
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

  // Estado del diálogo modal de desistimiento voluntario (T-27 / RF14 / CUS17 / RN-10)
  const [cancellingBooking, setCancellingBooking] = useState<BookingDetailResponse | null>(null);
  const [cancelReason, setCancelReason] = useState<string>('');
  const [isSubmittingCancel, setIsSubmittingCancel] = useState<boolean>(false);
  const [cancelError, setCancelError] = useState<string | null>(null);

  // Mensaje de notificación global
  const [notificationMessage, setNotificationMessage] = useState<{
    type: 'success' | 'info' | 'error';
    text: string;
  } | null>(null);

  // Estado para modal de encuesta de calidad post-mentoría (T-38 / RF18 / RN-12 / RN-13)
  const [activeSurveyBooking, setActiveSurveyBooking] = useState<BookingDetailResponse | null>(null);
  const [evaluatedBookings, setEvaluatedBookings] = useState<Set<number>>(new Set());
  const [componentMountTime] = useState<number>(() => currentTime ?? Date.now());

  // Referencias para accesibilidad y focus trap en diálogos
  const confirmCancelBtnRef = useRef<HTMLButtonElement>(null);
  const cancelDismissBtnRef = useRef<HTMLButtonElement>(null);

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

      // Sincronizar tiempo simulado si se suministra por props
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

  // ==========================================================================
  // Manejadores del Diálogo de Ratificación (T-25)
  // ==========================================================================

  const handleCloseConfirmDialog = useCallback(() => {
    setConfirmingBooking(null);
    setConfirmError(null);
    setIsSubmittingConfirm(false);
  }, []);

  const handleOpenConfirmDialog = (booking: BookingDetailResponse) => {
    setConfirmingBooking(booking);
    setConfirmError(null);
  };

  const handleExecuteConfirmation = async () => {
    if (!confirmingBooking) return;

    try {
      setIsSubmittingConfirm(true);
      setConfirmError(null);

      const updated = await bookingService.confirmAttendance(
        confirmingBooking.id_reserva,
        effectiveEmail ?? undefined
      );

      setNotificationMessage({
        type: 'success',
        text: `¡Asistencia ratificada con éxito para ${updated.nombre_asignatura || 'la sesión'}! Tu cupo está asegurado en la evaluación de quórum.`,
      });

      handleCloseConfirmDialog();
      await loadBookings();
    } catch (err: unknown) {
      if (err instanceof BookingException) {
        if (err.code === 'ENDPOINT_NOT_IMPLEMENTED') {
          setConfirmError(
            'ℹ️ Servicio en integración: El servicio de ratificación en el servidor está en proceso de integración. La solicitud ha sido registrada localmente.'
          );
        } else if (err.code === 'WINDOW_CLOSED_T24H') {
          setConfirmError(
            'El plazo para ratificar tu asistencia cerró a las 24 horas previas al inicio de la sesión.'
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

  // ==========================================================================
  // Manejadores del Diálogo de Desistimiento Voluntario (T-27 / RF14 / CUS17)
  // ==========================================================================

  const handleCloseCancelDialog = useCallback(() => {
    setCancellingBooking(null);
    setCancelReason('');
    setCancelError(null);
    setIsSubmittingCancel(false);
  }, []);

  const handleOpenCancelDialog = (booking: BookingDetailResponse) => {
    setCancellingBooking(booking);
    setCancelReason('');
    setCancelError(null);
  };

  const handleExecuteCancel = async () => {
    if (!cancellingBooking) return;

    try {
      setIsSubmittingCancel(true);
      setCancelError(null);

      const cleanReason = cancelReason.trim();
      const updated = await bookingService.cancelReservation(
        cancellingBooking.id_reserva,
        cleanReason || undefined,
        effectiveEmail ?? undefined
      );

      setNotificationMessage({
        type: 'success',
        text: `¡Reserva ${updated.codigo_reserva} cancelada con éxito! La vacante ha sido liberada en el sistema para tus compañeros.`,
      });

      handleCloseCancelDialog();
      await loadBookings();
    } catch (err: unknown) {
      if (err instanceof BookingException) {
        if (err.code === 'ENDPOINT_NOT_IMPLEMENTED') {
          setCancelError(
            'ℹ️ Servicio en integración: El servicio de desistimiento en el servidor está en proceso de integración. La solicitud ha sido registrada localmente.'
          );
        } else if (err.code === 'WINDOW_CLOSED_T24H') {
          setCancelError(
            'El desistimiento voluntario solo está permitido con más de 24 horas de anticipación al inicio de la sesión.'
          );
        } else if (err.code === 'ALREADY_CANCELLED') {
          setCancelError('Esta reserva ya fue cancelada con anterioridad.');
        } else if (err.code === 'INVALID_STATUS_TRANSITION') {
          setCancelError('No es posible desistir de una sesión en el estado actual.');
        } else if (err.code === 'FORBIDDEN') {
          setCancelError('No tienes autorización para cancelar una reserva de otro estudiante.');
        } else if (err.code === 'NETWORK_ERROR') {
          setCancelError('No fue posible contactar al servidor. Verifica tu conectividad institucional.');
        } else {
          setCancelError(err.message);
        }
      } else {
        setCancelError('Error imprevisto al procesar el desistimiento voluntario.');
      }
    } finally {
      setIsSubmittingCancel(false);
    }
  };

  // Gestión de foco accesible para diálogos
  useEffect(() => {
    if (confirmingBooking) {
      setTimeout(() => {
        confirmCancelBtnRef.current?.focus();
      }, 50);
    }
  }, [confirmingBooking]);

  useEffect(() => {
    if (cancellingBooking) {
      setTimeout(() => {
        cancelDismissBtnRef.current?.focus();
      }, 50);
    }
  }, [cancellingBooking]);

  // Manejo de tecla Escape para cerrar diálogos
  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (confirmingBooking && !isSubmittingConfirm) {
          handleCloseConfirmDialog();
        } else if (cancellingBooking && !isSubmittingCancel) {
          handleCloseCancelDialog();
        }
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [
    confirmingBooking,
    isSubmittingConfirm,
    cancellingBooking,
    isSubmittingCancel,
    handleCloseConfirmDialog,
    handleCloseCancelDialog,
  ]);

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
  // Renderizado: Caso sin autenticación institucional (RN-01)
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
            Acceso Restringido a Mis Reservas
          </h2>
          <p style={{ color: '#4B5563', fontSize: '14px', maxWidth: '520px', margin: '0 auto 20px auto' }}>
            Para consultar tus cupos inscritos, ratificar asistencia o desistir de una reserva, debes iniciar sesión
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
            const isCancelEligible = isPending || isConfirmed;
            const canConfirm = isPending && timeCheck.isOpen;
            const canCancel = isCancelEligible && timeCheck.isOpen;

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
                  {isCancelEligible && (
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
                      <strong>Plazo de confirmación:</strong> {timeCheck.message}
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
                    alignItems: 'center',
                  }}
                >
                  {/* Botón de Ratificación (Solo para PENDIENTE_CONFIRMACION) */}
                  {isPending && (
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
                        Plazo Vencido (Cierre 24h)
                      </button>
                    )
                  )}

                  {/* Insignia para reservas ya confirmadas */}
                  {isConfirmed && (
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
                  )}

                  {/* Evaluación de Calidad y Satisfacción Post-Mentoría (T-38 / RF18 / RN-12 / RN-13) */}
                  {(() => {
                    const startMs = booking.fecha_inicio ? new Date(booking.fecha_inicio).getTime() : 0;
                    const durMin = booking.duracion_minutos || 60;
                    const endMs = startMs > 0 ? startMs + durMin * 60 * 1000 : 0;
                    const nowMs = currentTime !== undefined ? currentTime : componentMountTime;
                    const isSessionConcluded = endMs > 0 && nowMs >= endMs;
                    const elapsedHours = endMs > 0 ? (nowMs - endMs) / (1000 * 60 * 60) : 0;
                    const isSurveyWindowExpired = elapsedHours > 24;

                    const hasEffectiveAttendance =
                      booking.asistio === true ||
                      booking.asistencia_confirmada === true ||
                      booking.estado === 'ASISTIDA';
                    const isMarkedAbsent =
                      booking.asistio === false || booking.estado === 'INASISTENCIA';
                    const isEvaluated = evaluatedBookings.has(booking.id_reserva);

                    if (isEvaluated) {
                      return (
                        <span
                          style={{
                            fontSize: '12px',
                            color: '#4F46E5',
                            fontWeight: 700,
                            padding: '8px 12px',
                            backgroundColor: '#EEF2FF',
                            borderRadius: '6px',
                          }}
                        >
                          ✓ Evaluada
                        </span>
                      );
                    }

                    if (isSessionConcluded && !isMarkedAbsent && hasEffectiveAttendance) {
                      if (isSurveyWindowExpired) {
                        return (
                          <button
                            disabled
                            aria-disabled="true"
                            title="El plazo reglamentario de 24 horas para remitir tu evaluación ha expirado (RN-13)."
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
                            Encuesta Cerrada (Plazo de 24h Vencido)
                          </button>
                        );
                      }
                      return (
                        <button
                          onClick={() => setActiveSurveyBooking(booking)}
                          style={{
                            backgroundColor: '#4338CA',
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
                          ⭐ Evaluar Mentoría
                        </button>
                      );
                    }
                    return null;
                  })()}

                  {/* Botón de Desistimiento Voluntario */}
                  {isCancelEligible && (
                    canCancel ? (
                      <button
                        onClick={() => handleOpenCancelDialog(booking)}
                        aria-label={`Cancelar reserva / Desistir de ${booking.codigo_reserva}`}
                        style={{
                          backgroundColor: '#FFFFFF',
                          color: '#DC2626',
                          border: '1px solid #DC2626',
                          borderRadius: '6px',
                          padding: '9px 16px',
                          fontSize: '13px',
                          fontWeight: 600,
                          cursor: 'pointer',
                          display: 'flex',
                          alignItems: 'center',
                          gap: '6px',
                          transition: 'background-color 0.15s ease',
                        }}
                      >
                        <span aria-hidden="true">✕</span> Cancelar Reserva / Desistir
                      </button>
                    ) : (
                      <button
                        disabled
                        aria-disabled="true"
                        title="El desistimiento voluntario no está permitido a menos de 24 horas del inicio."
                        style={{
                          backgroundColor: '#F1F5F9',
                          color: '#94A3B8',
                          border: '1px solid #E2E8F0',
                          borderRadius: '6px',
                          padding: '9px 16px',
                          fontSize: '13px',
                          fontWeight: 600,
                          cursor: 'not-allowed',
                        }}
                      >
                        Desistimiento Cerrado (Cierre 24h)
                      </button>
                    )
                  )}

                  {/* Estado terminal para reservas no activas */}
                  {!isCancelEligible && (
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
              handleCloseConfirmDialog();
            }
          }}
        >
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby={`${componentId}-confirm-modal-title`}
            aria-describedby={`${componentId}-confirm-modal-desc`}
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
                  Confirmación
                </span>
                <span style={{ fontSize: '13px', color: '#CBD5E1' }}>
                  {confirmingBooking.codigo_reserva}
                </span>
                <h3
                  id={`${componentId}-confirm-modal-title`}
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
                onClick={handleCloseConfirmDialog}
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

            {/* Cuerpo del Diálogo */}
            <div style={{ padding: '24px' }}>
              <div
                id={`${componentId}-confirm-modal-desc`}
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

              {/* Mensajes de Compromiso Formativo */}
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
                  📜 Compromiso de Asistencia y Quórum:
                </p>
                <ul style={{ margin: 0, paddingLeft: '18px', lineHeight: 1.4 }}>
                  <li>
                    Al ratificar, tu cupo pasa a estado <strong>CONFIRMADA</strong> y se contabiliza en el quórum
                    mínimo del 50% requerido para habilitar el dictado de la clase.
                  </li>
                  <li>
                    Si surge algún imprevisto, puedes desistir voluntariamente hasta 24 horas antes del inicio sin penalización académica.
                  </li>
                  <li>
                    <em>Aviso institucional:</em> La ratificación individual asegura tu plaza; la realización de la sesión depende de alcanzar el quórum mínimo al cierre de las 24 horas.
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
                  ref={confirmCancelBtnRef}
                  type="button"
                  onClick={handleCloseConfirmDialog}
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

      {/* ====================================================================== */}
      {/* Diálogo Modal Accesible: Desistimiento Voluntario (T-27 / RF14 / CUS17) */}
      {/* ====================================================================== */}
      {cancellingBooking && (
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
            if (e.target === e.currentTarget && !isSubmittingCancel) {
              handleCloseCancelDialog();
            }
          }}
        >
          <div
            role="dialog"
            aria-modal="true"
            aria-labelledby={`${componentId}-cancel-modal-title`}
            aria-describedby={`${componentId}-cancel-modal-desc`}
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
            {/* Cabecera del Diálogo de Desistimiento */}
            <div
              style={{
                backgroundColor: '#991B1B',
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
                    backgroundColor: '#FEE2E2',
                    color: '#991B1B',
                    fontSize: '11px',
                    fontWeight: 800,
                    padding: '2px 6px',
                    borderRadius: '4px',
                    marginRight: '8px',
                  }}
                >
                  Desistimiento
                </span>
                <span style={{ fontSize: '13px', color: '#FCA5A5' }}>
                  {cancellingBooking.codigo_reserva}
                </span>
                <h3
                  id={`${componentId}-cancel-modal-title`}
                  style={{
                    fontSize: '18px',
                    fontWeight: 700,
                    margin: '4px 0 0 0',
                    color: '#FFFFFF',
                  }}
                >
                  Desistimiento Voluntario de Cupo
                </h3>
              </div>
              <button
                onClick={handleCloseCancelDialog}
                disabled={isSubmittingCancel}
                aria-label="Cerrar diálogo de desistimiento"
                style={{
                  background: 'transparent',
                  border: 'none',
                  color: '#FFFFFF',
                  fontSize: '20px',
                  cursor: isSubmittingCancel ? 'not-allowed' : 'pointer',
                  padding: '4px 8px',
                  lineHeight: 1,
                }}
              >
                ✕
              </button>
            </div>

            {/* Cuerpo del Diálogo */}
            <div style={{ padding: '24px' }}>
              <div
                id={`${componentId}-cancel-modal-desc`}
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
                  {cancellingBooking.nombre_asignatura || 'Asignatura Formativa'}
                </div>
                <div style={{ color: '#475569', marginBottom: '8px' }}>
                  Tema: <strong>{cancellingBooking.nombre_tema || 'Contenido curricular'}</strong>
                </div>
                <div style={{ color: '#0F172A', fontSize: '12px' }}>
                  📅 Horario: <strong>{formatDateTime(cancellingBooking.fecha_inicio)}</strong>
                </div>
                <div style={{ color: '#0F172A', fontSize: '12px' }}>
                  Modalidad: <strong>{cancellingBooking.modalidad === 'virtual' ? '🌐 Virtual' : '🏛️ Presencial'}</strong>
                </div>
                <div style={{ color: '#0F172A', fontSize: '12px' }}>
                  Estado actual: <strong>{getStatusConfig(cancellingBooking.estado).label}</strong>
                </div>
              </div>

              {/* Advertencia Institucional RN-10 y PB-015 */}
              <div
                style={{
                  backgroundColor: '#FEF2F2',
                  borderLeft: '4px solid #DC2626',
                  padding: '12px 14px',
                  borderRadius: '0 6px 6px 0',
                  marginBottom: '16px',
                  fontSize: '12px',
                  color: '#7F1D1D',
                }}
              >
                <p style={{ margin: '0 0 6px 0', fontWeight: 700 }}>
                  ⚠️ Política de Desistimiento y Liberación de Cupo:
                </p>
                <ul style={{ margin: 0, paddingLeft: '18px', lineHeight: 1.4 }}>
                  <li>
                    Al desistir voluntariamente con más de 24 horas de antelación, tu vacante será cancelada sin penalización en tu historial formativo institucional.
                  </li>
                  <li>
                    <em>Liberación efectiva del aforo:</em> La vacante se restituye al catálogo de mentorías para que otro estudiante pueda aprovecharla.
                  </li>
                  <li>
                    Esta acción es irreversible. Para volver a inscribirte deberás reservar nuevamente desde la cartelera si aún quedan vacantes disponibles.
                  </li>
                </ul>
              </div>

              {/* Campo Opcional para Motivo de Desistimiento */}
              <div style={{ marginBottom: '16px' }}>
                <label
                  htmlFor={`${componentId}-cancel-reason`}
                  style={{
                    display: 'block',
                    fontSize: '13px',
                    fontWeight: 600,
                    color: '#334155',
                    marginBottom: '6px',
                  }}
                >
                  Motivo de desistimiento (opcional):
                </label>
                <textarea
                  id={`${componentId}-cancel-reason`}
                  value={cancelReason}
                  onChange={(e) => setCancelReason(e.target.value.slice(0, 300))}
                  maxLength={300}
                  rows={3}
                  placeholder="Describe brevemente el motivo (ej. cruce de horario académico, imprevisto de salud...)"
                  disabled={isSubmittingCancel}
                  style={{
                    width: '100%',
                    padding: '10px',
                    borderRadius: '6px',
                    border: '1px solid #CBD5E1',
                    fontSize: '13px',
                    boxSizing: 'border-box',
                    resize: 'vertical',
                    fontFamily: 'inherit',
                  }}
                />
                <div style={{ textAlign: 'right', fontSize: '11px', color: '#64748B', marginTop: '2px' }}>
                  {cancelReason.length} / 300 caracteres
                </div>
              </div>

              {/* Errores dentro del Diálogo */}
              {cancelError && (
                <div
                  role="alert"
                  style={{
                    backgroundColor: cancelError.includes('ℹ️') ? '#EFF6FF' : '#FEF2F2',
                    border: `1px solid ${cancelError.includes('ℹ️') ? '#93C5FD' : '#FCA5A5'}`,
                    borderRadius: '6px',
                    padding: '10px 14px',
                    marginBottom: '16px',
                    color: cancelError.includes('ℹ️') ? '#1E40AF' : '#991B1B',
                    fontSize: '12px',
                  }}
                >
                  {cancelError}
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
                  ref={cancelDismissBtnRef}
                  type="button"
                  onClick={handleCloseCancelDialog}
                  disabled={isSubmittingCancel}
                  style={{
                    backgroundColor: '#FFFFFF',
                    color: '#475569',
                    border: '1px solid #CBD5E1',
                    borderRadius: '6px',
                    padding: '9px 18px',
                    fontSize: '13px',
                    fontWeight: 600,
                    cursor: isSubmittingCancel ? 'not-allowed' : 'pointer',
                  }}
                >
                  Volver
                </button>
                <button
                  type="button"
                  onClick={handleExecuteCancel}
                  disabled={isSubmittingCancel}
                  style={{
                    backgroundColor: isSubmittingCancel ? '#9CA3AF' : '#DC2626',
                    color: '#FFFFFF',
                    border: 'none',
                    borderRadius: '6px',
                    padding: '9px 20px',
                    fontSize: '13px',
                    fontWeight: 700,
                    cursor: isSubmittingCancel ? 'not-allowed' : 'pointer',
                    display: 'flex',
                    alignItems: 'center',
                    gap: '6px',
                  }}
                >
                  {isSubmittingCancel ? 'Procesando desistimiento...' : 'Confirmar Desistimiento'}
                </button>
              </div>
            </div>
          </div>
        </div>
      )}

      {/* Modal Accesible de Encuesta Post-Mentoría (T-38 / RF18 / RN-12 / RN-13) */}
      {activeSurveyBooking && (
        <PostSessionSurveyModal
          isOpen={Boolean(activeSurveyBooking)}
          onClose={() => setActiveSurveyBooking(null)}
          sessionId={activeSurveyBooking.id_sesion}
          sessionTitle={activeSurveyBooking.nombre_asignatura || activeSurveyBooking.nombre_tema || 'Sesión de Mentoría'}
          mentorName={activeSurveyBooking.mentor_email || 'Mentor Titular'}
          sessionEndDate={
            activeSurveyBooking.fecha_inicio
              ? new Date(new Date(activeSurveyBooking.fecha_inicio).getTime() + (activeSurveyBooking.duracion_minutos || 60) * 60000)
              : undefined
          }
          asistenciaConfirmada={
            activeSurveyBooking.asistio !== false &&
            activeSurveyBooking.estado !== 'INASISTENCIA' &&
            (activeSurveyBooking.asistio === true ||
              activeSurveyBooking.asistencia_confirmada === true ||
              activeSurveyBooking.estado === 'ASISTIDA')
          }
          currentTime={currentTime}
          onSurveySubmitted={() => {
            if (activeSurveyBooking) {
              setEvaluatedBookings((prev) => new Set(prev).add(activeSurveyBooking.id_reserva));
            }
          }}
        />
      )}
    </section>
  );
};
