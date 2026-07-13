const API_URL = import.meta.env.VITE_API_URL || "http://localhost:8000";

export async function fetchPilots() {
  const res = await fetch(`${API_URL}/pilots`);
  return res.json();
}

export async function fetchRaces() {
  const res = await fetch(`${API_URL}/races`);
  return res.json();
}

export async function fetchResults() {
  const res = await fetch(`${API_URL}/results`);
  return res.json();
}

export async function fetchAlertLowDNF() {
  const res = await fetch(`${API_URL}/alerts/high-dnf-rate`);
  return res.json();
}

export async function fetchAlertRetired() {
  const res = await fetch(`${API_URL}/alerts/retired-pilots`);
  return res.json();
}

export async function fetchAlertDominant() {
  const res = await fetch(`${API_URL}/alerts/dominant-pilots`);
  return res.json();
}

export async function registerPilot(data) {
  const res = await fetch(`${API_URL}/pilots`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function registerRace(data) {
  const res = await fetch(`${API_URL}/races`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}

export async function registerResult(data) {
  const res = await fetch(`${API_URL}/results`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(data),
  });
  return res.json();
}
