from django.shortcuts import render, redirect

# Create your views here.
from django.urls import reverse
from django.utils.crypto import get_random_string
from django.views import View
from .forms import RegisterForm, LoginForm, ForgotPasswordForm, ResetPasswordForm
from .models import User
from django.http import HttpRequest, Http404
from django.contrib.auth import login, logout
from utils.email_service import send_email


class RegisterView(View):
    def get(self, request):
        register_form = RegisterForm()
        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context=context)

    def post(self, request):
        register_form = RegisterForm(request.POST)
        if register_form.is_valid():
            user_email = register_form.cleaned_data.get("email")
            user_password = register_form.cleaned_data.get("password")
            user: bool = User.objects.filter(email__iexact=user_email).exists()
            if user:
                register_form.add_error("email", "ایمیل وارد شده تکراری می باشد.")
            else:
                new_user = User(
                    email=user_email,
                    email_active_code=get_random_string(72),
                    is_active=False,
                    username=user_email
                )
                new_user.set_password(user_password)
                new_user.save()
                # todo: send email active code
                send_email(
                    subject='فعالسازی حساب کاربری',
                    to=new_user.email,
                    context={'user': new_user},
                    template_name='emails/activate_account.html',
                    # template_name='emails/beefree.html',
                )
                return redirect(reverse('login_page'))


        context = {
            'register_form': register_form
        }
        return render(request, 'account_module/register.html', context=context)


class LoginView(View):
    def get(self, request):
        login_form = LoginForm()
        context = {
            'login_form': login_form
        }
        return render(request, 'account_module/login.html', context=context)

    def post(self, request: HttpRequest):
        login_form = LoginForm(data=request.POST)
        if login_form.is_valid():
            user_email = login_form.cleaned_data.get("email")
            user_pass = login_form.cleaned_data.get("password")
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is None:
                login_form.add_error('email', 'کاربری با مشخصات وارد شده یافت نشد')
                return redirect(reverse('login_page'))
            else:
                if not user.is_active:
                    login_form.add_error('email', 'جساب کاربری شما فعال نشده است')
                else:
                    is_password_correct = user.check_password(user_pass)
                    if is_password_correct:
                        login(request, user)
                        return redirect(reverse('home_page'))

        context = {
            'login_form': login_form
        }

        return render(request, 'account_module/login.html', context=context)


class ActivateAccountView(View):
    def get(self, request, email_active_code):
        user: User = User.objects.filter(email_active_code__iexact=email_active_code).first()
        if user is not None:
            if not user.is_active:
                user.is_active = True
                user.email_active_code = get_random_string(72)
                user.save()
                # todo: show success message to user
                return redirect(reverse('login_page'))
            else:
                # todo: show your account was activated message to user
                pass
        raise Http404


class ForgetPasswordView(View):
    def get(self, request: HttpRequest):
        forget_password_form = ForgotPasswordForm()
        context = {
            'forget_password_form': forget_password_form
        }
        return render(request, 'account_module/forgot_password.html', context=context)

    def post(self, request: HttpRequest):
        forget_password_form = ForgotPasswordForm(data=request.POST)
        if forget_password_form.is_valid():
            user_email = forget_password_form.cleaned_data.get("email")
            user: User = User.objects.filter(email__iexact=user_email).first()
            if user is not None:
                send_email(
                    subject='فعالسازی حساب کاربری',
                    to=user.email,
                    context={'user': user},
                    template_name='emails/forgot_password.html'
                )
                return redirect(reverse('home_page'))

        context = {
            'forget_password_form': forget_password_form,
        }
        return render(request, 'account_module/forgot_password.html', context=context)


class ResetPasswordView(View):
    def get(self, request: HttpRequest, active_code):
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if user is None:
            return redirect(reverse('login_page'))

        reset_password_form = ResetPasswordForm()
        context = {
            'user': user,
            'reset_password_form': reset_password_form
        }
        return render(request, 'account_module/reset_password.html', context=context)

    def post(self, request: HttpRequest, active_code):
        reset_password_form = ResetPasswordForm(data=request.POST)
        user: User = User.objects.filter(email_active_code__iexact=active_code).first()
        if reset_password_form.is_valid():
            if user is None:
                return redirect(reverse('login_page'))
            user_new_pass = reset_password_form.cleaned_data.get('password')
            user.set_password(user_new_pass)
            user.email_active_code = get_random_string(72)
            user.is_active = True
            user.save()
            return redirect(reverse('login_page'))

        context = {
            'user': user,
            'reset_password_form': reset_password_form,
        }
        return render(request, 'account_module/reset_password.html', context=context)


class LogoutView(View):
    def get(self, request: HttpRequest):
        logout(request)
        return redirect(reverse('login_page'))

    def post(self, requset: HttpRequest):
        pass
