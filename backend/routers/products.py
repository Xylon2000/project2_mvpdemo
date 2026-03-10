from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from models import Product, ProductCreate, ProductRead

router = APIRouter(prefix="/products", tags=["products"])


@router.get("", response_model=list[ProductRead])
def list_products(session: Session = Depends(get_session)) -> list[Product]:
    return session.exec(select(Product).order_by(Product.id)).all()


@router.post("", response_model=ProductRead, status_code=status.HTTP_201_CREATED)
def create_product(
    payload: ProductCreate, session: Session = Depends(get_session)
) -> Product:
    existing = session.exec(select(Product).where(Product.sku == payload.sku)).first()
    if existing:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Product with sku '{payload.sku}' already exists.",
        )

    product = Product.model_validate(payload)
    session.add(product)
    session.commit()
    session.refresh(product)
    return product


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(product_id: int, session: Session = Depends(get_session)) -> None:
    product = session.get(Product, product_id)
    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Product {product_id} not found.",
        )

    session.delete(product)
    session.commit()
