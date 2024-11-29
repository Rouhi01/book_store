from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


class UserCreationForm(forms.ModelForm):
    p1 = forms.CharField(widget=forms.PasswordInput, label='password')
    p2 = forms.CharField(widget=forms.PasswordInput, label='confirm password')

    class Meta:
        model = User
        fields = '__all__'

    def clean_p2(self):
        p1 = self.cleaned_data['p1']
        p2 = self.cleaned_data['p2']
        if p1 and p2 and p1 != p2:
            raise ValidationError
        return p2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['p1'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(help_text="You can change the password using <a href=\"../password/\">this form</a>.")

    class Meta:
        model = User
        fields = '__all__'