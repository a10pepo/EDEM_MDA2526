import { Link } from "react-router-dom";

export function Layout({ children }: { children: React.ReactNode }) {
  return (
    <div className="min-h-screen bg-background">
      <nav className="border-b px-6 py-3 flex gap-6 items-center">
        <span className="font-bold text-lg">Aerodrome</span>
        <Link to="/airplanes" className="text-sm hover:underline">Airplanes</Link>
        <Link to="/flights" className="text-sm hover:underline">Flights</Link>
        <Link to="/passengers" className="text-sm hover:underline">Passengers</Link>
      </nav>
      <main className="p-6">{children}</main>
    </div>
  );
}
