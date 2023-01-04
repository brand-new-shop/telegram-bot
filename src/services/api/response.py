import logging
import json
from typing import Protocol

import exceptions

__all__ = (
    'safely_decode_response_json',
    'raise_for_unexpected_status_code',
)


class HTTPResponse(Protocol):

    def json(self) -> dict | list: ...


def safely_decode_response_json(response: HTTPResponse) -> dict | list:
    """Unified way to get JSON from httpx response to catch it."""
    error_message = 'Unable to parse response JSON'
    try:
        return response.json()
    except json.JSONDecodeError:
        logging.error(error_message)
        raise exceptions.ServerAPIError(error_message)


def raise_for_unexpected_status_code(status_code: int) -> None:
    error_message = f'Unexpected status code "{status_code}"'
    logging.error(error_message)
    raise exceptions.ServerAPIError(error_message)
