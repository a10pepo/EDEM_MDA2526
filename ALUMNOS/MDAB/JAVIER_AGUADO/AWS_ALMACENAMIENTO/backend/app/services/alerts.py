from datetime import date


def days_until_maintenance(next_maintenance_date: date, today: date = None) -> int:
    if today is None:
        today = date.today()
    return (next_maintenance_date - today).days


def maintenance_alert(next_maintenance_date: date, today: date = None) -> bool:
    return days_until_maintenance(next_maintenance_date, today) < 100


def calculate_empty_seats(capacity: int, occupied_seats: int) -> int:
    return capacity - occupied_seats


def empty_seats_alert(capacity: int, occupied_seats: int) -> bool:
    empty = calculate_empty_seats(capacity, occupied_seats)
    return empty > 0.1 * capacity


def fuel_alert(fuel_consumption: float, fuel_capacity: float) -> bool:
    return fuel_consumption > 0.1 * fuel_capacity
