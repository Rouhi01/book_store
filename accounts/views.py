from django.contrib.auth import login, authenticate, logout
from django.utils.encoding import force_str
from django.shortcuts import render, redirect
from django.utils.http import urlsafe_base64_decode
from django.views import View
from .forms import UserCreationForm, UserLoginForm, EditProfileForm
from django.contrib import messages
from utils import email_registration_code
from .tokens import account_activation_token
from .models import User
from django.contrib.auth.mixins import LoginRequiredMixin


# SignUp
class Signup(View):
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'به صفحه موردنظر دسترسی ندارید.')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context = {
            'form':form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            user.is_active = False
            user.save()

            email_registration_code(request, user, form)

            return redirect('accounts:message_send_email')
        return render(request, self.template_name, {'form':form})


class MessageSendEmailView(View):
    template_name = 'accounts/message_send_email.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'به صفحه موردنظر دسترسی ندارید.')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        return render(request, self.template_name)


class SignUpFinallyView(View):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'به صفحه موردنظر دسترسی ندارید.')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except(TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            user.save()
            messages.success(request, 'حساب کاربری شم فعال شد')
            return redirect('accounts:login')
        else:
            return render(request, 'accounts/invalid_activation_link.html')


# Login
class Login(View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            messages.error(request, 'به صفحه موردنظر دسترسی ندارید.')
            return redirect('home:home')
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        context = {
            'form': form
        }
        return render(request, self.template_name, context=context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            email = cd['email']
            password = cd['password']
            user = authenticate(username=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, 'خوش آمدید')
                return redirect('home:home')
            else:
                messages.error(request, 'نام کاربری / ایمیل یا رمز عبور اشتباه است.')
                return render(request, self.template_name, {'form': form})
        return render(request, self.template_name, {'form':form})


class LogOut(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'شما از حساب کاربری تان خازج شدید')
        return redirect('home:home')


class ProfileView(View):
    template_name = 'accounts/profile.html'
    form_class = 'ProfilePostForm'

    # def dispatch(self, request, *args, **kwargs):
    #     pass
    #
    # def setup(self, request, *args, **kwargs):
    #     pass

    def get(self, request, user_id):
        user = User.objects.get(pk=user_id)
        return render(request, self.template_name, {'user':user})

    def post(self, request, user_id):
        pass


class EditProfileView(LoginRequiredMixin, View):
    templates_name = 'accounts/edit_profile.html'
    form_class = EditProfileForm

    def setup(self, request, *args, **kwargs):
        super().setup(request, *args, **kwargs)
        self.user = User.objects.get(pk=kwargs['user_id'])

    def dispatch(self, request, *args, **kwargs):
        if request.user.id != self.user.id:
            return render(request, '404.html', {}, status=404)
        else:
            return super().dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.user.id)
        form = self.form_class(instance=request.user.profile)
        context = {'form': form, 'user':user}
        return render(request, self.templates_name, context=context)

    def post(self, request, *args, **kwargs):
        user = User.objects.get(pk=self.user)
        form = self.form_class(request.POST, request.FILES, instance=request.user.profile)
        context = {'form': form, 'user':user}
        if form.is_valid():
            form.save()
            messages.success(request, 'پروفایل بروزرسانی شد', 'success')
            return redirect('accounts:profile', user_id=self.user.id)
        return render(request, self.templates_name, context=context)




