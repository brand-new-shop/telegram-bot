from aiogram.types import InlineKeyboardButton

__all__ = ('RemoveMessageButton',)


class RemoveMessageButton(InlineKeyboardButton):

    def __init__(self):
        super().__init__(text='🚫 Close', callback_data='remove-message')
