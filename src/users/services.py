from pydantic import parse_obj_as

from core import exceptions
from core.services import BaseAPIClient, safely_decode_response_json
from products.models import OrdersTotalCount, Order
from users.models import User

__all__ = ('UsersAPIClient',)


class UsersAPIClient(BaseAPIClient):

    async def create(self, telegram_id: int, username: str | None) -> User:
        url = '/users/'
        request_data = {'telegram_id': telegram_id, 'username': username}
        response = await self._http_client.post(url, json=request_data)
        if response.status_code == 409:
            raise exceptions.UserAlreadyExistsError
        response_json = safely_decode_response_json(response)
        return User.parse_obj(response_json)

    async def get_by_telegram_id(self, telegram_id: int) -> User:
        url = f'/users/telegram-id/{telegram_id}/'
        response = await self._http_client.get(url)
        if response.status_code == 404:
            raise exceptions.UserNotFoundError(
                f'User by Telegram ID {telegram_id} is not found')
        response_json = safely_decode_response_json(response)
        return User.parse_obj(response_json)

    async def get_orders_by_telegram_id(
            self,
            user_telegram_id: int,
    ) -> tuple[Order, ...]:
        url = f'/carts/users/{user_telegram_id}/orders/'
        response = await self._http_client.get(url)
        response_json = safely_decode_response_json(response)
        return parse_obj_as(tuple[Order, ...], response_json['orders'])

    async def get_user_orders_count(self, telegram_id: int) -> OrdersTotalCount:
        url = f'/users/telegram-id/{telegram_id}/orders/count/'
        response = await self._http_client.get(url)
        response_json = safely_decode_response_json(response)
        return OrdersTotalCount.parse_obj(response_json)
