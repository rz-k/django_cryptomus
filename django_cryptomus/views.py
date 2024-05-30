from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import CryptoPaymentForm
from django.conf import settings
from .models import CryptoMusPayment
from uuid import uuid4
from cryptomus import Client



class Metadata:
    api_key = getattr(settings, "CRYPTOMUS_API_KEY")
    merchant = getattr(settings, "CRYPTOMUS_MERCHANT") 
    callback_url = getattr(settings, "CRYPTOMUS_BASE_URL") + getattr(settings, "CRYPTOMUS_CALLBACK_URL", "/payment/cryptopay/cryptomus/callback/")
    url_success = getattr(settings, "CRYPTOMUS_BASE_URL") + getattr(settings, "CRYPTOMUS_SUCCESS_URL", "/payment/cryptopay/cryptomus/success/")

class CreateTransactionView(APIView, Metadata):

    def post(self, request, *args, **kwargs):

        if request.content_type == 'application/json':
            data = request.data
            form = CryptoPaymentForm(data)
        else:
            form = CryptoPaymentForm(request.POST)
        
        if form.is_valid():
            order_id = uuid4().__str__() if not form.cleaned_data.get('order_id') else form.cleaned_data.get('order_id')

            cryptomus_payment = CryptoMusPayment.objects.create(
                user=request.user,
                amount=form.cleaned_data['amount'],
                currency=form.cleaned_data['currency'],
                order_id=order_id
            )

            payment_data = {
                "amount": str(form.cleaned_data['amount']),
                "currency": form.cleaned_data['currency'],
                "order_id": str(order_id),
                "url_callback": self.callback_url.format(cryptomus_payment.pk),
                "url_success": self.url_success.format(cryptomus_payment.pk)
            }
            # Merge additional data if provided
            if 'additional_data' in form.cleaned_data and form.cleaned_data['additional_data']:
                payment_data.update(form.cleaned_data['additional_data'])
            
            # payment_data['cryptomus_payment_db_id']=cryptomus_payment.pk
            print(payment_data)
            response = self.send_to_cryptomus(payment_data)
            return redirect(to=response['url'])
            return Response(response, status=status.HTTP_200_OK)

        return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

    def send_to_cryptomus(self, payload):
        payment = Client.payment(payment_key=self.api_key, merchant_uuid=self.merchant)
        return payment.create(payload)

    def get(self, request, *args, **kwargs):
        form = CryptoPaymentForm()
        return render(request, getattr(settings, 'CRYPTOMUS_PAYMENT_HTML_FORM', 'cryptopay/payment_form.html'), {'form': form})

class SuccessCryptomusView(APIView):

    def get(self, request):
        return render(request, getattr(settings, 'CRYPTOMUS_PAYMENT_SUCCESS_HTML', 'cryptopay/success_page.html'), {'form': form})
        
class CallbackCryptomusView(APIView):

    def post(self, request):
        data = request.data
        if data['status'] == 'paid':
            cryptopay = CryptoMusPayment.objects.filter(order_id=data['order_id'])
            cryptopay.update(
                payment_amount_usd=data['payment_amount_usd'],
                payer_currency=data['payer_currency'],
                from_addres=data['from'],
                status=data['status'],
                txid=data['txid'],
                payment_data=data
            )
        return Response(data, status=status.HTTP_200_OK)
