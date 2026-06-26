import { useEffect, useState } from 'react'
import { customersApi } from '../api/client'
import StatusBadge from '../components/StatusBadge'

const EMPTY_FORM = {
  customer_id: '', name: '', email: '', phone: '',
  date_of_birth: '', membership_level: 'none',
}

const MEMBERSHIPS = ['none', 'basic', 'silver', 'gold']

export default function Customers() {
  const [customers, setCustomers] = useState([])
  const [form, setForm]           = useState(EMPTY_FORM)
  const [showForm, setShowForm]   = useState(false)
  const [selected, setSelected]   = useState(null)   // customer detail
  const [saving, setSaving]       = useState(false)
  const [error, setError]         = useState(null)

  const load = () => customersApi.list().then(r => setCustomers(r.data)).catch(() => setError('API unreachable'))
  useEffect(() => { load() }, [])

  const handleSubmit = async e => {
    e.preventDefault()
    setSaving(true)
    try {
      await customersApi.create(form)
      setForm(EMPTY_FORM)
      setShowForm(false)
      load()
    } catch {
      setError('Failed to save customer')
    } finally {
      setSaving(false)
    }
  }

  const handleSelect = async id => {
    const r = await customersApi.get(id)
    setSelected(r.data)
  }

  const handleDelete = async id => {
    if (!confirm(`Delete customer ${id}?`)) return
    await customersApi.delete(id)
    setSelected(null)
    load()
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="fw-bold mb-0">Customers</h4>
        <button className="btn btn-dark" onClick={() => setShowForm(s => !s)}>
          <i className={`bi bi-${showForm ? 'x' : 'plus'}-lg me-1`} />
          {showForm ? 'Cancel' : 'Register Customer'}
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {/* Registration form */}
      {showForm && (
        <div className="card mb-4">
          <div className="card-header fw-bold">New Customer</div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div className="row g-3">
                {[
                  { name: 'customer_id',   label: 'ID (DNI/Passport)', type: 'text' },
                  { name: 'name',          label: 'Full Name',          type: 'text' },
                  { name: 'email',         label: 'Email',              type: 'email' },
                  { name: 'phone',         label: 'Phone',              type: 'text' },
                  { name: 'date_of_birth', label: 'Date of Birth',      type: 'date' },
                ].map(({ name, label, type }) => (
                  <div className="col-md-4" key={name}>
                    <label className="form-label small fw-bold">{label}</label>
                    <input type={type} className="form-control" required value={form[name]}
                      onChange={e => setForm(f => ({ ...f, [name]: e.target.value }))} />
                  </div>
                ))}
                <div className="col-md-4">
                  <label className="form-label small fw-bold">Membership Level</label>
                  <select className="form-select" value={form.membership_level}
                    onChange={e => setForm(f => ({ ...f, membership_level: e.target.value }))}>
                    {MEMBERSHIPS.map(m => <option key={m}>{m}</option>)}
                  </select>
                </div>
              </div>
              <div className="mt-3 text-end">
                <button type="submit" className="btn btn-dark" disabled={saving}>
                  {saving ? 'Saving…' : 'Save Customer'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      <div className="row g-3">
        {/* Customers table */}
        <div className={selected ? 'col-md-7' : 'col-12'}>
          <div className="card">
            <div className="card-body p-0">
              <table className="table table-hover mb-0">
                <thead className="table-dark">
                  <tr>
                    <th>ID</th>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Phone</th>
                    <th>Born</th>
                    <th>Membership</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {customers.map(c => (
                    <tr key={c.customer_id} className={selected?.customer_id === c.customer_id ? 'table-active' : ''}>
                      <td>
                        <button className="btn btn-link p-0 text-decoration-none" onClick={() => handleSelect(c.customer_id)}>
                          <code>{c.customer_id}</code>
                        </button>
                      </td>
                      <td>{c.name}</td>
                      <td className="small">{c.email}</td>
                      <td>{c.phone}</td>
                      <td>{c.date_of_birth}</td>
                      <td><StatusBadge value={c.membership_level} /></td>
                      <td>
                        <button className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(c.customer_id)}>
                          <i className="bi bi-trash" />
                        </button>
                      </td>
                    </tr>
                  ))}
                  {customers.length === 0 && (
                    <tr><td colSpan={7} className="text-center text-muted py-4">No customers registered.</td></tr>
                  )}
                </tbody>
              </table>
            </div>
          </div>
        </div>

        {/* Customer detail panel */}
        {selected && (
          <div className="col-md-5">
            <div className="card">
              <div className="card-header d-flex justify-content-between align-items-center">
                <span className="fw-bold">{selected.name}</span>
                <button className="btn-close" onClick={() => setSelected(null)} />
              </div>
              <div className="card-body small">
                <p><strong>ID:</strong> {selected.customer_id}</p>
                <p><strong>Email:</strong> {selected.email}</p>
                <p><strong>Phone:</strong> {selected.phone}</p>
                <p><strong>Born:</strong> {selected.date_of_birth}</p>
                <p><strong>Membership:</strong> <StatusBadge value={selected.membership_level} /></p>
                <p className="fw-bold text-success">Total spent: €{selected.total_spent?.toFixed(2) ?? '0.00'}</p>
                <hr />
                <p className="fw-bold">Purchase history ({selected.tickets?.length ?? 0} tickets)</p>
                {selected.tickets?.length > 0 ? (
                  <table className="table table-sm">
                    <thead><tr><th>Ticket</th><th className="text-end">Total</th><th>Status</th></tr></thead>
                    <tbody>
                      {selected.tickets.map(t => (
                        <tr key={t.ticket_id}>
                          <td><code className="small">{t.ticket_id}</code></td>
                          <td className="text-end">€{t.total_amount.toFixed(2)}</td>
                          <td><StatusBadge value={t.status} /></td>
                        </tr>
                      ))}
                    </tbody>
                  </table>
                ) : (
                  <p className="text-muted">No purchases yet.</p>
                )}
              </div>
            </div>
          </div>
        )}
      </div>
    </>
  )
}
