import pathlib
from functools import partial

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

import payments.handlers
import products.handlers
import support.handlers
import users.handlers
from config import load_config
from core.middlewares import DependencyInjectMiddleware
from core.services import closing_http_client_factory
from info.services import ShopInfoAPIClient
from payments.services import PaymentsAPIClient
from products.services import ProductsAPIClient
from support.services import SupportAPIClient
from users.services import UsersAPIClient


def register_handlers(dispatcher: Dispatcher) -> None:
    payments.handlers.register_handlers(dispatcher)
    products.handlers.register_handlers(dispatcher)
    support.handlers.register_handlers(dispatcher)
    users.handlers.register_handlers(dispatcher)


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.toml'
    config = load_config(config_file_path)

    bot = Bot(config.telegram_bot_token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher(bot, storage=MemoryStorage())

    dependency_inject_middleware = DependencyInjectMiddleware(
        closing_http_client_factory=partial(
            closing_http_client_factory,
            base_url=config.server_base_url,
        ),
    )

    dispatcher.setup_middleware(dependency_inject_middleware)

    register_handlers(dispatcher)

    executor.start_polling(dispatcher=dispatcher, skip_updates=True)


if __name__ == '__main__':
    main()
