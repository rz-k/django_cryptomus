from django.urls import path
from django.conf import settings
from .views import *
from django.utils.module_loading import import_string



success_view_class = import_string(getattr(settings, "CRYPTOMUS_SUCCESS_VIEW_CLASS", "cryptopay.views.SuccessCryptomusView"))
callback_view_class = import_string(getattr(settings, "CRYPTOMUS_CALLBACK_VIEW_CLASS", "cryptopay.views.CallbackCryptomusView"))

app_name= "cryptopay"
urlpatterns = [
    path(getattr(settings, "CRYPTOMUS_CREATE_TRANSACTION_URL", "cryptopay/cryptomus/create-transaction/") , CreateTransactionView.as_view(), name="create-transaction"),
    path(getattr(settings, "CRYPTOMUS_SUCCESS_URL", "cryptopay/cryptomus/success/") , success_view_class.as_view(), name="succsess-payment"),
    path(getattr(settings, "CRYPTOMUS_CALLBACK_URL", "cryptopay/cryptomus/callback/") , callback_view_class.as_view(), name="callback-payment"),
]
