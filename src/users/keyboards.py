from aiogram.types import (
    ReplyKeyboardMarkup,
    KeyboardButton,
    InlineKeyboardButton,
)

__all__ = ('MenuMarkup', 'RemoveMessageButton',)


class MenuMarkup(ReplyKeyboardMarkup):

    def __init__(self):
        super().__init__(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton('🛒 Products'),
                    KeyboardButton('🛒 My Shopping Cart'),
                ],
                [
                    KeyboardButton('ℹ️ FAQ'),
                    KeyboardButton('📗 Rules'),
                    KeyboardButton('💲 Balance'),
                ],
                [
                    KeyboardButton('📱 Profile'),
                    KeyboardButton('👨‍💻 Support'),
                ],
            ],
        )


class RemoveMessageButton(InlineKeyboardButton):

    def __init__(self):
        super().__init__(text='🚫 Close', callback_data='remove-message')
