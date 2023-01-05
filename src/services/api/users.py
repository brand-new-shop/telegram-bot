from pydantic import parse_obj_as

import exceptions
import models
from services.api.api_client import APIClient
from services.api.response import safely_decode_response_json, raise_for_unexpected_status_code

__all__ = ('UsersAPIClient',)


class UsersAPIClient:

    def __init__(self, api_client: APIClient):
        self._api_client = api_client

    async def create(self, telegram_id: int, username: str | None) -> models.User:
        async with self._api_client.closing_http_client() as client:
            response = await client.post('/users/', json={'telegram_id': telegram_id, 'username': username})
        if response.status_code == 409:
            raise exceptions.UserAlreadyExistsError
        elif response.status_code != 201:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return models.User.parse_obj(response_json)

    async def get_by_telegram_id(self, telegram_id: int) -> models.User:
        url = f'/users/telegram-id/{telegram_id}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code == 404:
            raise exceptions.UserNotFoundError(f'User by Telegram ID {telegram_id} is not found')
        elif response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return models.User.parse_obj(response_json)

    async def get_orders_by_telegram_id(
            self,
            user_telegram_id: int,
            limit: int | None = None,
            offset: int | None = None,
    ) -> tuple[models.OrderPreview, ...]:
        url = f'/users/telegram-id/{user_telegram_id}/orders/'
        params = {}
        if limit is not None:
            params['limit'] = limit
        if offset is not None:
            params['offset'] = offset
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url, params=params)
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return parse_obj_as(tuple[models.OrderPreview, ...], response_json)

    async def get_orders_statistics(self, user_telegram_id: int) -> models.OrdersStatistics:
        url = f'/users/telegram-id/{user_telegram_id}/orders/statistics/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return models.OrdersStatistics.parse_obj(response_json)

    async def get_user_orders_count(self, telegram_id: int) -> models.OrdersTotalCount:
        url = f'/users/telegram-id/{telegram_id}/orders/count/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return models.OrdersTotalCount.parse_obj(response_json)
