from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from database import get_session
from models import Inventory, InventoryRead, Product, Warehouse

router = APIRouter(prefix="/inventory", tags=["inventory"])


@router.get("", response_model=list[InventoryRead])
def list_inventory(session: Session = Depends(get_session)) -> list[InventoryRead]:
    query = (
        select(Inventory, Product, Warehouse)
        .join(Product, Product.id == Inventory.product_id)
        .join(Warehouse, Warehouse.id == Inventory.warehouse_id)
        .order_by(Inventory.id)
    )
    rows = session.exec(query).all()

    return [
        InventoryRead(
            id=inventory.id,
            product_id=inventory.product_id,
            product_name=product.name,
            warehouse_id=inventory.warehouse_id,
            warehouse_name=warehouse.name,
            quantity=inventory.quantity,
            updated_at=inventory.updated_at,
        )
        for inventory, product, warehouse in rows
    ]
