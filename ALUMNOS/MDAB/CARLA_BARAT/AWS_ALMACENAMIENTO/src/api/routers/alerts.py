from fastapi import APIRouter

from src.api.schemas.alert import AlertsResponse
from src.services.alert_service import get_all_alerts

router = APIRouter()


@router.get("/", response_model=AlertsResponse)
def check_all():
    alerts = get_all_alerts()
    return {
        **alerts,
        "total_alerts": sum(len(v) for v in alerts.values()),
    }
