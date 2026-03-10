from fastapi import FastAPI

from database import create_db_and_tables
from routers import inbound, inventory, outbound, products, stock_movements, warehouses

app = FastAPI(title="Fresh Warehouse Demo API", version="0.1.0")


@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


app.include_router(products.router)
app.include_router(warehouses.router)
app.include_router(inventory.router)
app.include_router(inbound.router)
app.include_router(outbound.router)
app.include_router(stock_movements.router)
