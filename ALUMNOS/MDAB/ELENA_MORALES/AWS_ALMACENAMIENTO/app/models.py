"""Modelos de la base de datos (tablas) con SQLAlchemy.

Esquema:
  products          -> productos en almacén
  customers         -> clientes
  orders            -> pedidos (cada pedido referencia 1 producto)
  order_customers   -> qué clientes van en cada pedido y su estado
                       (tabla intermedia, relación N:M con dato extra 'status')
"""

from datetime import date, datetime

from sqlalchemy import ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database import Base


class Product(Base):
    __tablename__ = "products"

    productCode: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str]
    brand: Mapped[str]
    category: Mapped[str]
    manufactureDate: Mapped[date]
    expiryDate: Mapped[date]
    maxStock: Mapped[int]
    supplierId: Mapped[str]
    supplierName: Mapped[str]
    shelfId: Mapped[str]
    price: Mapped[float]

    orders: Mapped[list["Order"]] = relationship(back_populates="product")


class Customer(Base):
    __tablename__ = "customers"

    customerId: Mapped[str] = mapped_column(String, primary_key=True)
    name: Mapped[str]
    nationalId: Mapped[str]
    dateOfBirth: Mapped[date]


class Order(Base):
    __tablename__ = "orders"

    orderId: Mapped[str] = mapped_column(String, primary_key=True)
    productCode: Mapped[str] = mapped_column(ForeignKey("products.productCode"))
    orderDate: Mapped[datetime]
    shipDate: Mapped[datetime]
    unitsSold: Mapped[int]
    channel: Mapped[str]
    store: Mapped[str]

    product: Mapped["Product"] = relationship(back_populates="orders")
    order_customers: Mapped[list["OrderCustomer"]] = relationship(
        back_populates="order", cascade="all, delete-orphan"
    )


class OrderCustomer(Base):
    __tablename__ = "order_customers"

    orderId: Mapped[str] = mapped_column(ForeignKey("orders.orderId"), primary_key=True)
    customerId: Mapped[str] = mapped_column(ForeignKey("customers.customerId"), primary_key=True)
    status: Mapped[str]  # 'Confirmed' / 'Cancelled' / 'Returned'

    order: Mapped["Order"] = relationship(back_populates="order_customers")
