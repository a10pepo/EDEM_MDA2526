import { useState, useEffect } from 'react'
import './App.css'

const TEAM_COLORS = {
  "Red Bull Racing": "#3671C6",
  "Ferrari":         "#E8002D",
  "Mercedes":        "#27F4D2",
  "McLaren":         "#FF8000",
  "Aston Martin":    "#229971",
  "Alpine":          "#FF87BC",
  "Williams":        "#64C4FF",
  "RB":              "#6692FF",
  "Kick Sauber":     "#52E252",
  "Haas":            "#B6BABD",
}

const NATIONALITY_FLAG = {
  "Dutch":       "🇳🇱",
  "Mexican":     "🇲🇽",
  "Monégasque":  "🇲🇨",
  "Spanish":     "🇪🇸",
  "British":     "🇬🇧",
  "Australian":  "🇦🇺",
  "Canadian":    "🇨🇦",
  "French":      "🇫🇷",
  "Finnish":     "🇫🇮",
  "Japanese":    "🇯🇵",
  "Thai":        "🇹🇭",
  "Chinese":     "🇨🇳",
  "Danish":      "🇩🇰",
  "German":      "🇩🇪",
  "American":    "🇺🇸",
}

const COUNTRY_FLAG = {
  "Bahrain":      "🇧🇭",
  "Saudi Arabia": "🇸🇦",
  "Australia":    "🇦🇺",
  "Japan":        "🇯🇵",
}

function teamColor(name) { return TEAM_COLORS[name] || "#555" }

function useFetch(path) {
  const [data, setData] = useState(null)
  useEffect(() => {
    fetch(`/api${path}`).then(r => r.json()).then(setData)
  }, [path])
  return data
}

function useStandings() {
  const results = useFetch('/results')
  const drivers = useFetch('/drivers')

  if (!results || !drivers) return { driverStandings: null, constructorStandings: null }

  const driverMap = {}
  drivers.forEach(d => { driverMap[d.code] = d })

  const driverPts = {}
  results.forEach(r => {
    if (!driverPts[r.driver]) {
      driverPts[r.driver] = {
        code: r.driver, name: r.driver_name, points: 0,
        team: driverMap[r.driver]?.team || '',
      }
    }
    driverPts[r.driver].points += r.points
  })

  const driverStandings = Object.values(driverPts).sort((a, b) => b.points - a.points)

  const constructorPts = {}
  driverStandings.forEach(d => {
    constructorPts[d.team] = (constructorPts[d.team] || 0) + d.points
  })
  const constructorStandings = Object.entries(constructorPts)
    .map(([team, points]) => ({ team, points }))
    .sort((a, b) => b.points - a.points)

  return { driverStandings, constructorStandings }
}

function Loading({ label }) {
  return <div className="loading">Loading {label}...</div>
}

