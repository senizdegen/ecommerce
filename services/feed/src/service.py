from sqlalchemy.ext.asyncio import AsyncSession
from .schemas import ProductCreateModel, ProductUpdateModel
from .models import FeedProduct
from sqlmodel import select, desc
from typing import Optional


class FeedService:

    async def create_product(self, session: AsyncSession, product_data: ProductCreateModel):
        new_product = FeedProduct(
            uid=product_data.product_uid,
            name=product_data.name,
            description=product_data.description,
            price=product_data.price,
            available_quantity=product_data.available_quantity,
            image_url=product_data.image_url,
            category_uid=product_data.category_uid,
            category_name=product_data.category_name,
        )
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        return new_product
    
    async def get_all(self, session: AsyncSession, category_uid: Optional[str] = None):
        statement = select(FeedProduct).order_by(desc(FeedProduct.created_at))
        if category_uid:
            statement = statement.where(FeedProduct.category_uid == category_uid)
        result = await session.execute(statement)
        return result.scalars().all()

    async def get_one_by_uid(self, uid: str, session: AsyncSession):
        statement = select(FeedProduct).where(FeedProduct.uid == uid)
        result = await session.execute(statement)
        return result.scalar_one_or_none()

    async def update_product(self, session: AsyncSession, product_uid: str, product_data: ProductUpdateModel):
        statement = select(FeedProduct).where(FeedProduct.uid == product_uid)
        result = await session.execute(statement)
        product = result.scalar_one_or_none()
        if not product:
            return None
        if product_data.name is not None:
            product.name = product_data.name
        if product_data.description is not None:
            product.description = product_data.description
        if product_data.price is not None:
            product.price = product_data.price
        if product_data.image_url is not None:
            product.image_url = product_data.image_url
        if product_data.category_uid is not None:
            product.category_uid = product_data.category_uid
        if product_data.category_name is not None:
            product.category_name = product_data.category_name
        session.add(product)
        await session.commit()
        await session.refresh(product)
        return product

    async def delete_product(self, session: AsyncSession, product_uid: str):
        statement = select(FeedProduct).where(FeedProduct.uid == product_uid)
        result = await session.execute(statement)
        product = result.scalar_one_or_none()
        if not product:
            return None
        await session.delete(product)
        await session.commit()
        return {}
    
    async def get_categories(self, session: AsyncSession):
        statement = select(FeedProduct.category_uid, FeedProduct.category_name).where(
            FeedProduct.category_name.isnot(None)
        ).distinct()
        result = await session.execute(statement)
        rows = result.all()
        return [{"uid": row.category_uid, "name": row.category_name} for row in rows]