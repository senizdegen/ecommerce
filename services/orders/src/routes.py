from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from .database import get_session
from .service import OrderService
from .schemas import OrderModel, OrderWithItemsResponse, StatusUpdateRequest
from .dependencies import AccessTokenBearer


order_router = APIRouter()
order_service = OrderService()
access_token_bearer = AccessTokenBearer()


@order_router.post("/checkout", response_model=OrderWithItemsResponse, status_code=status.HTTP_201_CREATED)
async def checkout(
    request: Request,
    token_details: dict = Depends(access_token_bearer),
    session: AsyncSession = Depends(get_session)
):
    user_uid = token_details["user"]["user_uid"]
    auth_header = request.headers.get("Authorization")
    access_token = auth_header.split(" ")[1]

    return await order_service.checkout(user_uid, access_token, session)


@order_router.get("/", response_model=List[OrderModel])
async def get_my_orders(
    token_details: dict = Depends(access_token_bearer),
    session: AsyncSession = Depends(get_session)
):
    user_uid = token_details["user"]["user_uid"]
    return await order_service.get_orders_by_user(user_uid, session)


@order_router.get("/admin/all", response_model=List[OrderWithItemsResponse])
async def get_all_orders_admin(
    token_details: dict = Depends(access_token_bearer),
    session: AsyncSession = Depends(get_session)
):
    return await order_service.get_all_orders(session)


@order_router.get("/{order_uid}", response_model=OrderWithItemsResponse)
async def get_order(
    order_uid: str,
    token_details: dict = Depends(access_token_bearer),
    session: AsyncSession = Depends(get_session)
):
    user_uid = token_details["user"]["user_uid"]
    order = await order_service.get_order_by_uid(order_uid, user_uid, session)

    if order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order with provided uid not found"
        )

    return order


@order_router.patch("/{order_uid}/status", response_model=OrderWithItemsResponse)
async def update_order_status(
    order_uid: str,
    body: StatusUpdateRequest,
    token_details: dict = Depends(access_token_bearer),
    session: AsyncSession = Depends(get_session)
):
    updated = await order_service.update_order_status(order_uid, body.status, session)
    if updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order with provided uid not found"
        )
    return updated


@order_router.post("/{order_uid}/cancel", response_model=OrderWithItemsResponse)
async def cancel_order(
    order_uid: str,
    token_details: dict = Depends(access_token_bearer),
    session: AsyncSession = Depends(get_session)
):
    user_uid = token_details["user"]["user_uid"]
    cancelled_order = await order_service.cancel_order(order_uid, user_uid, session)

    if cancelled_order is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Order with provided uid not found"
        )

    return cancelled_order