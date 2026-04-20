from fastapi import APIRouter, Depends, status, HTTPException, Request, UploadFile, File, Form
from sqlmodel.ext.asyncio.session import AsyncSession
from .service import ProductService
from typing import List, Optional
from .schemas import ProductModel
from .database import get_session
from .dependencies import AccessTokenBearer
from .minio_client import upload_image, ensure_bucket_exists
from decimal import Decimal
import uuid

product_router = APIRouter()
product_service = ProductService()
access_token_bearer = AccessTokenBearer()


@product_router.get('/', response_model=List[ProductModel])
async def get_all_products(
    session: AsyncSession = Depends(get_session)
):
    return await product_service.get_all_products(session)


@product_router.get('/{product_uid}', response_model=ProductModel)
async def get_product(
    product_uid: str,
    session: AsyncSession = Depends(get_session)
):
    product = await product_service.get_product(product_uid, session)
    if product:
        return product
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with provided uid not found")


@product_router.post('/', status_code=status.HTTP_201_CREATED)
async def create_product(
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: str = Form(...),
    available_quantity: int = Form(...),
    image: Optional[UploadFile] = File(None),
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    image_url = None

    if image and image.filename:
        ensure_bucket_exists()
        file_bytes = await image.read()
        ext = image.filename.rsplit('.', 1)[-1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        image_url = upload_image(file_bytes, filename, image.content_type)

    from .schemas import ProductCreateModel
    product_data = ProductCreateModel(
        name=name,
        description=description,
        price=Decimal(price),
        available_quantity=available_quantity,
    )

    new_product = await product_service.create_product(product_data, image_url, session)

    await request.app.state.rabbit.publish_product_created({
        "product_uid": str(new_product.uid),
        "name": new_product.name,
        "description": new_product.description,
        "price": float(new_product.price),
        "available_quantity": available_quantity,
        "image_url": new_product.image_url,
    })

    return {
        "message": "Product created successfully",
        "product": {
            "uid": str(new_product.uid),
            "image_url": new_product.image_url
        }
    }


@product_router.patch('/{product_uid}', response_model=ProductModel)
async def update_product(
    product_uid: str,
    request: Request,
    name: str = Form(...),
    description: str = Form(...),
    price: str = Form(...),
    image: Optional[UploadFile] = File(None),
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    image_url = None

    if image and image.filename:
        ensure_bucket_exists()
        file_bytes = await image.read()
        ext = image.filename.rsplit('.', 1)[-1].lower()
        filename = f"{uuid.uuid4()}.{ext}"
        image_url = upload_image(file_bytes, filename, image.content_type)

    from .schemas import ProductUpdateModel
    product_data = ProductUpdateModel(
        name=name,
        description=description,
        price=Decimal(price),
    )

    updated_product = await product_service.update_product(product_uid, product_data, image_url, session)

    if not updated_product:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with provided uid not found")

    await request.app.state.rabbit.publish_product_updated({
        "product_uid": str(updated_product.uid),
        "name": updated_product.name,
        "description": updated_product.description,
        "price": float(updated_product.price),
        "image_url": updated_product.image_url,
    })

    return updated_product


@product_router.delete('/{product_uid}', status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_uid: str,
    session: AsyncSession = Depends(get_session),
    token_details: dict = Depends(access_token_bearer)
):
    response = await product_service.delete_product(product_uid, session)
    if response is not None:
        return {}
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Product with provided uid not found")