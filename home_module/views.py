from django.shortcuts import render
from utils.convertors import group_list
from django.db.models import Count, Sum
from django.views.generic.base import TemplateView
from product_module.models import Product, ProductCategory
from site_module.models import SiteSetting, FooterLinkBox, Slider


# Create your views here.


# def index_page(request):
#     return render(request, 'home_module/index_page.html')


# class HomeView(View):
#     def get(self, request):
#         context = {
#             'data': 'this is data'
#         }
#         return render(request, 'home_module/index_page.html', context=context)


class HomeView(TemplateView):
    template_name = 'home_module/index_page.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['sliders'] = Slider.objects.filter(is_active=True)

        latest_products = Product.objects.filter(is_active=True, is_delete=False).order_by('-id')[:12]
        most_visit_products = Product.objects.filter(is_active=True, is_delete=False).annotate(
            visit_count=Count('productvisit')).order_by('-visit_count')[:12]

        context['latest_products'] = group_list(custom_list=latest_products, size=4)
        context['most_visit_products'] = group_list(custom_list=most_visit_products, size=4)

        categories = list(
            ProductCategory.objects.annotate(product_count=Count('product_categories')).filter(is_active=True,
                                                                                               is_delete=False,
                                                                                               product_count__gt=0))
        categories_products = []
        for category in categories:
            item = {
                'id': category.id,
                'title': category.title,
                'products': list(category.product_categories.all()[:4])
            }
            categories_products.append(item)

        context['categories_products'] = categories_products
        most_bought_products = Product.objects.filter(orderdetail__order__is_paid=True).annotate(
            order_count=Sum('orderdetail__count')).order_by('-order_count')[:12]

        context['most_bought_products'] = group_list(custom_list=most_bought_products, size=4)

        return context


def contact_page(request):
    return render(request, 'home_module/contact_page.html')


def site_header_component(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    context = {
        'site_setting': site_setting
    }
    return render(request, 'shared/site_header_component.html', context=context)


def site_footer_component(request):
    site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
    footer_link_boxes = FooterLinkBox.objects.all()
    context = {
        'site_setting': site_setting,
        'footer_link_boxes': footer_link_boxes,
    }
    return render(request, 'shared/site_footer_component.html', context=context)


class AboutView(TemplateView):
    template_name = 'home_module/about_page.html'

    def get_context_data(self, **kwargs):
        context = super(AboutView, self).get_context_data(**kwargs)
        site_setting: SiteSetting = SiteSetting.objects.filter(is_main_setting=True).first()
        context['site_setting'] = site_setting
        return context
