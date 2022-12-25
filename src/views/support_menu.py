from views.base import View
from keyboards import SupportMenuMarkup

__all__ = ('SupportMenuView',)


class SupportMenuView(View):
    text = '👨‍💻 Support'
    reply_markup = SupportMenuMarkup()
