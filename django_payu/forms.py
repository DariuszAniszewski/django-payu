from django import forms
from django.forms.widgets import HiddenInput, TextInput, NumberInput, Textarea


class PayuPaymentForm(forms.Form):
    buyer_first_name = forms.CharField(widget=TextInput(attrs={"placeholder": ""}))
    buyer_last_name = forms.CharField(widget=TextInput(attrs={"placeholder": ""}))
    buyer_email = forms.EmailField(widget=TextInput(attrs={"placeholder": ""}))
    buyer_ip_address = forms.IPAddressField(widget=HiddenInput())

    product_name = forms.CharField(widget=TextInput(attrs={"placeholder": ""}))
    product_unit_price = forms.IntegerField(widget=NumberInput(attrs={"placeholder": ""}))
    product_quantity = forms.IntegerField(widget=NumberInput(attrs={"placeholder": ""}))

    purchase_description = forms.CharField(widget=Textarea(attrs={"rows": 3, "placeholder": "Describe your payment"}))