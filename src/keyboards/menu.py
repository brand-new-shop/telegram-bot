from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

__all__ = ('MenuMarkup',)


class MenuMarkup(ReplyKeyboardMarkup):

    def __init__(self):
        super().__init__(
            resize_keyboard=True,
            keyboard=[
                [KeyboardButton('đ Products'), KeyboardButton('đ My Shopping Cart')],
                [KeyboardButton('âšī¸ FAQ'), KeyboardButton('đ Rules'), KeyboardButton('đ˛ Balance')],
                [KeyboardButton('đą Profile'), KeyboardButton('đ¨âđģ Support')],
            ],
        )
