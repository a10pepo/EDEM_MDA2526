import { useEffect, useState } from 'react'
import { Link } from 'react-router-dom'
import { productsApi, ticketsApi, customersApi, alertsApi } from '../api/client'
import StatusBadge from '../components/StatusBadge'

export default function Dashboard() {
  const [data, setData]       = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError]     = useState(null)

  useEffect(() => {
    Promise.all([
      productsApi.list(),
      ticketsApi.list(),
      customersApi.list(),
      alertsApi.check(),
    ])
      .then(([p, t, c, a]) =>
        setData({
          products:      p.data,
          tickets:       t.data,
          customers:     c.data,
          alerts:        a.data,
          recentTickets: [...t.data].sort((a, b) => b.date_time.localeCompare(a.date_time)).slice(0, 6),
        })
      )
      .catch(() => setError('Could not reach the API. Is the backend running?'))
      .finally(() => setLoading(false))
  }, [])

  if (loading) return <Spinner />
  if (error)   return <div className="alert alert-danger">{error}</div>

  const { products, tickets, customers, alerts, recentTickets } = data
  const totalRevenue = tickets.filter(t => t.status === 'completed').reduce((s, t) => s + t.total_amount, 0)

  return (
    <>
      <h4 className="mb-4 fw-bold">Dashboard</h4>

      {/* KPI cards */}
      <div className="row g-3 mb-4">
        <StatCard title="Products"    value={products.length}            icon="box-seam"    color="primary"   to="/products"  />
        <StatCard title="Tickets"     value={tickets.length}             icon="receipt"     color="success"   to="/tickets"   />
        <StatCard title="Customers"   value={customers.length}           icon="people"      color="info"      to="/customers" />
        <StatCard title="Revenue"     value={`€${totalRevenue.toFixed(2)}`} icon="cash-coin" color="warning" />
      </div>

      {/* Alerts */}
      {alerts.total_alerts > 0 && (
        <div className="mb-4">
          <h6 className="fw-bold text-danger"><i className="bi bi-exclamation-triangle me-2" />Active Alerts ({alerts.total_alerts})</h6>
          {alerts.low_stock.map(a => (
            <div key={a.sku} className="alert alert-warning py-2 mb-2">
              <i className="bi bi-box me-2" />
              <strong>Low Stock:</strong> {a.name} ({a.sku}) — {a.stock} units left (min: {a.threshold})
            </div>
          ))}
          {alerts.high_discount.map(a => (
            <div key={a.ticket_id} className="alert alert-danger py-2 mb-2">
              <i className="bi bi-percent me-2" />
              <strong>High Discount:</strong> Ticket {a.ticket_id} — {a.discount_pct.toFixed(1)}% off (€{a.discount_total.toFixed(2)})
            </div>
          ))}
          {alerts.return_rate.map((a, i) => (
            <div key={i} className="alert alert-danger py-2 mb-2">
              <i className="bi bi-arrow-return-left me-2" />
              <strong>High Return Rate:</strong> {a.returned}/{a.total} tickets returned ({a.rate_pct}%)
            </div>
          ))}
        </div>
      )}

      {alerts.total_alerts === 0 && (
        <div className="alert alert-success mb-4 py-2">
          <i className="bi bi-check-circle me-2" />All systems OK — no active alerts.
        </div>
      )}

      {/* Recent tickets */}
      <div className="card">
        <div className="card-header d-flex justify-content-between align-items-center">
          <span className="fw-bold">Recent Tickets</span>
          <Link to="/tickets" className="btn btn-sm btn-outline-primary">View all</Link>
        </div>
        <div className="card-body p-0">
          <table className="table table-hover mb-0">
            <thead className="table-light">
              <tr>
                <th>Ticket ID</th>
                <th>Date</th>
                <th>Cashier</th>
                <th className="text-end">Items</th>
                <th className="text-end">Total</th>
                <th>Status</th>
              </tr>
            </thead>
            <tbody>
              {recentTickets.map(t => (
                <tr key={t.ticket_id}>
                  <td><code className="small">{t.ticket_id}</code></td>
                  <td className="small">{t.date_time.replace('T', ' ')}</td>
                  <td>{t.cashier_id}</td>
                  <td className="text-end">{t.items.length}</td>
                  <td className="text-end fw-bold">€{t.total_amount.toFixed(2)}</td>
                  <td><StatusBadge value={t.status} /></td>
                </tr>
              ))}
              {recentTickets.length === 0 && (
                <tr><td colSpan={6} className="text-center text-muted py-3">No tickets yet.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}

function StatCard({ title, value, icon, color, to }) {
  const inner = (
    <div className={`card border-${color} h-100`}>
      <div className="card-body d-flex align-items-center gap-3">
        <i className={`bi bi-${icon} fs-1 text-${color}`} />
        <div>
          <div className="fs-3 fw-bold">{value}</div>
          <div className="text-muted small">{title}</div>
        </div>
      </div>
    </div>
  )
  return (
    <div className="col-md-3">
      {to ? <Link to={to} className="text-decoration-none">{inner}</Link> : inner}
    </div>
  )
}

function Spinner() {
  return (
    <div className="text-center mt-5">
      <div className="spinner-border text-primary" role="status" />
      <div className="mt-2 text-muted">Loading...</div>
    </div>
  )
}
