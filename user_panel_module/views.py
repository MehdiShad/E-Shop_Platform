from django.views import View
from django.urls import reverse
from django.http import HttpRequest
from django.contrib.auth import logout
from account_module.models import User
from django.views.generic import TemplateView
from django.shortcuts import render, redirect
from order_module.models import Order, OrderDetail
from .forms import EditProfileModelForm, ChangePasswordForm


# Create your views here.

class UserPanelDashboardPage(TemplateView):
    template_name = 'user_panel_module/user_panel_dashboard_page.html'


class EditUserProfilePage(View):
    def get(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        # method 1
        # edit_form = EditProfileModelForm(initial={'first_name': current_user.first_name, 'last_name': current_user.last_name})
        # method 2
        edit_form = EditProfileModelForm(instance=current_user)
        context = {
            'form': edit_form,
            'current_user': current_user,
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context=context)

    def post(self, request: HttpRequest):
        current_user = User.objects.filter(id=request.user.id).first()
        edit_form = EditProfileModelForm(request.POST, request.FILES, instance=current_user)
        if edit_form.is_valid():
            edit_form.save(commit=True)

        context = {
            'form': edit_form,
            'current_user': current_user,
        }
        return render(request, 'user_panel_module/edit_profile_page.html', context=context)


class ChangePasswordPage(View):
    def get(self, request: HttpRequest):
        context = {
            'form': ChangePasswordForm(),
        }
        return render(request, 'user_panel_module/change_password_page.html', context=context)

    def post(self, request: HttpRequest):
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            current_user: User = User.objects.filter(id=request.user.id).first()
            if current_user.check_password(form.cleaned_data.get('current_password')):
                current_user.set_password(form.cleaned_data.get('password'))
                current_user.save()
                logout(request)
                return redirect(reverse('login_page'))
            else:
                form.add_error('password', 'کلمه عبور اشتباه است')

        context = {
            'form': form,
        }
        return render(request, 'user_panel_module/change_password_page.html', context=context)


def user_panel_menu_component(request: HttpRequest):
    context = {}
    return render(request, 'user_panel_module/components/user_panel_menu_component.html', context=context)


def user_basket(request: HttpRequest):
    current_order, created = Order.objects.prefetch_related('orderdetail_set').get_or_create(is_paid=False, user_id=request.user.id)
    total_cart_amount = 0
    for order_detail in current_order.orderdetail_set.all():
        total_cart_amount += order_detail.count * order_detail.product.price

    context = {
        'order': current_order,
        'total_cart_amount': total_cart_amount,
    }
    return render(request, 'user_panel_module/user_basket.html', context=context)
