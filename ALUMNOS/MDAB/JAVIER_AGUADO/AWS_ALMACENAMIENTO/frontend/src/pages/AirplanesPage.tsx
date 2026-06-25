import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getAirplanes, createAirplane } from "../api/airplanes";
import type { AirplaneCreate } from "../types";
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

const emptyForm: AirplaneCreate = {
  plate_number: "", type: "", last_maintenance_date: "", next_maintenance_date: "",
  capacity: 0, owner_id: "", owner_name: "", hangar_id: "", fuel_capacity: 0,
};

export function AirplanesPage() {
  const qc = useQueryClient();
  const { data: airplanes = [], isLoading } = useQuery({
    queryKey: ["airplanes"],
    queryFn: getAirplanes,
  });
  const [form, setForm] = useState<AirplaneCreate>(emptyForm);
  const [open, setOpen] = useState(false);

  const mutation = useMutation({
    mutationFn: createAirplane,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["airplanes"] });
      setOpen(false);
      setForm(emptyForm);
    },
  });

  const set = (k: keyof AirplaneCreate) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({
      ...f,
      [k]: e.target.type === "number" ? Number(e.target.value) : e.target.value,
    }));

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Airplanes in Hangars</h1>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Register Airplane</DialogTrigger>
          <DialogContent>
            <DialogHeader><DialogTitle>Register New Airplane</DialogTitle></DialogHeader>
            <div className="grid gap-3">
              {(["plate_number", "type", "owner_id", "owner_name", "hangar_id"] as const).map((k) => (
                <div key={k}>
                  <Label>{k}</Label>
                  <Input value={form[k] as string} onChange={set(k)} />
                </div>
              ))}
              <div>
                <Label>last_maintenance_date</Label>
                <Input type="date" value={form.last_maintenance_date} onChange={set("last_maintenance_date")} />
              </div>
              <div>
                <Label>next_maintenance_date</Label>
                <Input type="date" value={form.next_maintenance_date} onChange={set("next_maintenance_date")} />
              </div>
              <div>
                <Label>capacity</Label>
                <Input type="number" value={form.capacity} onChange={set("capacity")} />
              </div>
              <div>
                <Label>fuel_capacity</Label>
                <Input type="number" value={form.fuel_capacity} onChange={set("fuel_capacity")} />
              </div>
              <Button onClick={() => mutation.mutate(form)} disabled={mutation.isPending}>Save</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>Plate</TableHead>
            <TableHead>Type</TableHead>
            <TableHead>Owner</TableHead>
            <TableHead>Hangar</TableHead>
            <TableHead>Capacity</TableHead>
            <TableHead>Next Maintenance</TableHead>
            <TableHead>Status</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {airplanes.map((a) => (
            <TableRow key={a.plate_number}>
              <TableCell>{a.plate_number}</TableCell>
              <TableCell>{a.type}</TableCell>
              <TableCell>{a.owner_name}</TableCell>
              <TableCell>{a.hangar_id}</TableCell>
              <TableCell>{a.capacity}</TableCell>
              <TableCell>{a.next_maintenance_date} ({a.days_until_maintenance}d)</TableCell>
              <TableCell>
                <AlertBadge
                  alert={a.maintenance_alert}
                  label={a.maintenance_alert ? "Maintenance Soon" : "OK"}
                />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
