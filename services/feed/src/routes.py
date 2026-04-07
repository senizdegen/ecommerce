from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from .database import get_session
from .service import FeedService

feed_router = APIRouter()
feed_service = FeedService()

@feed_router.get("/products")
async def get_all_product(session: AsyncSession = Depends(get_session)):
    return await feed_service.get_all(session)

@feed_router.get("/products/{product_uid}")
async def get_all_product(product_uid: str, session: AsyncSession = Depends(get_session)):
    result = await feed_service.get_one_by_uid(product_uid, session)
    if result:
        return result
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with provided uid not found")
