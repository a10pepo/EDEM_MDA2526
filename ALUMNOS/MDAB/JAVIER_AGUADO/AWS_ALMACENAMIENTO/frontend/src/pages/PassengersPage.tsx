import { useState } from "react";
import { useQuery, useMutation, useQueryClient } from "@tanstack/react-query";
import { getPassengers, createPassenger } from "../api/passengers";
import type { PassengerCreate } from "../types";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";
import {
  Table, TableBody, TableCell, TableHead, TableHeader, TableRow,
} from "@/components/ui/table";
import {
  Dialog, DialogContent, DialogHeader, DialogTitle, DialogTrigger,
} from "@/components/ui/dialog";

const emptyForm: PassengerCreate = {
  passenger_id: "", name: "", national_id: "", date_of_birth: "",
};

export function PassengersPage() {
  const qc = useQueryClient();
  const { data: passengers = [], isLoading } = useQuery({
    queryKey: ["passengers"],
    queryFn: getPassengers,
  });
  const [form, setForm] = useState<PassengerCreate>(emptyForm);
  const [open, setOpen] = useState(false);

  const mutation = useMutation({
    mutationFn: createPassenger,
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ["passengers"] });
      setOpen(false);
      setForm(emptyForm);
    },
  });

  const set = (k: keyof PassengerCreate) => (e: React.ChangeEvent<HTMLInputElement>) =>
    setForm((f) => ({ ...f, [k]: e.target.value }));

  if (isLoading) return <p>Loading...</p>;

  return (
    <div>
      <div className="flex justify-between items-center mb-4">
        <h1 className="text-2xl font-bold">Passengers</h1>
        <Dialog open={open} onOpenChange={setOpen}>
          <DialogTrigger render={<Button />}>Register Passenger</DialogTrigger>
          <DialogContent>
            <DialogHeader><DialogTitle>Register New Passenger</DialogTitle></DialogHeader>
            <div className="grid gap-3">
              {(["passenger_id", "name", "national_id"] as const).map((k) => (
                <div key={k}>
                  <Label>{k}</Label>
                  <Input value={form[k]} onChange={set(k)} />
                </div>
              ))}
              <div>
                <Label>date_of_birth</Label>
                <Input type="date" value={form.date_of_birth} onChange={set("date_of_birth")} />
              </div>
              <Button onClick={() => mutation.mutate(form)} disabled={mutation.isPending}>Save</Button>
            </div>
          </DialogContent>
        </Dialog>
      </div>
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>ID</TableHead>
            <TableHead>Name</TableHead>
            <TableHead>National ID</TableHead>
            <TableHead>Date of Birth</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {passengers.map((p) => (
            <TableRow key={p.passenger_id}>
              <TableCell>{p.passenger_id}</TableCell>
              <TableCell>{p.name}</TableCell>
              <TableCell>{p.national_id}</TableCell>
              <TableCell>{p.date_of_birth}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  );
}
