from datetime import date
from app.services.alerts import days_until_maintenance, maintenance_alert, calculate_empty_seats, empty_seats_alert, fuel_alert


def test_days_until_maintenance_positive():
    future = date(2026, 12, 31)
    today = date(2026, 5, 16)
    assert days_until_maintenance(future, today) == 229


def test_maintenance_alert_triggered():
    future = date(2026, 6, 1)
    today = date(2026, 5, 16)
    assert maintenance_alert(future, today) is True


def test_maintenance_alert_not_triggered():
    future = date(2027, 1, 1)
    today = date(2026, 5, 16)
    assert maintenance_alert(future, today) is False


def test_calculate_empty_seats_normal():
    assert calculate_empty_seats(capacity=9, occupied_seats=7) == 2


def test_calculate_empty_seats_full():
    assert calculate_empty_seats(capacity=9, occupied_seats=9) == 0


def test_empty_seats_alert_triggered():
    # 9 capacity, 7 occupied → 2 empty → 22% > 10%
    assert empty_seats_alert(capacity=9, occupied_seats=7) is True


def test_empty_seats_alert_not_triggered():
    # 9 capacity, 9 occupied → 0 empty
    assert empty_seats_alert(capacity=9, occupied_seats=9) is False


def test_fuel_alert_triggered():
    # 850 / 1000 = 85% > 10%
    assert fuel_alert(fuel_consumption=850, fuel_capacity=1000) is True


def test_fuel_alert_not_triggered():
    # 50 / 1000 = 5% < 10%
    assert fuel_alert(fuel_consumption=50, fuel_capacity=1000) is False
