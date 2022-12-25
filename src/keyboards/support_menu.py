from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

__all__ = ('SupportMenuMarkup',)


class SupportMenuMarkup(ReplyKeyboardMarkup):

    def __init__(self):
        super().__init__(
            resize_keyboard=True,
            keyboard=[
                [
                    KeyboardButton('📋 New Support Request'),
                    KeyboardButton('📓 My Support Requests'),
                    KeyboardButton('🆘 New Support Subject'),
                ],
                [
                    KeyboardButton('⬅️ Back'),
                ],
            ],
        )
