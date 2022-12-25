from views.base import View
from keyboards import AcceptRulesMarkup

__all__ = ('AcceptRulesView',)


class AcceptRulesView(View):
    text = 'Rules'
    reply_markup = AcceptRulesMarkup()
