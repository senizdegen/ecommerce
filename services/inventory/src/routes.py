from fastapi import APIRouter
from .service import InventoryService
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from uuid import UUID
from .schemas import InventoryCreate, ReserveRequest, StockUpdate
from .database import get_session

inventory_router = APIRouter()
inventory_service = InventoryService()

@inventory_router.post("/")
async def create_inventory(
    data: InventoryCreate, session: AsyncSession = Depends(get_session)
):
    existing = await inventory_service.find_inventory(session, data.product_uid)
    if existing:
        raise HTTPException(status_code=400, detail="Already exists")

    return await inventory_service.create_inventory(session, data)

@inventory_router.get("/{product_id}")
async def get_inventory(product_id: UUID, session: AsyncSession = Depends(get_session)):
    inv = await inventory_service.get_inventory(session, product_id)
    if not inv:
        raise HTTPException(404, "Not found")
    return inv


@inventory_router.post("/add-stock")
async def add_stock(data: StockUpdate, session: AsyncSession = Depends(get_session)):
    return await inventory_service.add_stock(session, data.product_uid, data.quantity)


@inventory_router.post("/reserve")
async def reserve(data: ReserveRequest, session: AsyncSession = Depends(get_session)):
    try:
        return await inventory_service.reserve(session, data.product_uid, data.quantity)
    except Exception as e:
        raise HTTPException(400, str(e))


@inventory_router.post("/release")
async def release(data: ReserveRequest, session: AsyncSession = Depends(get_session)):
    return await inventory_service.release(session, data.product_uid, data.quantity)


@inventory_router.post("/confirm")
async def confirm(data: ReserveRequest, session: AsyncSession = Depends(get_session)):
    return await inventory_service.confirm(session, data.product_uid, data.quantity)
