from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

__all__ = ('AcceptRulesMarkup',)


class AcceptRulesMarkup(ReplyKeyboardMarkup):

    def __init__(self):
        super().__init__(
            resize_keyboard=True,
            keyboard=[[KeyboardButton('✅ Accept')]],
        )
