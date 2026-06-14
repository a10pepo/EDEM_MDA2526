from decimal import Decimal

from pydantic import BaseModel, Field


# ---------- Categorías ----------
class CategoryCreate(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    slug: str = Field(min_length=1, max_length=140)
    parent_id: int | None = None


class CategoryRead(BaseModel):
    id: int
    name: str
    slug: str
    parent_id: int | None = None


# ---------- Variantes ----------
class VariantCreate(BaseModel):
    size: str = Field(min_length=1, max_length=20)
    color: str = Field(min_length=1, max_length=40)
    sku: str = Field(min_length=1, max_length=64)
    price_override: Decimal | None = Field(default=None, ge=0)
    stock_quantity: int = Field(default=0, ge=0)


class VariantRead(BaseModel):
    id: int
    size: str
    color: str
    sku: str
    price_override: Decimal | None
    stock_quantity: int
    effective_price: Decimal


# ---------- Imágenes ----------
class ImageRegister(BaseModel):
    """Registra una imagen ya subida a S3 (se guarda solo la key)."""

    s3_key: str = Field(min_length=1, max_length=512)
    is_primary: bool = False
    sort_order: int = 0


class ImageRead(BaseModel):
    id: int
    s3_key: str
    is_primary: bool
    sort_order: int
    url: str  # URL prefirmada temporal


class PresignUploadRequest(BaseModel):
    s3_key: str = Field(min_length=1, max_length=512)
    content_type: str = "image/jpeg"


class PresignUploadResponse(BaseModel):
    upload_url: str
    s3_key: str


# ---------- Productos ----------
class ProductCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    slug: str = Field(min_length=1, max_length=220)
    description: str | None = None
    category_id: int | None = None
    base_price: Decimal = Field(ge=0)


class ProductRead(BaseModel):
    id: int
    name: str
    slug: str
    description: str | None
    category_id: int | None
    base_price: Decimal
    is_active: bool


class ProductDetail(ProductRead):
    variants: list[VariantRead] = []
    images: list[ImageRead] = []
