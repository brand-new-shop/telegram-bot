import json

import httpx
from pydantic import parse_obj_as

import models
import exceptions

__all__ = ('SupportAPIClient',)


class SupportAPIClient:

    def __init__(self, base_url: str):
        self.__base_url = base_url

    async def create_subject(self, name: str) -> models.SupportSubject:
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.post('/support/', json={'name': name})
        if response.status_code != 201:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return models.SupportSubject.parse_obj(response_json)

    async def get_subjects(self) -> tuple[models.SupportSubject, ...]:
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get('/support/')
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return parse_obj_as(tuple[models.SupportSubject, ...], response_json)

    async def get_subject_by_id(self, support_subject_id: int) -> models.SupportSubject:
        url = f'/support/{support_subject_id}/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.post(url)
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return models.SupportSubject.parse_obj(response_json())

    async def get_request_by_id(self, support_request_id: int) -> models.SupportRequest:
        url = f'/support/requests/{support_request_id}/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return models.SupportRequest.parse_obj(response_json)

    async def get_requests_by_user_telegram_id(self, user_telegram_id: int) -> tuple[models.SupportRequestPreview, ...]:
        url = f'/support/requests/users/telegram-id/{user_telegram_id}/'
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.get(url)
        if response.status_code != 200:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return parse_obj_as(tuple[models.SupportRequestPreview, ...], response_json)

    async def create_request(self, support_request_create: models.SupportRequestCreate) -> models.SupportRequestCreated:
        url = f'/support/requests/users/telegram-id/{support_request_create.user_telegram_id}/'
        request_json = support_request_create.dict(include={'issue', 'subject_id'})
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            response = await client.post(url, json=request_json)
        if response.status_code != 201:
            raise exceptions.ServerAPIError(f'Unexpected status code "{response.status_code}"')
        try:
            response_json = response.json()
        except json.JSONDecodeError:
            raise exceptions.ServerAPIError('Unable to parse response JSON')
        return models.SupportRequestCreated.parse_obj(response_json)
