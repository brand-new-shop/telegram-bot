import structlog
from pydantic import parse_obj_as
from structlog.contextvars import bound_contextvars

from cart import models, exceptions
from core.services import BaseAPIClient, safely_decode_response_json

__all__ = ('CartAPIClient',)

logger = structlog.get_logger('api_calls')


class CartAPIClient(BaseAPIClient):

    async def create_cart_product(
            self,
            telegram_id: int,
            product_id: int,
            quantity: int,
    ) -> models.CartProduct:
        url = f'/carts/users/{telegram_id}/'
        request_body = {'product_id': product_id, 'quantity': quantity}
        with bound_contextvars(
                request_body=request_body,
                telegram_id=telegram_id,
        ):
            logger.info('Request to API: create cart product')
            response = await self._http_client.post(url, json=request_body)
            if response.status_code == 409:
                logger.info('Response from API: product already in cart')
                raise exceptions.ProductAlreadyInCartError
            logger.info('Response from API: product added to cart', )
            response_data = safely_decode_response_json(response)
            logger.info(
                'Response from API: create cart product',
                data=response_data,
            )
        return models.CartProduct.parse_obj(response_data)

    async def delete_cart_product(self, cart_product_id: int):
        url = f'/carts/{cart_product_id}/'
        response = await self._http_client.delete(url)

    async def get_cart_product(self, cart_product_id: int):
        url = f'/carts/{cart_product_id}/'
        response = await self._http_client.get(url)
        return models.CartProduct.parse_obj(response.json())

    async def get_cart_products(
            self,
            telegram_id: int,
    ) -> tuple[models.CartProduct, ...]:
        url = f'/carts/users/{telegram_id}/'
        cart_products: list[dict] = []
        with bound_contextvars(telegram_id=telegram_id):
            while True:
                logger.info('Request to API: cart products')
                response = await self._http_client.get(url)
                logger.info(
                    'Response from API: cart products',
                    response=response,
                )
                response_data = safely_decode_response_json(response)
                cart_products += response_data['cart_products']
                if response_data['is_end_of_list_reached']:
                    break
            logger.info('Response from API: cart products', data=response_data)
        return parse_obj_as(tuple[models.CartProduct, ...], cart_products)

    async def update_cart_product_quantity(self, cart_product_id: int,
                                           quantity: int):
        url = f'/carts/{cart_product_id}/'
        request_body = {'quantity': quantity}
        response = await self._http_client.patch(url, json=request_body)

    async def get_orders_statistics(
            self,
            telegram_id: int,
    ) -> models.OrdersStatistics:
        url = f'/carts/users/{telegram_id}/orders/statistics/'
        with bound_contextvars(telegram_id=telegram_id):
            logger.info('Request to API: orders statistics')
            response = await self._http_client.get(url)
            logger.info(
                'Response from API: orders statistics',
                response=response,
            )
            response_data = response.json()
            logger.info(
                'Response from API: orders statistics',
                data=response_data,
            )
        return models.OrdersStatistics.parse_obj(response_data)
