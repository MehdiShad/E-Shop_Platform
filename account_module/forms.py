from django import forms
from django.core.exceptions import ValidationError
from django.core import validators


class RegisterForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput,
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    password = forms.CharField(
        label="کلمه عبور",
        widget=forms.PasswordInput,
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label="تکرار کلمه عبور",
        widget=forms.PasswordInput,
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )

    def clean_confirm_password(self):
        confirm_password = self.cleaned_data.get("confirm_password")
        password = self.cleaned_data.get("password")

        if password == confirm_password:
            return confirm_password

        raise ValidationError("کلمه عبور و تکرار آن مغایرت دارند")


class LoginForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput,
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )
    password = forms.CharField(
        label="کلمه عبور",
        widget=forms.PasswordInput(),
        validators=[
            validators.MaxLengthValidator(100)
        ]
    )

class ForgotPasswordForm(forms.Form):
    email = forms.EmailField(
        label="ایمیل",
        widget=forms.EmailInput,
        validators=[
            validators.MaxLengthValidator(100),
            validators.EmailValidator,
        ]
    )

class ResetPasswordForm(forms.Form):
    password = forms.CharField(
        label="کلمه عبور",
        widget=forms.PasswordInput,
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label="تکرار کلمه عبور",
        widget=forms.PasswordInput,
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )