from django import forms
from .models import Order

class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = [
            "customer_name", "customer_email", "customer_phone", "address_line",
            "landmark", "city", "state", "pincode", "payment_method",
        ]
        widgets = {
            "customer_name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "customer_email": forms.EmailInput(attrs={"placeholder": "Email address"}),
            "customer_phone": forms.TextInput(attrs={"placeholder": "10-digit phone number"}),
            "address_line": forms.TextInput(attrs={"placeholder": "House/flat, street, area"}),
            "landmark": forms.TextInput(attrs={"placeholder": "Landmark (optional)"}),
            "city": forms.TextInput(attrs={"placeholder": "City"}),
            "state": forms.TextInput(attrs={"placeholder": "State"}),
            "pincode": forms.TextInput(attrs={"placeholder": "PIN code"}),
        }
