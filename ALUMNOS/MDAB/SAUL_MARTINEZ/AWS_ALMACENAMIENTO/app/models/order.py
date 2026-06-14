from datetime import datetime
from decimal import Decimal
from enum import Enum

from sqlalchemy import Numeric
from sqlmodel import Column, Field, Relationship, SQLModel

from app.models.user import utcnow


class OrderStatus(str, Enum):
    pending = "pending"
    paid = "paid"
    shipped = "shipped"
    delivered = "delivered"
    cancelled = "cancelled"


class Order(SQLModel, table=True):
    __tablename__ = "orders"

    id: int | None = Field(default=None, primary_key=True)
    user_id: int | None = Field(default=None, foreign_key="users.id", index=True)
    status: OrderStatus = Field(default=OrderStatus.pending)
    total_amount: Decimal = Field(
        default=Decimal("0.00"), sa_column=Column(Numeric(10, 2), nullable=False)
    )
    shipping_address: str | None = Field(default=None)
    created_at: datetime = Field(default_factory=utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=utcnow, nullable=False)

    items: list["OrderItem"] = Relationship(
        back_populates="order",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class OrderItem(SQLModel, table=True):
    __tablename__ = "order_items"

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", index=True)
    variant_id: int = Field(foreign_key="product_variants.id")
    quantity: int = Field(ge=1)
    # Precio congelado en el momento de la compra (no depende del catálogo futuro).
    unit_price: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))

    order: Order = Relationship(back_populates="items")
