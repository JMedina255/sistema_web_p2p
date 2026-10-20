import { describe, it, expect } from 'vitest';
import { render, screen, fireEvent } from '@testing-library/react';
import { App } from '../App';

describe('App Component (Sprint 1 Navigation)', () => {
  it('permite alternar entre la pestaña de Acceso OTP y el Monitor de Servicios', () => {
    render(<App />);

    // Por defecto inicia en pestaña de acceso (T-02)
    expect(screen.getByText(/Acceso & OTP de Prueba \(T-02\)/i)).toBeInTheDocument();
    expect(screen.getByLabelText(/Correo Electrónico Institucional/i)).toBeInTheDocument();

    // Cambiar a Monitor de Servicios (T-01)
    const monitorTab = screen.getByRole('button', { name: /🛰️ Monitor de Servicios & BD \(T-01\)/i });
    fireEvent.click(monitorTab);

    expect(screen.getByText(/Monitor de Servicios \(Hito 2 · T-01\)/i)).toBeInTheDocument();

    // Regresar a Acceso OTP (T-02)
    const authTab = screen.getByRole('button', { name: /🔐 Acceso & OTP de Prueba \(T-02\)/i });
    fireEvent.click(authTab);

    expect(screen.getByLabelText(/Correo Electrónico Institucional/i)).toBeInTheDocument();
  });
});
