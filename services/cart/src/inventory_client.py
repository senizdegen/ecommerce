import httpx
from fastapi import HTTPException, status

from .config import Config

class InventoryClient:
    def __init__(self):
        self.base_url = Config.INVENTORY_SERVICE_URL

    
    async def get_inventory(self, product_uid: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(f"{self.base_url}/{product_uid}")

            if response.status_code == 404:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Product inventory not found"
                )
            
            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Inventory service is unavailable"
                )
            
            return response.json()