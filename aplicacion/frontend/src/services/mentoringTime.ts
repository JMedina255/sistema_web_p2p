const limaDate = new Intl.DateTimeFormat('es-PE', {
  timeZone: 'America/Lima', day: 'numeric', month: 'short', year: 'numeric',
  hour: '2-digit', minute: '2-digit', hourCycle: 'h23',
});

export function formatMentoringTime(iso?: string | null): string {
  if (!iso) return 'Por coordinar';
  const instant = new Date(iso);
  return Number.isNaN(instant.getTime()) ? iso : `${limaDate.format(instant)} (Lima)`;
}
