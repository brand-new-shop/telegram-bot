from decimal import Decimal

from payments import models
from core.services import safely_decode_response_json, BaseAPIClient

__all__ = ('PaymentsAPIClient',)


class PaymentsAPIClient(BaseAPIClient):

    async def create_coinbase_payment(
            self,
            telegram_id: int,
            payment_amount: Decimal,
    ) -> models.CoinbasePaymentCreated:
        url = f'/users/telegram-id/{telegram_id}/payments/coinbase/'
        request_data = {'payment_amount': str(payment_amount)}
        response = await self._http_client.post(url, json=request_data)
        response_json = safely_decode_response_json(response)
        return models.CoinbasePaymentCreated.parse_obj(response_json)
