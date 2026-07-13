import { useEffect, useState } from "react";
import { fetchResults, registerResult } from "../api";

export default function Results() {
  const [results, setResults] = useState([]);
  const [msg, setMsg] = useState("");
  const [form, setForm] = useState({
    result_id: "", race_id: "", driver: "", position: "", points: "", status: "Finished"
  });

  useEffect(() => {
    fetchResults().then(setResults);
  }, []);

  function handleChange(e) {
    setForm({ ...form, [e.target.name]: e.target.value });
  }

  async function handleSubmit(e) {
    e.preventDefault();
    const res = await registerResult({
      ...form,
      position: parseInt(form.position),
      points: parseInt(form.points),
    });
    setMsg(res.message || res.detail);
    fetchResults().then(setResults);
  }

  return (
    <div>
      <h2>Resultados</h2>

      <form onSubmit={handleSubmit}>
        <h3>Registrar resultado</h3>
        <input name="result_id" placeholder="ID (ej. RES-041)" value={form.result_id} onChange={handleChange} required />
        <input name="race_id" placeholder="ID carrera (ej. R-001)" value={form.race_id} onChange={handleChange} required />
        <input name="driver" placeholder="Nombre del piloto" value={form.driver} onChange={handleChange} required />
        <input name="position" placeholder="Posicion (0 si DNF)" value={form.position} onChange={handleChange} required />
        <input name="points" placeholder="Puntos" value={form.points} onChange={handleChange} required />
        <select name="status" value={form.status} onChange={handleChange}>
          <option value="Finished">Finished</option>
          <option value="DNF">DNF</option>
          <option value="DNS">DNS</option>
        </select>
        <button type="submit">Registrar</button>
        {msg && <p className="success">{msg}</p>}
      </form>

      <table>
        <thead>
          <tr>
            <th>ID</th>
            <th>Carrera</th>
            <th>Piloto</th>
            <th>Posicion</th>
            <th>Puntos</th>
            <th>Estado</th>
          </tr>
        </thead>
        <tbody>
          {results.map((r) => (
            <tr key={r.result_id}>
              <td>{r.result_id}</td>
              <td>{r.race_id}</td>
              <td>{r.driver}</td>
              <td>{r.position || "-"}</td>
              <td>{r.points}</td>
              <td>
                <span className={`badge ${r.status.toLowerCase()}`}>{r.status}</span>
              </td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
