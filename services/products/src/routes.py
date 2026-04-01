from fastapi import APIRouter, Depends, status, HTTPException, Request
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ProductService
from typing import List
from .schemas import ProductModel, ProductCreateModel, ProductUpdateModel
from .database import get_session
from .dependencies import AccessTokenBearer



product_router = APIRouter()
product_service = ProductService()

access_token_bearer = AccessTokenBearer()

@product_router.get('/', response_model=List[ProductModel])
async def get_all_products(
    session: AsyncSession = Depends(get_session)
):
    products = await product_service.get_all_products(session)
    return products

@product_router.get('/{product_uid}', response_model=ProductModel)
async def get_product(
    product_uid: str,
    session: AsyncSession = Depends(get_session)
):
    product = await product_service.get_product(product_uid, session)
    if product:
        return product
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with provided uid not found")

@product_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(
    product_data: ProductCreateModel,
    request: Request,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    new_product = await product_service.create_product(product_data, session)
    await request.app.state.rabbit.publish_product_created(
        {
            "product_uid": str(new_product.uid),
            "available_quantity": int(product_data.available_quantity)
        }
    )

    return {
        "message": "Product created successfully",
        "product":{
            "uid": str(new_product.uid)
        }
    }

@product_router.patch('/{product_uid}', response_model=ProductModel)
async def update_product(
    product_uid: str,
    product_update_data: ProductUpdateModel,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    updated_book = await product_service.update_product(product_uid, product_update_data, session)
    if updated_book:
        return updated_book
    else:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with provided uid not found")

@product_router.delete('/{product_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_uid: str, 
    session:AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
    ):
    response = await product_service.delete_product(product_uid, session)
    if response is not None:
        return {}
    else: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with provided uid not found")