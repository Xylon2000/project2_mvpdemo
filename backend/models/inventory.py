from datetime import datetime

from sqlmodel import Field, SQLModel, UniqueConstraint


class Inventory(SQLModel, table=True):
    __tablename__ = "inventory"
    __table_args__ = (
        UniqueConstraint("product_id", "warehouse_id", name="uq_inventory_product_warehouse"),
    )

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id", nullable=False, index=True)
    warehouse_id: int = Field(foreign_key="warehouses.id", nullable=False, index=True)
    quantity: int = Field(default=0, ge=0, nullable=False)
    updated_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class InventoryRead(SQLModel):
    id: int
    product_id: int
    product_name: str
    warehouse_id: int
    warehouse_name: str
    quantity: int
    updated_at: datetime
