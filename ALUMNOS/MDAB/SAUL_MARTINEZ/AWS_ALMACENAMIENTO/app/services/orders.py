from decimal import Decimal

from sqlmodel import Session

from app.models.order import Order, OrderItem
from app.models.product import ProductVariant
from app.schemas.order import OrderCreate


class OrderError(Exception):
    """Error de negocio al crear un pedido (variante inexistente o sin stock)."""


def create_order(session: Session, data: OrderCreate) -> Order:
    """Crea un pedido de forma atómica.

    Valida que cada variante exista y tenga stock suficiente, congela el precio
    unitario en el momento de la compra, descuenta el inventario y calcula el
    total. Si algo falla, no persiste nada.
    """
    order = Order(user_id=data.user_id, shipping_address=data.shipping_address)
    total = Decimal("0.00")

    for line in data.items:
        variant = session.get(ProductVariant, line.variant_id)
        if variant is None:
            raise OrderError(f"La variante {line.variant_id} no existe")
        if variant.stock_quantity < line.quantity:
            raise OrderError(
                f"Stock insuficiente para la variante {line.variant_id}: "
                f"disponible {variant.stock_quantity}, solicitado {line.quantity}"
            )

        unit_price = (
            variant.price_override
            if variant.price_override is not None
            else variant.product.base_price
        )

        variant.stock_quantity -= line.quantity
        session.add(variant)

        order.items.append(
            OrderItem(
                variant_id=variant.id,
                quantity=line.quantity,
                unit_price=unit_price,
            )
        )
        total += unit_price * line.quantity

    order.total_amount = total
    session.add(order)
    session.commit()
    session.refresh(order)
    return order
