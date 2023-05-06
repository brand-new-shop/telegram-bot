import structlog
from pydantic import parse_obj_as
from structlog.contextvars import bound_contextvars

from core import exceptions
from core.services import BaseAPIClient, safely_decode_response_json
from products.models import Order
from users.models import User

__all__ = ('UsersAPIClient',)

logger = structlog.get_logger('api_calls')


class UsersAPIClient(BaseAPIClient):

    async def create(self, telegram_id: int, username: str | None) -> User:
        url = '/users/'
        request_data = {'telegram_id': telegram_id, 'username': username}
        with bound_contextvars(request_data=request_data):
            logger.info('Request to API: create user')
            response = await self._http_client.post(url, json=request_data)
            logger.info('Response from API: create user', response=response)
            if response.status_code == 409:
                logger.warning('Response from API: user was already created')
                raise exceptions.UserAlreadyExistsError
            response_data = safely_decode_response_json(response)
            logger.info('Response from API: create user', data=response_data)
        return User.parse_obj(response_data)

    async def get_by_telegram_id(self, telegram_id: int) -> User:
        url = f'/users/telegram-id/{telegram_id}/'
        with bound_contextvars(telegram_id=telegram_id):
            logger.info('Request to API: user by Telegram ID')
            response = await self._http_client.get(url)
            logger.info(
                'Response from API: user by Telegram ID',
                response=response,
            )
            if response.status_code == 404:
                logger.warning('Response from API: user does not exist')
                raise exceptions.UserNotFoundError(
                    f'User by Telegram ID {telegram_id} is not found')
            response_data = safely_decode_response_json(response)
            logger.info(
                'Response from API: user by Telegram ID',
                data=response_data,
            )
        return User.parse_obj(response_data)

    async def get_orders_by_telegram_id(
            self,
            user_telegram_id: int,
    ) -> tuple[Order, ...]:
        url = f'/carts/users/{user_telegram_id}/orders/'
        with bound_contextvars(telegram_id=user_telegram_id):
            logger.info('Request to API: user orders list')
            response = await self._http_client.get(url)
            logger.info(
                'Response from API: user orders list',
                response=response,
            )
            response_data = safely_decode_response_json(response)
            logger.info(
                'Response from API: user orders list',
                data=response_data,
            )
        return parse_obj_as(tuple[Order, ...], response_data['orders'])
