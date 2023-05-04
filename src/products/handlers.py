import structlog
from aiogram import Dispatcher
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.utils.exceptions import BadRequest

from core.services import HTTPClientFactory
from core.shortcuts import answer_views, edit_message_by_view
from products import models
from products.callback_data import (
    CategoryDetailCallbackData,
    ProductDetailCallbackData,
)
from products.services import ProductsAPIClient
from products.views import (
    CategoriesListView,
    ProductDetailView,
    ProductDetailPhotosView,
)

logger = structlog.get_logger('telegram_bot')


async def on_product_menu(
        callback_query: CallbackQuery,
        callback_data: models.ChooseProductCallbackData,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    product_id = callback_data['product_id']
    async with closing_http_client_factory() as http_client:
        products_api_client = ProductsAPIClient(http_client)
        product = await products_api_client.get_product_by_id(product_id)
    views = []
    if product.picture_urls:
        views.append(ProductDetailPhotosView(product))
    views.append(ProductDetailView(product))
    await answer_views(callback_query.message, *views)
    await callback_query.answer()


async def show_nested_categories_list(
        callback_query: CallbackQuery,
        closing_http_client_factory: HTTPClientFactory,
        callback_data: dict,
) -> None:
    category_id = callback_data['category_id']
    async with closing_http_client_factory() as http_client:
        products_api_client = ProductsAPIClient(http_client)
        products = await products_api_client.get_products_by_category_id(
            category_id=category_id,
        )
        subcategories = await products_api_client.get_categories(
            parent_id=category_id,
        )
    view = CategoriesListView(
        categories=subcategories,
        products=products,
    )
    await edit_message_by_view(callback_query.message, view)
    await callback_query.answer()


async def on_top_categories_list(
        message: Message,
        closing_http_client_factory: HTTPClientFactory,
) -> None:
    async with closing_http_client_factory() as http_client:
        products_api_client = ProductsAPIClient(http_client)
        categories = await products_api_client.get_categories()
    view = CategoriesListView(categories)
    await answer_views(message, view)


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_callback_query_handler(
        on_product_menu,
        ProductDetailCallbackData().filter(),
        state='*',
    )
    dispatcher.register_callback_query_handler(
        show_nested_categories_list,
        CategoryDetailCallbackData().filter(),
        state='*',
    )
    dispatcher.register_message_handler(
        on_top_categories_list,
        Text('🛒 Products'),
        state='*',
    )
