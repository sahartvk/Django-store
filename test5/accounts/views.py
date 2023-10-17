from django.shortcuts import render, redirect
from django.views import View
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import User
from django.utils.crypto import get_random_string
from django.urls import reverse
from django.http import Http404, HttpRequest
from django.contrib.auth import login, logout
from utils.email_service import send_email
# Create your views here.


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'accounts/register.html', context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get('email')
            user_pass = register_form.cleaned_data.get('password')
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error('email', 'ایمیل وارد شده تکراری میباشد')
            else:
                new_user = User(
                    email=user_email,
                    username=user_email,
                    is_active=False,
                    email_active_code=get_random_string(63)
                )
                new_user.set_password(user_pass)
                new_user.save()
                send_email('فعالسازی حساب کاربری',new_user.email, {'user': new_user}, 'emails/activate_account.html')
                return redirect(reverse('home_page'))

        context = {
            'register_form': register_form
        }

        return render(request, 'accounts/register.html', context)


class ActivateView(View):
    def get(self, request, email_active_code):
        user = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            user.is_active = True
            user.email_active_code = get_random_string(63)
            user.save()
            # todo: show success message
            return redirect(reverse('login_page'))
        else:
            # todo: show account was activated
            pass

        raise Http404


class LoginView(View):

    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'accounts/login.html', context)

    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get('email')
            user_pass = login_form.cleaned_data.get('password')
            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                if not user.is_active:
                    login_form.add_error('email', 'اکانت فعال نشده است')
                else:
                    if user.check_password(user_pass):
                        login(request, user)
                        return redirect(reverse('home_page'))
                    else:
                        login_form.add_error('email', 'نام کاربری یا کلمه عبور اشتباه است')
            else:
                login_form.add_error('email', 'نام کاربری یا کلمه عبور اشتباه است')

        context = {
            'login_form': login_form
        }
        return render(request, 'accounts/login.html', context)


class ForgotPasswordFormView(View):
    def get(self, request):
        forget_pass_form = ForgotPasswordForm()
        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'accounts/forgot_password.html', context)

    def post(self, request):
        forget_pass_form = ForgotPasswordForm(request.POST)

        if forget_pass_form.is_valid():
            user_email = forget_pass_form.cleaned_data.get('email')

            user = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email('بازیابی کلمه عبور', user.email, {'user': user}, 'emails/forgot_password.html')

            else:
                forget_pass_form.add_error('email', 'ایمیل وارد شده صحیح نمیباشد')

        context = {
            'forget_pass_form': forget_pass_form
        }
        return render(request, 'accounts/forgot_password.html', context)


class ResetPasswordView(View):
    def get(self, request, email_active_code):
        print('hi')
        reset_pass_form = ResetPasswordForm()
        user = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is None:
            return redirect(reverse('login_page'))
        context = {
            'reset_pass_form': reset_pass_form
        }
        return render(request, 'accounts/reset_password.html', context)

    def post(self, request, email_active_code):
        reset_pass_form = ResetPasswordForm(request.POST)

        if reset_pass_form.is_valid():
            user_pass = reset_pass_form.cleaned_data.get('password')
            user = User.objects.filter(email_active_code__iexact=email_active_code).first()
            if user is None:
                return redirect(reverse('login_page'))
            else:
                user.set_password(user_pass)
                user.email_active_code = get_random_string(63)
                user.is_active = True
                user.save()
                return redirect(reverse('login_page'))

        context = {
            'reset_pass_form': reset_pass_form,

        }
        return render(request, 'accounts/reset_password.html', context)


class LogoutView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login_page'))

