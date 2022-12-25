from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from services.api import ProductsAPIClient
from shortcuts import answer_views
from views import CategoriesListView


async def on_categories_list(message: Message, products_api_client: ProductsAPIClient) -> None:
    categories = await products_api_client.get_categories()
    view = CategoriesListView(categories)
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_categories_list,
        Text('🛒 Products'),
        state='*',
    )
