/**
 * Prueba de Integración End-to-End de Cierre de Sesión y Ciclo de Vida Pedagógico (T-37)
 *
 * Flujo Completo:
 * 1. Publicación de Oferta de Mentoría (T-14 / RF08)
 * 2. Formalización de Reserva y Cupo (T-21 / RF12)
 * 3. Ratificación de Asistencia en Ventana T-48h (T-27 / RF13 / RN-08)
 * 4. Evaluación de Quórum y Contingencia en T-24h (T-29 / T-33 / RF15 / RF16)
 * 5. Check-in de Asistencia Digital con QR TOTP (T-34 / T-36 / RF17)
 * 6. Registro y Sellado de Bitácora Pedagógica SHA-256 (T-34 / T-35 / RN-12)
 * 7. Navegación e Integración UI de MentorSessionsView -> Attendance -> Bitacora (T-32 / T-34)
 */

import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { offerService } from '../services/offerService';
import { bookingService } from '../services/bookingService';
import { attendanceService } from '../services/attendanceService';
import { bitacoraService } from '../services/bitacoraService';
import { MentorSessionsView } from '../components/MentorSessionsView';

describe('SessionClosureIntegration (T-37 / Lifecycle End-to-End)', () => {
  const mentorEmail = 'mentor.cierre@upt.pe';
  const menteeEmail = '2024073333@upt.pe';

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  it('1. Pipeline real de servicios: ejecuta el ciclo completo hasta la persistencia y sellado de la bitácora', async () => {
    const futureStartTime = new Date(Date.now() + 30 * 3600 * 1000).toISOString();

    // 1. Publicar Oferta con mockAdapter real
    const publishedSession = await offerService.publishOffer({
      id_asignatura: 1,
      codigo_asignatura: 'CALC-101',
      nombre_asignatura: 'Cálculo I',
      id_tema: 1,
      nombre_tema: 'Integrales Definidas',
      fecha_inicio: futureStartTime,
      duracion_minutos: 60,
      modalidad: 'presencial',
      aforo_maximo: 10,
      espacio_asignado: 'Lab 105',
      mentor_email: mentorEmail,
    });

    expect(publishedSession.codigo_sesion).toBeDefined();
    expect(publishedSession.estado).toBe('PUBLICADA');

    // 2. Reserva de plaza por mentoreado
    const sessionIdNum = parseInt(publishedSession.id_oferta, 10) || 501;
    const booking = await bookingService.reserveSeat({
      id_sesion: sessionIdNum,
      estudiante_email: menteeEmail,
    });
    expect(booking.estado).toBe('PENDIENTE_CONFIRMACION');
    expect(booking.id_reserva).toBeDefined();

    // 3. Ratificación de asistencia en ventana T-48h
    const confirmedBooking = await bookingService.confirmAttendance(booking.id_reserva);
    expect(confirmedBooking.estado).toBe('CONFIRMADA');

    // 4. Resolución de Quórum ante contingencia
    const quorumResult = await offerService.resolveQuorum(publishedSession.id_oferta, {
      decision: 'PROCEED',
    });
    expect(quorumResult.estado_nuevo).toBe('CONFIRMADA');

    // 5. Generación de QR dinámico y Check-in digital
    const tokenData = await attendanceService.getDynamicQrToken(sessionIdNum);
    expect(tokenData.totp_code).toHaveLength(6);
    expect(tokenData.expires_in).toBe(30);

    const checkin = await attendanceService.checkIn(sessionIdNum, {
      numeric_code: tokenData.totp_code,
      estudiante_email: menteeEmail,
    });
    expect(checkin.asistio).toBe(true);

    const roster = await attendanceService.getAttendanceList(sessionIdNum);
    expect(roster.length).toBeGreaterThan(0);
    const menteeRow = roster.find((r) => r.estudiante_email === menteeEmail);
    expect(menteeRow?.asistio).toBe(true);

    // 6. Registro y sellado de bitácora pedagógica SHA-256
    const bitacora = await bitacoraService.submitBitacora(sessionIdNum, {
      temas_cubiertos: ['Integrales Definidas', 'Método de sustitución'],
      observaciones: 'Se desarrollaron ejercicios de aplicación con excelente participación y comprensión de los estudiantes.',
      nivel_dificultad: 'Medio',
    });

    expect(bitacora.id_bitacora).toBe(sessionIdNum);
    expect(bitacora.hash_firma).toBeDefined();
    expect(bitacora.horas_declaradas).toBe(1.0);

    // 7. Verificación de consulta de bitácora sellada
    const retrieved = await bitacoraService.getBitacora(sessionIdNum);
    expect(retrieved.hash_firma).toBe(bitacora.hash_firma);
    expect(retrieved.temas_cubiertos).toContain('Integrales Definidas');
  });

  it('2. Flujo UI Integrado: transiciona desde MentorSessionsView hacia Asistencia y Bitácora y retorna fluidamente', async () => {
    // Configurar sesiones del mentor con una sesión con quórum insuficiente y otra confirmada
    vi.spyOn(offerService, 'getOffers').mockResolvedValue([
      {
        id_oferta: '701',
        codigo_sesion: 'SES-701',
        estado: 'CONFIRMADA',
        mensaje: 'Sesión confirmada',
        fecha_publicacion: new Date().toISOString(),
        espacio_asignado: 'Lab 201',
        modo: 'mock',
        aforo: 10,
        offer: {
          id_asignatura: 1,
          codigo_asignatura: 'CALC-101',
          nombre_asignatura: 'Cálculo I',
          id_tema: 1,
          nombre_tema: 'Límites Notables',
          fecha_inicio: new Date(Date.now() - 3600 * 1000).toISOString(),
          duracion_minutos: 60,
          modalidad: 'presencial',
          aforo_maximo: 10,
          espacio_asignado: 'Lab 201',
          mentor_email: mentorEmail,
        },
      },
    ]);

    render(<MentorSessionsView mentorEmail={mentorEmail} />);

    // Esperar a que cargue la lista de sesiones
    await waitFor(() => {
      expect(screen.getByText('SES-701')).toBeInTheDocument();
      expect(screen.getByText('Cálculo I')).toBeInTheDocument();
    });

    // 1. Abrir vista de Asistencia Digital
    const attendanceBtn = screen.getByRole('button', { name: /📱 Asistencia/i });
    fireEvent.click(attendanceBtn);

    // Debe renderizar SessionAttendanceView con QR y botón de retorno
    await waitFor(() => {
      expect(screen.getByText(/Control de Asistencia Digital/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /← Volver a Mis Sesiones/i })).toBeInTheDocument();
      expect(screen.getByTestId('qr-code-display')).toBeInTheDocument();
    });

    // Retornar a Mis Sesiones
    const backFromAttBtn = screen.getByRole('button', { name: /← Volver a Mis Sesiones/i });
    fireEvent.click(backFromAttBtn);

    // Debe volver al panel del mentor
    await waitFor(() => {
      expect(screen.getByText('SES-701')).toBeInTheDocument();
    });

    // 2. Abrir vista de Bitácora Pedagógica
    const bitacoraBtn = screen.getByRole('button', { name: /📝 Bitácora/i });
    fireEvent.click(bitacoraBtn);

    // Debe renderizar BitacoraFormView
    await waitFor(() => {
      expect(screen.getByText(/Bitácora Pedagógica de Mentoría/i)).toBeInTheDocument();
      expect(screen.getByRole('button', { name: /← Volver a Mis Sesiones/i })).toBeInTheDocument();
    });

    // Retornar al panel del mentor
    const backFromBitBtn = screen.getByRole('button', { name: /← Volver a Mis Sesiones/i });
    fireEvent.click(backFromBitBtn);

    await waitFor(() => {
      expect(screen.getByText('SES-701')).toBeInTheDocument();
    });
  });
});
