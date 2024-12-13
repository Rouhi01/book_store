from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User


class UserCreationForm(forms.ModelForm):
    p1 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور'}),
        label='رمز عبور'
    )
    p2 = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور خود را مجدد وارد کنید'}),
        label='تأییدیه رمز عبور'
    )

    class Meta:
        model = User
        fields = ['email']
        widgets = {
            'email': forms.EmailInput(attrs={'placeholder':'ایمیل'})
        }
        labels = {
            'email': 'ایمیل'
        }

    def clean_p2(self):
        ps1 = self.cleaned_data['p1']
        ps2 = self.cleaned_data['p2']
        if ps1 and ps2 and ps1 != ps2:
            raise ValidationError('رمز عبورها مطابقت ندارند.')
        return ps2

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('کاربری با این ایمیل وجود دارد.')
        return email

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


class UserLoginForm(forms.Form):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'placeholder':'رمز عبور خود را وارد کنید'}),
        label='رمزعبور'
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder':'ایمیل / نام کاربری'}),
        label='نام کاربری یا ایمیل'
    )