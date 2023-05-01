import models
from core.views import View

__all__ = ('ShopInfoView',)


class ShopInfoView(View):

    def __init__(self, shop_info: models.ShopInfo):
        self.__shop_info = shop_info

    def get_text(self) -> str:
        return self.__shop_info.value
