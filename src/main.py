import pathlib

from aiogram import Bot, Dispatcher, executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import ParseMode

from handlers import register_handlers
from config import Config
from middlewares import DependencyInjectMiddleware
from services.api import UsersAPIClient, SupportAPIClient


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.ini'
    config = Config.from_file(config_file_path)

    bot = Bot(config.telegram_bot.token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher(bot, storage=MemoryStorage())

    users_api_client = UsersAPIClient(config.server.base_url)
    support_api_client = SupportAPIClient(config.server.base_url)

    dependency_inject_middleware = DependencyInjectMiddleware(
        users_api_client=users_api_client,
        support_api_client=support_api_client
    )

    dispatcher.setup_middleware(dependency_inject_middleware)

    register_handlers(dispatcher)

    executor.start_polling(dispatcher=dispatcher, skip_updates=True)


if __name__ == '__main__':
    main()
