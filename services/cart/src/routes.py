from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel.ext.asyncio.session import AsyncSession

from .database import get_session
from .service import CartService
from .schemas import (
    AddToCartRequest,
    UpdateCartItemRequest,
    CartWithItemsResponse,
    CartItemModel,
)

cart_router = APIRouter()
cart_service = CartService()


@cart_router.get("/{user_uid}", response_model=CartWithItemsResponse)
async def get_cart(user_uid: str, session: AsyncSession = Depends(get_session)):
    return await cart_service.get_cart_by_user(user_uid, session)


@cart_router.post("/{user_uid}/items", response_model=CartItemModel, status_code=status.HTTP_201_CREATED)
async def add_to_cart(
    user_uid: str,
    item_data: AddToCartRequest,
    session: AsyncSession = Depends(get_session)
):
    return await cart_service.add_item_to_cart(user_uid, item_data, session)


@cart_router.patch("/items/{item_uid}", response_model=CartItemModel)
async def update_cart_item(
    item_uid: str,
    update_data: UpdateCartItemRequest,
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
    session: AsyncSession = Depends(get_session)
):
    deleted_item = await cart_service.remove_cart_item(item_uid, session)

    if deleted_item is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Cart item with provided uid not found"
        )

    return {}


@cart_router.delete("/{user_uid}/clear", status_code=status.HTTP_204_NO_CONTENT)
async def clear_cart(
    user_uid: str,
    session: AsyncSession = Depends(get_session)
):
    await cart_service.clear_cart(user_uid, session)
    return {}