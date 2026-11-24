import { describe, expect, it } from 'vitest';
import { formatMentoringTime } from '../mentoringTime';

describe('Horario de mentoría en Lima', () => {
  it('muestra el mismo día y hora para ISO UTC y para el desfase de Lima', () => {
    const time = formatMentoringTime('2026-11-28T00:30:00Z');
    expect(time).toBe(formatMentoringTime('2026-11-27T19:30:00-05:00'));
    expect(time).toMatch(/27.*19:30.*Lima/);
  });
});
