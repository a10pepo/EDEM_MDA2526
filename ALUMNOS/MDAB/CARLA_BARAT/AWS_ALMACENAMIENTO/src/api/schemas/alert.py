from pydantic import BaseModel
from typing import List, Any, Dict


class AlertsResponse(BaseModel):
    low_stock: List[Dict[str, Any]]
    high_discount: List[Dict[str, Any]]
    return_rate: List[Dict[str, Any]]
    total_alerts: int
