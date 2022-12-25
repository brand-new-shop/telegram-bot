from aiogram import Dispatcher

from . import start, remove_message, balance, profile, support

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    for module in (remove_message, start, balance, profile, support):
        module.register_handlers(dispatcher)
