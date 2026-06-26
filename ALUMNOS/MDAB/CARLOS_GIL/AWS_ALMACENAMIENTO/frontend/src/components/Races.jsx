import { useEffect, useState } from "react";
import { fetchRaces, registerRace } from "../api";

export default function Races() {
  const [races, setRaces] = useState([]);
  const [msg, setMsg] = useState("");
  const [form, setForm] = useState({
    race_id: "", name: "", circuit: "", date: "", laps: "", total_distance_km: ""
  });

  useEffect(() => {
    fetchRaces().then(setRaces);
  }, []);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const res = await registerRace({
      ...form,
      laps: parseInt(form.laps),
      total_distance_km: parseInt(form.total_distance_km),
    });
    setMsg(res.message || res.detail);
    fetchRaces().then(setRaces);
  }

  return (
    <div>
      <h2>Carreras</h2>

      <form onSubmit={handleSubmit}>
        <h3>Registrar carrera</h3>
        <input name="race_id" placeholder="ID (ej. R-011)" value={form.race_id} onChange={handleChange} required />
        <input name="name" placeholder="Nombre del GP" value={form.name} onChange={handleChange} required />
        <input name="circuit" placeholder="Circuito" value={form.circuit} onChange={handleChange} required />
        <input name="date" type="date" value={form.date} onChange={handleChange} required />
        <input name="laps" placeholder="Vueltas" value={form.laps} onChange={handleChange} required />
        <input name="total_distance_km" placeholder="Distancia (km)" value={form.total_distance_km} onChange={handleChange} required />
        <button type="submit">Registrar</button>
        {msg && <p className="success">{msg}</p>}
      </form>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Gran Premio</th>
            <th>Circuito</th>
            <th>Fecha</th>
            <th>Vueltas</th>
            <th>Distancia</th>
          </tr>
        </thead>
        <tbody>
          {races.map((r) => (
            <tr key={r.race_id}>
              <td>{r.race_id}</td>
              <td>{r.name}</td>
              <td>{r.circuit}</td>
              <td>{r.date}</td>
              <td>{r.laps}</td>
              <td>{r.total_distance_km} km</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
