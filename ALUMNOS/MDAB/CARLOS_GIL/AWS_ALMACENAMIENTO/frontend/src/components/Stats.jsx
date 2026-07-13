import { useEffect, useState } from "react";

const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export default function Stats() {
  const [summary, setSummary] = useState(null);
  const [points, setPoints] = useState([]);
  const [circuits, setCircuits] = useState([]);

  useEffect(() => {
    fetch(`${API_URL}/stats/summary`).then(r => r.json()).then(setSummary);
    fetch(`${API_URL}/stats/points-per-pilot`).then(r => r.json()).then(setPoints);
    fetch(`${API_URL}/stats/wins-per-circuit`).then(r => r.json()).then(setCircuits);
  }, []);

  return (
    <div>
      <h2>Resumen</h2>
      {summary && (
        <table style={{ marginBottom: 32 }}>
          <tbody>
            <tr><td>Total pilotos</td><td><strong>{summary.total_pilots}</strong></td></tr>
            <tr><td>Total carreras</td><td><strong>{summary.total_races}</strong></td></tr>
            <tr><td>Total resultados</td><td><strong>{summary.total_results}</strong></td></tr>
            <tr><td>Piloto con mas victorias</td><td><strong>{summary.most_wins_driver}</strong></td></tr>
          </tbody>
        </table>
      )}

      <h2>Puntos por piloto</h2>
      <table>
        <thead>
          <tr>
            <th>Piloto</th>
            <th>Carreras</th>
            <th>Victorias</th>
            <th>Puntos totales</th>
            <th>Media puntos</th>
          </tr>
        </thead>
        <tbody>
          {points.map((p) => (
            <tr key={p.driver}>
              <td>{p.driver}</td>
              <td>{p.races}</td>
              <td>{p.wins}</td>
              <td>{p.total_points}</td>
              <td>{p.avg_points}</td>
            </tr>
          ))}
        </tbody>
      </table>

      <h2>Carreras por circuito</h2>
      <table>
        <thead>
          <tr>
            <th>Circuito</th>
            <th>Total carreras</th>
          </tr>
        </thead>
        <tbody>
          {circuits.map((c) => (
            <tr key={c.circuit}>
              <td>{c.circuit}</td>
              <td>{c.total_races}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
