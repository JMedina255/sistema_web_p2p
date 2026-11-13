/**
 * Vista de Administración: Ingesta y Procesamiento de Cronogramas Oficiales (RF10 / CUS11 / RN-06 / MOD-04)
 */

import React, { useState, useEffect, useCallback, useMemo, useRef } from 'react';
import {
  spacesService,
  type FreeSlotItem,
  type ScheduleImportResponse,
} from '../services/spacesService';

export interface AdminScheduleUploadViewProps {
  onScheduleUpdated?: (totalSlots: number) => void;
}

export const AdminScheduleUploadView: React.FC<AdminScheduleUploadViewProps> = ({
  onScheduleUpdated,
}) => {
  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [isDragging, setIsDragging] = useState<boolean>(false);
  const [isProcessing, setIsProcessing] = useState<boolean>(false);
  const [errorMessage, setErrorMessage] = useState<string | null>(null);
  const [successResult, setSuccessResult] = useState<ScheduleImportResponse | null>(null);

  // Lista de franjas horarias activas y filtros
  const [slots, setSlots] = useState<FreeSlotItem[]>([]);
  const [isLoadingSlots, setIsLoadingSlots] = useState<boolean>(true);
  const [classroomFilter, setClassroomFilter] = useState<string>('ALL');
  const [dayFilter, setDayFilter] = useState<string>('ALL');
  const [searchTerm, setSearchTerm] = useState<string>('');

  const fileInputRef = useRef<HTMLInputElement>(null);

  const fetchCurrentSlots = useCallback(async () => {
    setIsLoadingSlots(true);
    try {
      const data = await spacesService.getFreeSlots();
      setSlots(data);
    } catch {
      // Ignorar fallo secundario
    } finally {
      setIsLoadingSlots(false);
    }
  }, []);

  useEffect(() => {
    fetchCurrentSlots();
  }, [fetchCurrentSlots]);

  const handleFileChange = (e: React.ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files.length > 0) {
      setSelectedFile(e.target.files[0]);
      setErrorMessage(null);
      setSuccessResult(null);
    }
  };

  const handleDragOver = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(true);
  };

  const handleDragLeave = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
  };

  const handleDrop = (e: React.DragEvent<HTMLDivElement>) => {
    e.preventDefault();
    setIsDragging(false);
    if (e.dataTransfer.files && e.dataTransfer.files.length > 0) {
      setSelectedFile(e.dataTransfer.files[0]);
      setErrorMessage(null);
      setSuccessResult(null);
    }
  };

  const handleProcessSchedule = async () => {
    if (!selectedFile) {
      setErrorMessage('Debe seleccionar un archivo oficial en formato Excel (.xlsx) o PDF (.pdf).');
      return;
    }

    setIsProcessing(true);
    setErrorMessage(null);
    setSuccessResult(null);

    try {
      const resp = await spacesService.uploadSchedule(selectedFile);
      setSuccessResult(resp);
      setSlots(resp.aulas_libres);
      setSelectedFile(null);
      if (fileInputRef.current) {
        fileInputRef.current.value = '';
      }
      if (onScheduleUpdated) {
        onScheduleUpdated(resp.total_aulas_libres_identificadas);
      }
    } catch (err: unknown) {
      setErrorMessage(
        err instanceof Error ? err.message : 'Error inesperado al procesar el cronograma oficial.'
      );
    } finally {
      setIsProcessing(false);
    }
  };

  // Recintos únicos para selector de filtro
  const uniqueClassrooms = useMemo(() => {
    const set = new Set<string>();
    slots.forEach((s) => {
      if (s.aula) set.add(s.aula);
    });
    return Array.from(set).sort();
  }, [slots]);

  // Días únicos para selector de filtro
  const uniqueDays = useMemo(() => {
    const set = new Set<string>();
    slots.forEach((s) => {
      if (s.dia) set.add(s.dia);
    });
    return Array.from(set);
  }, [slots]);

  // Franjas filtradas según búsqueda y controles
  const filteredSlots = useMemo(() => {
    return slots.filter((slot) => {
      if (classroomFilter !== 'ALL' && slot.aula !== classroomFilter) return false;
      if (dayFilter !== 'ALL' && slot.dia !== dayFilter) return false;
      if (searchTerm.trim()) {
        const query = searchTerm.toLowerCase();
        const matchesAula = slot.aula.toLowerCase().includes(query);
        const matchesDia = slot.dia.toLowerCase().includes(query);
        const matchesHoras = `${slot.hora_inicio} ${slot.hora_fin}`.includes(query);
        if (!matchesAula && !matchesDia && !matchesHoras) return false;
      }
      return true;
    });
  }, [slots, classroomFilter, dayFilter, searchTerm]);

  return (
    <div style={{ width: '100%', display: 'flex', flexDirection: 'column', gap: '1.5rem' }}>
      {/* Cabecera del Módulo */}
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #E2E8F0',
          padding: '1.5rem',
          boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
        }}
      >
        <div style={{ display: 'flex', alignItems: 'center', gap: '0.75rem', marginBottom: '0.5rem' }}>
          <span style={{ fontSize: '1.75rem' }}>📅</span>
          <div>
            <h2 style={{ margin: 0, fontSize: '1.35rem', fontWeight: 800, color: '#1C2A59' }}>
              Procesamiento de Cronogramas Institucionales (Parser de Horarios)
            </h2>
            <span
              style={{
                fontSize: '0.78rem',
                backgroundColor: '#EFF6FF',
                color: '#1D4ED8',
                fontWeight: 700,
                padding: '0.15rem 0.5rem',
                borderRadius: '4px',
              }}
            >
              Requerimiento RF10 / Caso de Uso CUS11 / Regla RN-06
            </span>
          </div>
        </div>
        <p style={{ margin: '0.5rem 0 0 0', fontSize: '0.88rem', color: '#64748B', lineHeight: 1.5 }}>
          Carga y análisis de los archivos oficiales de programación académica de aulas y laboratorios de la EPIS-UPT.
          El motor interno procesa los documentos en <strong>Excel (.xlsx)</strong> o <strong>PDF</strong>, extrae las franjas horarias y
          recintos libres respecto de las clases de cátedra, y actualiza el banco de infraestructura física disponible para prevenir
          solapamientos en sesiones presenciales (<strong>RN-06</strong>).
        </p>
      </div>

      {/* Zona de Carga de Archivos (Drag & Drop) */}
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #E2E8F0',
          padding: '1.5rem',
          boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
        }}
      >
        <h3 style={{ margin: '0 0 1rem 0', fontSize: '1.05rem', fontWeight: 700, color: '#1E293B' }}>
          📤 Cargar Archivo Oficial de Distribución Horaria
        </h3>

        <div
          onDragOver={handleDragOver}
          onDragLeave={handleDragLeave}
          onDrop={handleDrop}
          onClick={() => fileInputRef.current?.click()}
          style={{
            border: isDragging ? '2px dashed #1C2A59' : '2px dashed #CBD5E1',
            borderRadius: '10px',
            backgroundColor: isDragging ? '#EFF6FF' : '#F8FAFC',
            padding: '2.5rem 1.5rem',
            textAlign: 'center',
            cursor: 'pointer',
            transition: 'all 0.2s ease',
          }}
        >
          <input
            ref={fileInputRef}
            type="file"
            accept=".xlsx, .xls, .pdf"
            onChange={handleFileChange}
            style={{ display: 'none' }}
            aria-label="Seleccionar archivo oficial de cronograma"
          />

          <div style={{ fontSize: '2.5rem', marginBottom: '0.75rem' }}>📄</div>
          <p style={{ margin: '0 0 0.35rem 0', fontSize: '0.95rem', fontWeight: 700, color: '#1E293B' }}>
            {selectedFile ? selectedFile.name : 'Arrastra aquí el archivo oficial de horarios o haz clic para explorar'}
          </p>
          <p style={{ margin: 0, fontSize: '0.82rem', color: '#64748B' }}>
            Formatos oficiales admitidos: <strong>Excel (.xlsx, .xls)</strong> y <strong>Documentos PDF (.pdf)</strong> (Máximo 15 MB)
          </p>
          {selectedFile && (
            <p style={{ marginTop: '0.5rem', fontSize: '0.78rem', color: '#059669', fontWeight: 600 }}>
              Tamaño: {(selectedFile.size / 1024).toFixed(1)} KB — Listo para parseo
            </p>
          )}
        </div>

        {/* Botón de Procesamiento */}
        <div style={{ marginTop: '1.25rem', display: 'flex', justifyContent: 'flex-end', gap: '0.75rem' }}>
          {selectedFile && (
            <button
              type="button"
              onClick={() => {
                setSelectedFile(null);
                if (fileInputRef.current) fileInputRef.current.value = '';
              }}
              style={{
                backgroundColor: 'transparent',
                border: '1px solid #CBD5E1',
                borderRadius: '8px',
                padding: '0.65rem 1.25rem',
                fontSize: '0.88rem',
                fontWeight: 600,
                color: '#64748B',
                cursor: 'pointer',
              }}
            >
              Cancelar
            </button>
          )}

          <button
            type="button"
            disabled={!selectedFile || isProcessing}
            onClick={handleProcessSchedule}
            style={{
              backgroundColor: !selectedFile || isProcessing ? '#94A3B8' : '#1C2A59',
              color: '#FFFFFF',
              border: 'none',
              borderRadius: '8px',
              padding: '0.65rem 1.5rem',
              fontSize: '0.9rem',
              fontWeight: 700,
              cursor: !selectedFile || isProcessing ? 'not-allowed' : 'pointer',
              display: 'flex',
              alignItems: 'center',
              gap: '0.5rem',
              boxShadow: '0 2px 6px rgba(28, 42, 89, 0.2)',
            }}
          >
            <span>{isProcessing ? '⏳' : '⚡'}</span>
            {isProcessing ? 'Procesando Cronograma con Parser...' : 'Procesar Cronograma con Parser'}
          </button>
        </div>

        {/* Mensajes de feedback */}
        {errorMessage && (
          <div
            role="alert"
            style={{
              marginTop: '1rem',
              backgroundColor: '#FEF2F2',
              border: '1px solid #F87171',
              borderRadius: '8px',
              padding: '0.85rem 1.25rem',
              color: '#991B1B',
              fontSize: '0.88rem',
            }}
          >
            <strong>Error de Ingesta:</strong> {errorMessage}
          </div>
        )}

        {successResult && (
          <div
            role="status"
            style={{
              marginTop: '1rem',
              backgroundColor: '#DEF7EC',
              border: '1px solid #31C48D',
              borderRadius: '8px',
              padding: '1rem 1.25rem',
              color: '#03543F',
            }}
          >
            <div style={{ display: 'flex', alignItems: 'center', gap: '0.5rem', marginBottom: '0.25rem' }}>
              <span>✅</span>
              <strong style={{ fontSize: '0.95rem' }}>
                ¡Cronograma oficial procesado exitosamente por el Parser de Horarios!
              </strong>
            </div>
            <p style={{ margin: 0, fontSize: '0.85rem', color: '#046C4E' }}>
              Se identificaron <strong>{successResult.total_aulas_libres_identificadas}</strong> franjas horarias libres
              en el archivo <code>{successResult.archivo}</code>. La infraestructura física de la EPIS ha sido actualizada para la
              validación de colisiones con clases regulares (<strong>RN-06</strong>).
            </p>
          </div>
        )}
      </div>

      {/* Tarjetas de Métricas de Infraestructura */}
      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '1rem' }}>
        <div
          style={{
            backgroundColor: '#FFFFFF',
            border: '1px solid #E2E8F0',
            borderRadius: '10px',
            padding: '1.25rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
          }}
        >
          <span style={{ fontSize: '0.8rem', color: '#64748B', display: 'block', marginBottom: '0.25rem' }}>
            Bloques / Franjas Libres Detectadas
          </span>
          <strong style={{ fontSize: '1.6rem', color: '#1C2A59' }}>{slots.length}</strong>
        </div>

        <div
          style={{
            backgroundColor: '#FFFFFF',
            border: '1px solid #E2E8F0',
            borderRadius: '10px',
            padding: '1.25rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
          }}
        >
          <span style={{ fontSize: '0.8rem', color: '#64748B', display: 'block', marginBottom: '0.25rem' }}>
            Recintos Físicos Únicos (Aulas / Labs)
          </span>
          <strong style={{ fontSize: '1.6rem', color: '#B99451' }}>{uniqueClassrooms.length}</strong>
        </div>

        <div
          style={{
            backgroundColor: '#FFFFFF',
            border: '1px solid #E2E8F0',
            borderRadius: '10px',
            padding: '1.25rem',
            boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
          }}
        >
          <span style={{ fontSize: '0.8rem', color: '#64748B', display: 'block', marginBottom: '0.25rem' }}>
            Garantía de Cero Colisiones (RN-06)
          </span>
          <strong style={{ fontSize: '1.05rem', color: '#059669', display: 'block', marginTop: '0.35rem' }}>
            PROTECCIÓN ACTIVA ✅
          </strong>
        </div>
      </div>

      {/* Tabla Interactiva de Aulas y Franjas Libres */}
      <div
        style={{
          backgroundColor: '#FFFFFF',
          borderRadius: '12px',
          border: '1px solid #E2E8F0',
          padding: '1.5rem',
          boxShadow: '0 1px 3px rgba(0,0,0,0.05)',
        }}
      >
        <div
          style={{
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            marginBottom: '1rem',
            flexWrap: 'wrap',
            gap: '1rem',
          }}
        >
          <div>
            <h3 style={{ margin: '0 0 0.25rem 0', fontSize: '1.1rem', fontWeight: 700, color: '#1E293B' }}>
              🏢 Disponibilidad de Aulas y Laboratorios Extraídos
            </h3>
            <p style={{ margin: 0, fontSize: '0.84rem', color: '#64748B' }}>
              Horarios desocupados por cátedras regulares aptos para agendamiento de mentorías formativas.
            </p>
          </div>

          {/* Filtros */}
          <div style={{ display: 'flex', gap: '0.5rem', flexWrap: 'wrap', alignItems: 'center' }}>
            <input
              type="text"
              placeholder="Buscar aula o día..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              aria-label="Buscar recinto o día"
              style={{
                padding: '0.45rem 0.75rem',
                borderRadius: '6px',
                border: '1px solid #CBD5E1',
                fontSize: '0.84rem',
              }}
            />

            {uniqueClassrooms.length > 0 && (
              <select
                value={classroomFilter}
                onChange={(e) => setClassroomFilter(e.target.value)}
                aria-label="Filtrar por aula o laboratorio"
                style={{
                  padding: '0.45rem 0.75rem',
                  borderRadius: '6px',
                  border: '1px solid #CBD5E1',
                  fontSize: '0.84rem',
                  backgroundColor: '#FFFFFF',
                  cursor: 'pointer',
                }}
              >
                <option value="ALL">Todas las Aulas ({uniqueClassrooms.length})</option>
                {uniqueClassrooms.map((a) => (
                  <option key={a} value={a}>
                    {a}
                  </option>
                ))}
              </select>
            )}

            {uniqueDays.length > 0 && (
              <select
                value={dayFilter}
                onChange={(e) => setDayFilter(e.target.value)}
                aria-label="Filtrar por día de la semana"
                style={{
                  padding: '0.45rem 0.75rem',
                  borderRadius: '6px',
                  border: '1px solid #CBD5E1',
                  fontSize: '0.84rem',
                  backgroundColor: '#FFFFFF',
                  cursor: 'pointer',
                }}
              >
                <option value="ALL">Todos los Días</option>
                {uniqueDays.map((d) => (
                  <option key={d} value={d}>
                    {d}
                  </option>
                ))}
              </select>
            )}

            <button
              type="button"
              onClick={fetchCurrentSlots}
              disabled={isLoadingSlots}
              style={{
                padding: '0.45rem 0.85rem',
                borderRadius: '6px',
                border: '1px solid #CBD5E1',
                backgroundColor: '#FFFFFF',
                fontSize: '0.84rem',
                fontWeight: 600,
                color: '#1C2A59',
                cursor: isLoadingSlots ? 'not-allowed' : 'pointer',
              }}
            >
              🔄
            </button>
          </div>
        </div>

        {/* Tabla */}
        {isLoadingSlots && (
          <div style={{ textAlign: 'center', padding: '2rem', color: '#64748B' }}>
            <p>Consultando disponibilidad de infraestructura física...</p>
          </div>
        )}

        {!isLoadingSlots && filteredSlots.length === 0 && (
          <div style={{ textAlign: 'center', padding: '2.5rem', color: '#64748B' }}>
            <p>No se encontraron ambientes disponibles bajo los criterios de filtrado seleccionados.</p>
          </div>
        )}

        {!isLoadingSlots && filteredSlots.length > 0 && (
          <div style={{ overflowX: 'auto' }}>
            <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.85rem' }}>
              <thead>
                <tr style={{ borderBottom: '2px solid #E2E8F0', textAlign: 'left', color: '#64748B' }}>
                  <th style={{ padding: '0.65rem 0.75rem' }}>Recinto / Aula</th>
                  <th style={{ padding: '0.65rem 0.75rem' }}>Día</th>
                  <th style={{ padding: '0.65rem 0.75rem' }}>Franja Horaria</th>
                  <th style={{ padding: '0.65rem 0.75rem' }}>Estado</th>
                  <th style={{ padding: '0.65rem 0.75rem' }}>Trazabilidad</th>
                </tr>
              </thead>
              <tbody>
                {filteredSlots.map((slot, idx) => (
                  <tr
                    key={`${slot.aula}-${slot.dia}-${slot.hora_inicio}-${idx}`}
                    style={{ borderBottom: '1px solid #F1F5F9' }}
                  >
                    <td style={{ padding: '0.65rem 0.75rem' }}>
                      <span
                        style={{
                          backgroundColor: '#EFF6FF',
                          color: '#1D4ED8',
                          fontWeight: 700,
                          padding: '0.2rem 0.55rem',
                          borderRadius: '4px',
                          fontSize: '0.8rem',
                        }}
                      >
                        {slot.aula}
                      </span>
                    </td>
                    <td style={{ padding: '0.65rem 0.75rem', fontWeight: 600, color: '#1E293B' }}>
                      {slot.dia}
                    </td>
                    <td style={{ padding: '0.65rem 0.75rem', color: '#334155' }}>
                      <strong>{slot.hora_inicio}</strong> a <strong>{slot.hora_fin}</strong>
                    </td>
                    <td style={{ padding: '0.65rem 0.75rem' }}>
                      <span
                        style={{
                          backgroundColor: '#DEF7EC',
                          color: '#03543F',
                          padding: '0.15rem 0.5rem',
                          borderRadius: '999px',
                          fontWeight: 700,
                          fontSize: '0.74rem',
                        }}
                      >
                        {slot.estado}
                      </span>
                    </td>
                    <td style={{ padding: '0.65rem 0.75rem', color: '#94A3B8', fontSize: '0.78rem' }}>
                      {slot.fila_origen ? `Fila Excel #${slot.fila_origen}` : slot.pagina ? `Pág. PDF #${slot.pagina}` : 'Catálogo Oficial'}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </div>
  );
};
