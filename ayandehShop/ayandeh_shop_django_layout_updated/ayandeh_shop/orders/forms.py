from django import forms
from .models import Order

class OrderCreateForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["full_name", "phone", "address", "postal_code"]
        widgets = {
            "full_name": forms.TextInput(attrs={"class": "form-control"}),
            "phone": forms.TextInput(attrs={"class": "form-control", "dir": "ltr"}),
            "address": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
            "postal_code": forms.TextInput(attrs={"class": "form-control", "dir": "ltr"}),
        }
