from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status
from datetime import datetime
from decimal import Decimal
import uuid

from .models import Order, OrderItem
from .clients.cart_client import CartClient
from .clients.inventory_client import InventoryClient


class OrderService:
    def __init__(self):
        self.cart_client = CartClient()
        self.inventory_client = InventoryClient()

    async def get_orders_by_user(self, user_uid: str, session: AsyncSession):
        statement = select(Order).where(Order.user_uid == user_uid).order_by(desc(Order.created_at))
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_order_by_uid(self, order_uid: str, user_uid: str, session: AsyncSession):
        try:
            order_uuid = uuid.UUID(order_uid)
            user_uuid = uuid.UUID(user_uid)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Invalid uid was provided"
            )

        statement = select(Order).where(
            Order.uid == order_uuid,
            Order.user_uid == user_uuid
        )
        result = await session.execute(statement)
        order = result.scalars().first()

        if order is None:
            return None

        items_statement = select(OrderItem).where(OrderItem.order_uid == order.uid)
        items_result = await session.execute(items_statement)
        items = items_result.scalars().all()

        return {
            "order": order,
            "items": items
        }

    async def checkout(self, user_uid: str, access_token: str, session: AsyncSession):
        cart_data = await self.cart_client.get_my_cart(access_token)

        cart = cart_data["cart"]
        items = cart_data["items"]

        if not items:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cart is empty"
            )

        reserved_items = []
        total_amount = Decimal("0.00")

        try:
            for item in items:
                await self.inventory_client.reserve(
                    product_uid=item["product_uid"],
                    quantity=item["quantity"]
                )
                reserved_items.append(item)

            order = Order(
                user_uid=uuid.UUID(user_uid),
                status="PENDING",
                total_amount=Decimal("0.00")
            )
            session.add(order)
            await session.commit()
            await session.refresh(order)

            order_items = []

            for item in items:
                price_snapshot = Decimal("0.00")  # временно, пока cart/product не дают цену
                line_total = price_snapshot * item["quantity"]
                total_amount += line_total

                order_item = OrderItem(
                    order_uid=order.uid,
                    product_uid=uuid.UUID(item["product_uid"]),
                    quantity=item["quantity"],
                    price_snapshot=price_snapshot
                )
                session.add(order_item)
                order_items.append(order_item)

            order.total_amount = total_amount
            order.updated_at = datetime.now()

            await session.commit()

            for order_item in order_items:
                await session.refresh(order_item)

            await self.cart_client.clear_cart(access_token)

            return {
                "order": order,
                "items": order_items
            }

        except Exception:
            for item in reserved_items:
                await self.inventory_client.release(
                    product_uid=item["product_uid"],
                    quantity=item["quantity"]
                )
            raise

    async def cancel_order(self, order_uid: str, user_uid: str, session: AsyncSession):
        order_data = await self.get_order_by_uid(order_uid, user_uid, session)

        if order_data is None:
            return None

        order = order_data["order"]
        items = order_data["items"]

        if order.status == "CANCELLED":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Order is already cancelled"
            )

        if order.status == "PAID":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Paid order cannot be cancelled"
            )

        for item in items:
            await self.inventory_client.release(
                product_uid=str(item.product_uid),
                quantity=item.quantity
            )

        order.status = "CANCELLED"
        order.updated_at = datetime.now()

        await session.commit()
        await session.refresh(order)

        return {
            "order": order,
            "items": items
        }