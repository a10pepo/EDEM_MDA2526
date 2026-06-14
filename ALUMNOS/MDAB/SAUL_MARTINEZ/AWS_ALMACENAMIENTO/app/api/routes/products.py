from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from app.api.deps import get_session, get_storage
from app.models.product import Product, ProductImage, ProductVariant
from app.schemas.catalog import (
    ImageRead,
    ImageRegister,
    PresignUploadRequest,
    PresignUploadResponse,
    ProductCreate,
    ProductDetail,
    ProductRead,
    VariantCreate,
    VariantRead,
)
from app.services.storage import StorageService

router = APIRouter(prefix="/products", tags=["products"])


def _variant_read(v: ProductVariant, base_price) -> VariantRead:
    effective = v.price_override if v.price_override is not None else base_price
    return VariantRead(
        id=v.id,
        size=v.size,
        color=v.color,
        sku=v.sku,
        price_override=v.price_override,
        stock_quantity=v.stock_quantity,
        effective_price=effective,
    )


def _get_product_or_404(product_id: int, session: Session) -> Product:
    product = session.get(Product, product_id)
    if product is None:
        raise HTTPException(status.HTTP_404_NOT_FOUND, "Producto no encontrado")
    return product


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(data: ProductCreate, session: Session = Depends(get_session)):
    if session.exec(select(Product).where(Product.slug == data.slug)).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "El slug ya existe")
    product = Product.model_validate(data.model_dump())
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.get("", response_model=list[ProductRead])
def list_products(
    category_id: int | None = None, session: Session = Depends(get_session)
):
    query = select(Product).where(Product.is_active == True)  # noqa: E712
    if category_id is not None:
        query = query.where(Product.category_id == category_id)
    return session.exec(query).all()


@router.get("/{product_id}", response_model=ProductDetail)
def get_product(
    product_id: int,
    session: Session = Depends(get_session),
    storage: StorageService = Depends(get_storage),
):
    product = _get_product_or_404(product_id, session)
    images = [
        ImageRead(
            id=img.id,
            s3_key=img.s3_key,
            is_primary=img.is_primary,
            sort_order=img.sort_order,
            url=storage.presigned_get_url(img.s3_key),
        )
        for img in sorted(product.images, key=lambda i: i.sort_order)
    ]
    return ProductDetail(
        id=product.id,
        name=product.name,
        slug=product.slug,
        description=product.description,
        category_id=product.category_id,
        base_price=product.base_price,
        is_active=product.is_active,
        variants=[_variant_read(v, product.base_price) for v in product.variants],
        images=images,
    )


@router.post(
    "/{product_id}/variants",
    response_model=VariantRead,
    status_code=status.HTTP_201_CREATED,
)
def add_variant(
    product_id: int,
    data: VariantCreate,
    session: Session = Depends(get_session),
):
    product = _get_product_or_404(product_id, session)
    if session.exec(
        select(ProductVariant).where(ProductVariant.sku == data.sku)
    ).first():
        raise HTTPException(status.HTTP_409_CONFLICT, "El SKU ya existe")
    variant = ProductVariant(product_id=product.id, **data.model_dump())
    session.add(variant)
    session.commit()
    session.refresh(variant)
    return _variant_read(variant, product.base_price)


@router.post(
    "/{product_id}/images",
    response_model=ImageRead,
    status_code=status.HTTP_201_CREATED,
)
def register_image(
    product_id: int,
    data: ImageRegister,
    session: Session = Depends(get_session),
    storage: StorageService = Depends(get_storage),
):
    _get_product_or_404(product_id, session)
    image = ProductImage(product_id=product_id, **data.model_dump())
    session.add(image)
    session.commit()
    session.refresh(image)
    return ImageRead(
        id=image.id,
        s3_key=image.s3_key,
        is_primary=image.is_primary,
        sort_order=image.sort_order,
        url=storage.presigned_get_url(image.s3_key),
    )


@router.post("/{product_id}/images/presign", response_model=PresignUploadResponse)
def presign_image_upload(
    product_id: int,
    data: PresignUploadRequest,
    session: Session = Depends(get_session),
    storage: StorageService = Depends(get_storage),
):
    """Devuelve una URL prefirmada para subir la imagen directamente a S3."""
    _get_product_or_404(product_id, session)
    upload_url = storage.presigned_put_url(data.s3_key, data.content_type)
    return PresignUploadResponse(upload_url=upload_url, s3_key=data.s3_key)
