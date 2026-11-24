import type { AvailabilitySlot } from './profileService';

function minutes(time: string) {
  const [hour, minute] = time.split(':').map(Number);
  return hour * 60 + minute;
}

function merged(slots: AvailabilitySlot[]): AvailabilitySlot[] {
  const result: AvailabilitySlot[] = [];
  for (const slot of [...slots].sort((a, b) => a.dia_semana - b.dia_semana || minutes(a.hora_inicio) - minutes(b.hora_inicio))) {
    const last = result[result.length - 1];
    if (last?.dia_semana === slot.dia_semana && minutes(slot.hora_inicio) <= minutes(last.hora_fin)) {
      if (minutes(slot.hora_fin) > minutes(last.hora_fin)) last.hora_fin = slot.hora_fin;
    } else result.push({ ...slot });
  }
  return result;
}

export function hoursAvailable(slots: AvailabilitySlot[]) {
  const total = merged(slots).reduce((sum, slot) => sum + minutes(slot.hora_fin) - minutes(slot.hora_inicio), 0);
  return Number((total / 60).toFixed(2));
}

export function overlapsHour(slots: AvailabilitySlot[], day: number, start: string, end: string) {
  return slots.some(s => s.dia_semana === day && minutes(s.hora_inicio) < minutes(end) && minutes(start) < minutes(s.hora_fin));
}

export function toggleHour(slots: AvailabilitySlot[], day: number, start: string, end: string): AvailabilitySlot[] {
  if (!overlapsHour(slots, day, start, end)) return merged([...slots, { dia_semana: day, hora_inicio: start, hora_fin: end }]);
  return merged(slots).flatMap(s => {
    if (!overlapsHour([s], day, start, end)) return [s];
    const pieces = [];
    if (minutes(s.hora_inicio) < minutes(start)) pieces.push({ ...s, hora_fin: start });
    if (minutes(s.hora_fin) > minutes(end)) pieces.push({ ...s, hora_inicio: end });
    return pieces;
  });
}
