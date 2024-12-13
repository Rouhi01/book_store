from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserCreationForm, UserLoginForm
from .models import User
from django.contrib import messages


class Signup(View):
    template_name = 'accounts/signup.html'
    form_class = UserCreationForm

    def get(self, request):
        form = self.form_class()
        context = {
            'form':form
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            form.save()
            return redirect('accounts:login')
        return render(request, self.template_name, {'form':form})


class Login(View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

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

