import {
  Activity,
  AlertTriangle,
  Bell,
  CalendarDays,
  CheckCircle2,
  CirclePlus,
  ClipboardList,
  Cloud,
  Database,
  Filter,
  LayoutDashboard,
  MapPin,
  RefreshCcw,
  Search,
  Shield,
  Trophy,
  UserCheck,
  Users,
  XCircle,
} from "lucide-react";
import { useEffect, useMemo, useState } from "react";
import { loadFootballData } from "./api/client.js";

const positionLabels = {
  goalkeeper: "Portero",
  defender: "Defensa",
  midfielder: "Centrocampista",
  forward: "Delantero",
};

const statusLabels = {
  available: "Disponible",
  injured: "Lesionado",
  suspended: "Sancionado",
  called: "Convocado",
  confirmed: "Confirmado",
  absent: "Ausente",
};

const navItems = [
  { id: "overview", label: "Panel", icon: LayoutDashboard },
  { id: "players", label: "Jugadores", icon: Users },
  { id: "matches", label: "Partidos", icon: CalendarDays },
  { id: "callups", label: "Convocatoria", icon: ClipboardList },
  { id: "alerts", label: "Alertas", icon: Bell },
];

const initialPlayerForm = {
  name: "",
  age: "21",
  position: "midfielder",
  status: "available",
  last_medical_review: new Date().toISOString().slice(0, 10),
};

function formatDate(value) {
  return new Intl.DateTimeFormat("es-ES", {
    day: "2-digit",
    month: "short",
    year: "numeric",
  }).format(new Date(`${value}T00:00:00`));
}

function daysSince(value) {
  const reviewDate = new Date(`${value}T00:00:00`);
  const today = new Date();
  const diff = today.getTime() - reviewDate.getTime();
  return Math.max(0, Math.floor(diff / 86400000));
}

function getInitials(name) {
  return name
    .split(" ")
    .slice(0, 2)
    .map((part) => part[0])
    .join("")
    .toUpperCase();
}

function summarizeMatches(matches, callups) {
  return matches
    .map((match) => {
      const matchCallups = callups.filter((callup) => callup.match_id === match.id);
      const confirmed = matchCallups.filter(
        (callup) => callup.callup_status === "confirmed",
      ).length;
      const total = matchCallups.length;
      const free = Math.max(0, match.max_callups - total);

      return {
        ...match,
        total_callups: total,
        confirmed_players: confirmed,
        free_spots: free,
        free_percentage: free / match.max_callups,
      };
    })
    .sort((a, b) => a.match_date.localeCompare(b.match_date));
}

function enrichCallups(callups, players) {
  const playersById = new Map(players.map((player) => [player.id, player]));

  return callups.map((callup) => {
    const player = playersById.get(callup.player_id);
    return {
      ...callup,
      player_name: callup.player_name ?? player?.name ?? "Jugador",
      position: callup.position ?? player?.position ?? "midfielder",
      player_status: callup.player_status ?? player?.status ?? "available",
    };
  });
}

function buildAlerts(players, matches) {
  const alerts = [];

  matches.forEach((match) => {
    if (match.confirmed_players < 11) {
      alerts.push({
        id: `confirmed-${match.id}`,
        type: "Partido",
        severity: "critical",
        title: `${match.opponent} necesita titulares`,
        detail: `${match.confirmed_players} confirmados de 11 minimos para el ${formatDate(match.match_date)}.`,
      });
    }

    if (match.free_percentage > 0.1) {
      alerts.push({
        id: `free-${match.id}`,
        type: "Convocatoria",
        severity: "warning",
        title: `${match.opponent} tiene huecos libres`,
        detail: `${match.free_spots} plazas libres de ${match.max_callups} (${Math.round(
          match.free_percentage * 100,
        )}%).`,
      });
    }
  });

  players.forEach((player) => {
    const reviewDays = daysSince(player.last_medical_review);
    if (reviewDays > 365) {
      alerts.push({
        id: `medical-${player.id}`,
        type: "Revision medica",
        severity: "warning",
        title: `${player.name} necesita revision`,
        detail: `${reviewDays} dias desde la ultima revision.`,
      });
    }
  });

  return alerts;
}

