import json

import httpx

import exceptions
from models import User

__all__ = ('UsersAPIClient',)


class UsersAPIClient:

    def __init__(self, base_url: str):
        self.__base_url = base_url

    async def create(self, telegram_id: int, username: str | None) -> User:
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
        return User.parse_obj(response_json)

    async def get_by_telegram_id(self, telegram_id: int) -> User:
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
        return User.parse_obj(response_json)
