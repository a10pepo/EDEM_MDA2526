from decimal import Decimal

from pydantic import BaseModel, Field

from app.models.order import OrderStatus


class OrderItemCreate(BaseModel):
    variant_id: int
    quantity: int = Field(ge=1)


class OrderCreate(BaseModel):
    user_id: int | None = None
    shipping_address: str | None = None
    items: list[OrderItemCreate] = Field(min_length=1)


class OrderItemRead(BaseModel):
    id: int
    variant_id: int
    quantity: int
    unit_price: Decimal


class OrderRead(BaseModel):
    id: int
    user_id: int | None
    status: OrderStatus
    total_amount: Decimal
    shipping_address: str | None
    items: list[OrderItemRead]
