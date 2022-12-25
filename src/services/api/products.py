import json

import httpx
from pydantic import parse_obj_as

import models
import exceptions

__all__ = ('ProductsAPIClient',)


class ProductsAPIClient:

    def __init__(self, base_url: str):
        self.__base_url = base_url

    async def get_categories(self) -> tuple[models.Category]:
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get('/categories/')
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return parse_obj_as(tuple[models.Category, ...], response_json)
