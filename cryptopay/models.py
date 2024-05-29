from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()


class CryptoMusPayment(models.Model):
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='crypto_payments'
    )
    
    amount = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    )  # user send amount
    payment_amount_usd = models.DecimalField(
        max_digits=10, 
        decimal_places=2, 
        null=True, 
        blank=True
    ) # amount after payment
    
    currency = models.CharField(
        max_length=10, 
        default="USD", 
        null=True, 
        blank=True
    )
    payer_currency = models.CharField(
        max_length=10, 
        null=True, 
        blank=True
    )
    order_id = models.CharField(
        max_length=50, 
        unique=True
    )
    status = models.CharField(
        max_length=20, 
        null=True, 
        blank=True
    )

    from_addres = models.CharField(
        max_length=150, 
        null=True, 
        blank=True
    )

    txid = models.CharField(
        max_length=100, 
        null=True, 
        blank=True
    ) 

    created_at = models.DateTimeField(
        auto_now_add=True
    )
    
    updated_at = models.DateTimeField(
        auto_now=True
    )
    
    payment_data = models.JSONField(
        null=True, 
        blank=True
    )


    def __str__(self):
        return f"Payment : {self.order_id}"