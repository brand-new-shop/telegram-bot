from aiogram.types import InlineKeyboardMarkup, ReplyKeyboardMarkup, ForceReply, ReplyKeyboardRemove, MediaGroup

__all__ = ('View',)


class View:
    text: str | None = None
    reply_markup: InlineKeyboardMarkup | ReplyKeyboardMarkup | ForceReply | ReplyKeyboardRemove | None = None
    media_group: MediaGroup | None = None

    def get_text(self) -> str | None:
        return self.text

    def get_reply_markup(self) -> InlineKeyboardMarkup | ReplyKeyboardMarkup | ForceReply | ReplyKeyboardRemove | None:
        return self.reply_markup

    def get_media_group(self) -> MediaGroup:
        return self.media_group
