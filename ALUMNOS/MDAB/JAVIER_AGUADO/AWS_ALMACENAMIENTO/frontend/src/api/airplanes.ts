import client from "./client";
import type { Airplane, AirplaneCreate } from "../types";

export const getAirplanes = () =>
  client.get<Airplane[]>("/airplanes/").then((r) => r.data);

export const createAirplane = (data: AirplaneCreate) =>
  client.post<Airplane>("/airplanes/", data).then((r) => r.data);
