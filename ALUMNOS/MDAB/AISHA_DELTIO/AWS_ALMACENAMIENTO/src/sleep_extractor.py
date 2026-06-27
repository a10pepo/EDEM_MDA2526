"""
Extrae metricas de sueno de Garmin Connect y las guarda en DynamoDB.

Atencion: en Garmin, sleep_date = dia en que te DESPIERTAS, no en que te duermes.
Si duermes la noche del lunes al martes, el registro tiene fecha de martes.
Esto afecta al JOIN con workouts: workout_date N -> sleep_date N+1.
"""
import logging
from datetime import date, datetime, timedelta

from src import config, dynamo_client
from src.garmin_client import get_client

logger = logging.getLogger(__name__)


def _epoch_ms_to_iso(epoch_ms) -> str | None:
    if not epoch_ms:
        return None
    return datetime.fromtimestamp(epoch_ms / 1000).isoformat()


def _map_sleep(raw: dict, sleep_date: str) -> dict | None:
    """
    Transforma la respuesta de get_sleep_data en el item de DynamoDB.
    Devuelve None si no hay datos de sueno para esa fecha.
    """
    dto = raw.get("dailySleepDTO") or {}
    if not dto.get("sleepStartTimestampLocal"):
        return None

    # El score de sueno viene anidado en sleepScores.overall.value
    scores  = dto.get("sleepScores") or {}
    overall = scores.get("overall") if isinstance(scores, dict) else None
    score   = overall.get("value") if isinstance(overall, dict) else None

    return {
        "date":                 dto.get("calendarDate", sleep_date),
        "sleep_start":          _epoch_ms_to_iso(dto.get("sleepStartTimestampLocal")),
        "sleep_end":            _epoch_ms_to_iso(dto.get("sleepEndTimestampLocal")),
        "total_sleep_seconds":  dto.get("sleepTimeSeconds"),
        "deep_sleep_seconds":   dto.get("deepSleepSeconds"),
        "light_sleep_seconds":  dto.get("lightSleepSeconds"),
        "rem_sleep_seconds":    dto.get("remSleepSeconds"),
        "awake_seconds":        dto.get("awakeSleepSeconds"),
        "avg_spo2":             dto.get("averageSpO2Value"),
        "avg_respiration":      dto.get("averageRespirationValue"),
        "resting_hr":           dto.get("restingHeartRate"),
        "sleep_score":          score,
    }


def _get_hrv(client, sleep_date: str) -> dict:
    """
    Obtiene los datos de HRV nocturno para una fecha.
    hrv_status: BALANCED / LOW / POOR / NONE — indicador de recuperacion.
    """
    try:
        hrv_raw  = client.get_hrv_data(sleep_date)
        summary  = hrv_raw.get("hrvSummary") or {}
        baseline = summary.get("baseline") or {}
        return {
            "hrv_avg":            summary.get("lastNightAvg"),
            "hrv_5min_high":      summary.get("lastNight5MinHigh"),
            "hrv_status":         summary.get("status"),
            "hrv_baseline_low":   baseline.get("balancedLow"),
            "hrv_baseline_high":  baseline.get("balancedUpper"),
        }
    except Exception as e:
        logger.debug(f"HRV no disponible para {sleep_date}: {e}")
        return {}


def load_sleep(days: int = 30) -> int:
    """
    Extrae los datos de sueno de los ultimos N dias y los guarda en DynamoDB.
    Devuelve el numero de noches procesadas con datos validos.
    """
    client  = get_client()
    end     = date.today()
    start   = end - timedelta(days=days)

    count   = 0
    current = start
    while current <= end:
        date_str = current.isoformat()
        try:
            raw  = client.get_sleep_data(date_str)
            item = _map_sleep(raw, date_str)
            if item:
                item.update(_get_hrv(client, date_str))
                dynamo_client.put_item(config.DYNAMO_TABLE_SLEEP, item)
                hours = (item.get("total_sleep_seconds") or 0) / 3600
                logger.info(
                    f"  -> {date_str} | {hours:.1f}h | score:{item.get('sleep_score', '?')} | "
                    f"hrv:{item.get('hrv_avg', '?')} ({item.get('hrv_status', '?')})"
                )
                count += 1
            else:
                logger.info(f"  -> {date_str} | sin datos")
        except Exception as e:
            logger.warning(f"  -> {date_str} | error: {e}")

        current += timedelta(days=1)

    return count
