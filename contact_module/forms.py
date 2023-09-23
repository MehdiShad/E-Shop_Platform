from django import forms
from .models import ContactUs

class ContactUsForm(forms.Form):
    full_name = forms.CharField(
        label="نام و نام خانوادگی",
        max_length=25,
        error_messages={
        'required': 'لطفا نام و نام خانوداگی را انتخاب کنید'
        },
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'نام و نام خانوادگی',
        })
    )
    email = forms.EmailField(
        label="ایمیل", widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'ایمیل',
        })
    )
    title = forms.CharField(
        label="عنوان",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'عنوان',
        })
    )
    message = forms.CharField(
        label="متن پیام",
        widget=forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder': 'متن پیام',
            'id': 'message'
        })
    )


class ContactUsModelForm(forms.ModelForm):
    class Meta:
        model = ContactUs
        fields = ['full_name', 'title', 'email', 'message']
        # fields = '__all__'
        # exclude = 'response'


        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'email': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'title': forms.TextInput(attrs={
                'class': 'form-control'
            }),
            'message': forms.TextInput(attrs={
                'class': 'form-control',
                'rows': 5,
                'id': 'message',

            }),
        }

        labels = {
            'full_name': 'نام و نام خانوادگی شما',
            'email': 'ایمیل',
            'title': 'عنوان',
            'message': 'متن پیام',
        }

        error_messages = {
            'full_name': {
                'required': 'نام و نام خانوادگی شما الزامی است لطفا وارد کنید'
            },
            'email': {
                'required': 'ایمیل شما الزامی است.'
            }
        }


class ProfileForm(forms.Form):
    # user_image = forms.FileField()
    user_image = forms.ImageField()

