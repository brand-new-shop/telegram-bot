from aiogram.utils.callback_data import CallbackData

from cart import models

__all__ = ('ChangeProductQuantityInCartCallbackData',)


class ChangeProductQuantityInCartCallbackData(CallbackData):

    def __init__(self):
        super().__init__(
            'change-product-quantity',
            'cart_product_id',
            'product_id',
            'quantity',
        )

    def parse(
            self, callback_data: str,
    ) -> models.ChangeProductQuantityInCartTypedDict:
        callback_data = super().parse(callback_data)
        return {
            'quantity': int(callback_data['quantity']),
            'product_id': int(callback_data['product_id']),
            'cart_product_id': int(callback_data['cart_product_id']),
        }
