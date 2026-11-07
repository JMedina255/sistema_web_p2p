import { describe, it, expect, vi, beforeEach } from 'vitest';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import { BitacoraFormView } from '../BitacoraFormView';
import { bitacoraService } from '../../services/bitacoraService';

describe('BitacoraFormView Component (T-34 / RF17 / CUS13 / RN-12 / RNF05)', () => {
  const sessionId = 101;

  beforeEach(() => {
    vi.restoreAllMocks();
  });

  // 1. Bloquea formulario con alerta roja si pasaron > 48h del fin
  it('1. Bloquea formulario con alerta roja si pasaron > 48h del fin (RN-12)', () => {
    // Sesión finalizada hace 50 horas (> 48h)
    const sessionEndDate = new Date(Date.now() - 50 * 3600 * 1000).toISOString();

    render(
      <BitacoraFormView
        sessionId={sessionId}
        sessionEndDate={sessionEndDate}
      />
    );

    expect(screen.getByTestId('deadline-expired-alert')).toBeInTheDocument();
    expect(
      screen.getByText(/Formulario Bloqueado: Plazo Ordinario de 48 Horas Expirado/i)
    ).toBeInTheDocument();

    const submitBtn = screen.getByRole('button', { name: /Firmar y Registrar Bitácora/i });
    expect(submitBtn).toBeDisabled();
  });

  // 2. Habilita checklist de temas curriculares de la materia
  it('2. Habilita checklist de temas curriculares de la materia', () => {
    const customTopics = [
      'Límites algebraicos',
      'Asíntotas oblicuas',
      'Teorema del emparedado',
    ];

    render(
      <BitacoraFormView
        sessionId={sessionId}
        syllabusTopics={customTopics}
      />
    );

    customTopics.forEach((topic) => {
      const checkbox = screen.getByLabelText(topic);
      expect(checkbox).toBeInTheDocument();
      expect(checkbox).not.toBeChecked();

      // Al marcarlo cambia de estado
      fireEvent.click(checkbox);
      expect(checkbox).toBeChecked();
    });
  });

  // 3. Invalida envío si observaciones pedagógicas tienen < 50 caracteres
  it('3. Invalida envío si observaciones pedagógicas tienen < 50 caracteres (RN-12)', async () => {
    const submitSpy = vi.spyOn(bitacoraService, 'submitBitacora');

    render(<BitacoraFormView sessionId={sessionId} />);

    // Marcar un tema
    const checkbox = screen.getByLabelText('Límites algebraicos e indeterminaciones');
    fireEvent.click(checkbox);

    // Escribir solo 20 caracteres en observaciones
    const textarea = screen.getByRole('textbox', { name: /3\. Observaciones Pedagógicas y Conclusiones:/i });
    fireEvent.change(textarea, { target: { value: 'Texto corto de prueba' } });

    // Marcar declaración jurada
    const swornCheckbox = screen.getByLabelText(/Declaración Jurada de Veracidad Académica/i);
    fireEvent.click(swornCheckbox);

    // Intentar enviar
    const submitBtn = screen.getByRole('button', { name: /Firmar y Registrar Bitácora/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(
        screen.getByText(/Las observaciones pedagógicas deben poseer al menos 50 caracteres/i)
      ).toBeInTheDocument();
      expect(submitSpy).not.toHaveBeenCalled();
    });
  });

  // 4. Exige marcar la declaración jurada de veracidad académica
  it('4. Exige marcar la declaración jurada de veracidad académica', async () => {
    const submitSpy = vi.spyOn(bitacoraService, 'submitBitacora');

    render(<BitacoraFormView sessionId={sessionId} />);

    // Marcar un tema
    const checkbox = screen.getByLabelText('Límites algebraicos e indeterminaciones');
    fireEvent.click(checkbox);

    // Escribir observaciones válidas (>= 50 caracteres)
    const textarea = screen.getByRole('textbox', { name: /3\. Observaciones Pedagógicas y Conclusiones:/i });
    fireEvent.change(textarea, {
      target: {
        value: 'Se resolvieron 6 ejercicios de indeterminaciones 0/0 con excelente participación grupal.',
      },
    });

    // Sin marcar declaración jurada
    const submitBtn = screen.getByRole('button', { name: /Firmar y Registrar Bitácora/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(
        screen.getByText(/Debe suscribir la declaración jurada de veracidad académica/i)
      ).toBeInTheDocument();
      expect(submitSpy).not.toHaveBeenCalled();
    });
  });

  // 5. Envía payload estructurado y muestra código de firma digital SHA-256
  it('5. Envía payload estructurado y muestra código de firma digital SHA-256', async () => {
    const mockHash = 'e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855';
    const submitSpy = vi.spyOn(bitacoraService, 'submitBitacora').mockResolvedValue({
      id_bitacora: 1,
      id_sesion: sessionId,
      id_mentor: 'mentor@upt.pe',
      temas_cubiertos: ['Límites algebraicos e indeterminaciones'],
      observaciones: 'Se resolvieron 6 ejercicios de indeterminaciones 0/0 con excelente participación grupal y compromiso formativo.',
      nivel_dificultad: 'Medio',
      hash_firma: mockHash,
      horas_declaradas: 1.0,
      visado_administrador: false,
      created_at: new Date().toISOString(),
      mensaje: 'Bitácora pedagógica registrada y sellada criptográficamente con éxito.',
    });

    const onSuccess = vi.fn();

    render(
      <BitacoraFormView
        sessionId={sessionId}
        onSuccess={onSuccess}
      />
    );

    // 1. Marcar tema
    const checkbox = screen.getByLabelText('Límites algebraicos e indeterminaciones');
    fireEvent.click(checkbox);

    // 2. Observaciones >= 50 caracteres
    const textarea = screen.getByRole('textbox', { name: /3\. Observaciones Pedagógicas y Conclusiones:/i });
    fireEvent.change(textarea, {
      target: {
        value: 'Se resolvieron 6 ejercicios de indeterminaciones 0/0 con excelente participación grupal y compromiso formativo.',
      },
    });

    // 3. Declaración jurada
    const swornCheckbox = screen.getByLabelText(/Declaración Jurada de Veracidad Académica/i);
    fireEvent.click(swornCheckbox);

    // 4. Enviar
    const submitBtn = screen.getByRole('button', { name: /Firmar y Registrar Bitácora/i });
    fireEvent.click(submitBtn);

    await waitFor(() => {
      expect(submitSpy).toHaveBeenCalledWith(sessionId, {
        temas_cubiertos: ['Límites algebraicos e indeterminaciones'],
        observaciones: 'Se resolvieron 6 ejercicios de indeterminaciones 0/0 con excelente participación grupal y compromiso formativo.',
        nivel_dificultad: 'Medio',
      });
      expect(screen.getByTestId('bitacora-success-card')).toBeInTheDocument();
      expect(screen.getByText(mockHash)).toBeInTheDocument();
      expect(onSuccess).toHaveBeenCalledWith(mockHash);
    });
  });
});
