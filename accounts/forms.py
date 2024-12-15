from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from .models import User, Profile


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


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['first_name', 'last_name', 'phone_number', 'gender', 'date_of_birth', 'bio', 'profile_picture']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control valid', 'type': 'text', 'placeholder': 'نام'}),
            'last_name': forms.TextInput(
                attrs={'class': 'form-control valid', 'type': 'text', 'placeholder': 'نام خانوادگی'}
            ),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'type': 'text', 'placeholder': 'شماره تلفن'}),
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 5, 'placeholder': 'درباره خودت بنویس'}),
            'date_of_birth': forms.DateInput(
                attrs={'class': 'form-control valid', 'type': 'date', 'placeholder': 'تاریخ تولد'}
            ),
            'gender': forms.Select(attrs={'class': 'form-control'}),
            'profile_picture': forms.ClearableFileInput(
                attrs={'class': 'form-control-file avatar img-thumbnail border border-success shadow'}),
        }

    def clean_phone_number(self):
        phone_number = self.cleaned_data['phone_number']
        current_profile = self.instance

        if Profile.objects.filter(phone_number=phone_number).exclude(id=current_profile.id).exists():
            raise ValidationError('کاربری با این شماره تلفن وجود دارد.')
        return phone_number