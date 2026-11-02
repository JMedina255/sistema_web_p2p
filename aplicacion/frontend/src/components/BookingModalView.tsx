import React, { useState, useEffect, useRef, useCallback, useId } from 'react';
import { authService } from '../services/authService';
import type { OfferRecommendationItem } from '../services/recommendationService';

/**
 * Datos de respuesta tras formalizar una reserva provisional (CUS04 / RF12).
 */
export interface BookingSuccessData {
  codigo_reserva: string;
  estado: string;
  fecha_limite_confirmacion?: string | null;
  mensaje?: string;
  ticket_hash?: string | null;
}

/**
 * Propiedades del componente BookingModalView (T-21 / CUS04 / RF12 / RN-05 / RN-08).
 */
export interface BookingModalViewProps {
  /** Determina si el modal está visible */
  isOpen: boolean;
  /** Oferta seleccionada desde RecommendationFeedView */
  offer: OfferRecommendationItem | null;
  /** Correo del estudiante autenticado (se resuelve desde el token si no se pasa) */
  currentUserEmail?: string;
  /** Indica si la petición de reserva está en procesamiento asíncrono */
  isSubmitting?: boolean;
  /** Mensaje de error retornado por la validación o backend */
  error?: string | null;
  /** Datos de la reserva exitosa para despliegue de comprobante provisional */
  successData?: BookingSuccessData | null;
  /** Callback para cerrar el modal */
  onClose: () => void;
  /** Callback tipado para formalizar la intención de reserva */
  onConfirmReservation: (offer: OfferRecommendationItem) => void | Promise<void>;
  /** Callback opcional para redirigir a solicitudes por demanda si no hay aforo */
  onDemandRedirect?: () => void;
}

/**
 * Resuelve la identidad del estudiante desde props, token de sesión o fallback canónico.
 * Garantiza que la identidad proceda de la autenticación del sistema y no de campos editables.
 */
function resolveCurrentUserEmail(explicitEmail?: string): string {
  if (explicitEmail && explicitEmail.trim()) {
    return explicitEmail.trim().toLowerCase();
  }
  const token = authService.getToken();
  if (token) {
    try {
      const parts = token.split('.');
      if (parts.length === 3) {
        const payloadJson = atob(parts[1].replace(/-/g, '+').replace(/_/g, '/'));
        const payload = JSON.parse(payloadJson);
        if (payload.sub && typeof payload.sub === 'string' && payload.sub.includes('@')) {
          return payload.sub.trim().toLowerCase();
        }
        if (payload.email && typeof payload.email === 'string') {
          return payload.email.trim().toLowerCase();
        }
      }
    } catch {
      // Ignorar fallos de decodificación de token
    }
  }
  return '2022074255@upt.pe';
}

/**
 * Formatea una fecha ISO 8601 a un formato comprensible en español peruano.
 */
function formatSessionDateTime(isoString: string): string {
  try {
    const date = new Date(isoString);
    if (isNaN(date.getTime())) {
      return isoString;
    }
    return new Intl.DateTimeFormat('es-PE', {
      weekday: 'long',
      year: 'numeric',
      month: 'long',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit',
      hour12: false,
    }).format(date);
  } catch {
    return isoString;
  }
}

/**
 * Componente modal de confirmación de reserva de mentoría (T-21 / CUS04 / RF12).
 * Aplica validaciones preventivas de aforo (RN-05), restricción de autoreserva (RN-03),
 * ventana perentoria T-24h (RN-08) y accesibilidad modal WAI-ARIA (RNF05).
 */
