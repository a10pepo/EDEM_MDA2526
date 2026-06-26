from dataclasses import dataclass
from datetime import date


@dataclass
class Product:
    sku: str
    name: str
    category: str
    size: str
    color: str
    price: float
    stock_quantity: int
    restock_threshold: int
    last_restock_date: str  # ISO date string YYYY-MM-DD
    supplier_id: str

    def days_since_restock(self) -> int:
        return (date.today() - date.fromisoformat(self.last_restock_date)).days

    def is_below_threshold(self) -> bool:
        return self.stock_quantity <= self.restock_threshold

    def to_dynamodb_item(self) -> dict:
        return {
            "sku": self.sku,
            "name": self.name,
            "category": self.category,
            "size": self.size,
            "color": self.color,
            "price": str(self.price),
            "stock_quantity": self.stock_quantity,
            "restock_threshold": self.restock_threshold,
            "last_restock_date": self.last_restock_date,
            "supplier_id": self.supplier_id,
        }

    @classmethod
    def from_dynamodb_item(cls, item: dict) -> "Product":
        return cls(
            sku=item["sku"],
            name=item["name"],
            category=item["category"],
            size=item["size"],
            color=item["color"],
            price=float(item["price"]),
            stock_quantity=int(item["stock_quantity"]),
            restock_threshold=int(item["restock_threshold"]),
            last_restock_date=item["last_restock_date"],
            supplier_id=item["supplier_id"],
        )
