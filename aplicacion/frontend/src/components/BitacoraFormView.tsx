/**
 * Vista de Formulario de Bitácora Pedagógica y Acreditación de Horas (T-34 / Sprint 6)
 *
 * Trazabilidad:
 * - Requerimiento Funcional: RF17 (Registro de bitácoras pedagógicas y horas de mentoría)
 * - Casos de Uso: CUS13
 * - Regla de Negocio RN-12: Ventana perentoria de 48h, observaciones >= 50 caracteres y firma SHA-256
 * - Requerimiento No Funcional: RNF05 (Accesibilidad WCAG 2.1 AA)
 */

import React, { useState } from 'react';
import {
  bitacoraService,
  type BitacoraPayload,
  type BitacoraResponse,
} from '../services/bitacoraService';

export interface BitacoraFormViewProps {
  sessionId: string | number;
  sessionTitle?: string;
  sessionEndDate?: string | Date;
  subjectName?: string;
  syllabusTopics?: string[];
  onSuccess?: (hash: string) => void;
  onBack?: () => void;
}

const DEFAULT_SYLLABUS_TOPICS: string[] = [
  'Límites algebraicos e indeterminaciones',
  'Continuidad puntual y en intervalos',
  'Teorema de Bolzano y de los Valores Intermedios',
  'Derivadas y reglas de derivación',
  'Optimización y razones de cambio',
];

