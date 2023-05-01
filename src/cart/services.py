import models
from core.services import BaseAPIClient, safely_decode_response_json

__all__ = ('CartsAPIClient',)


class CartsAPIClient(BaseAPIClient):

    async def create_cart_product(
            self,
            telegram_id: int,
            product_id: int,
            quantity: int,
    ) -> models.CartProduct:
        url = f'/carts/users/{telegram_id}/'
        request_body = {'product_id': product_id, 'quantity': quantity}
        response = await self._http_client.post(url, json=request_body)
        response_body = safely_decode_response_json(response)
        return models.CartProduct.parse_obj(response_body)

    async def delete_card_product(self, cart_product_id: int):
        url = f'/carts/{cart_product_id}/'
        response = await self._http_client.delete(url)

    async def get_card_product(self, cart_product_id: int):
        url = f'/carts/{cart_product_id}/'
        response = await self._http_client.get(url)

    async def get_user_card_products(self, telegram_id: int):
        url = f'/carts/users/{telegram_id}/'
        response = await self._http_client.get(url)
        response_body = safely_decode_response_json(response)
        return models.CartProduct.parse_obj(response_body)

    async def update_card_product_quantity(self, cart_product_id: int,
                                           quantity: int):
        url = f'/carts/{cart_product_id}/'
        request_body = {'quantity': quantity}
        response = await self._http_client.patch(url, json=request_body)
