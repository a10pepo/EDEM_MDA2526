"""
Cliente de Open-Meteo (gratuito, sin API key).
Descarga datos meteorologicos historicos por hora para una ubicacion.

API usada: https://archive-api.open-meteo.com
No requiere registro ni clave. Limite de uso no documentado pero
generoso para uso personal.
"""
import json
import logging
import urllib.request
import urllib.parse

from src import config

logger = logging.getLogger(__name__)

_BASE_URL  = "https://archive-api.open-meteo.com/v1/archive"
_VARIABLES = ",".join([
    "temperature_2m",
    "apparent_temperature",
    "relative_humidity_2m",
    "precipitation",
    "wind_speed_10m",
])


def fetch_weather_range(start_date: str, end_date: str) -> dict:
    """
    Descarga datos horarios para el rango de fechas indicado.
    Devuelve {(date_str, hour_int): {temp_c, feels_like_c, humidity_pct,
                                      precipitation_mm, wind_speed_kmh}}
    """
    params = {
        "latitude":   config.LOCATION_LAT,
        "longitude":  config.LOCATION_LON,
        "start_date": start_date,
        "end_date":   end_date,
        "hourly":     _VARIABLES,
        "timezone":   config.LOCATION_TZ,
    }
    url = _BASE_URL + "?" + urllib.parse.urlencode(params)
    logger.info(f"Descargando meteorologia {start_date} -> {end_date}")

    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read())
    except Exception as e:
        logger.warning(f"No se pudo obtener datos meteorologicos: {e}")
        return {}

    hourly = data.get("hourly", {})
    times  = hourly.get("time", [])

    result = {}
    for idx, t in enumerate(times):
        # Formato de 't': "2026-04-07T18:00"
        date_str, hr_str = t.split("T")
        hour = int(hr_str[:2])
        result[(date_str, hour)] = {
            "temp_c":           _safe(hourly, "temperature_2m",       idx),
            "feels_like_c":     _safe(hourly, "apparent_temperature",  idx),
            "humidity_pct":     _safe(hourly, "relative_humidity_2m",  idx),
            "precipitation_mm": _safe(hourly, "precipitation",         idx),
            "wind_speed_kmh":   _safe(hourly, "wind_speed_10m",        idx),
        }
    return result


def get_workout_weather(weather_cache: dict, date_str: str, start_time: str) -> dict:
    """
    Extrae el clima para la hora de inicio del entrenamiento.
    start_time formato esperado: "2026-06-04 18:30:00"
    """
    if not start_time or not weather_cache:
        return {}
    try:
        hour = int(start_time[11:13])
        return weather_cache.get((date_str, hour), {})
    except (IndexError, ValueError):
        return {}


def _safe(hourly: dict, key: str, idx: int):
    vals = hourly.get(key, [])
    return vals[idx] if idx < len(vals) else None
