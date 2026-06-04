export function getDeadlineStatus(deadline) {
  if (!deadline) return { type: 'ok', label: null, color: null }
  const diff = new Date(deadline) - new Date()
  const hours = diff / 3600000
  if (diff < 0) return { type: 'overdue', label: 'ПРОСРОЧКА', color: 'var(--color-overdue)' }
  if (hours <= 24) return { type: 'urgent', label: 'Завтра дедлайн', color: 'var(--color-urgent)' }
  if (hours <= 48) return { type: 'warning', label: 'Скоро дедлайн', color: 'var(--color-warning)' }
  return { type: 'ok', label: null, color: null }
}
