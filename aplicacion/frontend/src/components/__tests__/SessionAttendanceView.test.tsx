import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
import { render, screen, fireEvent, waitFor, act } from '@testing-library/react';
import { SessionAttendanceView } from '../SessionAttendanceView';
import { attendanceService } from '../../services/attendanceService';

describe('SessionAttendanceView Component (T-34 / RF17 / CUS12 / RN-05 / RN-12)', () => {
  const sessionId = 101;

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.useRealTimers();
  });

  // 1. Genera y proyecta código QR dinámico con token TOTP
  it('1. Genera y proyecta código QR dinámico con token TOTP', async () => {
    vi.spyOn(attendanceService, 'getDynamicQrToken').mockResolvedValue({
      session_id: sessionId,
      token: 'jwt-totp-dynamic-token-12345',
      totp_code: '458921',
      expires_in: 30,
      expires_at: new Date(Date.now() + 30000).toISOString(),
    });
    vi.spyOn(attendanceService, 'getAttendanceList').mockResolvedValue([]);

    render(<SessionAttendanceView sessionId={sessionId} sessionTitle="Cálculo I - Sesión 101" />);

    await waitFor(() => {
      expect(screen.getByTestId('qr-code-display')).toBeInTheDocument();
      expect(screen.getByText('458921')).toBeInTheDocument();
      expect(screen.getByText(/30s restantes/i)).toBeInTheDocument();
    });
  });

  // 2. Temporizador regresivo refresca el token automáticamente cada 30s
  it('2. Temporizador regresivo refresca el token automáticamente cada 30s', async () => {
    vi.useFakeTimers();

    const getQrSpy = vi.spyOn(attendanceService, 'getDynamicQrToken').mockResolvedValue({
      session_id: sessionId,
      token: 'token-cycle-1',
      totp_code: '111111',
      expires_in: 30,
      expires_at: new Date(Date.now() + 30000).toISOString(),
    });
    vi.spyOn(attendanceService, 'getAttendanceList').mockResolvedValue([]);

    render(<SessionAttendanceView sessionId={sessionId} />);

    // Esperar primera carga
    await act(async () => {
      await Promise.resolve();
    });
    expect(getQrSpy).toHaveBeenCalledTimes(1);

    // Avanzar reloj 30 segundos
    getQrSpy.mockResolvedValueOnce({
      session_id: sessionId,
      token: 'token-cycle-2',
      totp_code: '222222',
      expires_in: 30,
      expires_at: new Date(Date.now() + 30000).toISOString(),
    });

    await act(async () => {
      vi.advanceTimersByTime(30000);
      await Promise.resolve();
    });

    expect(getQrSpy).toHaveBeenCalledTimes(2);
  });

  // 3. Permite ingreso alternativo por código numérico de 6 dígitos
  it('3. Permite ingreso alternativo por código numérico de 6 dígitos', async () => {
    vi.spyOn(attendanceService, 'getDynamicQrToken').mockResolvedValue({
      session_id: sessionId,
      token: 'token-qr',
      totp_code: '654321',
      expires_in: 30,
      expires_at: new Date(Date.now() + 30000).toISOString(),
    });
    vi.spyOn(attendanceService, 'getAttendanceList').mockResolvedValue([]);
    const checkinSpy = vi.spyOn(attendanceService, 'checkIn').mockResolvedValue({
      id_asistencia: 1,
      id_sesion: sessionId,
      estudiante_email: '2024071111@upt.pe',
      asistio: true,
      fecha_checkin: new Date().toISOString(),
      mensaje: '¡Asistencia registrada exitosamente! Gracias por tu puntualidad.',
    });

    render(<SessionAttendanceView sessionId={sessionId} />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/Ej. 123456/i)).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText(/Ej. 123456/i);
    fireEvent.change(input, { target: { value: '654321' } });

    const submitBtn = screen.getByRole('button', { name: /Registrar Asistencia/i });
    expect(submitBtn).not.toBeDisabled();
    fireEvent.submit(submitBtn.closest('form')!);

    await waitFor(() => {
      expect(checkinSpy).toHaveBeenCalledWith(sessionId, expect.objectContaining({
        numeric_code: '654321',
      }));
      expect(screen.getByText(/¡Asistencia registrada exitosamente!/i)).toBeInTheDocument();
    });
  });

  // 4. Actualiza reactivamente la lista de alumnos presentes con badge verde
  it('4. Actualiza reactivamente la lista de alumnos presentes con badge verde', async () => {
    vi.spyOn(attendanceService, 'getDynamicQrToken').mockResolvedValue({
      session_id: sessionId,
      token: 'token-qr',
      totp_code: '888888',
      expires_in: 30,
      expires_at: new Date().toISOString(),
    });

    const getRosterSpy = vi.spyOn(attendanceService, 'getAttendanceList')
      .mockResolvedValueOnce([
        {
          id_asistencia: 1,
          id_sesion: sessionId,
          estudiante_email: '2024072222@upt.pe',
          asistio: false,
          fecha_checkin: null,
        },
      ])
      .mockResolvedValueOnce([
        {
          id_asistencia: 1,
          id_sesion: sessionId,
          estudiante_email: '2024072222@upt.pe',
          asistio: true,
          fecha_checkin: new Date().toISOString(),
        },
      ]);

    render(<SessionAttendanceView sessionId={sessionId} />);

    await waitFor(() => {
      expect(screen.getByText('2024072222@upt.pe')).toBeInTheDocument();
      expect(screen.getByText('Ausente')).toBeInTheDocument();
    });

    // Actualizar nómina pulsando Actualizar
    const refreshBtn = screen.getByRole('button', { name: /🔄 Actualizar/i });
    fireEvent.click(refreshBtn);

    await waitFor(() => {
      expect(getRosterSpy).toHaveBeenCalledTimes(2);
      expect(screen.getByText('Presente')).toBeInTheDocument();
    });
  });

  // 5. Rechaza escaneo fuera del horario de la sesión con mensaje accesible
  it('5. Rechaza escaneo fuera del horario de la sesión con mensaje accesible', async () => {
    vi.spyOn(attendanceService, 'getDynamicQrToken').mockResolvedValue({
      session_id: sessionId,
      token: 'token-qr',
      totp_code: '999999',
      expires_in: 30,
      expires_at: new Date().toISOString(),
    });
    vi.spyOn(attendanceService, 'getAttendanceList').mockResolvedValue([]);
    vi.spyOn(attendanceService, 'checkIn').mockRejectedValue(
      new Error('WINDOW_CLOSED: El pase de asistencia solo está habilitado entre 15 min antes y 30 min después de la sesión.')
    );

    render(<SessionAttendanceView sessionId={sessionId} />);

    await waitFor(() => {
      expect(screen.getByPlaceholderText(/Ej. 123456/i)).toBeInTheDocument();
    });

    const input = screen.getByPlaceholderText(/Ej. 123456/i);
    fireEvent.change(input, { target: { value: '999999' } });

    const submitBtn = screen.getByRole('button', { name: /Registrar Asistencia/i });
    fireEvent.submit(submitBtn.closest('form')!);

    await waitFor(() => {
      expect(screen.getByText(/WINDOW_CLOSED: El pase de asistencia solo está habilitado/i)).toBeInTheDocument();
    });
  });
});
