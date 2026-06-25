import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getFlights, createFlight } from "../api/flights";
import type { FlightCreate } from "../types";
import { AlertBadge } from "../components/AlertBadge";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";

const emptyForm: FlightCreate = {
  flight_id: "", plate_number: "", arrival_time: "", departure_time: "",
  fuel_consumption: 0, occupied_seats: 0, origin: "", destination: "", passengers: [],
};

export function FlightsPage() {
  const qc = useQueryClient();
  const { data: flights = [], isLoading } = useQuery({
    queryKey: ["flights"],
    queryFn: getFlights,
  });
  const [form, setForm] = useState<FlightCreate>(emptyForm);
  const [open, setOpen] = useState(false);

  const mutation = useMutation({
    mutationFn: createFlight,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["flights"] });
      setOpen(false);
      setForm(emptyForm);
    },
  });

  const set = (k: keyof FlightCreate) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({
      ...f,
      [k]: e.target.type === "number" ? Number(e.target.value) : e.target.value,
    }));

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Flights</h1>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Register Flight</DialogTrigger>
          <DialogContent>
            <DialogHeader><DialogTitle>Register New Flight</DialogTitle></DialogHeader>
            <div className="grid gap-3">
              {(["flight_id", "plate_number", "origin", "destination"] as const).map((k) => (
                <div key={k}>
                  <Label>{k}</Label>
                  <Input value={form[k] as string} onChange={set(k)} />
                </div>
              ))}
              <div>
                <Label>arrival_time</Label>
                <Input type="datetime-local" value={form.arrival_time} onChange={set("arrival_time")} />
              </div>
              <div>
                <Label>departure_time</Label>
                <Input type="datetime-local" value={form.departure_time} onChange={set("departure_time")} />
              </div>
              <div>
                <Label>fuel_consumption</Label>
                <Input type="number" value={form.fuel_consumption} onChange={set("fuel_consumption")} />
              </div>
              <div>
                <Label>occupied_seats</Label>
                <Input type="number" value={form.occupied_seats} onChange={set("occupied_seats")} />
              </div>
              <Button onClick={() => mutation.mutate(form)} disabled={mutation.isPending}>Save</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Flight ID</TableHead>
            <TableHead>Airplane</TableHead>
            <TableHead>Origin → Dest</TableHead>
            <TableHead>Arrival</TableHead>
            <TableHead>Empty Seats</TableHead>
            <TableHead>Fuel</TableHead>
            <TableHead>Occupancy</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {flights.map((f) => (
            <TableRow key={f.flight_id}>
              <TableCell>{f.flight_id}</TableCell>
              <TableCell>{f.plate_number}</TableCell>
              <TableCell>{f.origin} → {f.destination}</TableCell>
              <TableCell>{new Date(f.arrival_time).toLocaleString()}</TableCell>
              <TableCell>{f.empty_seats}</TableCell>
              <TableCell>
                <AlertBadge alert={f.fuel_alert} label={f.fuel_alert ? "High Fuel" : "OK"} />
              </TableCell>
              <TableCell>
                <AlertBadge
                  alert={f.empty_seats_alert}
                  label={f.empty_seats_alert ? "Low Occupancy" : "OK"}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
