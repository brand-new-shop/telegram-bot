import json

import httpx
from pydantic import parse_obj_as

import exceptions
import models

__all__ = ('UsersAPIClient',)


class UsersAPIClient:

    def __init__(self, base_url: str):
        self.__base_url = base_url

    async def create(self, telegram_id: int, username: str | None) -> models.User:
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.post('/users/', json={'telegram_id': telegram_id, 'username': username})
        if response.status_code == 409:
            raise exceptions.UserAlreadyExistsError
        elif response.status_code != 201:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return models.User.parse_obj(response_json)

    async def get_by_telegram_id(self, telegram_id: int) -> models.User:
        url = f'/users/telegram-id/{telegram_id}/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get(url)
        if response.status_code == 404:
            raise exceptions.UserNotFoundError(f'User by Telegram ID {telegram_id} is not found')
        elif response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
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
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get(url, params=params)
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return parse_obj_as(tuple[models.OrderPreview, ...], response_json)

    async def get_orders_statistics(self, user_telegram_id: int) -> models.OrdersStatistics:
        url = f'/users/telegram-id/{user_telegram_id}/orders/statistics/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return models.OrdersStatistics.parse_obj(response_json)
