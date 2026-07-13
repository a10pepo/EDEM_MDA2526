import { useEffect, useState } from 'react'
import { ticketsApi, productsApi } from '../api/client'
import StatusBadge from '../components/StatusBadge'

const STATUSES = ['pending', 'completed', 'returned']

const EMPTY_FORM = { cashier_id: '', payment_method: 'card', customer_id: '', items: [] }
const EMPTY_ITEM = { sku: '', quantity: 1, unit_price: 0, discount: 0 }

export default function Tickets() {
  const [tickets, setTickets]   = useState([])
  const [products, setProducts] = useState([])
  const [form, setForm]         = useState(EMPTY_FORM)
  const [newItem, setNewItem]   = useState(EMPTY_ITEM)
  const [showForm, setShowForm] = useState(false)
  const [saving, setSaving]     = useState(false)
  const [error, setError]       = useState(null)

  const load = () => {
    ticketsApi.list().then(r => setTickets(r.data)).catch(() => setError('API unreachable'))
    productsApi.list().then(r => setProducts(r.data))
  }

  useEffect(() => { load() }, [])

  const skuToName = Object.fromEntries(products.map(p => [p.sku, p]))

  const addItem = () => {
    if (!newItem.sku) return
    setForm(f => ({ ...f, items: [...f.items, { ...newItem }] }))
    setNewItem(EMPTY_ITEM)
  }

  const removeItem = idx => setForm(f => ({ ...f, items: f.items.filter((_, i) => i !== idx) }))

  const handleSkuChange = (sku) => {
    const p = products.find(p => p.sku === sku)
    setNewItem(i => ({ ...i, sku, unit_price: p ? p.price : 0 }))
  }

  const handleSubmit = async e => {
    e.preventDefault()
    if (form.items.length === 0) { setError('Add at least one item'); return }
    setSaving(true)
    try {
      await ticketsApi.create({
        ...form,
        customer_id: form.customer_id || null,
        items: form.items.map(i => ({ ...i, quantity: parseInt(i.quantity), unit_price: parseFloat(i.unit_price), discount: parseFloat(i.discount) })),
      })
      setForm(EMPTY_FORM)
      setShowForm(false)
      load()
    } catch {
      setError('Failed to save ticket')
    } finally {
      setSaving(false)
    }
  }

  const handleStatus = async (id, status) => {
    await ticketsApi.updateStatus(id, status)
    load()
  }

  const handleDelete = async id => {
    if (!confirm(`Delete ticket ${id}?`)) return
    await ticketsApi.delete(id)
    load()
  }

  const gross  = form.items.reduce((s, i) => s + i.unit_price * i.quantity, 0)
  const disc   = form.items.reduce((s, i) => s + parseFloat(i.discount || 0), 0)
  const total  = gross - disc

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="fw-bold mb-0">Tickets</h4>
        <button className="btn btn-dark" onClick={() => setShowForm(s => !s)}>
          <i className={`bi bi-${showForm ? 'x' : 'plus'}-lg me-1`} />
          {showForm ? 'Cancel' : 'New Ticket'}
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {/* Ticket form */}
      {showForm && (
        <div className="card mb-4">
          <div className="card-header fw-bold">New Ticket</div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div className="row g-3 mb-3">
                <div className="col-md-4">
                  <label className="form-label small fw-bold">Cashier ID</label>
                  <input className="form-control" required value={form.cashier_id}
                    onChange={e => setForm(f => ({ ...f, cashier_id: e.target.value }))} />
                </div>
                <div className="col-md-4">
                  <label className="form-label small fw-bold">Payment Method</label>
                  <select className="form-select" value={form.payment_method}
                    onChange={e => setForm(f => ({ ...f, payment_method: e.target.value }))}>
                    {['card', 'cash', 'online'].map(m => <option key={m}>{m}</option>)}
                  </select>
                </div>
                <div className="col-md-4">
                  <label className="form-label small fw-bold">Customer ID (optional)</label>
                  <input className="form-control" value={form.customer_id}
                    onChange={e => setForm(f => ({ ...f, customer_id: e.target.value }))} />
                </div>
              </div>

              {/* Add item row */}
              <div className="card bg-light mb-3">
                <div className="card-body">
                  <p className="fw-bold small mb-2">Add Item</p>
                  <div className="row g-2 align-items-end">
                    <div className="col-md-3">
                      <label className="form-label small">SKU</label>
                      <select className="form-select form-select-sm" value={newItem.sku}
                        onChange={e => handleSkuChange(e.target.value)}>
                        <option value="">Select product…</option>
                        {products.map(p => <option key={p.sku} value={p.sku}>{p.sku} — {p.name}</option>)}
                      </select>
                    </div>
                    <div className="col-md-2">
                      <label className="form-label small">Qty</label>
                      <input type="number" className="form-control form-control-sm" min={1} value={newItem.quantity}
                        onChange={e => setNewItem(i => ({ ...i, quantity: e.target.value }))} />
                    </div>
                    <div className="col-md-2">
                      <label className="form-label small">Unit Price (€)</label>
                      <input type="number" className="form-control form-control-sm" step="0.01" value={newItem.unit_price}
                        onChange={e => setNewItem(i => ({ ...i, unit_price: e.target.value }))} />
                    </div>
                    <div className="col-md-2">
                      <label className="form-label small">Discount (€)</label>
                      <input type="number" className="form-control form-control-sm" step="0.01" min={0} value={newItem.discount}
                        onChange={e => setNewItem(i => ({ ...i, discount: e.target.value }))} />
                    </div>
                    <div className="col-md-2">
                      <button type="button" className="btn btn-sm btn-outline-dark w-100" onClick={addItem}>
                        <i className="bi bi-plus me-1" />Add
                      </button>
                    </div>
                  </div>
                </div>
              </div>

              {/* Items in ticket */}
              {form.items.length > 0 && (
                <table className="table table-sm mb-3">
                  <thead><tr><th>SKU</th><th>Name</th><th className="text-end">Qty</th><th className="text-end">Price</th><th className="text-end">Disc.</th><th className="text-end">Subtotal</th><th /></tr></thead>
                  <tbody>
                    {form.items.map((item, i) => {
                      const p = skuToName[item.sku]
                      return (
                        <tr key={i}>
                          <td><code>{item.sku}</code></td>
                          <td>{p?.name ?? '—'}</td>
                          <td className="text-end">{item.quantity}</td>
                          <td className="text-end">€{parseFloat(item.unit_price).toFixed(2)}</td>
                          <td className="text-end text-danger">-€{parseFloat(item.discount).toFixed(2)}</td>
                          <td className="text-end fw-bold">€{(item.unit_price * item.quantity - parseFloat(item.discount)).toFixed(2)}</td>
                          <td><button type="button" className="btn btn-sm btn-outline-danger" onClick={() => removeItem(i)}><i className="bi bi-trash" /></button></td>
                        </tr>
                      )
                    })}
                  </tbody>
                  <tfoot className="table-light">
                    <tr>
                      <td colSpan={5} className="text-end fw-bold">Total</td>
                      <td className="text-end fw-bold text-success">€{total.toFixed(2)}</td>
                      <td />
                    </tr>
                  </tfoot>
                </table>
              )}

              <div className="text-end">
                <button type="submit" className="btn btn-dark" disabled={saving || form.items.length === 0}>
                  {saving ? 'Saving…' : `Save Ticket (€${total.toFixed(2)})`}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Tickets table */}
      <div className="card">
        <div className="card-body p-0">
          <table className="table table-hover mb-0">
            <thead className="table-dark">
              <tr>
                <th>Ticket ID</th>
                <th>Date</th>
                <th>Cashier</th>
                <th>Customer</th>
                <th>Payment</th>
                <th className="text-end">Items</th>
                <th className="text-end">Total</th>
                <th className="text-end">Disc %</th>
                <th>Status</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {tickets.map(t => (
                <tr key={t.ticket_id}>
                  <td><code className="small">{t.ticket_id}</code></td>
                  <td className="small">{t.date_time.replace('T', ' ')}</td>
                  <td>{t.cashier_id}</td>
                  <td>{t.customer_id ?? '—'}</td>
                  <td>{t.payment_method}</td>
                  <td className="text-end">{t.items.length}</td>
                  <td className="text-end fw-bold">€{t.total_amount.toFixed(2)}</td>
                  <td className={`text-end ${t.discount_percentage > 20 ? 'text-danger fw-bold' : ''}`}>
                    {t.discount_percentage.toFixed(1)}%
                  </td>
                  <td><StatusBadge value={t.status} /></td>
                  <td>
                    <div className="d-flex gap-1">
                      <select className="form-select form-select-sm" style={{ width: 120 }} value={t.status}
                        onChange={e => handleStatus(t.ticket_id, e.target.value)}>
                        {STATUSES.map(s => <option key={s} value={s}>{s}</option>)}
                      </select>
                      <button className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(t.ticket_id)}>
                        <i className="bi bi-trash" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
              {tickets.length === 0 && (
                <tr><td colSpan={10} className="text-center text-muted py-4">No tickets registered.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
