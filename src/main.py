import pathlib

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from handlers import register_handlers
from config import Config
from middlewares import DependencyInjectMiddleware
from services.api import UsersAPIClient, SupportAPIClient, ProductsAPIClient, ShopInfoAPIClient, PaymentsAPIClient, \
    APIClient


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.ini'
    config = Config.from_file(config_file_path)

    bot = Bot(config.telegram_bot.token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher(bot, storage=MemoryStorage())

    api_client = APIClient(config.server.base_url.removesuffix('/') + '/api/')
    users_api_client = UsersAPIClient(api_client)
    support_api_client = SupportAPIClient(api_client)
    products_api_client = ProductsAPIClient(api_client)
    shop_info_api_client = ShopInfoAPIClient(api_client)
    payments_api_client = PaymentsAPIClient(api_client)

    dependency_inject_middleware = DependencyInjectMiddleware(
        server_base_url=config.server.base_url,
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
