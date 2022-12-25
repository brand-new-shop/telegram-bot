import pathlib

from aiogram import Bot, Dispatcher, executor
from aiogram.types import ParseMode

from handlers import register_handlers
from config import Config
from middlewares import DependencyInjectMiddleware
from services.api.users import UsersAPIClient


def main():
    config_file_path = pathlib.Path(__file__).parent.parent / 'config.ini'
    config = Config.from_file(config_file_path)

    bot = Bot(config.telegram_bot.token, parse_mode=ParseMode.HTML)
    dispatcher = Dispatcher(bot)

    users_api_client = UsersAPIClient(config.server.base_url)
    dispatcher.setup_middleware(DependencyInjectMiddleware(users_api_client=users_api_client))

    register_handlers(dispatcher)

    executor.start_polling(dispatcher=dispatcher, skip_updates=True)


if __name__ == '__main__':
    main()
