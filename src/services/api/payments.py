from decimal import Decimal

import models
from services.api.api_client import APIClient
from services.api.response import safely_decode_response_json, raise_for_unexpected_status_code

__all__ = ('PaymentsAPIClient',)


class PaymentsAPIClient:

    def __init__(self, api_client: APIClient):
        self._api_client = api_client

    async def create_coinbase_payment(
            self,
            telegram_id: int,
            payment_amount: Decimal,
    ) -> models.CoinbasePaymentCreated:
        url = f'/users/telegram-id/{telegram_id}/payments/coinbase/'
        async with self._api_client.closing_http_client() as client:
            response = await client.post(url, json={'payment_amount': str(payment_amount)})
        if response.status_code != 201:
            raise_for_unexpected_status_code(response.status_code)
        response_json = safely_decode_response_json(response)
        return models.CoinbasePaymentCreated.parse_obj(response_json)
