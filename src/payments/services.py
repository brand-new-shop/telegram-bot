from decimal import Decimal

import structlog
from structlog.contextvars import bound_contextvars

from core.services import safely_decode_response_json, BaseAPIClient
from payments import models

__all__ = ('PaymentsAPIClient',)

logger = structlog.get_logger('api_calls')


class PaymentsAPIClient(BaseAPIClient):

    async def create_coinbase_payment(
            self,
            telegram_id: int,
            payment_amount: Decimal,
    ) -> models.CoinbasePaymentCreated:
        url = f'/users/telegram-id/{telegram_id}/payments/coinbase/'
        request_data = {'payment_amount': str(payment_amount)}
        with bound_contextvars(
                telegram_id=telegram_id,
                payment_amount=payment_amount,
        ):
            logger.info('Request to API: create coinbase payment')
            response = await self._http_client.post(url, json=request_data)
            logger.info(
                'Response from API: create coinbase payment',
                response=response,
            )
            response_json = safely_decode_response_json(response)
            logger.info(
                'Response from API: create coinbase payment',
                data=response_json,
            )
        return models.CoinbasePaymentCreated.parse_obj(response_json)
