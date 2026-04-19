import httpx
from fastapi import HTTPException, status
from ..config import Config

class CartClient:
    def __init__(self):
        self.base_url = Config.CART_SERVICE_URL

    async def get_my_cart(self, access_token: str):
        async with httpx.AsyncClient() as client:
            response = await client.get(
                f"{self.base_url}/me",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if response.status_code == 401:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Unauthorized"
                )

            if response.status_code != 200:
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Cart service is unavailable"
                )

            return response.json()

    async def clear_cart(self, access_token: str):
        async with httpx.AsyncClient() as client:  # были пропущены скобки ()
            response = await client.delete(
                f"{self.base_url}/clear",
                headers={"Authorization": f"Bearer {access_token}"}
            )

            if response.status_code not in [200, 204]:  # if был вне async with — после закрытия клиента
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
                    detail="Failed to clear cart"
                )