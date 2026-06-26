from datetime import datetime
from typing import List, Optional
from botocore.exceptions import ClientError
from src.db.dynamodb import get_table, TICKETS_TABLE
from src.models.ticket import Ticket


def _generate_ticket_id() -> str:
    now = datetime.now()
    return f"TKT-{now.strftime('%Y%m%d-%H%M%S-%f')[:18]}"


def register_ticket(ticket: Ticket) -> bool:
    if not ticket.ticket_id:
        ticket.ticket_id = _generate_ticket_id()
    try:
        get_table(TICKETS_TABLE).put_item(Item=ticket.to_dynamodb_item())
        return True
    except ClientError:
        return False


def get_ticket(ticket_id: str) -> Optional[Ticket]:
    response = get_table(TICKETS_TABLE).get_item(Key={"ticket_id": ticket_id})
    item = response.get("Item")
    return Ticket.from_dynamodb_item(item) if item else None


def list_tickets() -> List[Ticket]:
    response = get_table(TICKETS_TABLE).scan()
    return [Ticket.from_dynamodb_item(i) for i in response.get("Items", [])]


def update_ticket_status(ticket_id: str, status: str) -> bool:
    valid_statuses = {"pending", "completed", "returned"}
    if status not in valid_statuses:
        return False
    try:
        get_table(TICKETS_TABLE).update_item(
            Key={"ticket_id": ticket_id},
            UpdateExpression="SET #s = :s",
            ExpressionAttributeNames={"#s": "status"},
            ExpressionAttributeValues={":s": status},
        )
        return True
    except ClientError:
        return False


def delete_ticket(ticket_id: str) -> bool:
    try:
        get_table(TICKETS_TABLE).delete_item(Key={"ticket_id": ticket_id})
        return True
    except ClientError:
        return False
