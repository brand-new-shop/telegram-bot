import structlog
from structlog.contextvars import bound_contextvars
from pydantic import parse_obj_as

from core.services import safely_decode_response_json, BaseAPIClient
from products import models

__all__ = ('ProductsAPIClient',)

logger = structlog.get_logger('api_calls')


class ProductsAPIClient(BaseAPIClient):

    async def get_categories(
            self,
            parent_id: int | None = None,
    ) -> tuple[models.CategoryPreview, ...]:
        data = []
        url = '/categories/'
        request_query_params = {}
        if parent_id is not None:
            request_query_params['parent_id'] = parent_id

        with bound_contextvars(parent_category_id=parent_id):
            while True:
                logger.info('Request to API: categories list')
                response = await self._http_client.get(
                    url=url,
                    params=request_query_params,
                )
                logger.info(
                    'Response from API: categories list',
                    response=response,
                )
                response_data = response.json()
                data += response_data['categories']
                if response_data['is_end_of_list_reached']:
                    break
            logger.info('Response from API: categories list', data=data)
        return parse_obj_as(tuple[models.CategoryPreview, ...], data)

    async def get_products_by_category_id(
            self,
            category_id: int,
    ) -> tuple[models.ProductPreview, ...]:
        url = f'/categories/{category_id}/products/'
        products: list[dict] = []

        with bound_contextvars(category_id=category_id):
            while True:
                logger.info('Request to API: products by category ID')
                response = await self._http_client.get(url)
                logger.info(
                    'Response from API: products by category ID',
                    response=response,
                )
                response_json = safely_decode_response_json(response)
                products += response_json['products']
                if response_json['is_end_of_list_reached']:
                    break
            logger.info(
                'Response from API: products by category ID',
                data=response_json,
            )
        return parse_obj_as(tuple[models.ProductPreview, ...], products)

    async def get_category_by_id(
            self,
            category_id: int,
    ) -> models.Category:
        url = f'/categories/{category_id}/'
        response = await self._http_client.get(url)
        response_json = safely_decode_response_json(response)
        return models.Category.parse_obj(response_json)

    async def get_product_by_id(self, product_id: int) -> models.Product:
        url = f'/categories/products/{product_id}/'
        with bound_contextvars(product_id=product_id):
            logger.info('Request to API: product by ID')
            response = await self._http_client.get(url)
            logger.info(
                'Response from API: product by ID',
                response=response,
            )
            response_data = safely_decode_response_json(response)
            logger.info('Response from API: product by ID', data=response_data)
        return models.Product.parse_obj(response_data)
