import models
from core.services import APIClient, safely_decode_response_json

__all__ = ('CartsAPIClient',)


class CartsAPIClient:

    def __init__(self, api_client: APIClient):
        self._api_client = api_client

    async def create_cart_product(self, telegram_id: int, product_id: int, quantity: int) -> models.CartProduct:
        url = f'/carts/users/{telegram_id}/'
        request_body = {'product_id': product_id, 'quantity': quantity}
        async with self._api_client.closing_http_client() as client:
            response = await client.post(url, json=request_body)
        response_body = safely_decode_response_json(response)
        return models.CartProduct.parse_obj(response_body)

    async def delete_card_product(self, cart_product_id: int):
        url = f'/carts/{cart_product_id}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.delete(url)

    async def get_card_product(self, cart_product_id: int):
        url = f'/carts/{cart_product_id}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)

    async def get_user_card_products(self, telegram_id: int):
        url = f'/carts/users/{telegram_id}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        response_body = safely_decode_response_json(response)
        return models.CartProduct.parse_obj(response_body)

    async def update_card_product_quantity(self, cart_product_id: int, quantity: int):
        url = f'/carts/{cart_product_id}/'
        request_body = {'quantity': quantity}
        async with self._api_client.closing_http_client() as client:
            response = await client.patch(url, json=request_body)
