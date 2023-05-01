from aiogram.utils.callback_data import CallbackData

import models

__all__ = (
    'SupportTicketDetailCallbackData',
    'CreateReplyToTicketCallbackData',
    'CloseSupportTicketCallbackData',
    'ReplyToTicketDetailCallbackData',
)


class SupportTicketDetailCallbackData(CallbackData):

    def __init__(self):
        super().__init__('support-ticket-detail', 'ticket_id')

    def parse(self,
              callback_data: str) -> models.SupportTicketDetailCallbackData:
        callback_data = super().parse(callback_data)
        return {'ticket_id': int(callback_data['ticket_id'])}


class ReplyToTicketDetailCallbackData(CallbackData):

    def __init__(self):
        super().__init__('reply-to-ticket-detail', 'ticket_reply_id')

    def parse(self,
              callback_data: str) -> models.ReplyToTicketDetailCallbackData:
        callback_data = super().parse(callback_data)
        return {'ticket_reply_id': int(callback_data['ticket_reply_id'])}


class CreateReplyToTicketCallbackData(CallbackData):

    def __init__(self):
        super().__init__('create-reply-to-ticket', 'ticket_id')

    def parse(self,
              callback_data: str) -> models.ReplyToTicketCreateCallbackData:
        callback_data = super().parse(callback_data)
        return {'ticket_id': int(callback_data['ticket_id'])}


class CloseSupportTicketCallbackData(CallbackData):

    def __init__(self):
        super().__init__('close-ticket', 'ticket_id')

    def parse(self,
              callback_data: str) -> models.CloseSupportTicketCallbackData:
        callback_data = super().parse(callback_data)
        return {'ticket_id': int(callback_data['ticket_id'])}
