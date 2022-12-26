import json

import httpx
from pydantic import parse_obj_as

import models
import exceptions

__all__ = ('ProductsAPIClient',)


class ProductsAPIClient:

    def __init__(self, base_url: str):
        self.__base_url = base_url

    async def get_categories(self) -> tuple[models.CategoryPreview]:
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get('/categories/')
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return parse_obj_as(tuple[models.CategoryPreview, ...], response_json)

    async def get_products_by_category_id(self, category_id: int) -> tuple[models.ProductPreview, ...]:
        url = f'/categories/{category_id}/products/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return parse_obj_as(tuple[models.ProductPreview, ...], response_json)

    async def get_subcategories_by_category_id(self, category_id: int) -> tuple[models.CategoryPreview, ...]:
        url = f'/categories/{category_id}/subcategories/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return parse_obj_as(tuple[models.CategoryPreview, ...], response_json)

    async def get_category_by_id(self, category_id: int) -> models.Category:
        url = f'/categories/{category_id}/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return models.Category.parse_obj(response_json)