function groupLineup(callups) {
  const confirmed = callups
    .filter((callup) => callup.callup_status === "confirmed")
    .slice(0, 11);

  const byPosition = {
    goalkeeper: confirmed.filter((callup) => callup.position === "goalkeeper"),
    defender: confirmed.filter((callup) => callup.position === "defender"),
    midfielder: confirmed.filter((callup) => callup.position === "midfielder"),
    forward: confirmed.filter((callup) => callup.position === "forward"),
  };

  return [
    byPosition.forward,
    byPosition.midfielder,
    byPosition.defender,
    byPosition.goalkeeper,
  ].map((line) => (line.length ? line : []));
}

function StatusBadge({ value }) {
  return <span className={`status-badge status-${value}`}>{statusLabels[value]}</span>;
}

function MetricCard({ icon: Icon, label, value, note, tone = "neutral" }) {
  return (
    <article className={`metric-card metric-${tone}`}>
      <div className="metric-icon" aria-hidden="true">
        <Icon size={20} />
      </div>
      <div>
        <p>{label}</p>
        <strong>{value}</strong>
        <span>{note}</span>
      </div>
    </article>
  );
}

function SectionTitle({ icon: Icon, title, action }) {
  return (
    <div className="section-title">
      <div>
        <Icon size={20} aria-hidden="true" />
        <h2>{title}</h2>
      </div>
      {action}
    </div>
  );
}

function SegmentedControl({ label, value, options, onChange }) {
  return (
    <div className="segmented" aria-label={label}>
      {options.map((option) => (
        <button
          key={option.value}
          className={value === option.value ? "active" : ""}
          type="button"
          onClick={() => onChange(option.value)}
        >
          {option.label}
        </button>
      ))}
    </div>
  );
}

function Overview({ alerts, callups, matches, players, selectedMatch, onOpenCallups }) {
  const availablePlayers = players.filter((player) => player.status === "available");
  const injuredPlayers = players.filter((player) => player.status === "injured");
  const selectedCallups = callups.filter(
    (callup) => callup.match_id === selectedMatch?.id,
  );
  const lineup = groupLineup(selectedCallups);

  return (
    <div className="view-stack">
      <section className="matchday-panel">
        <div className="matchday-copy">
          <span className="eyebrow">Football Callup Manager</span>
          <h1>{selectedMatch?.opponent ?? "Sin partidos registrados"}</h1>
          {selectedMatch ? (
            <div className="match-meta">
              <span>
                <CalendarDays size={16} aria-hidden="true" />
                {formatDate(selectedMatch.match_date)}
              </span>
              <span>
                <MapPin size={16} aria-hidden="true" />
                {selectedMatch.stadium}
              </span>
            </div>
          ) : null}
          <button className="primary-action" type="button" onClick={onOpenCallups}>
            <ClipboardList size={18} aria-hidden="true" />
            Ver convocatoria
          </button>
        </div>

        <div className="pitch-visual" aria-label="Alineacion confirmada">
          <div className="pitch-center" />
          {lineup.map((line, index) => (
            <div className="pitch-line" key={`line-${index}`}>
              {line.length ? (
                line.map((callup) => (
                  <span
                    className="player-dot"
                    key={callup.id}
                    title={`${callup.player_name} - ${positionLabels[callup.position]}`}
                  >
                    {getInitials(callup.player_name)}
                  </span>
                ))
              ) : (
                <span className="empty-line">Pendiente</span>
              )}
            </div>
          ))}
        </div>
      </section>

      <section className="metrics-grid" aria-label="Resumen">
        <MetricCard
          icon={Users}
          label="Jugadores"
          value={players.length}
          note={`${availablePlayers.length} disponibles`}
          tone="green"
        />
        <MetricCard
          icon={CalendarDays}
          label="Partidos"
          value={matches.length}
          note="Calendario activo"
          tone="blue"
        />
        <MetricCard
          icon={UserCheck}
          label="Confirmados"
          value={selectedMatch?.confirmed_players ?? 0}
          note={`Maximo ${selectedMatch?.max_callups ?? 0}`}
          tone="amber"
        />
        <MetricCard
          icon={AlertTriangle}
          label="Alertas"
          value={alerts.length}
          note={`${injuredPlayers.length} lesionados`}
          tone="red"
        />
      </section>

      <section className="content-grid two-columns">
        <div className="surface">
          <SectionTitle icon={Trophy} title="Proximos Partidos" />
          <div className="compact-list">
            {matches.slice(0, 4).map((match) => (
              <div className="match-row" key={match.id}>
                <div>
                  <strong>{match.opponent}</strong>
                  <span>{formatDate(match.match_date)}</span>
                </div>
                <div className="mini-meter" aria-hidden="true">
                  <span
                    style={{
                      width: `${Math.min(100, (match.confirmed_players / 11) * 100)}%`,
                    }}
                  />
                </div>
                <b>{match.confirmed_players}/11</b>
              </div>
            ))}
          </div>
        </div>

        <div className="surface">
          <SectionTitle icon={Bell} title="Alertas Activas" />
          <div className="alert-list compact-alerts">
            {alerts.slice(0, 4).map((alert) => (
              <div className={`alert-item alert-${alert.severity}`} key={alert.id}>
                <AlertTriangle size={18} aria-hidden="true" />
                <div>
                  <strong>{alert.title}</strong>
                  <span>{alert.detail}</span>
                </div>
              </div>
            ))}
            {!alerts.length ? (
              <div className="empty-state">
                <CheckCircle2 size={22} aria-hidden="true" />
                <span>No hay alertas activas.</span>
              </div>
            ) : null}
          </div>
        </div>
      </section>
    </div>
  );
}

