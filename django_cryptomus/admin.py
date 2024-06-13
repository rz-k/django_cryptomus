from django.contrib import admin
from .models import CryptoMusPayment

@admin.register(CryptoMusPayment)
class CryptoMusPaymentAdmin(admin.ModelAdmin):
    def get_queryset(self, request):
        queryset = super().get_queryset(request).prefetch_related("user")
        return queryset
        
    list_display = ("id", "user", "order_id", "status")
    list_display_links = ("id",)
    empty_value_display = 'UNSET'
    search_fields = ("order_id", "user__id")

