import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { ConsentModalView } from '../ConsentModalView';
import { consentService } from '../../services/consentService';

describe('ConsentModalView Component (T-04 / RF02 / RN-02)', () => {
  const testEmail = '2022074255@upt.pe';

  beforeEach(async () => {
    consentService.setMode('mock');
    await consentService.revokeConsent(testEmail);
  });

  it('1. Renderiza el encabezado institucional y el texto de la Ley N° 29733', async () => {
    render(<ConsentModalView userEmail={testEmail} />);

    await waitFor(() => {
      expect(screen.getByRole('heading', { name: /Consentimiento Informado Digital/i })).toBeInTheDocument();
      expect(screen.getAllByText(/Ley N° 29733/i).length).toBeGreaterThanOrEqual(1);
      expect(screen.getByText(/POLÍTICA DE PRIVACIDAD Y TRATAMIENTO DE DATOS PERSONALES/i)).toBeInTheDocument();
    });
  });

  it('2. El botón de aceptar permanece deshabilitado hasta marcar la casilla de conformidad', async () => {
    render(<ConsentModalView userEmail={testEmail} />);

    const acceptButton = await screen.findByRole('button', { name: /Aceptar y Continuar/i });
    expect(acceptButton).toBeDisabled();

    const checkbox = screen.getByRole('checkbox');
    expect(checkbox).not.toBeChecked();

    fireEvent.click(checkbox);
    expect(checkbox).toBeChecked();
    expect(acceptButton).not.toBeDisabled();
  });

  it('3. Permite aceptar el consentimiento y ejecuta el callback onConsentAccepted', async () => {
    const onAcceptedMock = vi.fn();
    render(<ConsentModalView userEmail={testEmail} onConsentAccepted={onAcceptedMock} />);

    const acceptButton = await screen.findByRole('button', { name: /Aceptar y Continuar/i });
    const checkbox = screen.getByRole('checkbox');

    fireEvent.click(checkbox);
    await waitFor(() => {
      expect(acceptButton).not.toBeDisabled();
    });

    fireEvent.click(acceptButton);

    await waitFor(() => {
      expect(onAcceptedMock).toHaveBeenCalled();
      expect(screen.getByText(/Consentimiento registrado exitosamente/i)).toBeInTheDocument();
    });
  });

  it('4. Permite rechazar el consentimiento y ejecuta el callback onConsentRejected (bloqueo preventivo RN-02)', async () => {
    const onRejectedMock = vi.fn();
    render(<ConsentModalView userEmail={testEmail} onConsentRejected={onRejectedMock} />);

    const rejectButton = await screen.findByRole('button', { name: /Rechazar y Salir/i });
    await waitFor(() => {
      expect(rejectButton).not.toBeDisabled();
    });

    fireEvent.click(rejectButton);

    await waitFor(() => {
      expect(onRejectedMock).toHaveBeenCalled();
      expect(screen.getByText(/Has rechazado el tratamiento de datos/i)).toBeInTheDocument();
    });
  });
});
