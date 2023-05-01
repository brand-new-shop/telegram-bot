import pathlib

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

import payments.handlers
import products.handlers
import support.handlers
import users.handlers
from config import load_config
from core.middlewares import DependencyInjectMiddleware
from core.services import APIClient
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

    api_client = APIClient(config.server_base_url)
    users_api_client = UsersAPIClient(api_client)
    support_api_client = SupportAPIClient(api_client)
    products_api_client = ProductsAPIClient(api_client)
    shop_info_api_client = ShopInfoAPIClient(api_client)
    payments_api_client = PaymentsAPIClient(api_client)

    dependency_inject_middleware = DependencyInjectMiddleware(
        server_base_url=config.server_base_url,
        users_api_client=users_api_client,
        support_api_client=support_api_client,
        products_api_client=products_api_client,
        shop_info_api_client=shop_info_api_client,
        payments_api_client=payments_api_client,
    )

    dispatcher.setup_middleware(dependency_inject_middleware)

    register_handlers(dispatcher)

    executor.start_polling(dispatcher=dispatcher, skip_updates=True)


if __name__ == '__main__':
    main()
