import contextlib
import json
import logging
from abc import ABC
from typing import NewType, Callable

import httpx

from core import exceptions

__all__ = (
    'HTTPClient',
    'HTTPClientFactory',
    'closing_http_client_factory',
    'safely_decode_response_json',
    'raise_for_error',
    'get_decoded_json_and_check_for_errors',
    'BaseAPIClient',
)

HTTPClient = NewType('HTTPClient', httpx.AsyncClient)
HTTPClientFactory = Callable[[], HTTPClient]


@contextlib.asynccontextmanager
async def closing_http_client_factory(base_url: str) -> HTTPClient:
    async with httpx.AsyncClient(base_url=base_url) as client:
        yield HTTPClient(client)


class BaseAPIClient(ABC):

    def __init__(self, http_client: HTTPClient):
        self._http_client = http_client


status_code_to_errors: dict[int, dict[str, type[exceptions.ServerAPIError]]] = {
    404: {
        'User is not found': exceptions.UserNotFoundError,
        'Not enough product stocks': exceptions.NotEnoughProductStocksError,
        'Cart product is not found': exceptions.CartProductNotFoundError,
        'Product is not found': exceptions.ProductNotFoundError,
        'User\'s tickets have not found': exceptions.UserHasNoTicketsError,
        'Ticket is not found': exceptions.TicketNotFoundError,
    },
    409: {
        'Product is already exists in cart': exceptions.CartProductAlreadyExistsError,
        'Ticket was closed, so now only read-only operations available': exceptions.ClosedTicketError,
        'User already exists': exceptions.UserAlreadyExistsError,
    },
    429: {
        'Ticket creation rate limit exceeded': exceptions.SupportTicketCreationRateLimitExceededError,
    }
}


def safely_decode_response_json(response: httpx.Response) -> dict | list:
    """Unified way to get JSON from httpx response to catch it."""
    error_message = 'Unable to parse response JSON'
    try:
        return response.json()
    except json.JSONDecodeError:
        logging.error(error_message)
        raise exceptions.ServerAPIError(error_message)


def raise_for_error(status_code: int, response_body: dict) -> None:
    detail = response_body.get('detail',
                               f'Unexpected status code "{status_code}"')
    error_detail_to_exception_class = status_code_to_errors.get(status_code, {})
    exception_class = error_detail_to_exception_class.get(detail,
                                                          exceptions.ServerAPIError)
    raise exception_class(detail)


def get_decoded_json_and_check_for_errors(
        response: httpx.Response) -> list | dict:
    response_body = safely_decode_response_json(response)
    if response.is_error:
        raise_for_error(response.status_code, response_body)
    return response_body
