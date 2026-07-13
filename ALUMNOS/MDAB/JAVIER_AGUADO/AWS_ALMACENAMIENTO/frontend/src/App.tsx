import { Routes, Route, Navigate } from "react-router-dom";
import { Layout } from "./components/Layout";
import { AirplanesPage } from "./pages/AirplanesPage";
import { FlightsPage } from "./pages/FlightsPage";
import { PassengersPage } from "./pages/PassengersPage";

export default function App() {
  return (
    <Layout>
      <Routes>
        <Route path="/" element={<Navigate to="/airplanes" replace />} />
        <Route path="/airplanes" element={<AirplanesPage />} />
        <Route path="/flights" element={<FlightsPage />} />
        <Route path="/passengers" element={<PassengersPage />} />
      </Routes>
    </Layout>
  );
}
