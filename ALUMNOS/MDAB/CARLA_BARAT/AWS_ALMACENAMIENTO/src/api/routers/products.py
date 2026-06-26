from fastapi import APIRouter, HTTPException
from typing import List

from src.api.schemas.product import ProductCreate, ProductResponse, StockUpdate
from src.models.product import Product
from src.services.product_service import (
    delete_product,
    get_product,
    list_products,
    register_product,
    update_stock,
)

router = APIRouter()


def _to_response(p: Product) -> dict:
    return {
        **p.__dict__,
        "days_since_restock": p.days_since_restock(),
        "is_below_threshold": p.is_below_threshold(),
    }


@router.get("/", response_model=List[ProductResponse])
def list_all():
    return [_to_response(p) for p in list_products()]


@router.post("/", response_model=ProductResponse, status_code=201)
def create(data: ProductCreate):
    product = Product(**data.model_dump())
    if not register_product(product):
        raise HTTPException(500, "Failed to register product")
    return _to_response(product)


@router.get("/{sku}", response_model=ProductResponse)
def get_one(sku: str):
    p = get_product(sku)
    if not p:
        raise HTTPException(404, f"Product '{sku}' not found")
    return _to_response(p)


@router.get("/{sku}/stock")
def check_stock(sku: str):
    p = get_product(sku)
    if not p:
        raise HTTPException(404, f"Product '{sku}' not found")
    return {
        "sku": p.sku,
        "name": p.name,
        "stock_quantity": p.stock_quantity,
        "restock_threshold": p.restock_threshold,
        "is_below_threshold": p.is_below_threshold(),
        "days_since_restock": p.days_since_restock(),
    }


@router.put("/{sku}/stock", response_model=ProductResponse)
def update_stock_endpoint(sku: str, body: StockUpdate):
    p = get_product(sku)
    if not p:
        raise HTTPException(404, f"Product '{sku}' not found")
    update_stock(sku, body.quantity)
    p.stock_quantity = body.quantity
    return _to_response(p)


@router.delete("/{sku}", status_code=204)
def remove(sku: str):
    if not get_product(sku):
        raise HTTPException(404, f"Product '{sku}' not found")
    delete_product(sku)
