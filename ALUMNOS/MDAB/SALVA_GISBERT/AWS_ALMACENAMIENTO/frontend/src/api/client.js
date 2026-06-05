import { mockCallups, mockMatches, mockPlayers } from "../data/mockData.js";

const API_BASE_URL = import.meta.env.VITE_API_BASE_URL ?? "/api";

async function fetchJson(path) {
  const response = await fetch(`${API_BASE_URL}${path}`);

  if (!response.ok) {
    throw new Error(`API request failed: ${response.status}`);
  }

  return response.json();
}

export async function loadFootballData() {
  try {
    const [players, matches, callups, alerts] = await Promise.all([
      fetchJson("/players"),
      fetchJson("/matches"),
      fetchJson("/callups"),
      fetchJson("/alerts"),
    ]);

    return {
      players,
      matches,
      callups,
      alerts,
      source: "api",
    };
  } catch {
    return {
      players: mockPlayers,
      matches: mockMatches,
      callups: mockCallups,
      alerts: [],
      source: "mock",
    };
  }
}
