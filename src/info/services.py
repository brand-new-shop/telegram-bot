from core import exceptions
from core.services import APIClient, safely_decode_response_json
from info import models

__all__ = ('ShopInfoAPIClient',)


class ShopInfoAPIClient:

    def __init__(self, api_client: APIClient):
        self._api_client = api_client

    async def __get_shop_info(self, key: str) -> models.ShopInfo:
        url = f'/info/{key}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code == 404:
            raise exceptions.ShopInfoNotFoundError(key=key)
        response_json = safely_decode_response_json(response)
        return models.ShopInfo.parse_obj(response_json)

    async def get_faq_info(self) -> models.ShopInfo:
        return await self.__get_shop_info('faq')

    async def get_rules_info(self) -> models.ShopInfo:
        return await self.__get_shop_info('rules')

    async def get_support_rules_info(self) -> models.ShopInfo:
        return await self.__get_shop_info('support_rules')
