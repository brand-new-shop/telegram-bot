from decimal import Decimal

from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, ContentType

from services.api import UsersAPIClient, PaymentsAPIClient
from shortcuts import answer_views, edit_message_by_view
from states import BalanceTopUpStates
from views import UserBalanceView, PaymentMethodsView, CoinbasePaymentView

__all__ = ('register_handlers',)


async def on_top_up_via_coinbase(
        callback_query: CallbackQuery,
        state: FSMContext,
        payments_api_client: PaymentsAPIClient,
) -> None:
    state_data = await state.get_data()
    await state.finish()
    payment_amount = Decimal(state_data['payment_amount'])
    coinbase_payment_created = await payments_api_client.create_coinbase_payment(
        telegram_id=callback_query.from_user.id,
        payment_amount=payment_amount,
    )
    view = CoinbasePaymentView(payment_amount, coinbase_payment_created.hosted_url)
    await edit_message_by_view(callback_query.message, view)
    await callback_query.answer()


async def on_top_up_balance_amount_input(message: Message, state: FSMContext) -> None:
    await state.update_data(payment_amount=message.text)
    await answer_views(message, PaymentMethodsView())


async def on_top_up_balance(callback_query: CallbackQuery) -> None:
    await BalanceTopUpStates.amount.set()
    await callback_query.message.edit_text('🔢 Enter amount')
    await callback_query.answer()


async def on_user_balance(message: Message, users_api_client: UsersAPIClient) -> None:
    user = await users_api_client.get_by_telegram_id(message.from_user.id)
    view = UserBalanceView(user.balance)
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_top_up_via_coinbase,
        Text('coinbase-top-up'),
        state='*',
    )
    dispatcher.register_message_handler(
        on_top_up_balance_amount_input,
        content_types=ContentType.TEXT,
        state=BalanceTopUpStates.amount,
    )
    dispatcher.register_callback_query_handler(
        on_top_up_balance,
        Text('top-up'),
        state='*',
    )
    dispatcher.register_message_handler(on_user_balance, Text('💲 Balance'), state='*')
