from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from models import (
    Inventory,
    MovementType,
    Product,
    StockMovement,
    StockOperationRequest,
    StockOperationResponse,
    Warehouse,
)

router = APIRouter(prefix="/inbound", tags=["inbound"])


@router.post("", response_model=StockOperationResponse, status_code=status.HTTP_201_CREATED)
def inbound_stock(
    payload: StockOperationRequest, session: Session = Depends(get_session)
) -> StockOperationResponse:
    product = session.get(Product, payload.product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {payload.product_id} not found.",
        )

    warehouse = session.get(Warehouse, payload.warehouse_id)
    if not warehouse:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Warehouse {payload.warehouse_id} not found.",
        )

    inventory = session.exec(
        select(Inventory).where(
            Inventory.product_id == payload.product_id,
            Inventory.warehouse_id == payload.warehouse_id,
        )
    ).first()
    if not inventory:
        inventory = Inventory(
            product_id=payload.product_id,
            warehouse_id=payload.warehouse_id,
            quantity=0,
        )
        session.add(inventory)
        session.flush()

    inventory.quantity += payload.quantity
    inventory.updated_at = datetime.utcnow()

    movement = StockMovement(
        product_id=payload.product_id,
        warehouse_id=payload.warehouse_id,
        type=MovementType.inbound,
        quantity=payload.quantity,
    )
    session.add(movement)
    session.commit()
    session.refresh(movement)
    session.refresh(inventory)

    return StockOperationResponse(
        movement_id=movement.id,
        type=movement.type,
        product_id=movement.product_id,
        warehouse_id=movement.warehouse_id,
        quantity=movement.quantity,
        current_quantity=inventory.quantity,
        created_at=movement.created_at,
    )
