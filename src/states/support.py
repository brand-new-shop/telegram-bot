from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = (
    'NewSupportSubjectStates',
    'NewSupportRequestStates',
)


class NewSupportSubjectStates(StatesGroup):
    name = State()


class NewSupportRequestStates(StatesGroup):
    subject = State()
    issue = State()
