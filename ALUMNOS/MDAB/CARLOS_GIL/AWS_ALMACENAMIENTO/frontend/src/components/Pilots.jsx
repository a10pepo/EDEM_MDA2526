import { useEffect, useState } from "react";
import { fetchPilots, registerPilot } from "../api";

export default function Pilots() {
  const [pilots, setPilots] = useState([]);
  const [msg, setMsg] = useState("");
  const [form, setForm] = useState({
    rank: "", driver: "", nationality: "", wins: "",
    championships: "", years_active: "", team_most_wins_with: ""
  });

  useEffect(() => {
    fetchPilots().then(setPilots);
  }, []);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const res = await registerPilot({
      ...form,
      rank: parseInt(form.rank),
      wins: parseInt(form.wins),
      championships: parseInt(form.championships),
    });
    setMsg(res.message || res.detail);
    fetchPilots().then(setPilots);
  }

  return (
    <div>
      <h2>Pilotos</h2>

      <form onSubmit={handleSubmit}>
        <h3>Registrar piloto</h3>
        <input name="rank" placeholder="Ranking" value={form.rank} onChange={handleChange} required />
        <input name="driver" placeholder="Nombre" value={form.driver} onChange={handleChange} required />
        <input name="nationality" placeholder="Nacionalidad" value={form.nationality} onChange={handleChange} required />
        <input name="wins" placeholder="Victorias" value={form.wins} onChange={handleChange} required />
        <input name="championships" placeholder="Campeonatos" value={form.championships} onChange={handleChange} required />
        <input name="years_active" placeholder="Anos activo (ej. 2010-present)" value={form.years_active} onChange={handleChange} required />
        <input name="team_most_wins_with" placeholder="Equipo principal" value={form.team_most_wins_with} onChange={handleChange} required />
        <button type="submit">Registrar</button>
        {msg && <p className="success">{msg}</p>}
      </form>

      <table>
        <thead>
          <tr>
            <th>#</th>
            <th>Piloto</th>
            <th>Nacionalidad</th>
            <th>Victorias</th>
            <th>Campeonatos</th>
            <th>Equipo</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {pilots.map((p) => (
            <tr key={p.driver}>
              <td>{p.rank}</td>
              <td>{p.driver}</td>
              <td>{p.nationality}</td>
              <td>{p.wins}</td>
              <td>{p.championships}</td>
              <td>{p.team_most_wins_with}</td>
              <td>
                <span className={`badge ${p.years_active.includes("present") ? "activo" : "retirado"}`}>
                  {p.years_active.includes("present") ? "Activo" : "Retirado"}
                </span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
