from django.core.exceptions import ValidationError
from django import forms
from account_module.models import User
from django.core import validators


class EditProfileModelForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'avatar', 'address', 'about_user']
        # fields = '__all__'
        # exclude = 'response'


        widgets = {
            'first_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'avatar': forms.FileInput(attrs={
                'class': 'form-control'
            }),
            'address': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 3,
            }),
            'about_user': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 8,
                'id': 'message',

            }),
        }

        labels = {
            'first_name': 'نام',
            'last_name': 'نام خانوادگی',
            'avatar': 'تصویر پروفایل',
            'address': 'آدرس',
            'about_user': 'درباره شخص',
        }

        # error_messages = {
        #     'full_name': {
        #         'required': 'نام و نام خانوادگی شما الزامی است لطفا وارد کنید'
        #     },
        #     'email': {
        #         'required': 'ایمیل شما الزامی است.'
        #     }
        # }

class ChangePasswordForm(forms.Form):
    current_password = forms.CharField(
        label="کلمه عبور فعلی",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    password = forms.CharField(
        label="کلمه عبور",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
        validators=[
            validators.MaxLengthValidator(100),
        ]
    )
    confirm_password = forms.CharField(
        label="تکرار کلمه عبور",
        widget=forms.PasswordInput(
            attrs={
                'class': 'form-control'
            }
        ),
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