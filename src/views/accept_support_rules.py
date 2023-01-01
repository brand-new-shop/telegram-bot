from aiogram.types import ReplyKeyboardMarkup

import models
from views.base import View
from keyboards import AcceptSupportRulesMarkup

__all__ = ('AcceptSupportRulesView',)


class AcceptSupportRulesView(View):

    def __init__(self, support_rules: models.ShopInfo):
        self.__support_rules = support_rules

    def get_text(self) -> str:
        return self.__support_rules.value

    def get_reply_markup(self) -> ReplyKeyboardMarkup:
        return AcceptSupportRulesMarkup()
