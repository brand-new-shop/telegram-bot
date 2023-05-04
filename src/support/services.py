from pydantic import parse_obj_as

from core import exceptions
from support import models
from core.services import safely_decode_response_json, BaseAPIClient

__all__ = ('SupportAPIClient',)


class SupportAPIClient(BaseAPIClient):

    async def get_ticket_by_id(self, ticket_id: int) -> models.SupportTicket:
        url = f'/tickets/{ticket_id}/'
        response = await self._http_client.get(url)
        response_json = safely_decode_response_json(response)
        return models.SupportTicket.parse_obj(response_json)

    async def close_ticket_by_id(self, ticket_id: int) -> bool:
        url = f'/tickets/{ticket_id}/'
        response = await self._http_client.patch(url)
        return response.status_code == 204

    async def get_user_tickets(
            self,
            telegram_id: int,
    ) -> tuple[models.SupportTicketPreview, ...]:
        url = f'/users/telegram-id/{telegram_id}/tickets/'
        response = await self._http_client.get(url)
        if response.status_code == 404:
            raise exceptions.SupportTicketsNotFoundError
        response_json = safely_decode_response_json(response)
        return parse_obj_as(tuple[models.SupportTicketPreview, ...],
                            response_json)

    async def create_ticket(
            self,
            support_ticket_create: models.SupportTicketCreate,
    ) -> models.SupportTicketCreated:
        url = f'/users/telegram-id/{support_ticket_create.user_telegram_id}/tickets/'
        request_json = support_ticket_create.dict(include={'issue', 'subject'})
        response = await self._http_client.post(url, json=request_json)
        if response.status_code == 429:
            seconds_to_wait = int(response.json()['seconds_to_wait'])
            raise exceptions.SupportTicketCreationRateLimitExceededError(
                seconds_to_wait=seconds_to_wait)
        response_json = safely_decode_response_json(response)
        return models.SupportTicketCreated.parse_obj(response_json)

    async def create_reply_to_ticket(
            self,
            ticket_id: int,
            reply_text: str,
    ) -> models.ReplyToTicketCreated:
        url = f'/tickets/{ticket_id}/replies/'
        request_body = {'issue': reply_text}
        response = await self._http_client.post(url, json=request_body)
        response_json = safely_decode_response_json(response)
        return models.ReplyToTicketCreated.parse_obj(response_json)

    async def get_ticket_reply_ids(
            self,
            ticket_id: int,
    ) -> tuple[int]:
        url = f'/tickets/{ticket_id}/replies/'
        response = await self._http_client.get(url)
        response_json = safely_decode_response_json(response)
        return parse_obj_as(tuple[int, ...], response_json)

    async def get_reply_to_ticket(
            self,
            ticket_reply_id: int,
    ) -> models.ReplyToTicket:
        url = f'/tickets/replies/{ticket_reply_id}/'
        response = await self._http_client.get(url)
        response_json = safely_decode_response_json(response)
        return models.ReplyToTicket.parse_obj(response_json)
