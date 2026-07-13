import { useEffect, useState } from 'react'
import { productsApi } from '../api/client'

const EMPTY_FORM = {
  sku: '', name: '', category: '', size: '', color: '',
  price: '', stock_quantity: '', restock_threshold: '',
  last_restock_date: '', supplier_id: '',
}

export default function Products() {
  const [products, setProducts] = useState([])
  const [form, setForm]         = useState(EMPTY_FORM)
  const [showForm, setShowForm] = useState(false)
  const [stockEdit, setStockEdit] = useState({})   // { sku: newQty }
  const [saving, setSaving]     = useState(false)
  const [error, setError]       = useState(null)

  const load = () => productsApi.list().then(r => setProducts(r.data)).catch(() => setError('API unreachable'))

  useEffect(() => { load() }, [])

  const handleSubmit = async e => {
    e.preventDefault()
    setSaving(true)
    try {
      await productsApi.create({
        ...form,
        price: parseFloat(form.price),
        stock_quantity: parseInt(form.stock_quantity),
        restock_threshold: parseInt(form.restock_threshold),
      })
      setForm(EMPTY_FORM)
      setShowForm(false)
      load()
    } catch {
      setError('Failed to save product')
    } finally {
      setSaving(false)
    }
  }

  const handleStockUpdate = async (sku) => {
    const qty = parseInt(stockEdit[sku])
    if (isNaN(qty)) return
    await productsApi.updateStock(sku, qty)
    setStockEdit(s => ({ ...s, [sku]: undefined }))
    load()
  }

  const handleDelete = async sku => {
    if (!confirm(`Delete product ${sku}?`)) return
    await productsApi.delete(sku)
    load()
  }

  return (
    <>
      <div className="d-flex justify-content-between align-items-center mb-3">
        <h4 className="fw-bold mb-0">Products</h4>
        <button className="btn btn-dark" onClick={() => setShowForm(s => !s)}>
          <i className={`bi bi-${showForm ? 'x' : 'plus'}-lg me-1`} />
          {showForm ? 'Cancel' : 'Register Product'}
        </button>
      </div>

      {error && <div className="alert alert-danger">{error}</div>}

      {/* Registration form */}
      {showForm && (
        <div className="card mb-4">
          <div className="card-header fw-bold">New Product</div>
          <div className="card-body">
            <form onSubmit={handleSubmit}>
              <div className="row g-3">
                {[
                  { name: 'sku',              label: 'SKU',              type: 'text'   },
                  { name: 'name',             label: 'Name',             type: 'text'   },
                  { name: 'category',         label: 'Category',         type: 'text'   },
                  { name: 'size',             label: 'Size',             type: 'text'   },
                  { name: 'color',            label: 'Color',            type: 'text'   },
                  { name: 'price',            label: 'Price (€)',        type: 'number' },
                  { name: 'stock_quantity',   label: 'Initial Stock',    type: 'number' },
                  { name: 'restock_threshold',label: 'Restock Threshold',type: 'number' },
                  { name: 'last_restock_date',label: 'Last Restock Date',type: 'date'   },
                  { name: 'supplier_id',      label: 'Supplier ID',      type: 'text'   },
                ].map(({ name, label, type }) => (
                  <div className="col-md-4" key={name}>
                    <label className="form-label small fw-bold">{label}</label>
                    <input
                      type={type}
                      className="form-control"
                      value={form[name]}
                      step={type === 'number' ? 'any' : undefined}
                      required
                      onChange={e => setForm(f => ({ ...f, [name]: e.target.value }))}
                    />
                  </div>
                ))}
              </div>
              <div className="mt-3 text-end">
                <button type="submit" className="btn btn-dark" disabled={saving}>
                  {saving ? 'Saving…' : 'Save Product'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}

      {/* Products table */}
      <div className="card">
        <div className="card-body p-0">
          <table className="table table-hover mb-0">
            <thead className="table-dark">
              <tr>
                <th>SKU</th>
                <th>Name</th>
                <th>Category</th>
                <th>Size</th>
                <th>Color</th>
                <th className="text-end">Price</th>
                <th className="text-end">Stock</th>
                <th className="text-end">Threshold</th>
                <th>Supplier</th>
                <th>Actions</th>
              </tr>
            </thead>
            <tbody>
              {products.map(p => (
                <tr key={p.sku}>
                  <td><code>{p.sku}</code></td>
                  <td>{p.name}</td>
                  <td>{p.category}</td>
                  <td>{p.size}</td>
                  <td>{p.color}</td>
                  <td className="text-end">€{p.price.toFixed(2)}</td>
                  <td className="text-end">
                    {/* Inline stock edit */}
                    {stockEdit[p.sku] !== undefined ? (
                      <div className="d-flex gap-1 justify-content-end">
                        <input
                          type="number"
                          className="form-control form-control-sm"
                          style={{ width: 70 }}
                          value={stockEdit[p.sku]}
                          onChange={e => setStockEdit(s => ({ ...s, [p.sku]: e.target.value }))}
                        />
                        <button className="btn btn-sm btn-success" onClick={() => handleStockUpdate(p.sku)}>✓</button>
                        <button className="btn btn-sm btn-secondary" onClick={() => setStockEdit(s => ({ ...s, [p.sku]: undefined }))}>✕</button>
                      </div>
                    ) : (
                      <span
                        className={`fw-bold ${p.is_below_threshold ? 'text-danger' : 'text-success'} cursor-pointer`}
                        role="button"
                        title="Click to edit stock"
                        onClick={() => setStockEdit(s => ({ ...s, [p.sku]: p.stock_quantity }))}
                      >
                        {p.stock_quantity}
                        {p.is_below_threshold && <i className="bi bi-exclamation-triangle-fill ms-1 text-danger" />}
                      </span>
                    )}
                  </td>
                  <td className="text-end">{p.restock_threshold}</td>
                  <td>{p.supplier_id}</td>
                  <td>
                    <button className="btn btn-sm btn-outline-danger" onClick={() => handleDelete(p.sku)}>
                      <i className="bi bi-trash" />
                    </button>
                  </td>
                </tr>
              ))}
              {products.length === 0 && (
                <tr><td colSpan={10} className="text-center text-muted py-4">No products registered.</td></tr>
              )}
            </tbody>
          </table>
        </div>
      </div>
    </>
  )
}
