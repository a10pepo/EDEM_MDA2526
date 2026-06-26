from pydantic import BaseModel, Field


class ProductCreate(BaseModel):
    sku: str
    name: str
    category: str
    size: str
    color: str
    price: float = Field(gt=0)
    stock_quantity: int = Field(ge=0)
    restock_threshold: int = Field(ge=0)
    last_restock_date: str
    supplier_id: str


class ProductResponse(ProductCreate):
    days_since_restock: int
    is_below_threshold: bool


class StockUpdate(BaseModel):
    quantity: int = Field(ge=0)
