import contextlib

import httpx

__all__ = ('APIClient',)


class APIClient:

    def __init__(self, base_url: str):
        self.__base_url = base_url

    @contextlib.asynccontextmanager
    async def closing_http_client(self) -> httpx.AsyncClient:
        async with httpx.AsyncClient(base_url=self.__base_url) as client:
            yield client
