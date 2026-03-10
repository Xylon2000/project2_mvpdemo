from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from models import Warehouse, WarehouseCreate, WarehouseRead

router = APIRouter(prefix="/warehouses", tags=["warehouses"])


@router.get("", response_model=list[WarehouseRead])
def list_warehouses(session: Session = Depends(get_session)) -> list[Warehouse]:
    return session.exec(select(Warehouse).order_by(Warehouse.id)).all()


@router.post("", response_model=WarehouseRead, status_code=status.HTTP_201_CREATED)
def create_warehouse(
    payload: WarehouseCreate, session: Session = Depends(get_session)
) -> Warehouse:
    existing = session.exec(select(Warehouse).where(Warehouse.code == payload.code)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Warehouse with code '{payload.code}' already exists.",
        )

    warehouse = Warehouse.model_validate(payload)
    session.add(warehouse)
    session.commit()
    session.refresh(warehouse)
    return warehouse
