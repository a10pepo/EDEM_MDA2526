import client from "./client";
import type { Flight, FlightCreate } from "../types";

export const getFlights = () =>
  client.get<Flight[]>("/flights/").then((r) => r.data);

export const createFlight = (data: FlightCreate) =>
  client.post<Flight>("/flights/", data).then((r) => r.data);
