from sqlmodel import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime
import uuid

from .models import Cart, CartItem
from .schemas import AddToCartRequest, UpdateCartItemRequest
from .inventory_client import InventoryClient


class CartService:
    def __init__(self):
        self.inventory_client = InventoryClient()

    async def get_or_create_cart(self, user_uid: uuid.UUID, session: AsyncSession):
        statement = select(Cart).where(Cart.user_uid == user_uid)
        result = await session.execute(statement)
        cart = result.scalars().first()

        if cart is None:
            cart = Cart(user_uid=user_uid)
            session.add(cart)
            await session.commit()
            await session.refresh(cart)

        return cart

    async def get_cart_by_user(self, user_uid: str, session: AsyncSession):
        try:
            user_uuid = uuid.UUID(user_uid)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user uid was provided"
            )

        cart = await self.get_or_create_cart(user_uuid, session)

        statement = select(CartItem).where(CartItem.cart_uid == cart.uid)
        result = await session.execute(statement)
        items = result.scalars().all()

        return {
            "cart": cart,
            "items": items
        }

    async def add_item_to_cart(
        self,
        user_uid: str,
        item_data: AddToCartRequest,
        session: AsyncSession
    ):
        try:
            user_uuid = uuid.UUID(user_uid)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user uid was provided"
            )

        if item_data.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero"
            )

        cart = await self.get_or_create_cart(user_uuid, session)

        statement = select(CartItem).where(
            CartItem.cart_uid == cart.uid,
            CartItem.product_uid == item_data.product_uid
        )
        result = await session.execute(statement)
        existing_item = result.scalars().first()

        inventory_data = await self.inventory_client.get_inventory(str(item_data.product_uid))
        available_quantity = inventory_data["available_quantity"]

        requested_total_quantity = item_data.quantity
        if existing_item:
            requested_total_quantity = existing_item.quantity + item_data.quantity

        if requested_total_quantity > available_quantity:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Not enough stock available"
            )

        if existing_item:
            existing_item.quantity = requested_total_quantity
            existing_item.updated_at = datetime.now()
            await session.commit()
            await session.refresh(existing_item)
            return existing_item

        new_item = CartItem(
            cart_uid=cart.uid,
            product_uid=item_data.product_uid,
            quantity=item_data.quantity
        )
        session.add(new_item)
        await session.commit()
        await session.refresh(new_item)

        return new_item

    async def update_cart_item(
        self,
        item_uid: str,
        update_data: UpdateCartItemRequest,
        session: AsyncSession
    ):
        try:
            item_uuid = uuid.UUID(item_uid)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid item uid was provided"
            )

        if update_data.quantity <= 0:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Quantity must be greater than zero"
            )

        statement = select(CartItem).where(CartItem.uid == item_uuid)
        result = await session.execute(statement)
        item = result.scalars().first()

        if item is None:
            return None

        inventory_data = await self.inventory_client.get_inventory(str(item.product_uid))
        available_quantity = inventory_data["available_quantity"]

        if update_data.quantity > available_quantity:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Not enough stock available"
            )

        item.quantity = update_data.quantity
        item.updated_at = datetime.now()

        await session.commit()
        await session.refresh(item)
        return item

    async def remove_cart_item(self, item_uid: str, session: AsyncSession):
        try:
            item_uuid = uuid.UUID(item_uid)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid item uid was provided"
            )

        statement = select(CartItem).where(CartItem.uid == item_uuid)
        result = await session.execute(statement)
        item = result.scalars().first()

        if item is None:
            return None

        await session.delete(item)
        await session.commit()
        return {}

    async def clear_cart(self, user_uid: str, session: AsyncSession):
        try:
            user_uuid = uuid.UUID(user_uid)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid user uid was provided"
            )

        statement = select(Cart).where(Cart.user_uid == user_uuid)
        result = await session.execute(statement)
        cart = result.scalars().first()

        if cart is None:
            return {}

        statement = select(CartItem).where(CartItem.cart_uid == cart.uid)
        result = await session.execute(statement)
        items = result.scalars().all()

        for item in items:
            await session.delete(item)

        cart.updated_at = datetime.now()

        await session.commit()
        return {}