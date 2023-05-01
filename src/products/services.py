from pydantic import parse_obj_as

from core.services import APIClient, safely_decode_response_json
from products import models

__all__ = ('ProductsAPIClient',)


class ProductsAPIClient:

    def __init__(self, api_client: APIClient):
        self._api_client = api_client

    async def get_categories(self, parent_id: int | None = None) -> tuple[
        models.CategoryPreview]:
        data = []
        request_query_params = {}
        if parent_id is not None:
            request_query_params['parent_id'] = parent_id
        async with self._api_client.closing_http_client() as client:
            while True:
                response = await client.get('/categories/',
                                            params=request_query_params)
                response_data = response.json()
                data += response_data['categories']
                if response_data['is_end_of_list_reached']:
                    break
        return parse_obj_as(tuple[models.CategoryPreview, ...], data)

    async def get_products_by_category_id(self, category_id: int) -> tuple[
        models.ProductPreview, ...]:
        url = f'/categories/{category_id}/products/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        response_json = safely_decode_response_json(response)
        return parse_obj_as(tuple[models.ProductPreview, ...], response_json)

    async def get_category_by_id(self, category_id: int) -> models.Category:
        url = f'/categories/{category_id}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        response_json = safely_decode_response_json(response)
        return models.Category.parse_obj(response_json)

    async def get_product_by_id(self, product_id: int) -> models.Product:
        url = f'/categories/products/{product_id}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        response_json = safely_decode_response_json(response)
        return models.Product.parse_obj(response_json)
