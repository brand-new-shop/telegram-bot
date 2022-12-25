from aiogram.dispatcher.filters.state import StatesGroup, State

__all__ = ('NewSupportSubjectStates',)


class NewSupportSubjectStates(StatesGroup):
    name = State()
