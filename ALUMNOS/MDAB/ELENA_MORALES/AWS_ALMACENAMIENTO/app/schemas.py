"""Modelos de entrada (validación de las peticiones POST con Pydantic)."""

from typing import Literal

from pydantic import BaseModel, Field


class ProductIn(BaseModel):
    productCode: str
    name: str
    brand: str
    category: str
    manufactureDate: str = Field(examples=["2025-01-10"])
    expiryDate: str = Field(examples=["2026-12-31"])
    maxStock: int
    supplierId: str
    supplierName: str
    shelfId: str
    price: float


class CustomerRef(BaseModel):
    customerId: str
    status: Literal["Confirmed", "Cancelled", "Returned"] = "Confirmed"


class OrderIn(BaseModel):
    orderId: str
    productCode: str
    orderDate: str = Field(examples=["2026-06-01T10:30:00"])
    shipDate: str = Field(examples=["2026-06-03T09:00:00"])
    unitsSold: int
    channel: str
    store: str
    customers: list[CustomerRef] = []


class CustomerIn(BaseModel):
    customerId: str
    name: str
    nationalId: str
    dateOfBirth: str = Field(examples=["1990-05-15"])
