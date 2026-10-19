import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
import { render, screen, fireEvent, act } from '@testing-library/react';
import { LoginOtpView } from '../LoginOtpView';
import { authService } from '../../services/authService';

describe('LoginOtpView Component (T-02 / CUS01 / RF01 / RNF01)', () => {
  beforeEach(() => {
    vi.useFakeTimers();
    authService.cancelChallenge();
  });

  afterEach(() => {
    vi.useRealTimers();
    authService.cancelChallenge();
  });

  it('1. Renderiza el paso 1 con advertencia de modo simulación y campo de correo', () => {
    render(<LoginOtpView />);

    expect(screen.getByText(/Acceso de prueba — Simulación/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Correo Electrónico Institucional/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Continuar con Código OTP/i })).toBeInTheDocument();
  });

  it('2. Valida correo con dominio externo (@gmail.com) y muestra error', async () => {
    render(<LoginOtpView />);

    const emailInput = screen.getByLabelText(/Correo Electrónico Institucional/i);
    fireEvent.change(emailInput, { target: { value: 'estudiante@gmail.com' } });

    const submitBtn = screen.getByRole('button', { name: /Continuar con Código OTP/i });
    fireEvent.click(submitBtn);

    expect(screen.getByRole('alert')).toHaveTextContent(/Solo se permiten correos institucionales con dominio @upt\.pe/i);
  });

  it('3. Los atajos de prueba rápida precargan los correos seleccionados', () => {
    render(<LoginOtpView />);

    const joanBtn = screen.getByRole('button', { name: /Joan \(2022074255@upt\.pe\)/i });
    fireEvent.click(joanBtn);

    const emailInput = screen.getByLabelText(/Correo Electrónico Institucional/i) as HTMLInputElement;
    expect(emailInput.value).toBe('2022074255@upt.pe');
  });

  it('4. Flujo completo: Solicitar OTP, ingresar código válido (123456) y ver confirmación', async () => {
    render(<LoginOtpView />);

    const emailInput = screen.getByLabelText(/Correo Electrónico Institucional/i);
    fireEvent.change(emailInput, { target: { value: '2022074255@upt.pe' } });

    const submitBtn = screen.getByRole('button', { name: /Continuar con Código OTP/i });
    fireEvent.click(submitBtn);

    // Avanzar timer de latencia de red simulada (250ms)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    // Debe transicionar al paso 2
    expect(screen.getByLabelText(/Código de 6 dígitos/i)).toBeInTheDocument();
    expect(screen.getByText('Destino de verificación:')).toBeInTheDocument();
    expect(screen.getAllByText(/2022074255@upt\.pe/i).length).toBeGreaterThanOrEqual(1);

    // Ingresar código de prueba 123456
    const otpInput = screen.getByLabelText(/Código de 6 dígitos/i);
    fireEvent.change(otpInput, { target: { value: '123456' } });

    const verifyBtn = screen.getByRole('button', { name: /Verificar y Acceder/i });
    fireEvent.click(verifyBtn);

    // Avanzar timer de latencia de verificación
    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    // Transiciona a pantalla de confirmación (Paso 3)
    expect(screen.getByText(/Código OTP Verificado con Éxito/i)).toBeInTheDocument();
    expect(screen.getByText(/Acceso de prueba — Simulación \(T-02\)/i)).toBeInTheDocument();
    expect(screen.getByRole('button', { name: /Probar Otro Acceso \/ Reiniciar/i })).toBeInTheDocument();
  });

  it('5. Muestra error con OTP incorrecto', async () => {
    render(<LoginOtpView />);

    const emailInput = screen.getByLabelText(/Correo Electrónico Institucional/i);
    fireEvent.change(emailInput, { target: { value: '2022073504@upt.pe' } });
    fireEvent.click(screen.getByRole('button', { name: /Continuar con Código OTP/i }));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    const otpInput = screen.getByLabelText(/Código de 6 dígitos/i);
    fireEvent.change(otpInput, { target: { value: '999999' } });

    const verifyBtn = screen.getByRole('button', { name: /Verificar y Acceder/i });
    fireEvent.click(verifyBtn);

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByRole('alert')).toHaveTextContent(/Código OTP incorrecto/i);
  });

  it('6. El botón "Cambiar correo" cancela el desafío y regresa al Paso 1', async () => {
    render(<LoginOtpView />);

    const emailInput = screen.getByLabelText(/Correo Electrónico Institucional/i);
    fireEvent.change(emailInput, { target: { value: '2022074255@upt.pe' } });
    fireEvent.click(screen.getByRole('button', { name: /Continuar con Código OTP/i }));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByLabelText(/Código de 6 dígitos/i)).toBeInTheDocument();

    const changeEmailBtn = screen.getByRole('button', { name: /Cambiar correo/i });
    fireEvent.click(changeEmailBtn);

    // Regresa al Paso 1
    expect(screen.getByLabelText(/Correo Electrónico Institucional/i)).toBeInTheDocument();
    expect(screen.queryByLabelText(/Código de 6 dígitos/i)).not.toBeInTheDocument();
  });

  it('7. Conserva ceros a la izquierda en el campo OTP (formato string)', async () => {
    render(<LoginOtpView />);

    const emailInput = screen.getByLabelText(/Correo Electrónico Institucional/i);
    fireEvent.change(emailInput, { target: { value: '2022074255@upt.pe' } });
    fireEvent.click(screen.getByRole('button', { name: /Continuar con Código OTP/i }));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    const otpInput = screen.getByLabelText(/Código de 6 dígitos/i) as HTMLInputElement;
    fireEvent.change(otpInput, { target: { value: '012345' } });

    expect(otpInput.value).toBe('012345');
  });

  it('8. Botón "Probar Otro Acceso / Reiniciar" restablece el estado para nuevas pruebas', async () => {
    render(<LoginOtpView />);

    // Completar flujo hasta el final
    fireEvent.change(screen.getByLabelText(/Correo Electrónico Institucional/i), {
      target: { value: '2022074255@upt.pe' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Continuar con Código OTP/i }));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    const otpInput = screen.getByLabelText(/Código de 6 dígitos/i);
    fireEvent.change(otpInput, { target: { value: '123456' } });
    fireEvent.click(screen.getByRole('button', { name: /Verificar y Acceder/i }));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    const restartBtn = screen.getByRole('button', { name: /Probar Otro Acceso \/ Reiniciar/i });
    fireEvent.click(restartBtn);

    // Debe estar en paso 1 nuevamente
    expect(screen.getByLabelText(/Correo Electrónico Institucional/i)).toBeInTheDocument();
  });

  it('9. Cooldown de reenvío: botón deshabilitado inicialmente y habilitado tras 60s', async () => {
    render(<LoginOtpView />);

    fireEvent.change(screen.getByLabelText(/Correo Electrónico Institucional/i), {
      target: { value: '2022074255@upt.pe' },
    });
    fireEvent.click(screen.getByRole('button', { name: /Continuar con Código OTP/i }));

    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    // Iniciar intervalo de actualización (500ms)
    await act(async () => {
      await vi.advanceTimersByTimeAsync(500);
    });

    // Inicialmente en cooldown
    const resendBtn = screen.getByRole('button', { name: /Reenviar código en/i });
    expect(resendBtn).toBeDisabled();

    // Avanzar reloj 61 segundos
    await act(async () => {
      await vi.advanceTimersByTimeAsync(61 * 1000);
    });

    // Ahora habilitado con texto "Reenviar nuevo código"
    const readyResendBtn = screen.getByRole('button', { name: /Reenviar nuevo código/i });
    expect(readyResendBtn).not.toBeDisabled();

    // Clic en reenvío
    fireEvent.click(readyResendBtn);
    await act(async () => {
      await vi.advanceTimersByTimeAsync(300);
    });

    expect(screen.getByRole('status')).toHaveTextContent(/Se ha generado y enviado un nuevo código OTP/i);
  });
});