function PlayersView({ players, onAddPlayer }) {
  const [query, setQuery] = useState("");
  const [position, setPosition] = useState("all");
  const [status, setStatus] = useState("all");
  const [formOpen, setFormOpen] = useState(false);
  const [form, setForm] = useState(initialPlayerForm);

  const filteredPlayers = players.filter((player) => {
    const matchesQuery = player.name.toLowerCase().includes(query.toLowerCase());
    const matchesPosition = position === "all" || player.position === position;
    const matchesStatus = status === "all" || player.status === status;
    return matchesQuery && matchesPosition && matchesStatus;
  });

  function updateForm(event) {
    const { name, value } = event.target;
    setForm((current) => ({ ...current, [name]: value }));
  }

  function submitPlayer(event) {
    event.preventDefault();
    if (!form.name.trim()) {
      return;
    }

    onAddPlayer({
      ...form,
      id: Date.now(),
      age: Number(form.age),
      name: form.name.trim(),
    });
    setForm(initialPlayerForm);
    setFormOpen(false);
  }

  return (
    <div className="view-stack">
      <SectionTitle
        icon={Users}
        title="Jugadores"
        action={
          <button
            className="icon-text-button"
            type="button"
            onClick={() => setFormOpen((open) => !open)}
            title="Crear jugador"
          >
            <CirclePlus size={18} aria-hidden="true" />
            Nuevo jugador
          </button>
        }
      />

      {formOpen ? (
        <form className="surface form-grid" onSubmit={submitPlayer}>
          <label>
            Nombre
            <input name="name" value={form.name} onChange={updateForm} />
          </label>
          <label>
            Edad
            <input
              max="45"
              min="15"
              name="age"
              type="number"
              value={form.age}
              onChange={updateForm}
            />
          </label>
          <label>
            Posicion
            <select name="position" value={form.position} onChange={updateForm}>
              {Object.entries(positionLabels).map(([value, label]) => (
                <option key={value} value={value}>
                  {label}
                </option>
              ))}
            </select>
          </label>
          <label>
            Estado
            <select name="status" value={form.status} onChange={updateForm}>
              {["available", "injured", "suspended"].map((value) => (
                <option key={value} value={value}>
                  {statusLabels[value]}
                </option>
              ))}
            </select>
          </label>
          <label>
            Revision medica
            <input
              name="last_medical_review"
              type="date"
              value={form.last_medical_review}
              onChange={updateForm}
            />
          </label>
          <button className="primary-action form-submit" type="submit">
            <CheckCircle2 size={18} aria-hidden="true" />
            Guardar
          </button>
        </form>
      ) : null}

      <div className="toolbar">
        <label className="search-box">
          <Search size={18} aria-hidden="true" />
          <input
            placeholder="Buscar jugador"
            value={query}
            onChange={(event) => setQuery(event.target.value)}
          />
        </label>
        <SegmentedControl
          label="Filtrar por posicion"
          value={position}
          options={[
            { value: "all", label: "Todos" },
            { value: "goalkeeper", label: "POR" },
            { value: "defender", label: "DEF" },
            { value: "midfielder", label: "MED" },
            { value: "forward", label: "DEL" },
          ]}
          onChange={setPosition}
        />
        <SegmentedControl
          label="Filtrar por estado"
          value={status}
          options={[
            { value: "all", label: "Todos" },
            { value: "available", label: "OK" },
            { value: "injured", label: "Lesion" },
            { value: "suspended", label: "Sancion" },
          ]}
          onChange={setStatus}
        />
      </div>

      <div className="surface table-shell">
        <table>
          <thead>
            <tr>
              <th>Jugador</th>
              <th>Edad</th>
              <th>Posicion</th>
              <th>Estado</th>
              <th>Revision</th>
            </tr>
          </thead>
          <tbody>
            {filteredPlayers.map((player) => (
              <tr key={player.id}>
                <td>
                  <div className="identity-cell">
                    <span>{getInitials(player.name)}</span>
                    <strong>{player.name}</strong>
                  </div>
                </td>
                <td>{player.age}</td>
                <td>{positionLabels[player.position]}</td>
                <td>
                  <StatusBadge value={player.status} />
                </td>
                <td>{formatDate(player.last_medical_review)}</td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function MatchesView({ matches }) {
  return (
    <div className="view-stack">
      <SectionTitle icon={CalendarDays} title="Partidos" />
      <div className="surface table-shell">
        <table>
          <thead>
            <tr>
              <th>Rival</th>
              <th>Fecha</th>
              <th>Estadio</th>
              <th>Confirmados</th>
              <th>Plazas libres</th>
            </tr>
          </thead>
          <tbody>
            {matches.map((match) => (
              <tr key={match.id}>
                <td>
                  <strong>{match.opponent}</strong>
                </td>
                <td>{formatDate(match.match_date)}</td>
                <td>{match.stadium}</td>
                <td>
                  <div className="meter-cell">
                    <span>{match.confirmed_players}/11</span>
                    <div className="mini-meter" aria-hidden="true">
                      <span
                        style={{
                          width: `${Math.min(
                            100,
                            (match.confirmed_players / 11) * 100,
                          )}%`,
                        }}
                      />
                    </div>
                  </div>
                </td>
                <td>
                  <b>{match.free_spots}</b> de {match.max_callups}
                </td>
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}

function CallupsView({ callups, matches, selectedMatchId, setSelectedMatchId }) {
  const selectedMatch = matches.find((match) => match.id === selectedMatchId);
  const selectedCallups = callups
    .filter((callup) => callup.match_id === selectedMatchId)
    .sort((a, b) => a.shirt_number - b.shirt_number);

  return (
    <div className="content-grid callup-layout">
      <aside className="surface match-picker">
        <SectionTitle icon={Filter} title="Partido" />
        <div className="match-picker-list">
          {matches.map((match) => (
            <button
              className={match.id === selectedMatchId ? "active" : ""}
              key={match.id}
              type="button"
              onClick={() => setSelectedMatchId(match.id)}
            >
              <span>{match.opponent}</span>
              <small>{formatDate(match.match_date)}</small>
            </button>
          ))}
        </div>
      </aside>

      <section className="view-stack">
        <SectionTitle icon={ClipboardList} title="Convocatoria" />
        {selectedMatch ? (
          <div className="surface callup-summary">
            <div>
              <span className="eyebrow">Rival</span>
              <h3>{selectedMatch.opponent}</h3>
              <p>
                {formatDate(selectedMatch.match_date)} · {selectedMatch.stadium}
              </p>
            </div>
            <div className="callup-stat">
              <strong>{selectedMatch.confirmed_players}</strong>
              <span>confirmados</span>
            </div>
            <div className="callup-stat">
              <strong>{selectedMatch.free_spots}</strong>
              <span>plazas libres</span>
            </div>
          </div>
        ) : null}

        <div className="surface table-shell">
          <table>
            <thead>
              <tr>
                <th>Dorsal</th>
                <th>Jugador</th>
                <th>Posicion</th>
                <th>Estado jugador</th>
                <th>Convocatoria</th>
              </tr>
            </thead>
            <tbody>
              {selectedCallups.map((callup) => (
                <tr key={callup.id}>
                  <td>
                    <span className="shirt-number">{callup.shirt_number}</span>
                  </td>
                  <td>
                    <strong>{callup.player_name}</strong>
                  </td>
                  <td>{positionLabels[callup.position]}</td>
                  <td>
                    <StatusBadge value={callup.player_status} />
                  </td>
                  <td>
                    <StatusBadge value={callup.callup_status} />
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>
      </section>
    </div>
  );
}

function AlertsView({ alerts }) {
  return (
    <div className="view-stack">
      <SectionTitle icon={Bell} title="Alertas" />
      <div className="alert-list">
        {alerts.map((alert) => (
          <article className={`alert-card alert-${alert.severity}`} key={alert.id}>
            {alert.severity === "critical" ? (
              <XCircle size={22} aria-hidden="true" />
            ) : (
              <AlertTriangle size={22} aria-hidden="true" />
            )}
            <div>
              <span>{alert.type}</span>
              <h3>{alert.title}</h3>
              <p>{alert.detail}</p>
            </div>
          </article>
        ))}
        {!alerts.length ? (
          <div className="surface empty-state large-empty">
            <CheckCircle2 size={28} aria-hidden="true" />
            <strong>No hay alertas activas.</strong>
          </div>
        ) : null}
      </div>
    </div>
  );
}

function App() {
  const [activeView, setActiveView] = useState("overview");
  const [loading, setLoading] = useState(true);
  const [dataSource, setDataSource] = useState("mock");
  const [players, setPlayers] = useState([]);
  const [matches, setMatches] = useState([]);
  const [callups, setCallups] = useState([]);
  const [selectedMatchId, setSelectedMatchId] = useState(null);

  async function refreshData() {
    setLoading(true);
    const data = await loadFootballData();
    setPlayers(data.players);
    setMatches(data.matches);
    setCallups(data.callups);
    setDataSource(data.source);
    setSelectedMatchId((current) => current ?? data.matches[0]?.id ?? null);
    setLoading(false);
  }

  useEffect(() => {
    refreshData();
  }, []);

  const enrichedCallups = useMemo(
    () => enrichCallups(callups, players),
    [callups, players],
  );
  const summarizedMatches = useMemo(
    () => summarizeMatches(matches, enrichedCallups),
    [matches, enrichedCallups],
  );
  const alerts = useMemo(
    () => buildAlerts(players, summarizedMatches),
    [players, summarizedMatches],
  );
  const selectedMatch =
    summarizedMatches.find((match) => match.id === selectedMatchId) ??
    summarizedMatches[0];

  useEffect(() => {
    if (!selectedMatchId && summarizedMatches[0]) {
      setSelectedMatchId(summarizedMatches[0].id);
    }
  }, [selectedMatchId, summarizedMatches]);

  function addLocalPlayer(player) {
    setPlayers((current) => [player, ...current]);
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-mark">
            <Shield size={22} aria-hidden="true" />
          </div>
          <div>
            <strong>FC Manager</strong>
            <span>Callup Control</span>
          </div>
        </div>

        <nav className="main-nav" aria-label="Secciones">
          {navItems.map((item) => {
            const Icon = item.icon;
            return (
              <button
                className={activeView === item.id ? "active" : ""}
                key={item.id}
                type="button"
                onClick={() => setActiveView(item.id)}
                title={item.label}
              >
                <Icon size={19} aria-hidden="true" />
                <span>{item.label}</span>
              </button>
            );
          })}
        </nav>

        <div className="sidebar-status">
          {dataSource === "api" ? (
            <Cloud size={18} aria-hidden="true" />
          ) : (
            <Database size={18} aria-hidden="true" />
          )}
          <span>{dataSource === "api" ? "AWS RDS" : "Demo local"}</span>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <span className="eyebrow">Equipo senior</span>
            <h1>Gestion de convocatorias</h1>
          </div>
          <button
            className="icon-button"
            type="button"
            onClick={refreshData}
            title="Actualizar datos"
          >
            <RefreshCcw size={19} aria-hidden="true" />
          </button>
        </header>

        {loading ? (
          <div className="loading-state">
            <Activity size={24} aria-hidden="true" />
            <span>Cargando datos...</span>
          </div>
        ) : (
          <>
            {activeView === "overview" ? (
              <Overview
                alerts={alerts}
                callups={enrichedCallups}
                matches={summarizedMatches}
                players={players}
                selectedMatch={selectedMatch}
                onOpenCallups={() => setActiveView("callups")}
              />
            ) : null}

            {activeView === "players" ? (
              <PlayersView players={players} onAddPlayer={addLocalPlayer} />
            ) : null}

            {activeView === "matches" ? (
              <MatchesView matches={summarizedMatches} />
            ) : null}

            {activeView === "callups" ? (
              <CallupsView
                callups={enrichedCallups}
                matches={summarizedMatches}
                selectedMatchId={selectedMatch?.id}
                setSelectedMatchId={setSelectedMatchId}
              />
            ) : null}

            {activeView === "alerts" ? <AlertsView alerts={alerts} /> : null}
          </>
        )}
      </main>
    </div>
  );
}

export default App;
