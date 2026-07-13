"""Normaliza los datos de `initial_info.py` a filas listas para insertar.

El fichero `initial_info.py` está en la raíz del proyecto; lo importamos
añadiendo la raíz al path para no duplicar los datos de partida.
"""
import os
import sys

_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if _ROOT not in sys.path:
    sys.path.insert(0, _ROOT)

from initial_info import airplanes, flights, passengers  # noqa: E402


def airplane_rows():
    return [
        (
            a["plateNumber"],
            a["type"],
            a["lastMaintenanceDate"],
            a["nextMaintenanceDate"],
            a["capacity"],
            a["ownerId"],
            a["ownerName"],
            a["hangarId"],
            a["fuel_capacity"],
        )
        for a in airplanes
    ]


def passenger_rows():
    return [
        (
            p["passengerId"],
            p["name"],
            p["nationalId"],
            p["dateOfBirth"],
        )
        for p in passengers
    ]


def flight_rows():
    return [
        (
            f["flightId"],
            f["plateNumber"],
            f["arrivalTime"],
            f["departureTime"],
            f["fuelConsumption"],
            f["occupiedSeats"],
            f["origin"],
            f["destination"],
        )
        for f in flights
    ]


def flight_passenger_rows():
    """Relación N:M entre vuelos y pasajeros, con el estado del embarque."""
    rows = []
    for f in flights:
        for passenger_id, status in f["passengerIds"]:
            rows.append((f["flightId"], passenger_id, status))
    return rows
