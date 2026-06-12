"""Modelos SQLModel del dominio.

Se importan todos aquí para que queden registrados en SQLModel.metadata
(necesario para create_all y para resolver las relaciones por nombre).
"""

from app.models.category import Category
from app.models.order import Order, OrderItem, OrderStatus
from app.models.product import Product, ProductImage, ProductVariant
from app.models.user import User

__all__ = [
    "User",
    "Category",
    "Product",
    "ProductVariant",
    "ProductImage",
    "Order",
    "OrderItem",
    "OrderStatus",
]
