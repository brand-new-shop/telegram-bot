from pydantic import parse_obj_as

import models
from services.api.api_client import APIClient
from services.api.response import raise_for_unexpected_status_code, safely_decode_response_json

__all__ = ('ProductsAPIClient',)


class ProductsAPIClient:

    def __init__(self, api_client: APIClient):
        self._api_client = api_client

    async def get_categories(self) -> tuple[models.CategoryPreview]:
        async with self._api_client.closing_http_client() as client:
            response = await client.get('/categories/')
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return parse_obj_as(tuple[models.CategoryPreview, ...], response_json)

    async def get_products_by_category_id(self, category_id: int) -> tuple[models.ProductPreview, ...]:
        url = f'/categories/{category_id}/products/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return parse_obj_as(tuple[models.ProductPreview, ...], response_json)

    async def get_subcategories_by_category_id(self, category_id: int) -> tuple[models.CategoryPreview, ...]:
        url = f'/categories/{category_id}/subcategories/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return parse_obj_as(tuple[models.CategoryPreview, ...], response_json)

    async def get_category_by_id(self, category_id: int) -> models.Category:
        url = f'/categories/{category_id}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return models.Category.parse_obj(response_json)

    async def get_product_by_id(self, product_id: int) -> models.Product:
        url = f'/categories/products/{product_id}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return models.Product.parse_obj(response_json)
