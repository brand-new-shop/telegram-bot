import json

import httpx
from pydantic import parse_obj_as

import models
import exceptions

__all__ = ('SupportAPIClient',)


class SupportAPIClient:

    def __init__(self, base_url: str):
        self.__base_url = base_url

    async def get_ticket_by_id(self, ticket_id: int) -> models.SupportTicket:
        url = f'/tickets/{ticket_id}/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return models.SupportTicket.parse_obj(response_json)

    async def close_ticket_by_id(self, ticket_id: int) -> bool:
        url = f'/tickets/{ticket_id}/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.patch(url)
        return response.status_code == 204

    async def get_user_tickets(self, telegram_id: int) -> tuple[models.SupportTicketPreview, ...]:
        url = f'/users/telegram-id/{telegram_id}/tickets/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return parse_obj_as(tuple[models.SupportTicketPreview, ...], response_json)

    async def create_ticket(self, support_ticket_create: models.SupportTicketCreate) -> models.SupportTicketCreated:
        url = f'/users/telegram-id/{support_ticket_create.user_telegram_id}/tickets/'
        request_json = support_ticket_create.dict(include={'issue', 'subject'})
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.post(url, json=request_json)
        if response.status_code == 429:
            seconds_to_wait = int(response.json()['seconds_to_wait'])
            raise exceptions.SupportTicketCreationRateLimitExceededError(seconds_to_wait)
        elif response.status_code != 201:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return models.SupportTicketCreated.parse_obj(response_json)
