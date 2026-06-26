import { useState } from "react";
import Pilots from "./components/Pilots";
import Races from "./components/Races";
import Results from "./components/Results";
import Alerts from "./components/Alerts";
import Stats from "./components/Stats";
import "./App.css";

const TABS = ["Pilotos", "Carreras", "Resultados", "Alertas", "Estadisticas"];

export default function App() {
  const [tab, setTab] = useState("Pilotos");

  return (
    <div className="app">
      <header className="header">
        <h1>Gestor F1</h1>
        <nav>
          {TABS.map((t) => (
            <button
              key={t}
              className={tab === t ? "active" : ""}
              onClick={() => setTab(t)}
            >
              {t}
            </button>
          ))}
        </nav>
      </header>
      <main className="main">
        {tab === "Pilotos" && <Pilots />}
        {tab === "Carreras" && <Races />}
        {tab === "Resultados" && <Results />}
        {tab === "Alertas" && <Alerts />}
        {tab === "Estadisticas" && <Stats />}
      </main>
    </div>
  );
}
