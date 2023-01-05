from keyboards import PaymentMethodsMarkup
from views.base import View

__all__ = ('PaymentMethodsView',)


class PaymentMethodsView(View):
    text = '💲 Choose payment method'
    reply_markup = PaymentMethodsMarkup()
