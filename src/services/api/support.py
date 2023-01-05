from pydantic import parse_obj_as

import exceptions
import models
from services.api.api_client import APIClient
from services.api.response import raise_for_unexpected_status_code, safely_decode_response_json

__all__ = ('SupportAPIClient',)


class SupportAPIClient:

    def __init__(self, api_client: APIClient):
        self._api_client = api_client

    async def get_ticket_by_id(self, ticket_id: int) -> models.SupportTicket:
        url = f'/tickets/{ticket_id}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return models.SupportTicket.parse_obj(response_json)

    async def close_ticket_by_id(self, ticket_id: int) -> bool:
        url = f'/tickets/{ticket_id}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.patch(url)
        return response.status_code == 204

    async def get_user_tickets(self, telegram_id: int) -> tuple[models.SupportTicketPreview, ...]:
        url = f'/users/telegram-id/{telegram_id}/tickets/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code == 404:
            raise exceptions.SupportTicketsNotFoundError
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return parse_obj_as(tuple[models.SupportTicketPreview, ...], response_json)

    async def create_ticket(self, support_ticket_create: models.SupportTicketCreate) -> models.SupportTicketCreated:
        url = f'/users/telegram-id/{support_ticket_create.user_telegram_id}/tickets/'
        request_json = support_ticket_create.dict(include={'issue', 'subject'})
        async with self._api_client.closing_http_client() as client:
            response = await client.post(url, json=request_json)
        if response.status_code == 429:
            seconds_to_wait = int(response.json()['seconds_to_wait'])
            raise exceptions.SupportTicketCreationRateLimitExceededError(seconds_to_wait)
        elif response.status_code != 201:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return models.SupportTicketCreated.parse_obj(response_json)

    async def create_reply_to_ticket(self, ticket_id: int, reply_text: str) -> models.ReplyToTicketCreated:
        url = f'/tickets/{ticket_id}/replies/'
        request_body = {'issue': reply_text}
        async with self._api_client.closing_http_client() as client:
            response = await client.post(url, json=request_body)
        if response.status_code != 201:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return models.ReplyToTicketCreated.parse_obj(response_json)

    async def get_ticket_reply_ids(self, ticket_id: int) -> tuple[int]:
        url = f'/tickets/{ticket_id}/replies/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return parse_obj_as(tuple[int, ...], response_json)

    async def get_reply_to_ticket(self, ticket_reply_id: int) -> models.ReplyToTicket:
        url = f'/tickets/replies/{ticket_reply_id}/'
        async with self._api_client.closing_http_client() as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return models.ReplyToTicket.parse_obj(response_json)
