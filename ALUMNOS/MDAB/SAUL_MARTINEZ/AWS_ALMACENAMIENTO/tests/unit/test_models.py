from decimal import Decimal

import pytest
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from app.models.category import Category
from app.models.product import Product, ProductVariant


def test_create_product_with_variant(session: Session):
    product = Product(name="Camiseta", slug="camiseta", base_price=Decimal("19.99"))
    session.add(product)
    session.commit()
    session.refresh(product)

    variant = ProductVariant(
        product_id=product.id, size="M", color="Negro", sku="CAM-M-NEG", stock_quantity=10
    )
    session.add(variant)
    session.commit()

    assert variant.id is not None
    assert variant.product.name == "Camiseta"
    assert product.variants[0].sku == "CAM-M-NEG"


def test_variant_combo_must_be_unique(session: Session):
    product = Product(name="Camiseta", slug="camiseta", base_price=Decimal("19.99"))
    session.add(product)
    session.commit()

    session.add(
        ProductVariant(product_id=product.id, size="M", color="Negro", sku="A1")
    )
    session.commit()

    # Misma talla+color en el mismo producto => debe fallar.
    session.add(
        ProductVariant(product_id=product.id, size="M", color="Negro", sku="A2")
    )
    with pytest.raises(IntegrityError):
        session.commit()


def test_category_slug_is_unique(session: Session):
    session.add(Category(name="Hombre", slug="hombre"))
    session.commit()
    session.add(Category(name="Hombre 2", slug="hombre"))
    with pytest.raises(IntegrityError):
        session.commit()
