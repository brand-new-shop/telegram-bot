from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

__all__ = ('AcceptSupportRulesMarkup',)


class AcceptSupportRulesMarkup(ReplyKeyboardMarkup):

    def __init__(self):
        super().__init__(
            resize_keyboard=True,
            keyboard=[[KeyboardButton('✅ I did')]],
        )
