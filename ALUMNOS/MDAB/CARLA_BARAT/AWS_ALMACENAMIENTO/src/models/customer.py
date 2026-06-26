from dataclasses import dataclass


@dataclass
class Customer:
    customer_id: str
    name: str
    email: str
    phone: str
    date_of_birth: str  # ISO date string YYYY-MM-DD
    membership_level: str  # none, basic, silver, gold

    def to_dynamodb_item(self) -> dict:
        return {
            "customer_id": self.customer_id,
            "name": self.name,
            "email": self.email,
            "phone": self.phone,
            "date_of_birth": self.date_of_birth,
            "membership_level": self.membership_level,
        }

    @classmethod
    def from_dynamodb_item(cls, item: dict) -> "Customer":
        return cls(
            customer_id=item["customer_id"],
            name=item["name"],
            email=item["email"],
            phone=item["phone"],
            date_of_birth=item["date_of_birth"],
            membership_level=item["membership_level"],
        )
