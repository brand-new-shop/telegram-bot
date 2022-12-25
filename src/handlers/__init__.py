from aiogram import Dispatcher

from . import start

__all__ = ('register_handlers',)


def register_handlers(dispatcher: Dispatcher) -> None:
    for module in (start,):
        module.register_handlers(dispatcher)
