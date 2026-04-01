from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from .database import get_session
from .service import CartService
from .schemas import (
    AddToCartRequest,
    UpdateCartItemRequest,
    CartWithItemsResponse,
    CartItemModel,
)
from .dependencies import get_current_user

cart_router = APIRouter()
cart_service = CartService()


@cart_router.get("/me", response_model=CartWithItemsResponse)
async def get_cart(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    user_uid = current_user["user"]["user_uid"]
    return await cart_service.get_cart_by_user(user_uid, session)


@cart_router.post("/items", response_model=CartItemModel, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    item_data: AddToCartRequest,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    user_uid = current_user["user"]["user_uid"]
    return await cart_service.add_item_to_cart(user_uid, item_data, session)


@cart_router.patch("/items/{item_uid}", response_model=CartItemModel)
async def update_cart_item(
    item_uid: str,
    update_data: UpdateCartItemRequest,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    updated_item = await cart_service.update_cart_item(item_uid, update_data, session)

    if updated_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item with provided uid not found"
        )

    return updated_item


@cart_router.delete("/items/{item_uid}", status_code=status.HTTP_204_NO_CONTENT)
async def remove_cart_item(
    item_uid: str,
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    deleted_item = await cart_service.remove_cart_item(item_uid, session)

    if deleted_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item with provided uid not found"
        )

    return {}


@cart_router.delete("/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    current_user: dict = Depends(get_current_user),
    session: AsyncSession = Depends(get_session)
):
    user_uid = current_user["user"]["user_uid"]
    await cart_service.clear_cart(user_uid, session)
    return {}