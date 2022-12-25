from views.base import View
from keyboards import MenuMarkup

__all__ = ('MenuView',)


class MenuView(View):
    text = '🔹 Main Menu 🔹'
    reply_markup = MenuMarkup()
