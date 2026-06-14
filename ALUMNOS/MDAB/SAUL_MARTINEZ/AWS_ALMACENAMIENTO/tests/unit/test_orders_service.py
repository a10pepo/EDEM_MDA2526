from decimal import Decimal

import pytest
from sqlmodel import Session

from app.models.product import Product, ProductVariant
from app.schemas.order import OrderCreate, OrderItemCreate
from app.services.orders import OrderError, create_order


def _seed_variant(session: Session, stock: int, override=None, base="20.00"):
    product = Product(name="P", slug=f"p-{stock}-{override}", base_price=Decimal(base))
    session.add(product)
    session.commit()
    session.refresh(product)
    variant = ProductVariant(
        product_id=product.id,
        size="M",
        color="Rojo",
        sku=f"SKU-{product.id}",
        stock_quantity=stock,
        price_override=Decimal(override) if override else None,
    )
    session.add(variant)
    session.commit()
    session.refresh(variant)
    return variant


def test_create_order_decrements_stock_and_freezes_price(session: Session):
    variant = _seed_variant(session, stock=10, base="20.00")

    order = create_order(
        session,
        OrderCreate(items=[OrderItemCreate(variant_id=variant.id, quantity=3)]),
    )

    assert order.total_amount == Decimal("60.00")
    assert order.items[0].unit_price == Decimal("20.00")
    session.refresh(variant)
    assert variant.stock_quantity == 7


def test_price_override_takes_precedence(session: Session):
    variant = _seed_variant(session, stock=5, override="12.50", base="20.00")

    order = create_order(
        session,
        OrderCreate(items=[OrderItemCreate(variant_id=variant.id, quantity=2)]),
    )

    assert order.total_amount == Decimal("25.00")
    assert order.items[0].unit_price == Decimal("12.50")


def test_insufficient_stock_raises_and_keeps_stock(session: Session):
    variant = _seed_variant(session, stock=1)

    with pytest.raises(OrderError):
        create_order(
            session,
            OrderCreate(items=[OrderItemCreate(variant_id=variant.id, quantity=5)]),
        )

    session.refresh(variant)
    assert variant.stock_quantity == 1


def test_unknown_variant_raises(session: Session):
    with pytest.raises(OrderError):
        create_order(
            session,
            OrderCreate(items=[OrderItemCreate(variant_id=999, quantity=1)]),
        )
