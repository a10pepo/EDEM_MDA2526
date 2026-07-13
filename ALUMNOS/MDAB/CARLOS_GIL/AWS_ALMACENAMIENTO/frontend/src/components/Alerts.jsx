import { useEffect, useState } from "react";
import { fetchAlertLowDNF, fetchAlertRetired, fetchAlertDominant } from "../api";

export default function Alerts() {
  const [dnf, setDnf] = useState([]);
  const [retired, setRetired] = useState([]);
  const [dominant, setDominant] = useState([]);

  useEffect(() => {
    fetchAlertLowDNF().then(setDnf);
    fetchAlertRetired().then(setRetired);
    fetchAlertDominant().then(setDominant);
  }, []);

  return (
    <div>
      <h2>Tasa de DNF alta (&gt;10%)</h2>
      {dnf.length === 0 ? (
        <p className="loading">Sin alertas</p>
      ) : (
        dnf.map((p) => (
          <div className="alert-card" key={p.driver}>
            <span>{p.driver}</span> — {p.dnfs}/{p.total} DNFs ({p.dnf_pct}%)
          </div>
        ))
      )}

      <br />
      <h2>Pilotos retirados</h2>
      {retired.map((p) => (
        <div className="alert-card" key={p.driver}>
          <span>{p.driver}</span> — {p.years_active}
        </div>
      ))}

      <br />
      <h2>Pilotos dominantes (&gt;10% del record)</h2>
      {dominant.map((p) => (
        <div className="alert-card" key={p.driver}>
          <span>{p.driver}</span> — {p.wins} victorias ({p.pct}% del record)
        </div>
      ))}
    </div>
  );
}
