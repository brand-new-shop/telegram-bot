import asyncio

from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

import models
from callback_data import CategoryDetailCallbackData
from services.api import ProductsAPIClient
from shortcuts import answer_views, edit_message_by_view
from views import CategoriesListView, CategoryMenuView


async def on_category_menu(
        callback_query: CallbackQuery,
        callback_data: models.ChooseCategoryCallbackData,
        products_api_client: ProductsAPIClient,
) -> None:
    category_id = callback_data['category_id']
    subcategories, products = await asyncio.gather(products_api_client.get_subcategories_by_category_id(category_id),
                                                   products_api_client.get_products_by_category_id(category_id))
    view = CategoryMenuView(subcategories, products)
    await edit_message_by_view(callback_query.message, view)
    await callback_query.answer()


async def on_categories_list(message: Message, products_api_client: ProductsAPIClient) -> None:
    categories = await products_api_client.get_categories()
    view = CategoriesListView(categories)
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_category_menu,
        CategoryDetailCallbackData().filter(),
        state='*',
    )
    dispatcher.register_message_handler(
        on_categories_list,
        Text('🛒 Products'),
        state='*',
    )
