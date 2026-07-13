"""
Extrae entrenamientos de Garmin Connect y los guarda en DynamoDB.

Por cada actividad obtiene:
  - Datos basicos: tipo, duracion, distancia, FC media/max, calorias
  - Zonas de FC (Z1-Z5 en segundos): permiten diferenciar bici steady de series de pista
  - Meteorologia: temperatura, sensacion termica, humedad, precipitacion, viento
  - Metricas diarias: Body Battery, Training Readiness, Estres
"""
import logging
import time
from datetime import date, timedelta

from src import config, dynamo_client
from src.garmin_client import get_client
from src.weather_client import fetch_weather_range, get_workout_weather
from src.daily_metrics import fetch_daily_metrics_range

logger = logging.getLogger(__name__)


def _get_hr_zones(client, activity_id: str) -> dict:
    """
    Descarga el tiempo en cada zona de FC para una actividad.
    Clave para el analisis: Z4-Z5 alto = sesion de series; Z2-Z3 = steady aerobico.
    """
    try:
        zones = client.get_activity_hr_in_timezones(activity_id)
        result = {}
        for z in zones:
            n = z.get("zoneNumber")
            if n in (1, 2, 3, 4, 5):
                result[f"zone{n}_seconds"] = z.get("secsInZone")
        return result
    except Exception as e:
        logger.debug(f"Zonas FC no disponibles para {activity_id}: {e}")
        return {}


def _map_activity(activity: dict, client, weather_cache: dict) -> dict:
    """Transforma un registro de actividad de Garmin en el item de DynamoDB."""
    activity_id = str(activity["activityId"])
    item = {
        "workout_id":            activity_id,
        "name":                  activity.get("activityName"),
        "type":                  activity.get("activityType", {}).get("typeKey"),
        "date":                  (activity.get("startTimeLocal") or "")[:10],
        "start_time":            activity.get("startTimeLocal"),
        "duration_seconds":      activity.get("duration"),
        "distance_meters":       activity.get("distance"),
        "avg_hr":                activity.get("averageHR"),
        "max_hr":                activity.get("maxHR"),
        "calories":              activity.get("calories"),
        "avg_speed_ms":          activity.get("averageSpeed"),
        "elevation_gain":        activity.get("elevationGain"),
        "training_effect":       activity.get("aerobicTrainingEffect"),
        "anaerobic_effect":      activity.get("anaerobicTrainingEffect"),
        "training_stress_score": activity.get("trainingStressScore"),
        "vo2max_value":          activity.get("vO2MaxValue"),
    }
    item.update(_get_hr_zones(client, activity_id))
    item.update(get_workout_weather(weather_cache, item["date"], item["start_time"]))
    time.sleep(0.5)  # respetar rate limit de Garmin
    return item


def load_workouts(days: int = 30) -> int:
    """
    Extrae los entrenamientos de los ultimos N dias y los guarda en DynamoDB.
    Devuelve el numero de actividades procesadas.
    """
    client = get_client()
    start = (date.today() - timedelta(days=days)).isoformat()
    end   = date.today().isoformat()

    activities = client.get_activities_by_date(start, end)
    logger.info(f"{len(activities)} entrenamientos entre {start} y {end}")

    weather_cache = fetch_weather_range(start, end)
    logger.info(f"Meteorologia cargada: {len(weather_cache)} registros horarios")

    metrics_cache = fetch_daily_metrics_range(client, start, end)

    for activity in activities:
        item = _map_activity(activity, client, weather_cache)
        item.update(metrics_cache.get(item["date"], {}))
        dynamo_client.put_item(config.DYNAMO_TABLE_WORKOUTS, item)

        z4 = item.get("zone4_seconds") or 0
        z5 = item.get("zone5_seconds") or 0
        bb = item.get("body_battery_start")
        tr = item.get("training_readiness")
        logger.info(
            f"  -> {item['date']} {(item.get('start_time') or '')[-8:-3]}h | "
            f"{item['type']} | fc_max:{item.get('max_hr')} | "
            f"z4:{int(z4//60)}min z5:{int(z5//60)}min | "
            f"bb:{bb} tr:{tr} | "
            f"te:{item.get('training_effect')} ta:{item.get('anaerobic_effect')}"
        )

    return len(activities)
