import { expect, it } from 'vitest';
import { hoursAvailable, toggleHour, overlapsHour } from '../availabilityIntervals';

it('cuenta la unión y divide un intervalo al quitar una celda', () => {
  const slots = [{ dia_semana: 1, hora_inicio: '08:00', hora_fin: '10:30' },
    { dia_semana: 1, hora_inicio: '09:30', hora_fin: '11:00' }];
  expect(hoursAvailable(slots)).toBe(3);
  expect(overlapsHour(slots, 1, '09:00', '10:00')).toBe(true);
  const edited = toggleHour(slots, 1, '09:00', '10:00');
  expect(edited).toEqual([{ dia_semana: 1, hora_inicio: '08:00', hora_fin: '09:00' },
    { dia_semana: 1, hora_inicio: '10:00', hora_fin: '11:00' }]);
  expect(hoursAvailable(toggleHour(edited, 1, '09:00', '10:00'))).toBe(3);
  expect(hoursAvailable([{ dia_semana: 2, hora_inicio: '08:30', hora_fin: '09:00' }])).toBe(0.5);
});
