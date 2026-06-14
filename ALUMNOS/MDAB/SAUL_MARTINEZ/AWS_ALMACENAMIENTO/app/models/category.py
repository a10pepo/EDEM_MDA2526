from datetime import datetime

from sqlmodel import Field, Relationship, SQLModel

from app.models.user import utcnow


class Category(SQLModel, table=True):
    __tablename__ = "categories"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(max_length=120)
    slug: str = Field(index=True, unique=True, max_length=140)
    # Jerarquía opcional: una categoría puede tener una categoría padre.
    parent_id: int | None = Field(default=None, foreign_key="categories.id")
    created_at: datetime = Field(default_factory=utcnow, nullable=False)

    products: list["Product"] = Relationship(back_populates="category")  # noqa: F821
