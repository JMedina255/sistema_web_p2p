import { describe, it, expect, beforeEach, vi } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { CertificateDownloadView } from '../CertificateDownloadView';
import { certificateService } from '../../services/certificateService';

describe('CertificateDownloadView Component (T-43 / RF22 / RF23 / RN-14 / WCAG 2.1 AA)', () => {
  beforeEach(() => {
    vi.restoreAllMocks();
    certificateService.setMode('mock');
    certificateService.resetMockState();
  });

  it('1. Renderiza la barra de progreso formativo y bloquea la emisión si horas < 20 (RN-14)', async () => {
    certificateService.setMockHours('mentor.test1@upt.pe', 16.0, 4.0);

    render(<CertificateDownloadView mentorEmail="mentor.test1@upt.pe" />);

    await waitFor(() => {
      expect(screen.getByRole('progressbar')).toBeInTheDocument();
    });

    const progressbar = screen.getByRole('progressbar');
    expect(progressbar).toHaveAttribute('aria-valuenow', '16');
    expect(progressbar).toHaveAttribute('aria-valuemin', '0');
    expect(progressbar).toHaveAttribute('aria-valuemax', '20');

    expect(screen.getByText(/16.0 \/ 20.0 horas/)).toBeInTheDocument();
    expect(screen.getByText(/\(80%\)/)).toBeInTheDocument();

    const emitBtn = screen.getByRole('button', { name: /Emitir Constancia/i });
    expect(emitBtn).toBeDisabled();
  });

  it('2. Despliega aviso pedagógico accesible indicando las horas visadas faltantes', async () => {
    certificateService.setMockHours('mentor.test2@upt.pe', 14.0, 2.0);

    render(<CertificateDownloadView mentorEmail="mentor.test2@upt.pe" />);

    await waitFor(() => {
      expect(screen.getByText(/Aviso Pedagógico RN-14:/i)).toBeInTheDocument();
    });

    expect(screen.getByText(/Te faltan 6.0 horas visadas para solicitar tu constancia oficial/i)).toBeInTheDocument();
  });

  it('3. Habilita el botón de emisión al alcanzar >= 20.0 horas visadas y ejecuta la emisión', async () => {
    certificateService.setMockHours('mentor.test3@upt.pe', 22.0, 0.0);
    const downloadSpy = vi.spyOn(certificateService, 'downloadPdf');

    render(<CertificateDownloadView mentorEmail="mentor.test3@upt.pe" />);

    await waitFor(() => {
      expect(screen.getByText(/22.0 \/ 20.0 horas/)).toBeInTheDocument();
    });

    const emitBtn = screen.getByRole('button', { name: /Emitir Constancia Oficial/i });
    expect(emitBtn).not.toBeDisabled();

    fireEvent.click(emitBtn);

    await waitFor(() => {
      expect(screen.getByText(/¡Constancia oficial emitida exitosamente!/i)).toBeInTheDocument();
    });

    expect(downloadSpy).toHaveBeenCalled();
    expect(screen.getByText(/Folio:/i)).toBeInTheDocument();
  });

  it('4. Despliega metadatos institucionales y botón de descarga directa para constancias emitidas', async () => {
    certificateService.setMockHours('mentor.test4@upt.pe', 20.0, 0.0);
    await certificateService.generateCertificate({ mentorEmail: 'mentor.test4@upt.pe' });
    const downloadSpy = vi.spyOn(certificateService, 'downloadPdf');

    render(<CertificateDownloadView mentorEmail="mentor.test4@upt.pe" />);

    await waitFor(() => {
      expect(screen.getByText(/CONSTANCIA EMITIDA • EMITIDO_DEMO/i)).toBeInTheDocument();
    });

    expect(screen.getByText(/Folio: CERT-2026-II-/i)).toBeInTheDocument();
    expect(screen.getByText(/DEMO - FINES ACADÉMICOS/i)).toBeInTheDocument();

    const downloadBtn = screen.getByRole('button', { name: /Descargar Constancia en PDF/i });
    expect(downloadBtn).toBeInTheDocument();

    fireEvent.click(downloadBtn);

    await waitFor(() => {
      expect(downloadSpy).toHaveBeenCalled();
    });
  });

  it('5. Abre el diálogo de verificación QR y responde a la tecla Escape (WCAG 2.1 AA)', async () => {
    certificateService.setMockHours('mentor.test5@upt.pe', 20.0, 0.0);
    await certificateService.generateCertificate({ mentorEmail: 'mentor.test5@upt.pe' });

    render(<CertificateDownloadView mentorEmail="mentor.test5@upt.pe" />);

    await waitFor(() => {
      expect(screen.getByRole('button', { name: /Verificar QR/i })).toBeInTheDocument();
    });

    const verifyBtn = screen.getByRole('button', { name: /Verificar QR/i });
    fireEvent.click(verifyBtn);

    await waitFor(() => {
      expect(screen.getByRole('dialog')).toBeInTheDocument();
    });

    expect(screen.getByText(/Verificación de Autenticidad Institucional/i)).toBeInTheDocument();

    // Presionar tecla Escape para cerrar
    fireEvent.keyDown(window, { key: 'Escape' });

    await waitFor(() => {
      expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
    });
  });
});
