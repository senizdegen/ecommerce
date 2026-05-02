from fastapi import APIRouter, Depends, status, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_session
from .service import FeedService
from .schemas import FeedProductModel, CategoryModel
from typing import List, Optional

feed_router = APIRouter()
feed_service = FeedService()


@feed_router.get("/categories", response_model=List[CategoryModel])
async def get_categories(session: AsyncSession = Depends(get_session)):
    return await feed_service.get_categories(session)


@feed_router.get("/products", response_model=List[FeedProductModel])
async def get_all_products(
    category_uid: Optional[str] = Query(None),
    session: AsyncSession = Depends(get_session)
):
    return await feed_service.get_all(session, category_uid=category_uid)


@feed_router.get("/products/{product_uid}", response_model=FeedProductModel)
async def get_product(
    product_uid: str,
    session: AsyncSession = Depends(get_session)
):
    result = await feed_service.get_one_by_uid(product_uid, session)
    if result:
        return result
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with provided uid not found")