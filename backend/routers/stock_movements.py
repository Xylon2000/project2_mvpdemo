from fastapi import APIRouter, Depends
from sqlmodel import Session, select

from database import get_session
from models import Product, StockMovement, StockMovementRead, Warehouse

router = APIRouter(prefix="/stock-movements", tags=["stock-movements"])


@router.get("", response_model=list[StockMovementRead])
def list_stock_movements(
    session: Session = Depends(get_session),
) -> list[StockMovementRead]:
    query = (
        select(StockMovement, Product, Warehouse)
        .join(Product, Product.id == StockMovement.product_id)
        .join(Warehouse, Warehouse.id == StockMovement.warehouse_id)
        .order_by(StockMovement.created_at.desc())
    )
    rows = session.exec(query).all()

    return [
        StockMovementRead(
            id=movement.id,
            product_id=movement.product_id,
            product_name=product.name,
            warehouse_id=movement.warehouse_id,
            warehouse_name=warehouse.name,
            type=movement.type,
            quantity=movement.quantity,
            created_at=movement.created_at,
        )
        for movement, product, warehouse in rows
    ]
