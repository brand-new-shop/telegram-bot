from aiogram import Dispatcher

from . import start, remove_message, balance, profile

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    for module in (remove_message, start, balance, profile):
        module.register_handlers(dispatcher)
