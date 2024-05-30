# Generated by Django 4.0.7 on 2024-05-30 15:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='CryptoMusPayment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('payment_amount_usd', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True)),
                ('currency', models.CharField(blank=True, default='USD', max_length=10, null=True)),
                ('payer_currency', models.CharField(blank=True, max_length=10, null=True)),
                ('order_id', models.CharField(max_length=50, unique=True)),
                ('status', models.CharField(blank=True, max_length=20, null=True)),
                ('from_addres', models.CharField(blank=True, max_length=150, null=True)),
                ('txid', models.CharField(blank=True, max_length=100, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('payment_data', models.JSONField(blank=True, null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='crypto_payments', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
