from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from .models import Inventory
from fastapi import HTTPException, status


class InventoryService:

    async def get_inventory(self, session: AsyncSession, product_uid):
        result = await session.execute(
            select(Inventory).where(Inventory.product_uid == product_uid)
        )
        return result.scalar_one_or_none()

    async def create_inventory(self, session: AsyncSession, data):
        inventory = Inventory(
            product_uid=data.product_uid,
            available_quantity=data.available_quantity,
            reserved_quantity=0,
        )
        session.add(inventory)
        await session.commit()
        await session.refresh(inventory)
        return inventory

    async def reserve(self, session: AsyncSession, product_uid, qty):
        result = await session.execute(
            select(Inventory)
            .where(Inventory.product_uid == product_uid)
            .with_for_update()  # 🔥 блокировка строки
        )
        inventory = result.scalar_one()

        if inventory.available_quantity < qty:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT, detail="Not enough stock"
            )

        inventory.available_quantity -= qty
        inventory.reserved_quantity += qty

        await session.commit()
        await session.refresh(inventory)

        return inventory

    async def add_stock(self, session: AsyncSession, product_uid, qty):
        inventory = await self.get_inventory(session, product_uid)

        inventory.available_quantity += qty

        await session.commit()
        await session.refresh(inventory)
        return inventory

    async def release(session: AsyncSession, product_uid, qty):
        result = await session.execute(
            select(Inventory)
            .where(Inventory.product_uid == product_uid)
            .with_for_update()
        )
        inventory = result.scalar_one()

        inventory.available_quantity += qty
        inventory.reserved_quantity -= qty

        await session.commit()
        await session.refresh(inventory)

        return inventory

    async def confirm(session: AsyncSession, product_uid, qty):
        result = await session.execute(
            select(Inventory)
            .where(Inventory.product_uid == product_uid)
            .with_for_update()
        )
        inventory = result.scalar_one()

        inventory.reserved_quantity -= qty

        await session.commit()
        await session.refresh(inventory)

        return inventory
