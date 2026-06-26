import { NavLink } from 'react-router-dom'

export default function Navbar() {
  return (
    <nav className="navbar navbar-expand-lg navbar-dark bg-dark px-4">
      <span className="navbar-brand fw-bold fs-5">
        <i className="bi bi-bag-heart me-2" />
        ZARA Management
      </span>
      <div className="navbar-nav ms-auto flex-row gap-2">
        {[
          { to: '/',          icon: 'speedometer2', label: 'Dashboard' },
          { to: '/products',  icon: 'box-seam',     label: 'Products'  },
          { to: '/tickets',   icon: 'receipt',      label: 'Tickets'   },
          { to: '/customers', icon: 'people',       label: 'Customers' },
        ].map(({ to, icon, label }) => (
          <NavLink
            key={to}
            to={to}
            end={to === '/'}
            className={({ isActive }) =>
              `nav-link px-3 py-1 rounded ${isActive ? 'bg-white text-dark fw-bold' : 'text-white'}`
            }
          >
            <i className={`bi bi-${icon} me-1`} />{label}
          </NavLink>
        ))}
      </div>
    </nav>
  )
}
