from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

__all__ = ('MenuMarkup',)


class MenuMarkup(ReplyKeyboardMarkup):

    def __init__(self):
        super().__init__(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton('🛒 Products'), KeyboardButton('🛒 My Shopping Cart')],
                [KeyboardButton('ℹ️ FAQ'), KeyboardButton('📗 Rules'), KeyboardButton('💲 Balance')],
                [KeyboardButton('📱 Profile'), KeyboardButton('👨‍💻 Support')],
            ],
        )
