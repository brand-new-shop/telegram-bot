from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ForceReply, ReplyKeyboardRemove

__all__ = ('View',)


class View:
    text: str | None = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ForceReply | ReplyKeyboardRemove | None = None

    def get_text(self) -> str | None:
        return self.text

    def get_reply_markup(self) -> InlineKeyboardMarkup | ReplyKeyboardMarkup | ForceReply | ReplyKeyboardRemove | None:
        return self.reply_markup
