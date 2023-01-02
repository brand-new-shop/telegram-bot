from views.base import View
from keyboards import BackToMenuMarkup

__all__ = ('SupportTicketCreatedView',)


class SupportTicketCreatedView(View):
    reply_markup = BackToMenuMarkup()

    def __init__(self, ticket_id: int):
        self.__ticket_id = ticket_id

    def get_text(self) -> str:
        return (
            'Your Support Enquiry has been sent.'
            ' We will respond within the next few hours.'
            ' Please expect delays on holidays and weekends.'
            f'\nRequest number: #{self.__ticket_id}'
        )
