from typing import List, Dict, Any
from src.services.product_service import list_products
from src.services.ticket_service import list_tickets

HIGH_DISCOUNT_THRESHOLD = 0.20   # alert if discount > 20% of gross total
RETURN_RATE_THRESHOLD = 0.10     # alert if returned tickets > 10% of all tickets


def check_low_stock_alerts() -> List[Dict[str, Any]]:
    """Alert when stock_quantity <= restock_threshold."""
    alerts = []
    for product in list_products():
        if product.is_below_threshold():
            alerts.append({
                "type": "LOW_STOCK",
                "sku": product.sku,
                "name": product.name,
                "stock": product.stock_quantity,
                "threshold": product.restock_threshold,
                "message": (
                    f"[LOW STOCK] {product.name} ({product.sku}) — "
                    f"{product.stock_quantity} units left (threshold: {product.restock_threshold})"
                ),
            })
    return alerts


def check_high_discount_alerts() -> List[Dict[str, Any]]:
    """Alert when a ticket's total discount exceeds 20% of gross amount."""
    alerts = []
    for ticket in list_tickets():
        if ticket.status == "returned":
            continue
        pct = ticket.discount_percentage()
        if pct > HIGH_DISCOUNT_THRESHOLD * 100:
            alerts.append({
                "type": "HIGH_DISCOUNT",
                "ticket_id": ticket.ticket_id,
                "discount_pct": pct,
                "discount_total": ticket.discount_total(),
                "total_amount": ticket.total_amount(),
                "message": (
                    f"[HIGH DISCOUNT] Ticket {ticket.ticket_id} — "
                    f"discount is {pct:.1f}% of gross (€{ticket.discount_total():.2f} off)"
                ),
            })
    return alerts


def check_return_rate_alert() -> List[Dict[str, Any]]:
    """Alert when returned tickets exceed 10% of total tickets."""
    tickets = list_tickets()
    if not tickets:
        return []
    returned = sum(1 for t in tickets if t.status == "returned")
    rate = returned / len(tickets)
    if rate > RETURN_RATE_THRESHOLD:
        return [
            {
                "type": "HIGH_RETURN_RATE",
                "returned": returned,
                "total": len(tickets),
                "rate_pct": round(rate * 100, 1),
                "message": (
                    f"[HIGH RETURN RATE] {returned}/{len(tickets)} tickets returned "
                    f"({rate * 100:.1f}% — threshold: {RETURN_RATE_THRESHOLD * 100:.0f}%)"
                ),
            }
        ]
    return []


def get_all_alerts() -> Dict[str, List[Dict[str, Any]]]:
    return {
        "low_stock": check_low_stock_alerts(),
        "high_discount": check_high_discount_alerts(),
        "return_rate": check_return_rate_alert(),
    }
