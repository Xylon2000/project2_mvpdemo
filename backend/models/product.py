from datetime import datetime

from sqlmodel import Field, SQLModel


class ProductBase(SQLModel):
    name: str
    sku: str = Field(unique=True, index=True)


class Product(ProductBase, table=True):
    __tablename__ = "products"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class ProductCreate(ProductBase):
    pass


class ProductRead(ProductBase):
    id: int
    created_at: datetime
