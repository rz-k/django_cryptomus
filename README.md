# Django Cryptomus

Django Cryptomus is a package for Django that allows you to fortify web applications with robust security measures. This package is entirely dynamic, enabling you to configure all aspects of your site's security based on your specific needs.

## Features

- **Advanced Security Capabilities**: This package provides advanced features such as data encryption, access control, and detection of security threats.
- **Dynamic Configuration Settings**: All settings in this package are dynamically configurable via an admin panel.
- **Ease of Use**: Designed to be highly intuitive, making it easy for developers familiar with Django to integrate and customize security features.

## Installation

To install via pip, simply run:

```bash
pip install django-rest-cryptomus
```

Then, add it to the `INSTALLED_APPS` list in your project settings:

```python
# settings.py

INSTALLED_APPS = [
    ...
    'django_cryptomus',
    'rest_framework',
]
```

## Configuration

Add the following required settings to your Django settings file (`settings.py`):

```python
# Cryptomus API configuration
CRYPTOMUS_API_KEY = 'your_api_key'
CRYPTOMUS_MERCHANT = 'your_merchant'
CRYPTOMUS_BASE_URL = 'your_base_url'  # For local testing, see below
```

### Local Testing

If you want to test the integration locally, you need to expose your local server to the internet. You can use tools like ngrok or pinggy to achieve this.

#### Using ngrok

1. Install ngrok from [ngrok.com](https://ngrok.com/).
2. Run the following command to start ngrok and expose your local server:

    ```sh
    ngrok http 8000
    ```

3. Use the URL provided by ngrok (e.g., `https://your-subdomain.ngrok.io`) as your `CRYPTOMUS_BASE_URL`.

#### Using pinggy

1. Use the following command to start pinggy and expose your local server:

    ```sh
    ssh -p 443 -R0:localhost:8000 -L4300:localhost:4300 qr@a.pinggy.io
    ```

2. Use the URL provided by pinggy as your `CRYPTOMUS_BASE_URL`.

## Usage

Include the `django_cryptomus` URLs in your project's `urls.py`:

```python
from django.urls import path, include

urlpatterns = [
    ...
    path('payment/', include("django_cryptomus.urls", namespace="django_cryptomus")),
]
```


## Custom Form Integration
You have the flexibility to create your own custom HTML form and use it instead of the default form provided by Django Cryptomus. To integrate your custom form, follow these steps:

1. Create your custom HTML form with the desired fields and styling. You can name this file `custom_payment_form.html`.

2. In your Django project, specify the path to your custom form in the settings:

``` python 
#settings.py

CRYPTOMUS_CUSTOM_PAYMENT_FORM = 'templates_path/custom_payment_form.html'
```

## JSON Example for Payment Data
In addition to using an HTML form, you can also provide payment data in JSON format. This can be useful for API integrations or other programmatic uses. Here is an example of the required fields in JSON format:

``` json
{
    "amount": "100.00",
    "currency": "USD",
    "order_id": "123456",
    "additional_data": {
        "network": "BTC",
        "is_payment_multiple": true,
        "lifetime": 3600,
        "to_currency": "BTC",
        "subtract": 0,
        "accuracy_payment_percent": 0,
        "additional_data": "Additional information for merchant",
        "currencies": ["BTC", "ETH", "LTC"],
        "except_currencies": [],
        "course_source": "Binance",
        "from_referral_code": "your_referral_code",
        "discount_percent": 5,
        "is_refresh": false
    }
}
```
To use JSON instead of a form, simply send a POST request to the appropriate endpoint with the JSON data. This approach allows for more flexibility and can easily be integrated into various systems and applications.

## Additional Data

The `additional_data` field in JSON is used to send additional data and advanced settings in the payment transaction request. This field is optional, meaning you can include it or omit it based on your requirements.

To get detailed information about each parameter within `additional_data` and how to use them, please refer to the official Cryptomus documentation:

- [Cryptomus Documentation on Creating Invoice](https://doc.cryptomus.com/payments/creating-invoice)

You can find comprehensive details about each parameter in the `additional_data` field, enabling you to utilize them effectively for your needs.

## Customizing Cryptomus Callback View and Using CryptoMusPayment Model

If you want to customize the behavior of the callback view provided by Django Cryptomus and use the `CryptoMusPayment` model to manage payment records, follow these steps:

1. Subclass the `CryptomusCallbackView` class and import the `CryptoMusPayment` model into your Django project:

```python
# views.py

from rest_framework import status
from rest_framework.response import Response
from django_cryptomus.views import CryptomusCallbackView
from django_cryptomus.models import CryptoMusPayment

class CustomCryptomusCallbackView(CryptomusCallbackView):
    def post(self, request, *args, **kwargs):
        data = request.data
        if data['status'] == 'paid':
            cryptomus_payment = CryptoMusPayment.objects.filter(order_id=data['order_id'])
            
            cryptomus_payment.update(
                payment_amount_usd=data['payment_amount_usd'],
                payer_currency=data['payer_currency'],
                from_address=data['from'],
                status=data['status'],
                txid=data['txid'],
                payment_data=data
            )
            
            return Response({'message': 'Payment status updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response({'error': 'Invalid payment status.'}, status=status.HTTP_400_BAD_REQUEST)
```

Specify the path to your custom callback view class in the settings:
```
# settings.py

CRYPTOMUS_CALLBACK_VIEW_CLASS = 'yourapp.views.CustomCryptomusCallbackView'
```

## Customizing Success View

To customize the success page of Cryptomus payment, you can create a custom view class and specify its path using the `CRYPTOMUS_SUCCESS_VIEW_CLASS` variable in your Django project settings.

### Example Custom Success View

```python
# views.py

from django_cryptomus.views import SuccessCryptomusView
from django.http import HttpResponse
from django.shortcuts import render

class CustomSuccessCryptomusView(SuccessCryptomusView):

    def get(self, request):
        """
        Handle GET requests to render the success page.

        Renders a success page template specified in
```


Setting Custom Success View
To set the custom success view, you need to specify the path to your custom view class in the settings.py file of your Django project:

```
# settings.py

CRYPTOMUS_SUCCESS_VIEW_CLASS = 'yourapp.views.CustomCryptomusSuccessView'
```

## Customizing Success Template

To customize the success page template for Cryptomus payment, you can create a custom HTML template and specify its path using the `CRYPTOMUS_PAYMENT_SUCCESS_HTML` variable in your Django project settings.

### Example Custom Success Template

```html
<!-- success_page.html -->

<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Payment Success</title>
    <!-- Add your custom CSS stylesheets or scripts here -->
</head>
<body>
    <div class="container">
        <h1>Payment Successful!</h1>
        <p>Thank you for your payment.</p>
        <!-- Add additional content or dynamic data here -->
    </div>
</body>
</html>
```
Setting Custom Success Template
To set the custom success template, you need to specify the path to your custom HTML template in the settings.py file of your Django proje

```
# settings.py

CRYPTOMUS_PAYMENT_SUCCESS_HTML = 'cryptopay/success_page.html'
```


Then, you can utilize the dynamic configuration settings provided by this package to tailor all aspects of your site's security.
## Contributing

We welcome contributions and feedback from the community. To report issues, make suggestions, or submit pull requests, please visit our [GitHub repository](https://github.com/rz-k/django_cryptomus).

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.