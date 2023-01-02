from keyboards import MenuMarkup
from views.base import View

__all__ = ('SupportTicketRateLimitExceededView',)


class SupportTicketRateLimitExceededView(View):
    reply_markup = MenuMarkup()

    def __init__(self, seconds_to_wait: int):
        self.__seconds_to_wait = seconds_to_wait

    def get_text(self) -> str:
        return f'You have to wait for {self.__seconds_to_wait} seconds in order to open another ticket.'
