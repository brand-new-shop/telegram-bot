from aiogram import Dispatcher
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ContentType

import exceptions
from services.api import SupportAPIClient
from shortcuts import answer_views
from views import SupportMenuView
from states import NewSupportSubjectStates

__all__ = ('register_handlers',)


async def on_new_support_subject_name_input(message: Message, support_api_client: SupportAPIClient, state: FSMContext):
    if len(message.text) > 64:
        await message.reply('Too long name')
        return
    try:
        await support_api_client.create_subject(message.text)
    except exceptions.ServerAPIError:
        await message.reply('❌ Could not create new support subject')
        return
    await state.finish()
    await message.answer('✅ Ready')


async def on_new_support_subject(message: Message) -> None:
    await NewSupportSubjectStates.name.set()
    await message.answer('🛟 Input support subject')


async def on_support_menu(message: Message) -> None:
    await answer_views(message, SupportMenuView())


def register_handlers(dispatcher: Dispatcher) -> None:
    dispatcher.register_message_handler(
        on_new_support_subject_name_input,
        content_types=ContentType.TEXT,
        state=NewSupportSubjectStates.name,
    )
    dispatcher.register_message_handler(on_new_support_subject, Text('🆘 New Support Subject'), state='*')
    dispatcher.register_message_handler(on_support_menu, Text('👨‍💻 Support'), state='*')
