from datetime import datetime
from decimal import Decimal

from sqlalchemy import Numeric, UniqueConstraint
from sqlmodel import Column, Field, Relationship, SQLModel

from app.models.category import Category
from app.models.user import utcnow


class Product(SQLModel, table=True):
    __tablename__ = "products"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=200)
    slug: str = Field(index=True, unique=True, max_length=220)
    description: str | None = Field(default=None)
    category_id: int | None = Field(default=None, foreign_key="categories.id")
    base_price: Decimal = Field(sa_column=Column(Numeric(10, 2), nullable=False))
    is_active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=utcnow, nullable=False)
    updated_at: datetime = Field(default_factory=utcnow, nullable=False)

    category: Category | None = Relationship(back_populates="products")
    variants: list["ProductVariant"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )
    images: list["ProductImage"] = Relationship(
        back_populates="product",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"},
    )


class ProductVariant(SQLModel, table=True):
    __tablename__ = "product_variants"
    # No puede haber dos variantes con la misma talla+color en un producto.
    __table_args__ = (
        UniqueConstraint("product_id", "size", "color", name="uq_variant_combo"),
    )

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id", index=True)
    size: str = Field(max_length=20)
    color: str = Field(max_length=40)
    sku: str = Field(index=True, unique=True, max_length=64)
    # Precio específico de la variante; si es None se usa product.base_price.
    price_override: Decimal | None = Field(
        default=None, sa_column=Column(Numeric(10, 2), nullable=True)
    )
    stock_quantity: int = Field(default=0, ge=0)

    product: Product = Relationship(back_populates="variants")


class ProductImage(SQLModel, table=True):
    __tablename__ = "product_images"

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id", index=True)
    # Clave (key) del objeto en S3. La URL se genera prefirmada bajo demanda.
    s3_key: str = Field(unique=True, max_length=512)
    is_primary: bool = Field(default=False)
    sort_order: int = Field(default=0)
    created_at: datetime = Field(default_factory=utcnow, nullable=False)

    product: Product = Relationship(back_populates="images")
