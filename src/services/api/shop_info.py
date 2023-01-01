import json

import httpx

import exceptions
import models

__all__ = ('ShopInfoAPIClient',)


class ShopInfoAPIClient:

    def __init__(self, base_url: str):
        self.__base_url = base_url

    async def __get_shop_info(self, key: str) -> models.ShopInfo:
        url = f'/info/{key}/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get(url)
        if response.status_code == 404:
            raise exceptions.ShopInfoNotFoundError(key=key)
        elif response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return models.ShopInfo.parse_obj(response_json)

    async def get_faq_info(self) -> models.ShopInfo:
        return await self.__get_shop_info('faq')

    async def get_rules_info(self) -> models.ShopInfo:
        return await self.__get_shop_info('rules')

    async def get_support_rules_info(self) -> models.ShopInfo:
        return await self.__get_shop_info('support_rules')
