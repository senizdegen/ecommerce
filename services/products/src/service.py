from .schemas import ProductCreateModel, ProductUpdateModel
from sqlmodel import select, desc
from sqlalchemy.orm import selectinload
from .models import Product, Category
from sqlmodel.ext.asyncio.session import AsyncSession
import uuid
from fastapi import HTTPException, status
from typing import Optional
from datetime import datetime


class ProductService:
    async def get_all_products(self, session: AsyncSession):
        statement = select(Product).options(selectinload(Product.category)).order_by(desc(Product.created_at))
        result = await session.exec(statement)
        return result.all()

    async def get_product(self, product_uid: str, session: AsyncSession):
        try:
            uid = uuid.UUID(product_uid)
        except ValueError:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid uid was provided")
        statement = select(Product).options(selectinload(Product.category)).where(Product.uid == uid)
        result = await session.exec(statement)
        product = result.first()
        return product if product is not None else None

    async def create_product(self, product_data: ProductCreateModel, image_url: Optional[str], session: AsyncSession):
        product_data_dict = product_data.model_dump()
        new_product = Product(**product_data_dict, image_url=image_url)
        session.add(new_product)
        await session.commit()
        await session.refresh(new_product)
        # подгружаем категорию
        await session.refresh(new_product, attribute_names=["category"])
        return new_product

    async def update_product(self, product_uid: str, update_data: ProductUpdateModel, image_url: Optional[str], session: AsyncSession):
        product_to_update = await self.get_product(product_uid, session)
        if product_to_update is None:
            return None
        update_data_dict = update_data.model_dump()
        for k, v in update_data_dict.items():
            setattr(product_to_update, k, v)
        if image_url is not None:
            product_to_update.image_url = image_url
        product_to_update.updated_at = datetime.now()
        await session.commit()
        await session.refresh(product_to_update, attribute_names=["category"])
        return product_to_update

    async def delete_product(self, product_uid: str, session: AsyncSession):
        product_to_delete = await self.get_product(product_uid, session)
        if product_to_delete is not None:
            await session.delete(product_to_delete)
            await session.commit()
            return {}
        return None
    
    async def get_categories(self, session: AsyncSession):
        statement = select(Category).order_by(Category.name)
        result = await session.exec(statement)
        return result.all()