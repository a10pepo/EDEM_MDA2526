const STATUS_COLORS = {
  completed: 'success',
  pending:   'warning',
  returned:  'danger',
  none:      'secondary',
  basic:     'primary',
  silver:    'light',
  gold:      'warning',
}

export default function StatusBadge({ value }) {
  const color = STATUS_COLORS[value] ?? 'secondary'
  return <span className={`badge bg-${color} text-${color === 'light' ? 'dark' : 'white'}`}>{value}</span>
}
