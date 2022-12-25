from views.base import View

__all__ = ('SupportRequestCreatedView',)


class SupportRequestCreatedView(View):

    def __init__(self, support_request_id: int):
        self.__support_request_id = support_request_id

    def get_text(self) -> str:
        return (
            '✔️ Your support request has been sent\n\n'
            f'🆔 Request number: #{self.__support_request_id}'
        )
