from django import forms


class CryptoPaymentForm(forms.Form):
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    currency = forms.ChoiceField(choices=[('USD', 'USD'), ('EUR', 'EUR')])
    order_id = forms.CharField(max_length=100, required=False)
    # Define an optional JSON field to accept additional data
    additional_data = forms.JSONField(required=False)

    def clean(self):
        
        cleaned_data = super().clean()
        additional_data = cleaned_data.get("additional_data", {})
        if additional_data:
            for field in ["url_success", "url_callback"]:
                if field in additional_data:
                    additional_data.pop(field)
            cleaned_data["additional_data"] = additional_data     

        return cleaned_data