function DriversTable({ standings }) {
  const drivers = useFetch('/drivers')
  if (!drivers || !standings) return <Loading label="drivers" />

  const ptsMap = {}
  standings.forEach(s => { ptsMap[s.code] = s.points })

  const sorted = [...drivers].sort((a, b) => (ptsMap[b.code] ?? 0) - (ptsMap[a.code] ?? 0))

  return (
    <section>
      <h2 className="section-title">Drivers <span>2024</span></h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th className="col-pos">#</th>
              <th className="col-num">No.</th>
              <th>Driver</th>
              <th>Team</th>
              <th>Nationality</th>
              <th className="col-center">Points</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((d, i) => (
              <tr key={d.driver_id} style={{ borderLeftColor: teamColor(d.team) }}>
                <td className="pos-num">{i + 1}</td>
                <td><span className="drv-number">{d.permanent_number}</span></td>
                <td>
                  <span className="drv-code">{d.code}</span>
                  <span className="drv-name">{d.name}</span>
                </td>
                <td>
                  <span className="team-dot" style={{ background: teamColor(d.team) }} />
                  {d.team}
                </td>
                <td>{NATIONALITY_FLAG[d.nationality]} {d.nationality}</td>
                <td className="col-center"><strong className="pts">{ptsMap[d.code] ?? 0}</strong></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

function TeamsTable({ constructorStandings }) {
  const teams = useFetch('/teams')
  if (!teams || !constructorStandings) return <Loading label="teams" />

  const ptsMap = {}
  constructorStandings.forEach(c => { ptsMap[c.team] = c.points })

  const sorted = [...teams].sort((a, b) => (ptsMap[b.name] ?? 0) - (ptsMap[a.name] ?? 0))

  return (
    <section>
      <h2 className="section-title">Constructors <span>2024</span></h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th className="col-pos">#</th>
              <th>Team</th>
              <th>Base</th>
              <th>Team Principal</th>
              <th>Power Unit</th>
              <th className="col-center">Points</th>
              <th className="col-center">Titles</th>
            </tr>
          </thead>
          <tbody>
            {sorted.map((t, i) => (
              <tr key={t.team_id} style={{ borderLeftColor: teamColor(t.name) }}>
                <td className="pos-num">{i + 1}</td>
                <td>
                  <span className="team-dot" style={{ background: teamColor(t.name) }} />
                  <strong style={{ color: '#fff' }}>{t.name}</strong>
                </td>
                <td>{t.base}</td>
                <td>{t.team_principal}</td>
                <td>{t.power_unit}</td>
                <td className="col-center"><strong className="pts">{ptsMap[t.name] ?? 0}</strong></td>
                <td className="col-center">
                  {t.championships > 0
                    ? <span className="champ-badge">{t.championships}</span>
                    : <span className="no-champ">—</span>}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

function RacesTable() {
  const races = useFetch('/races')
  if (!races) return <Loading label="races" />
  return (
    <section>
      <h2 className="section-title">Race Calendar <span>2024</span></h2>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th className="col-pos">Rd</th>
              <th>Grand Prix</th>
              <th>Circuit</th>
              <th>Country</th>
              <th>Date</th>
              <th className="col-center">Laps</th>
            </tr>
          </thead>
          <tbody>
            {races.map(r => (
              <tr key={r.race_id}>
                <td className="pos-num">{r.round}</td>
                <td><strong style={{ color: '#fff' }}>{r.name}</strong></td>
                <td>{r.circuit}</td>
                <td>{COUNTRY_FLAG[r.country]} {r.country}</td>
                <td>{r.date}</td>
                <td className="col-center">{r.laps}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

function podiumClass(pos) {
  if (pos === 1) return 'podium-gold'
  if (pos === 2) return 'podium-silver'
  if (pos === 3) return 'podium-bronze'
  return ''
}

function ResultsTable() {
  const results = useFetch('/results')
  const [raceFilter, setRaceFilter] = useState('All')

  if (!results) return <Loading label="results" />

  const races = ['All', ...new Set(results.map(r => r.race))]
  const filtered = raceFilter === 'All' ? results : results.filter(r => r.race === raceFilter)

  return (
    <section>
      <div className="results-header">
        <h2 className="section-title">Race Results <span>2024</span></h2>
        <select className="race-filter" value={raceFilter} onChange={e => setRaceFilter(e.target.value)}>
          {races.map(r => <option key={r} value={r}>{r}</option>)}
        </select>
      </div>
      <div className="card">
        <table>
          <thead>
            <tr>
              <th>Race</th>
              <th>Driver</th>
              <th className="col-center">Grid</th>
              <th className="col-center">Finish</th>
              <th className="col-center">Pts</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody>
            {filtered.map((r, i) => (
              <tr key={i} className={podiumClass(r.final_position)}>
                <td>{r.race}</td>
                <td>
                  <span className="drv-code">{r.driver}</span>
                  <span className="drv-name">{r.driver_name}</span>
                </td>
                <td className="col-center">{r.grid_position > 0 ? `P${r.grid_position}` : '—'}</td>
                <td className="col-center">{r.final_position > 0 ? `P${r.final_position}` : '—'}</td>
                <td className="col-center"><strong className="pts">{r.points}</strong></td>
                <td><span className={`status status--${r.status.toLowerCase()}`}>{r.status}</span></td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </section>
  )
}

function StandingsTab({ driverStandings, constructorStandings }) {
  if (!driverStandings || !constructorStandings) return <Loading label="standings" />
  return (
    <div className="standings-grid">
      <section>
        <h2 className="section-title">Drivers <span>Championship</span></h2>
        <div className="card">
          <table>
            <thead>
              <tr>
                <th className="col-pos">#</th>
                <th>Driver</th>
                <th>Team</th>
                <th className="col-center">Points</th>
              </tr>
            </thead>
            <tbody>
              {driverStandings.map((d, i) => (
                <tr key={d.code} style={{ borderLeftColor: teamColor(d.team) }}>
                  <td className="pos-num">{i + 1}</td>
                  <td>
                    <span className="drv-code">{d.code}</span>
                    <span className="drv-name">{d.name}</span>
                  </td>
                  <td>
                    <span className="team-dot" style={{ background: teamColor(d.team) }} />
                    {d.team}
                  </td>
                  <td className="col-center"><strong className="pts">{d.points}</strong></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>

      <section>
        <h2 className="section-title">Constructors <span>Championship</span></h2>
        <div className="card">
          <table>
            <thead>
              <tr>
                <th className="col-pos">#</th>
                <th>Team</th>
                <th className="col-center">Points</th>
              </tr>
            </thead>
            <tbody>
              {constructorStandings.map((c, i) => (
                <tr key={c.team} style={{ borderLeftColor: teamColor(c.team) }}>
                  <td className="pos-num">{i + 1}</td>
                  <td>
                    <span className="team-dot" style={{ background: teamColor(c.team) }} />
                    <strong style={{ color: '#fff' }}>{c.team}</strong>
                  </td>
                  <td className="col-center"><strong className="pts">{c.points}</strong></td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  )
}

const TABS = ['Drivers', 'Teams', 'Races', 'Results', 'Standings']

export default function App() {
  const [tab, setTab] = useState('Drivers')
  const { driverStandings, constructorStandings } = useStandings()
  const leader = driverStandings?.[0]

  return (
    <div className="app">
      <header className="header">
        <div className="header-brand">
          <div className="f1-logo">F<span>1</span></div>
          <div className="header-text">
            <span className="header-title">Formula 1</span>
            <span className="header-sub">2024 Season · EDEM MDA2526</span>
          </div>
        </div>
        {leader && (
          <div className="header-leader">
            <span className="leader-label">Leader</span>
            <span className="leader-driver">
              <span className="drv-code" style={{ color: '#fff', marginRight: 6 }}>{leader.code}</span>
              {leader.name}
            </span>
            <span className="leader-pts">{leader.points} PTS</span>
          </div>
        )}
      </header>

      <nav className="nav">
        {TABS.map(t => (
          <button key={t} className={tab === t ? 'active' : ''} onClick={() => setTab(t)}>
            {t}
          </button>
        ))}
      </nav>

      <main className="content">
        {tab === 'Drivers'   && <DriversTable standings={driverStandings} />}
        {tab === 'Teams'     && <TeamsTable constructorStandings={constructorStandings} />}
        {tab === 'Races'     && <RacesTable />}
        {tab === 'Results'   && <ResultsTable />}
        {tab === 'Standings' && <StandingsTab driverStandings={driverStandings} constructorStandings={constructorStandings} />}
      </main>
    </div>
  )
}
