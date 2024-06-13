from django.shortcuts import render, redirect
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .forms import CryptoPaymentForm
from django.conf import settings
from .models import CryptoMusPayment
from uuid import uuid4
from cryptomus import Client
from rest_framework.permissions import IsAuthenticated


class Metadata:
    """
    Class for handling Cryptomus related metadata.
    """

    @property
    def api_key(self):
        return getattr(settings, "CRYPTOMUS_API_KEY")

    @property
    def merchant(self):
        return getattr(settings, "CRYPTOMUS_MERCHANT") 

    @property
    def url_callback(self):
        return getattr(settings, "CRYPTOMUS_BASE_URL") + getattr(settings, "CRYPTOMUS_CALLBACK_URL", "/payment/cryptomus/callback/")

    @property
    def url_success(self):
        return getattr(settings, "CRYPTOMUS_BASE_URL") + getattr(settings, "CRYPTOMUS_SUCCESS_URL", "/payment/cryptomus/success/")

class CreateTransactionView(APIView, Metadata):
    """
    API view for creating a transaction with Cryptomus payment gateway.

    This view handles POST requests to create a new payment transaction and GET requests to render a payment form.

    Attributes:
        permission_classes (tuple): Specifies the permissions that are required to access this view.
    
    Methods:
        post(request, *args, **kwargs): Handles POST requests to create a new payment transaction.
        send_to_cryptomus(payload): Sends the payment data to the Cryptomus payment gateway.
        get(request, *args, **kwargs): Handles GET requests to render the payment form.
    """

    permission_classes = (IsAuthenticated,)
    
    def post(self, request):
        """
        Handle POST requests to create a new payment transaction.

        Depending on the content type of the request, it processes the data using a form and sends it to the Cryptomus payment gateway.

        Args:
            request (HttpRequest): The request object containing the POST data

        Returns:
            Response: A DRF Response object containing the response from the Cryptomus payment gateway.
            HttpResponseRedirect: A redirect response to the Cryptomus payment URL if the request is not JSON.
        """

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
                "url_callback": self.url_callback.format(cryptomus_payment.pk),
                "url_success": self.url_success.format(cryptomus_payment.pk)
            }
            # Merge additional data if provided
            if 'additional_data' in form.cleaned_data and form.cleaned_data['additional_data']:
                payment_data.update(form.cleaned_data['additional_data'])
            
            response = self.send_to_cryptomus(payment_data)
            
            if request.content_type == 'application/json':
                return Response(response, status=status.HTTP_200_OK)
            return redirect(to=response['url'])
        return Response({"errors": form.errors}, status=status.HTTP_400_BAD_REQUEST)

    def send_to_cryptomus(self, payload):
        """
        Send the payment data to the Cryptomus payment gateway.

        Args:
            payload (dict): The payment data to be sent to the payment gateway.

        Returns:
            dict: The response from the payment gateway.
        """
        payment = Client.payment(payment_key=self.api_key, merchant_uuid=self.merchant)
        return payment.create(payload)

    def get(self, request):
        """
        Handle GET requests to render the payment form.
        Renders a payment form template to collect payment details from the user.

        Returns:
            HttpResponse: A response object containing the rendered form template.
        """
        form = CryptoPaymentForm()
        return render(request, getattr(settings, 'CRYPTOMUS_PAYMENT_HTML_FORM', 'django_cryptomus/payment_form.html'), {'form': form})

class SuccessCryptomusView(APIView):
    """
    API view for handling the success page of Cryptomus payment.

    This view renders a success page after a successful payment. 
    Users can override this view by specifying their own success view in the Django settings.

    Methods:
        get(request): Handles GET requests to render the success page.
    """

    def get(self, request):
        """
        Handle GET requests to render the success page.

        Renders a success page template specified in the settings. If not specified, the default template is used.

        Args:
            request (HttpRequest): The request object.

        Returns:
            HttpResponse: A response object containing the rendered success page template.
        """
        return render(request, getattr(settings, 'CRYPTOMUS_PAYMENT_SUCCESS_HTML', 'django_cryptomus/success_page.html'))
        
class CallbackCryptomusView(APIView):
    """
    API view for handling callback requests from Cryptomus.

    This view processes callback requests sent by Cryptomus to update the payment status 
    and details in the database.

    Note:
        Users can override this view by specifying a custom callback view in their settings.
        If no custom view is specified, this default view will be used.

    Methods:
        post(request): Handles POST requests to process the callback data from Cryptomus.
    """

    def post(self, request):
        """
        Handle POST requests to process the callback data from Cryptomus.

        Processes the callback data sent by Cryptomus and updates the payment details 
        in the database if the payment status is 'paid'.

        Args:
            request (HttpRequest): The request object containing callback data.

        Returns:
            Response: A response object containing the callback data and HTTP status 200.
        """

        data = request.data
        if data['status'] == 'paid':
            cryptomus_payment = CryptoMusPayment.objects.filter(order_id=data['order_id'])
            
            cryptomus_payment.update(
                payment_amount_usd=data['payment_amount_usd'],
                payer_currency=data['payer_currency'],
                from_addres=data['from'],
                status=data['status'],
                txid=data['txid'],
                payment_data=data
            )
        return Response(data, status=status.HTTP_200_OK)
