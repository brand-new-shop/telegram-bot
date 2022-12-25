import models
from keyboards import RemoveMessageMarkup
from views.base import View

__all__ = ('SupportRequestDetailView',)


class SupportRequestDetailView(View):
    reply_markup = RemoveMessageMarkup()

    def __init__(self, support_request: models.SupportRequest):
        self.__support_request = support_request

    def get_text(self) -> str:
        lines = [
            f'🆔 Request number: #{self.__support_request.id}',
            '➖➖➖➖➖➖➖➖➖➖',
            f'📗 Request Subject: {self.__support_request.subject.name}',
            f'📋 Description: {self.__support_request.issue}',
            '➖➖➖➖➖➖➖➖➖➖',
        ]
        if self.__support_request.answer:
            lines.append(f'📧 Answer: {self.__support_request.answer}')
            lines.append('➖➖➖➖➖➖➖➖➖➖')
        if self.__support_request.is_open:
            lines.append(f'📱 Status: ✅ Active')
        else:
            lines.append('📱 Status: ❌ Closed')
        return '\n'.join(lines)
