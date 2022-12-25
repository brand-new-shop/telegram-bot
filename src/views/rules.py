from views.base import View
from keyboards import AcceptRulesMarkup

__all__ = ('RulesView',)


class RulesView(View):
    text = 'Rules'
    reply_markup = AcceptRulesMarkup()
