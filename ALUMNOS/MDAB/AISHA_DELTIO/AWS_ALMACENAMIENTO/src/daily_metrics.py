"""
Metricas diarias de Garmin: Body Battery, Training Readiness y Estres.

Se precalculan en rango completo para minimizar llamadas a la API.
Nota: el Vivoactive 6 no expone Training Readiness via API publica;
      esos campos quedaran a None hasta que Garmin lo habilite.
"""
import logging
import time
from datetime import date, timedelta

logger = logging.getLogger(__name__)


def _date_from_record(rec: dict) -> str:
    """Extrae la fecha (YYYY-MM-DD) de un registro con distintos formatos posibles."""
    for key in ("date", "calendarDate"):
        if rec.get(key):
            return str(rec[key])[:10]
    for key in ("startTimestampLocal", "startTimestampGMT"):
        if rec.get(key):
            return str(rec[key])[:10]
    return ""


def _parse_body_battery_day(day_record: dict) -> dict:
    """
    Extrae inicio, fin y caida de Body Battery de un registro diario.
    La API puede devolver dos formatos segun la version de la libreria:
      A) bodyBatteryStatsList con lecturas horarias
      B) campos directos (charged, bodyBatteryLevel, value)
    """
    levels = []

    # Formato A: lista de lecturas horarias
    for s in day_record.get("bodyBatteryStatsList") or []:
        v = s.get("bodyBatteryLevel")
        if v is not None:
            levels.append(int(v))

    # Formato B: valor directo en el registro raiz
    if not levels:
        for key in ("charged", "bodyBatteryLevel", "value", "bodyBattery"):
            v = day_record.get(key)
            if v is not None:
                try:
                    levels.append(int(v))
                except (TypeError, ValueError):
                    pass

    if not levels:
        return {}

    return {
        "body_battery_start": float(levels[0]),
        "body_battery_end":   float(levels[-1]),
        "body_battery_min":   float(min(levels)),
        # Cuanto se agoto la bateria durante el dia
        "body_battery_drop":  float(levels[0] - min(levels)),
    }


def _parse_training_readiness(data) -> dict:
    if isinstance(data, list):
        data = data[0] if data else {}
    if not isinstance(data, dict):
        return {}
    score = (
        data.get("trainingReadinessScore") or
        data.get("score") or
        data.get("level") or
        data.get("value")
    )
    try:
        return {"training_readiness": float(score)} if score is not None else {}
    except (TypeError, ValueError):
        return {}


def _parse_stress(data) -> dict:
    if not isinstance(data, dict):
        return {}
    avg = (
        data.get("avgStressLevel") or
        data.get("averageStressLevel") or
        data.get("overallStressLevel")
    )
    try:
        return {"stress_avg": float(avg)} if avg is not None else {}
    except (TypeError, ValueError):
        return {}


def fetch_daily_metrics_range(client, start_date: str, end_date: str) -> dict:
    """
    Devuelve {date_str: {body_battery_start, body_battery_end, body_battery_min,
                          body_battery_drop, training_readiness, stress_avg}}

    Body Battery se pide en rango (una llamada); Training Readiness y Estres
    requieren una llamada por dia (limitacion de la API de Garmin).
    """
    cache: dict[str, dict] = {}

    # Body Battery: el endpoint acepta rango completo en una sola llamada
    try:
        bb_raw = client.get_body_battery(start_date, end_date)
        if isinstance(bb_raw, list):
            for rec in bb_raw:
                d = _date_from_record(rec)
                if d:
                    parsed = _parse_body_battery_day(rec)
                    if parsed:
                        cache.setdefault(d, {}).update(parsed)
        logger.info(f"Body Battery: {len(cache)} dias obtenidos")
    except Exception as e:
        logger.warning(f"Body Battery no disponible: {e}")

    # Training Readiness y Estres: una llamada por dia
    current = date.fromisoformat(start_date)
    end_d   = date.fromisoformat(end_date)
    while current <= end_d:
        d = current.isoformat()

        try:
            tr = _parse_training_readiness(client.get_training_readiness(d))
            if tr:
                cache.setdefault(d, {}).update(tr)
        except Exception as e:
            logger.debug(f"Training Readiness {d}: {e}")

        try:
            st = _parse_stress(client.get_stress_data(d))
            if st:
                cache.setdefault(d, {}).update(st)
        except Exception as e:
            logger.debug(f"Estres {d}: {e}")

        time.sleep(0.3)  # respetar rate limit de Garmin
        current += timedelta(days=1)

    logger.info(f"Metricas diarias completas: {len(cache)} dias con datos")
    return cache
