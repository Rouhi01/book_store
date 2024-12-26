from django import forms


class CartForm(forms.Form):
    quantity = forms.IntegerField(min_value=1, max_value=9)


class AddCartForm(forms.Form):
    content_id = forms.IntegerField(widget=
    forms.HiddenInput(attrs={
        'class': 'white-btn mr-10'
    }))
