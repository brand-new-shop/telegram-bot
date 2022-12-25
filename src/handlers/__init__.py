from aiogram import Dispatcher

from . import start, remove_message, balance, profile, support, products

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    for module in (remove_message, start, balance, profile, support, products):
        module.register_handlers(dispatcher)
