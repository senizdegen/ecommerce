import httpx
from fastapi import HTTPException, status
from ..config import Config

class InventoryClient:
    def __init__(self):
        self.base_url = Config.INVENTORY_SERVICE_URL

    async def reserve(self, product_uid: str, quantity: int):
        async with httpx.AsyncClient() as client:
            response = await client.post(
                f"{self.base_url}/reserve",
                json={
                    "product_uid": product_uid,
                    "quantity": quantity
                }
            )

        if response.status_code == 404:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Inventory not found"
            )

        if response.status_code == 409:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail="Not enough stock"
            )

        if response.status_code != 200:
            raise HTTPException(
                status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                detail="Inventory service is unavailable"
            )

        return response.json()

    async def release(self, product_uid: str, quantity: int):
        async with httpx.AsyncClient() as client:
            await client.post(
                f"{self.base_url}/release",
                json={
                    "product_uid": product_uid,
                    "quantity": quantity
                }
            )