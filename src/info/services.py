import structlog

from core import exceptions
from core.services import safely_decode_response_json, BaseAPIClient
from info import models

__all__ = ('ShopInfoAPIClient',)

logger = structlog.get_logger('api_calls')


class ShopInfoAPIClient(BaseAPIClient):

    async def __get_shop_info(self, key: str) -> models.ShopInfo:
        url = f'/info/{key}/'
        logger.info('Request to API: shop info', key=key)
        response = await self._http_client.get(url)
        logger.info('Response from API: shop info', key=key)
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
