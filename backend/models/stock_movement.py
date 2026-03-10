from datetime import datetime
from enum import Enum

from sqlmodel import Field, SQLModel


class MovementType(str, Enum):
    inbound = "inbound"
    outbound = "outbound"


class StockMovement(SQLModel, table=True):
    __tablename__ = "stock_movements"

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(foreign_key="products.id", nullable=False, index=True)
    warehouse_id: int = Field(foreign_key="warehouses.id", nullable=False, index=True)
    type: MovementType = Field(nullable=False)
    quantity: int = Field(gt=0, nullable=False)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class StockMovementRead(SQLModel):
    id: int
    product_id: int
    product_name: str
    warehouse_id: int
    warehouse_name: str
    type: MovementType
    quantity: int
    created_at: datetime


class StockOperationRequest(SQLModel):
    product_id: int
    warehouse_id: int
    quantity: int = Field(gt=0)


class StockOperationResponse(SQLModel):
    movement_id: int
    type: MovementType
    product_id: int
    warehouse_id: int
    quantity: int
    current_quantity: int
    created_at: datetime
