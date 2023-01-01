from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = (
    'NewSupportRequestStates',
)


class NewSupportRequestStates(StatesGroup):
    subject = State()
    issue = State()