export const BookingModalView: React.FC<BookingModalViewProps> = ({
  isOpen,
  offer,
  currentUserEmail,
  isSubmitting = false,
  error = null,
  successData = null,
  onClose,
  onConfirmReservation,
  onDemandRedirect,
}) => {
  const componentId = useId();
  const titleId = `booking-modal-title-${componentId}`;
  const descId = `booking-modal-desc-${componentId}`;

  const dialogRef = useRef<HTMLDivElement>(null);
  const previousFocusRef = useRef<HTMLElement | null>(null);
  const isProcessingRef = useRef(false);
  const [internalClickPrevented, setInternalClickPrevented] = useState(false);
  const [currentTime] = useState(() => Date.now());

  // Resolución de identidad del estudiante
  const resolvedStudentEmail = resolveCurrentUserEmail(currentUserEmail);

  // Gestión de foco accesible (RNF05)
  useEffect(() => {
    if (isOpen) {
      previousFocusRef.current = document.activeElement as HTMLElement | null;
      // Enfocar el diálogo o el botón principal al abrir
      setTimeout(() => {
        if (dialogRef.current) {
          dialogRef.current.focus();
        }
      }, 50);
    } else if (previousFocusRef.current) {
      previousFocusRef.current.focus();
    }
  }, [isOpen]);

  // Manejo de tecla Escape y trampa de foco (Focus Trap)
  const handleKeyDown = useCallback(
    (e: KeyboardEvent) => {
      if (!isOpen) return;

      if (e.key === 'Escape') {
        if (!isSubmitting) {
          onClose();
        }
        return;
      }

      if (e.key === 'Tab' && dialogRef.current) {
        const focusableElements = dialogRef.current.querySelectorAll<HTMLElement>(
          'button:not([disabled]), [href], input:not([disabled]), select:not([disabled]), textarea:not([disabled]), [tabindex]:not([tabindex="-1"])'
        );
        if (focusableElements.length === 0) return;

        const firstElement = focusableElements[0];
        const lastElement = focusableElements[focusableElements.length - 1];

        if (e.shiftKey) {
          if (document.activeElement === firstElement) {
            e.preventDefault();
            lastElement.focus();
          }
        } else {
          if (document.activeElement === lastElement) {
            e.preventDefault();
            firstElement.focus();
          }
        }
      }
    },
    [isOpen, isSubmitting, onClose]
  );

  useEffect(() => {
    if (isOpen) {
      window.addEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'hidden';
    }
    return () => {
      window.removeEventListener('keydown', handleKeyDown);
      document.body.style.overflow = 'unset';
    };
  }, [isOpen, handleKeyDown]);

  if (!isOpen) {
    return null;
  }

  // Si no hay oferta seleccionada
  if (!offer) {
    return (
      <div
        style={{
          position: 'fixed',
          inset: 0,
          backgroundColor: 'rgba(15, 23, 42, 0.65)',
          display: 'flex',
          alignItems: 'center',
          justifyContent: 'center',
          zIndex: 1050,
          padding: '1rem',
        }}
        onClick={onClose}
      >
        <div
          ref={dialogRef}
          role="dialog"
          aria-modal="true"
          aria-labelledby={titleId}
          tabIndex={-1}
          onClick={(e) => e.stopPropagation()}
          style={{
            backgroundColor: '#FFFFFF',
            borderRadius: '12px',
            padding: '2rem',
            maxWidth: '480px',
            width: '100%',
            boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.2)',
            textAlign: 'center',
          }}
        >
          <h2 id={titleId} style={{ color: '#1C2A59', fontSize: '1.25rem', marginBottom: '1rem' }}>
            Ninguna Sesión Seleccionada
          </h2>
          <p style={{ color: '#64748B', fontSize: '0.9rem', marginBottom: '1.5rem' }}>
            No se ha proporcionado una oferta de mentoría válida para realizar la reserva.
          </p>
          <button
            type="button"
            onClick={onClose}
            style={{
              backgroundColor: '#1C2A59',
              color: '#FFFFFF',
              border: 'none',
              borderRadius: '8px',
              padding: '0.65rem 1.5rem',
              fontWeight: 600,
              cursor: 'pointer',
            }}
          >
            Cerrar
          </button>
        </div>
      </div>
    );
  }

  // ============================================================================
  // Validaciones Previas Preventivas (RN-03, RN-05, RN-08)
  // ============================================================================
  const mentorEmailClean = (offer.mentor_email || '').trim().toLowerCase();
  const studentEmailClean = resolvedStudentEmail.trim().toLowerCase();

  // 1. Prohibición de autoreserva (RN-03 / MENTOR_CANNOT_BOOK)
  const isSelfBooking = mentorEmailClean !== '' && mentorEmailClean === studentEmailClean;

  // 2. Control de aforo completo (RN-05 / CAPACITY_EXCEEDED)
  const isCapacityExceeded = offer.aforo_disponible <= 0;

  // 3 & 4. Verificaciones temporales
  const sessionStartTime = new Date(offer.fecha_inicio).getTime();
  const now = currentTime;
  const isTimeValid = !isNaN(sessionStartTime);

  // Sesión vencida (fecha de inicio en el pasado)
  const isExpired = isTimeValid && sessionStartTime <= now;

  // Restricción perentoria T-24h (RN-08 / WINDOW_CLOSED_T24H)
  const isWindowClosed = isTimeValid && !isExpired && sessionStartTime <= now + 24 * 60 * 60 * 1000;

  // Capacidad de confirmación
  const canConfirm =
    !isSelfBooking &&
    !isCapacityExceeded &&
    !isExpired &&
    !isWindowClosed &&
    !isSubmitting &&
    !internalClickPrevented;

  const handleConfirm = async () => {
    if (!canConfirm || isProcessingRef.current) return;
    isProcessingRef.current = true;
    setInternalClickPrevented(true);
    try {
      await onConfirmReservation(offer);
    } finally {
      isProcessingRef.current = false;
      setInternalClickPrevented(false);
    }
  };

  const handleBackdropClick = (e: React.MouseEvent<HTMLDivElement>) => {
    if (e.target === e.currentTarget && !isSubmitting) {
      onClose();
    }
  };

  const isPresencial = (offer.modalidad || '').toLowerCase() === 'presencial';

  return (
    <div
      data-testid="booking-modal-backdrop"
      style={{
        position: 'fixed',
        inset: 0,
        backgroundColor: 'rgba(15, 23, 42, 0.65)',
        backdropFilter: 'blur(3px)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1050,
        padding: '1rem',
        overflowY: 'auto',
      }}
      onClick={handleBackdropClick}
    >
      <div
        ref={dialogRef}
        role="dialog"
        aria-modal="true"
        aria-labelledby={titleId}
        aria-describedby={descId}
        tabIndex={-1}
        onClick={(e) => e.stopPropagation()}
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '16px',
          maxWidth: '640px',
          width: '100%',
          boxShadow: '0 25px 50px -12px rgba(15, 23, 42, 0.25)',
          border: '1px solid #E2E8F0',
          overflow: 'hidden',
          display: 'flex',
          flexDirection: 'column',
          maxHeight: '90vh',
        }}
      >
        {/* Cabecera Institucional EPIS */}
        <div
          style={{
            backgroundColor: '#1C2A59',
            color: '#FFFFFF',
            padding: '1.25rem 1.5rem',
            display: 'flex',
            alignItems: 'flex-start',
            justifyContent: 'space-between',
            gap: '1rem',
          }}
        >
          <div>
            <div
              style={{
                fontSize: '0.72rem',
                fontWeight: 700,
                textTransform: 'uppercase',
                letterSpacing: '0.08em',
                color: '#93C5FD',
                marginBottom: '0.25rem',
              }}
            >
              Módulo MOD-05: Quórum y Reservas (CUS04 / RF12)
            </div>
            <h2
              id={titleId}
              style={{
                fontSize: '1.28rem',
                fontWeight: 700,
                color: '#FFFFFF',
                margin: 0,
                lineHeight: 1.3,
              }}
            >
              Confirmar Reserva de Cupo
            </h2>
          </div>
          <button
            type="button"
            onClick={onClose}
            disabled={isSubmitting}
            aria-label="Cerrar modal de reserva"
            style={{
              background: 'transparent',
              border: 'none',
              color: '#94A3B8',
              fontSize: '1.5rem',
              lineHeight: 1,
              cursor: isSubmitting ? 'not-allowed' : 'pointer',
              padding: '0.25rem',
              borderRadius: '6px',
              transition: 'color 0.15s',
            }}
          >
            &times;
          </button>
        </div>

        {/* Cuerpo del Diálogo con Scroll */}
        <div
          style={{
            padding: '1.5rem',
            overflowY: 'auto',
            display: 'flex',
            flexDirection: 'column',
            gap: '1.25rem',
          }}
        >
          {/* Identidad del Estudiante Postulante (Badge No Editable) */}
          <div
            style={{
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'space-between',
              backgroundColor: '#F8FAFC',
              border: '1px solid #E2E8F0',
              borderRadius: '8px',
              padding: '0.65rem 0.9rem',
              fontSize: '0.82rem',
            }}
          >
            <div style={{ color: '#475569' }}>
              👤 <strong>Estudiante Solicitante:</strong>{' '}
              <span style={{ color: '#1C2A59', fontWeight: 600 }}>{resolvedStudentEmail}</span>
            </div>
            <span
              style={{
                backgroundColor: '#DCFCE7',
                color: '#166534',
                padding: '0.15rem 0.5rem',
                borderRadius: '4px',
                fontWeight: 600,
                fontSize: '0.72rem',
              }}
            >
              UPT Autenticado
            </span>
          </div>

          {/* Estado de Éxito: Comprobante Provisional */}
          {successData ? (
            <div
              role="status"
              data-testid="booking-success-panel"
              style={{
                backgroundColor: '#F0FDF4',
                border: '1px solid #BBF7D0',
                borderRadius: '12px',
                padding: '1.5rem',
                textAlign: 'center',
              }}
            >
              <div
                style={{
                  width: '48px',
                  height: '48px',
                  borderRadius: '50%',
                  backgroundColor: '#22C55E',
                  color: '#FFFFFF',
                  fontSize: '1.5rem',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  margin: '0 auto 1rem auto',
                }}
              >
                ✓
              </div>
              <h3
                style={{
                  fontSize: '1.2rem',
                  fontWeight: 700,
                  color: '#166534',
                  margin: '0 0 0.5rem 0',
                }}
              >
                ¡Cupo Reservado Exitosamente!
              </h3>
              <p style={{ fontSize: '0.86rem', color: '#166534', margin: '0 0 1rem 0' }}>
                Tu solicitud ha sido registrada provisionalmente en el sistema.
              </p>

              <div
                style={{
                  backgroundColor: '#FFFFFF',
                  borderRadius: '8px',
                  border: '1px solid #DCFCE7',
                  padding: '1rem',
                  textAlign: 'left',
                  fontSize: '0.84rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.4rem',
                  marginBottom: '1rem',
                }}
              >
                <div>
                  <strong>Código de Reserva:</strong>{' '}
                  <span
                    data-testid="receipt-booking-code"
                    style={{
                      fontFamily: 'monospace',
                      fontWeight: 700,
                      color: '#1C2A59',
                      fontSize: '0.95rem',
                    }}
                  >
                    {successData.codigo_reserva}
                  </span>
                </div>
                <div>
                  <strong>Estado:</strong>{' '}
                  <span
                    style={{
                      backgroundColor: '#FEF3C7',
                      color: '#92400E',
                      padding: '0.15rem 0.45rem',
                      borderRadius: '4px',
                      fontWeight: 600,
                      fontSize: '0.78rem',
                    }}
                  >
                    {successData.estado}
                  </span>
                </div>
                {successData.fecha_limite_confirmacion && (
                  <div>
                    <strong>Fecha Límite para Ratificar (RN-08):</strong>{' '}
                    <span style={{ color: '#DC2626', fontWeight: 600 }}>
                      {formatSessionDateTime(successData.fecha_limite_confirmacion)}
                    </span>
                  </div>
                )}
                {successData.mensaje && (
                  <div style={{ marginTop: '0.35rem', color: '#475569', fontSize: '0.8rem' }}>
                    ℹ️ {successData.mensaje}
                  </div>
                )}
              </div>

              <button
                type="button"
                onClick={onClose}
                style={{
                  backgroundColor: '#1C2A59',
                  color: '#FFFFFF',
                  border: 'none',
                  borderRadius: '8px',
                  padding: '0.65rem 1.5rem',
                  fontSize: '0.88rem',
                  fontWeight: 600,
                  cursor: 'pointer',
                }}
              >
                Entendido, Cerrar
              </button>
            </div>
          ) : (
            <>
              {/* Tarjeta de Resumen de la Oferta */}
              <div
                style={{
                  backgroundColor: '#F8FAFC',
                  borderRadius: '12px',
                  border: '1px solid #E2E8F0',
                  padding: '1.25rem',
                  display: 'flex',
                  flexDirection: 'column',
                  gap: '0.85rem',
                }}
              >
                {/* Asignatura y Tema */}
                <div>
                  <div
                    style={{
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'space-between',
                      gap: '0.5rem',
                    }}
                  >
                    <span
                      style={{
                        fontSize: '0.75rem',
                        fontWeight: 700,
                        color: '#64748B',
                        textTransform: 'uppercase',
                        letterSpacing: '0.05em',
                      }}
                    >
                      {offer.codigo_asignatura || 'CURSO'}
                    </span>
                    <span
                      style={{
                        fontFamily: 'monospace',
                        fontSize: '0.75rem',
                        color: '#475569',
                        backgroundColor: '#E2E8F0',
                        padding: '0.1rem 0.4rem',
                        borderRadius: '4px',
                      }}
                    >
                      ID: {offer.codigo_sesion || offer.id_oferta}
                    </span>
                  </div>
                  <div
                    style={{
                      fontSize: '1.05rem',
                      fontWeight: 700,
                      color: '#1C2A59',
                      marginTop: '0.2rem',
                    }}
                  >
                    {offer.nombre_asignatura}
                  </div>
                  <div
                    style={{
                      fontSize: '0.9rem',
                      fontWeight: 600,
                      color: '#334155',
                      marginTop: '0.2rem',
                    }}
                  >
                    Tema: {offer.nombre_tema}
                  </div>
                </div>

                <div
                  style={{
                    height: '1px',
                    backgroundColor: '#E2E8F0',
                  }}
                />

                {/* Grilla de Atributos de Sesión */}
                <div
                  style={{
                    display: 'grid',
                    gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))',
                    gap: '0.85rem',
                    fontSize: '0.84rem',
                  }}
                >
                  {/* Mentor */}
                  <div>
                    <div style={{ color: '#64748B', fontSize: '0.75rem', fontWeight: 600 }}>
                      MENTOR RESPONSABLE
                    </div>
                    <div style={{ color: '#0F172A', fontWeight: 600, marginTop: '0.15rem' }}>
                      {offer.mentor_nombre || offer.mentor_email}
                    </div>
                    <div style={{ color: '#64748B', fontSize: '0.78rem' }}>
                      {offer.mentor_ciclo
                        ? `Ciclo ${offer.mentor_ciclo} • Mérito RN-03`
                        : offer.mentor_email}
                    </div>
                  </div>

                  {/* Horario y Duración */}
                  <div>
                    <div style={{ color: '#64748B', fontSize: '0.75rem', fontWeight: 600 }}>
                      FECHA Y HORARIO
                    </div>
                    <div style={{ color: '#0F172A', fontWeight: 600, marginTop: '0.15rem' }}>
                      📅 {formatSessionDateTime(offer.fecha_inicio)}
                    </div>
                    <div style={{ color: '#64748B', fontSize: '0.78rem' }}>
                      ⏱️ Duración: {offer.duracion_minutos} minutos
                    </div>
                  </div>

                  {/* Modalidad y Espacio */}
                  <div>
                    <div style={{ color: '#64748B', fontSize: '0.75rem', fontWeight: 600 }}>
                      MODALIDAD Y ESPACIO
                    </div>
                    <div
                      style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '0.4rem',
                        marginTop: '0.15rem',
                      }}
                    >
                      <span
                        style={{
                          backgroundColor: isPresencial ? '#DBEAFE' : '#EDE9FE',
                          color: isPresencial ? '#1E40AF' : '#5B21B6',
                          padding: '0.12rem 0.45rem',
                          borderRadius: '4px',
                          fontWeight: 700,
                          fontSize: '0.72rem',
                          textTransform: 'uppercase',
                        }}
                      >
                        {offer.modalidad}
                      </span>
                    </div>
                    <div
                      style={{
                        color: '#475569',
                        fontSize: '0.78rem',
                        marginTop: '0.2rem',
                        overflow: 'hidden',
                        textOverflow: 'ellipsis',
                        whiteSpace: 'nowrap',
                      }}
                    >
                      📍{' '}
                      {offer.espacio_asignado ||
                        (isPresencial
                          ? 'Aula física por asignar'
                          : 'Enlace virtual (se emitirá al ratificar)')}
                    </div>
                  </div>

                  {/* Aforo y Vacantes (RN-05) */}
                  <div>
                    <div style={{ color: '#64748B', fontSize: '0.75rem', fontWeight: 600 }}>
                      DISPONIBILIDAD DE AFORO (RN-05)
                    </div>
                    <div
                      style={{
                        color: offer.aforo_disponible > 0 ? '#15803D' : '#DC2626',
                        fontWeight: 700,
                        fontSize: '0.9rem',
                        marginTop: '0.15rem',
                      }}
                    >
                      {offer.aforo_disponible > 0
                        ? `${offer.aforo_disponible} vacantes disponibles`
                        : 'Aforo Completo (0 vacantes)'}
                    </div>
                    <div style={{ color: '#64748B', fontSize: '0.78rem' }}>
                      Capacidad total: {offer.aforo_maximo} cupos ({isPresencial ? '10' : '20'}{' '}
                      normados)
                    </div>
                  </div>
                </div>
              </div>

              {/* Alerta de Error Controlado si existe */}
              {error && (
                <div
                  role="alert"
                  data-testid="booking-error-alert"
                  style={{
                    backgroundColor: '#FEF2F2',
                    border: '1px solid #FECACA',
                    borderRadius: '8px',
                    padding: '0.85rem 1rem',
                    fontSize: '0.84rem',
                    color: '#991B1B',
                    lineHeight: 1.4,
                  }}
                >
                  <strong>⚠️ Error en Reserva:</strong> {error}
                </div>
              )}

              {/* Banners Preventivos según Reglas de Negocio */}
              {isSelfBooking && (
                <div
                  role="alert"
                  data-testid="warning-self-booking"
                  style={{
                    backgroundColor: '#FEF2F2',
                    border: '1px solid #FECACA',
                    borderRadius: '8px',
                    padding: '0.85rem 1rem',
                    fontSize: '0.84rem',
                    color: '#991B1B',
                    lineHeight: 1.4,
                  }}
                >
                  <strong>🚫 Restricción de Autoreserva (RN-03):</strong> Como mentor titular de esta
                  sesión formativa, no puedes postularte ni reservar una vacante como estudiante mentoreado.
                </div>
              )}

              {isCapacityExceeded && !isSelfBooking && (
                <div
                  role="alert"
                  data-testid="warning-capacity-exceeded"
                  style={{
                    backgroundColor: '#FFFBEB',
                    border: '1px solid #FDE68A',
                    borderRadius: '8px',
                    padding: '0.85rem 1rem',
                    fontSize: '0.84rem',
                    color: '#92400E',
                    lineHeight: 1.4,
                  }}
                >
                  <strong>⚠️ Aforo Agotado (RN-05):</strong> No quedan vacantes disponibles en esta
                  sesión. Puedes registrar una solicitud de mentoría por demanda para coordinar una
                  nueva fecha con un mentor.
                  {onDemandRedirect && (
                    <div style={{ marginTop: '0.5rem' }}>
                      <button
                        type="button"
                        onClick={onDemandRedirect}
                        style={{
                          backgroundColor: '#D97706',
                          color: '#FFFFFF',
                          border: 'none',
                          borderRadius: '6px',
                          padding: '0.35rem 0.8rem',
                          fontSize: '0.78rem',
                          fontWeight: 600,
                          cursor: 'pointer',
                        }}
                      >
                        Registrar Solicitud por Demanda (CUS03)
                      </button>
                    </div>
                  )}
                </div>
              )}

              {isExpired && !isSelfBooking && (
                <div
                  role="alert"
                  data-testid="warning-expired-session"
                  style={{
                    backgroundColor: '#FEF2F2',
                    border: '1px solid #FECACA',
                    borderRadius: '8px',
                    padding: '0.85rem 1rem',
                    fontSize: '0.84rem',
                    color: '#991B1B',
                    lineHeight: 1.4,
                  }}
                >
                  <strong>⏰ Sesión Vencida:</strong> El horario programado para el inicio de esta
                  mentoría ya ha transcurrido. No se admiten reservas para sesiones pasadas.
                </div>
              )}

              {isWindowClosed && !isExpired && !isSelfBooking && (
                <div
                  role="alert"
                  data-testid="warning-window-closed"
                  style={{
                    backgroundColor: '#FEF2F2',
                    border: '1px solid #FECACA',
                    borderRadius: '8px',
                    padding: '0.85rem 1rem',
                    fontSize: '0.84rem',
                    color: '#991B1B',
                    lineHeight: 1.4,
                  }}
                >
                  <strong>🔒 Ventana de Reserva Cerrada (T-24h / RN-08):</strong> Las reservas cierran
                  estrictamente 24 horas antes del inicio de la sesión para proceder a la evaluación de
                  quórum institucional (RN-09).
                </div>
              )}

              {/* Aviso Normativo sobre Reserva Provisional (RN-08 / RNF07) */}
              <div
                id={descId}
                style={{
                  backgroundColor: '#EFF6FF',
                  border: '1px solid #BFDBFE',
                  borderRadius: '8px',
                  padding: '0.85rem 1rem',
                  fontSize: '0.82rem',
                  color: '#1E40AF',
                  lineHeight: 1.45,
                }}
              >
                <div style={{ fontWeight: 700, marginBottom: '0.2rem' }}>
                  ℹ️ Información Institucional del Proceso de Reserva
                </div>
                <ul style={{ margin: 0, paddingLeft: '1.2rem' }}>
                  <li>
                    Tu reserva se registrará en estado <strong>PENDIENTE_CONFIRMACION</strong>.
                  </li>
                  <li>
                    Deberás ratificar tu asistencia obligatoriamente antes de las <strong>24 horas previas</strong>{' '}
                    al inicio de la sesión (RN-08) para confirmar tu plaza y cómputo de quórum.
                  </li>
                  <li>
                    <strong>Concurrencia ACID (RNF07):</strong> Las vacantes mostradas son referenciales
                    hasta que el servidor confirme la transacción bajo bloqueo pesimista.
                  </li>
                </ul>
              </div>
            </>
          )}
        </div>

        {/* Pie de Acciones del Modal */}
        {!successData && (
          <div
            style={{
              padding: '1rem 1.5rem',
              backgroundColor: '#F8FAFC',
              borderTop: '1px solid #E2E8F0',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'flex-end',
              gap: '0.75rem',
              flexWrap: 'wrap',
            }}
          >
            <button
              type="button"
              onClick={onClose}
              disabled={isSubmitting}
              style={{
                backgroundColor: '#FFFFFF',
                color: '#475569',
                border: '1px solid #CBD5E1',
                borderRadius: '8px',
                padding: '0.65rem 1.25rem',
                fontSize: '0.85rem',
                fontWeight: 600,
                cursor: isSubmitting ? 'not-allowed' : 'pointer',
                transition: 'all 0.15s',
              }}
            >
              Cancelar
            </button>

            <button
              type="button"
              onClick={handleConfirm}
              disabled={!canConfirm}
              aria-disabled={!canConfirm}
              style={{
                backgroundColor: canConfirm ? '#1C2A59' : '#94A3B8',
                color: '#FFFFFF',
                border: 'none',
                borderRadius: '8px',
                padding: '0.65rem 1.5rem',
                fontSize: '0.85rem',
                fontWeight: 700,
                cursor: canConfirm ? 'pointer' : 'not-allowed',
                boxShadow: canConfirm ? '0 4px 12px rgba(28, 42, 89, 0.2)' : 'none',
                display: 'flex',
                alignItems: 'center',
                gap: '0.5rem',
                transition: 'all 0.2s',
              }}
            >
              {isSubmitting ? (
                <>
                  <span
                    style={{
                      display: 'inline-block',
                      width: '14px',
                      height: '14px',
                      border: '2px solid #FFFFFF',
                      borderTopColor: 'transparent',
                      borderRadius: '50%',
                      animation: 'spin 1s linear infinite',
                    }}
                  />
                  <span>Procesando reserva...</span>
                </>
              ) : (
                <span>Confirmar Reserva de Cupo</span>
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
