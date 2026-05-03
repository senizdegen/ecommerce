import httpx
import logging
from ..config import Config

logger = logging.getLogger(__name__)

class ProductClient:
    def __init__(self):
        self.base_url = Config.PRODUCT_SERVICE_URL

    async def get_product(self, product_uid: str):
        async with httpx.AsyncClient() as client:
            try:
                url = f"{self.base_url}/{product_uid}"
                logger.info(f"Fetching product from: {url}")
                response = await client.get(url)
                logger.info(f"Product response status: {response.status_code}")
                logger.info(f"Product response body: {response.text}")
                if response.status_code == 200:
                    return response.json()
            except Exception as e:
                logger.error(f"Product client error: {e}")
        return None