export const BitacoraFormView: React.FC<BitacoraFormViewProps> = ({
  sessionId,
  sessionTitle = 'Sesión de Mentoría Concluida',
  sessionEndDate,
  subjectName = 'Cálculo I',
  syllabusTopics = DEFAULT_SYLLABUS_TOPICS,
  onSuccess,
  onBack,
}) => {
  const [now] = useState(() => Date.now());

  // Verificación de ventana perentoria de 48 horas (RN-12)
  const isPast48Hours = (() => {
    if (!sessionEndDate) return false;
    const endMs = new Date(sessionEndDate).getTime();
    if (isNaN(endMs)) return false;
    const diffHours = (now - endMs) / (3600 * 1000);
    return diffHours > 48.0;
  })();

  const [selectedTopics, setSelectedTopics] = useState<string[]>([]);
  const [customTopic, setCustomTopic] = useState<string>('');
  const [dificultad, setDificultad] = useState<'Bajo' | 'Medio' | 'Alto'>('Medio');
  const [observaciones, setObservaciones] = useState<string>('');
  const [swornDeclaration, setSwornDeclaration] = useState<boolean>(false);

  const [isSubmitting, setIsSubmitting] = useState<boolean>(false);
  const [validationError, setValidationError] = useState<string | null>(null);
  const [submittedBitacora, setSubmittedBitacora] = useState<BitacoraResponse | null>(null);

  const handleToggleTopic = (topic: string) => {
    setSelectedTopics((prev) =>
      prev.includes(topic) ? prev.filter((t) => t !== topic) : [...prev, topic]
    );
  };

  const handleAddCustomTopic = () => {
    const trimmed = customTopic.trim();
    if (trimmed && !selectedTopics.includes(trimmed)) {
      setSelectedTopics((prev) => [...prev, trimmed]);
      setCustomTopic('');
    }
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setValidationError(null);

    // Validación de regla RN-12: >= 50 caracteres
    if (observaciones.trim().length < 50) {
      setValidationError('Las observaciones pedagógicas deben poseer al menos 50 caracteres para garantizar una justificación académica sustantiva.');
      return;
    }

    if (selectedTopics.length === 0) {
      setValidationError('Debe marcar o agregar al menos un tema silábico abordado durante la sesión.');
      return;
    }

    if (!swornDeclaration) {
      setValidationError('Debe suscribir la declaración jurada de veracidad académica para formalizar el registro.');
      return;
    }

    setIsSubmitting(true);
    try {
      const payload: BitacoraPayload = {
        temas_cubiertos: selectedTopics,
        observaciones: observaciones.trim(),
        nivel_dificultad: dificultad,
      };

      const resp = await bitacoraService.submitBitacora(sessionId, payload);
      setSubmittedBitacora(resp);
      if (onSuccess) {
        onSuccess(resp.hash_firma);
      }
    } catch (err: unknown) {
      setValidationError(err instanceof Error ? err.message : 'Error al registrar la bitácora pedagógica.');
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <div style={{ maxWidth: '820px', margin: '0 auto', padding: '1rem' }}>
      {/* Botón de retorno opcional */}
      {onBack && (
        <button
          type="button"
          onClick={onBack}
          style={{
            background: 'none',
            border: 'none',
            color: '#1C2A59',
            fontWeight: 700,
            cursor: 'pointer',
            marginBottom: '1rem',
            display: 'flex',
            alignItems: 'center',
            gap: '0.4rem',
            fontSize: '0.9rem',
          }}
        >
          ← Volver a Mis Sesiones
        </button>
      )}

      {/* Cabecera */}
      <div
        style={{
          backgroundColor: '#1C2A59',
          color: '#FFFFFF',
          borderRadius: '12px',
          padding: '1.5rem',
          marginBottom: '1.5rem',
          boxShadow: '0 4px 12px rgba(28, 42, 89, 0.15)',
        }}
      >
        <span
          style={{
            backgroundColor: '#B99451',
            color: '#FFFFFF',
            fontSize: '0.72rem',
            fontWeight: 800,
            padding: '0.2rem 0.5rem',
            borderRadius: '4px',
            textTransform: 'uppercase',
            letterSpacing: '0.05em',
            display: 'inline-block',
            marginBottom: '0.5rem',
          }}
        >
          Registro Pedagógico Oficial
        </span>
        <h2 style={{ fontSize: '1.5rem', fontWeight: 800, margin: '0 0 0.5rem 0' }}>
          📝 Bitácora Pedagógica de Mentoría
        </h2>
        <p style={{ margin: 0, fontSize: '0.88rem', opacity: 0.9 }}>
          Asignatura: <strong>{subjectName}</strong> — {sessionTitle}. Registro formal de tópicos explicados,
          dificultades observadas y acreditación de horas académicas con firma digital SHA-256.
        </p>
      </div>

      {/* Alerta Roja de Bloqueo por Expiración de Plazo de 48 Horas (RN-12) */}
      {isPast48Hours && (
        <div
          data-testid="deadline-expired-alert"
          style={{
            backgroundColor: '#FEF2F2',
            border: '2px solid #DC2626',
            borderRadius: '12px',
            padding: '1.5rem',
            color: '#991B1B',
            marginBottom: '1.5rem',
            display: 'flex',
            alignItems: 'flex-start',
            gap: '1rem',
          }}
        >
          <span style={{ fontSize: '2rem' }}>⛔</span>
          <div>
            <h3 style={{ margin: '0 0 0.35rem 0', fontSize: '1.1rem', fontWeight: 800 }}>
              Formulario Bloqueado: Plazo Ordinario de 48 Horas Expirado
            </h3>
            <p style={{ margin: 0, fontSize: '0.85rem', lineHeight: 1.5 }}>
              Han transcurrido más de 48 horas desde la finalización de esta sesión. Conforme al reglamento de mentorías
              académicas de la EPIS-UPT, el registro ordinario se encuentra inhabilitado. Debe contactar a la Dirección de
              Escuela para gestionar una apertura extemporánea mediante visado administrativo.
            </p>
          </div>
        </div>
      )}

      {/* Comprobante de Envío Exitoso con Firma Digital Criptográfica */}
      {submittedBitacora && (
        <div
          data-testid="bitacora-success-card"
          style={{
            backgroundColor: '#DEF7EC',
            border: '2px solid #31C48D',
            borderRadius: '12px',
            padding: '1.5rem',
            color: '#03543F',
            marginBottom: '1.5rem',
          }}
        >
          <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.75rem' }}>
            <span style={{ fontSize: '1.8rem' }}>✅</span>
            <h3 style={{ margin: 0, fontSize: '1.2rem', fontWeight: 800 }}>
              Bitácora Pedagógica Registrada y Sellada con Éxito
            </h3>
          </div>
          <p style={{ fontSize: '0.88rem', margin: '0 0 1rem 0' }}>
            {submittedBitacora.mensaje} Se han computado provisionalmente{' '}
            <strong>{submittedBitacora.horas_declaradas} horas académicas</strong> a la espera del visado de Dirección de Escuela.
          </p>

          <div
            style={{
              backgroundColor: '#FFFFFF',
              border: '1px solid #A7F3D0',
              borderRadius: '8px',
              padding: '0.85rem 1rem',
              fontSize: '0.82rem',
              color: '#1E293B',
            }}
          >
            <div style={{ marginBottom: '0.35rem' }}>
              <strong>Código de Bitácora:</strong> #{submittedBitacora.id_bitacora} |{' '}
              <strong>Sesión:</strong> #{submittedBitacora.id_sesion}
            </div>
            <div style={{ marginBottom: '0.35rem' }}>
              <strong>Nivel de Dificultad:</strong> {submittedBitacora.nivel_dificultad} |{' '}
              <strong>Temas Cubiertos:</strong> {submittedBitacora.temas_cubiertos.join(', ')}
            </div>
            <div style={{ marginTop: '0.5rem', borderTop: '1px dashed #CBD5E1', paddingTop: '0.5rem' }}>
              <span style={{ fontSize: '0.75rem', color: '#64748B', display: 'block' }}>
                Firma Digital Criptográfica (SHA-256):
              </span>
              <code
                style={{
                  fontFamily: 'monospace',
                  fontSize: '0.85rem',
                  color: '#1C2A59',
                  fontWeight: 700,
                  wordBreak: 'break-all',
                }}
              >
                {submittedBitacora.hash_firma}
              </code>
            </div>
          </div>
        </div>
      )}

      {/* Formulario Principal de Captura */}
      <form
        onSubmit={handleSubmit}
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #E2E8F0',
          padding: '1.75rem',
          boxShadow: '0 2px 8px rgba(0, 0, 0, 0.05)',
          opacity: isPast48Hours ? 0.5 : 1,
          pointerEvents: isPast48Hours ? 'none' : 'auto',
        }}
      >
        {validationError && (
          <div
            role="alert"
            style={{
              backgroundColor: '#FEF2F2',
              border: '1px solid #F87171',
              borderRadius: '8px',
              padding: '0.75rem 1rem',
              color: '#991B1B',
              fontSize: '0.85rem',
              marginBottom: '1.25rem',
            }}
          >
            ⚠️ {validationError}
          </div>
        )}

        {/* 1. Checklist Silábico */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'block', fontSize: '0.9rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.5rem' }}>
            1. Temas Silábicos Desarrollados en la Sesión:
          </label>
          <p style={{ fontSize: '0.8rem', color: '#64748B', margin: '0 0 0.75rem 0' }}>
            Seleccione de la malla curricular oficial los tópicos efectivamente cubiertos durante la mentoría:
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '0.75rem' }}>
            {syllabusTopics.map((topic) => (
              <label
                key={topic}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.6rem',
                  fontSize: '0.85rem',
                  color: '#334155',
                  cursor: 'pointer',
                  padding: '0.35rem 0.5rem',
                  borderRadius: '6px',
                  backgroundColor: selectedTopics.includes(topic) ? '#F1F5F9' : 'transparent',
                }}
              >
                <input
                  type="checkbox"
                  checked={selectedTopics.includes(topic)}
                  onChange={() => handleToggleTopic(topic)}
                />
                <span>{topic}</span>
              </label>
            ))}
          </div>

          {/* Adición de tema adicional */}
          <div style={{ display: 'flex', gap: '0.5rem' }}>
            <input
              type="text"
              placeholder="Otro tema específico abordado..."
              value={customTopic}
              onChange={(e) => setCustomTopic(e.target.value)}
              style={{
                flex: 1,
                padding: '0.45rem 0.75rem',
                borderRadius: '6px',
                border: '1px solid #CBD5E1',
                fontSize: '0.82rem',
              }}
            />
            <button
              type="button"
              onClick={handleAddCustomTopic}
              style={{
                backgroundColor: '#F1F5F9',
                border: '1px solid #CBD5E1',
                color: '#1C2A59',
                borderRadius: '6px',
                padding: '0.45rem 0.85rem',
                fontSize: '0.82rem',
                fontWeight: 600,
                cursor: 'pointer',
              }}
            >
              ➕ Agregar
            </button>
          </div>
        </div>

        {/* 2. Nivel de Dificultad Percibido */}
        <div style={{ marginBottom: '1.5rem' }}>
          <label style={{ display: 'block', fontSize: '0.9rem', fontWeight: 700, color: '#1C2A59', marginBottom: '0.5rem' }}>
            2. Nivel de Dificultad Percibido del Grupo:
          </label>
          <div style={{ display: 'flex', gap: '1.5rem', flexWrap: 'wrap' }}>
            {(['Bajo', 'Medio', 'Alto'] as const).map((lvl) => (
              <label
                key={lvl}
                style={{
                  display: 'flex',
                  alignItems: 'center',
                  gap: '0.5rem',
                  fontSize: '0.85rem',
                  color: '#334155',
                  cursor: 'pointer',
                }}
              >
                <input
                  type="radio"
                  name="nivel_dificultad"
                  value={lvl}
                  checked={dificultad === lvl}
                  onChange={() => setDificultad(lvl)}
                />
                <span>{lvl === 'Bajo' ? '🟢 Bajo (Asimilación Fluida)' : lvl === 'Medio' ? '🟡 Medio (Dudas Puntuales)' : '🔴 Alto (Requiere Refuerzo)'}</span>
              </label>
            ))}
          </div>
        </div>

        {/* 3. Observaciones Pedagógicas (Mínimo 50 Caracteres) */}
        <div style={{ marginBottom: '1.5rem' }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: '0.35rem' }}>
            <label htmlFor="observaciones-textarea" style={{ fontSize: '0.9rem', fontWeight: 700, color: '#1C2A59' }}>
              3. Observaciones Pedagógicas y Conclusiones:
            </label>
            <span
              style={{
                fontSize: '0.78rem',
                fontWeight: 700,
                color: observaciones.trim().length >= 50 ? '#059669' : '#D97706',
              }}
            >
              {observaciones.trim().length} / 50 caracteres requeridos
            </span>
          </div>
          <p style={{ fontSize: '0.8rem', color: '#64748B', margin: '0 0 0.5rem 0' }}>
            Describa el desenvolvimiento de los estudiantes, ejercicios resueltos y recomendaciones para la próxima sesión (mínimo 50 caracteres).
          </p>
          <textarea
            id="observaciones-textarea"
            rows={4}
            placeholder="Redacte aquí las incidencias académicas, nivel de participación de los estudiantes y compromisos de estudio asumidos (al menos 50 caracteres)..."
            value={observaciones}
            onChange={(e) => setObservaciones(e.target.value)}
            style={{
              width: '100%',
              padding: '0.65rem 0.85rem',
              borderRadius: '8px',
              border: observaciones.trim().length > 0 && observaciones.trim().length < 50 ? '1px solid #F59E0B' : '1px solid #CBD5E1',
              fontSize: '0.88rem',
              lineHeight: 1.5,
              resize: 'vertical',
              boxSizing: 'border-box',
            }}
          />
        </div>

        {/* 4. Declaración Jurada */}
        <div
          style={{
            backgroundColor: '#F8FAFC',
            border: '1px solid #E2E8F0',
            borderRadius: '8px',
            padding: '1rem',
            marginBottom: '1.5rem',
          }}
        >
          <label style={{ display: 'flex', alignItems: 'flex-start', gap: '0.75rem', cursor: 'pointer' }}>
            <input
              type="checkbox"
              id="sworn-declaration-checkbox"
              checked={swornDeclaration}
              onChange={(e) => setSwornDeclaration(e.target.checked)}
              style={{ marginTop: '0.2rem' }}
            />
            <span style={{ fontSize: '0.82rem', color: '#334155', lineHeight: 1.4 }}>
              <strong>Declaración Jurada de Veracidad Académica:</strong> Declaro bajo juramento que los temas cubiertos,
              horas efectivas y observaciones consignadas en la presente bitácora reflejan con fidelidad la labor de mentoría
              impartida, sujetándome al reglamento de la EPIS-UPT y a la auditoría de Dirección de Escuela.
            </span>
          </label>
        </div>

        {/* Botón de Envío */}
        <div style={{ display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
          <button
            type="submit"
            disabled={isSubmitting || isPast48Hours}
            style={{
              backgroundColor: isSubmitting || isPast48Hours ? '#94A3B8' : '#1C2A59',
              color: '#FFFFFF',
              border: 'none',
              borderRadius: '8px',
              padding: '0.75rem 1.75rem',
              fontWeight: 700,
              fontSize: '0.9rem',
              cursor: isSubmitting || isPast48Hours ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
            }}
          >
            {isSubmitting ? 'Sellando Criptográficamente...' : 'Firmar y Registrar Bitácora'}
          </button>
        </div>
      </form>
    </div>
  );
};
