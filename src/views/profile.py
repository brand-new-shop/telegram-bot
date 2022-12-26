from models import UserProfileDTO
from views.base import View

__all__ = ('ProfileView',)


class ProfileView(View):

    def __init__(self, user_profile_dto: UserProfileDTO):
        self.__user_profile_dto = user_profile_dto

    def get_text(self) -> str:
        username = (f'@{self.__user_profile_dto.username}' if self.__user_profile_dto.username is not None
                    else self.__user_profile_dto.telegram_id)
        lines = [
            f'🙍‍♂ User: {username}',
            '➖➖➖➖➖➖➖➖➖➖',
            f'🛒 Number of purchases: {self.__user_profile_dto.purchases_total_count} pc(s).',
            f'💰 Total Amount: {self.__user_profile_dto.purchases_total_price} $.',
        ]
        if self.__user_profile_dto.last_purchases:
            lines.append('➖➖➖➖➖➖➖➖➖➖')
            lines.append(f'📱 Last {len(self.__user_profile_dto.last_purchases)} purchases:')
            for purchase in self.__user_profile_dto.last_purchases:
                lines.append(f'▫️ {purchase.product_name} | {purchase.quantity} pc(s) | ${purchase.total_price}')
        return '\n'.join(lines)
