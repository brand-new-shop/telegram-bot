from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = ('BalanceTopUpStates',)


class BalanceTopUpStates(StatesGroup):
    amount = State()
