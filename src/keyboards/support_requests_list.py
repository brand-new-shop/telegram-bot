from typing import Iterable

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import models
from keyboards.buttons import RemoveMessageButton
from callback_data import SupportRequestDetailCallbackData

__all__ = ('SupportRequestsListMarkup',)


class SupportRequestsListMarkup(InlineKeyboardMarkup):

    def __init__(self, support_requests: Iterable[models.SupportRequestPreview]):
        super().__init__(row_width=1)
        self.add(
            *(
                InlineKeyboardButton(
                    text=support_request.issue_preview,
                    callback_data=SupportRequestDetailCallbackData().new(support_request_id=support_request.id),
                )
                for support_request in support_requests
            ),
            RemoveMessageButton(),
        )
