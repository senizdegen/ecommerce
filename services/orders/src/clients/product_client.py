import httpx
from ..config import Config

class ProductClient:
    def __init__(self):
        self.base_url = Config.PRODUCT_SERVICE_URL

    async def get_product(self, product_uid: str):
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}/{product_uid}")
                if response.status_code == 200:
                    return response.json()
            except Exception:
                pass
        return None