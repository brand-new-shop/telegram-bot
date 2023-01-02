from aiogram.types import ReplyKeyboardRemove

from views.base import View

__all__ = ('RequireTicketSubjectView',)


class RequireTicketSubjectView(View):
    text = 'Enter The Subject of your inquiry (Please make it short and without any symbols):'
    reply_markup = ReplyKeyboardRemove()
