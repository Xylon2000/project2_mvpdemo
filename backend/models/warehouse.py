from datetime import datetime

from sqlmodel import Field, SQLModel


class WarehouseBase(SQLModel):
    name: str
    code: str = Field(unique=True, index=True)


class Warehouse(WarehouseBase, table=True):
    __tablename__ = "warehouses"

    id: int | None = Field(default=None, primary_key=True)
    created_at: datetime = Field(default_factory=datetime.utcnow, nullable=False)


class WarehouseCreate(WarehouseBase):
    pass


class WarehouseRead(WarehouseBase):
    id: int
    created_at: datetime
