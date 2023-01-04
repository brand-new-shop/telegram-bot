from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = (
    'NewSupportRequestStates',
    'NewReplyToTicketStates',
)


class NewSupportRequestStates(StatesGroup):
    subject = State()
    issue = State()


class NewReplyToTicketStates(StatesGroup):
    issue = State()
