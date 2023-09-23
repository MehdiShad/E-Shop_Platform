from django.db.models import Count
from django.http import HttpRequest
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View
from .models import Product, ProductCategory, ProductBrand


# Create your views here.


# def product_list(request):
#     products = Product.objects.all().order_by('-price')[:5] #DESC
#     number_of_products = products.count()
#
#     context = {
#         'products': products,
#     }
#     return render(request, 'product_module/product_list.html', context=context)


# class ProductListView(TemplateView):
#     template_name = 'product_module/product_list.html'
#
#     def get_context_data(self, **kwargs):
#         products = Product.objects.all().order_by('-price')[:5]  # DESC
#         context = super(ProductListView, self).get_context_data()
#         context['products'] = products
#         return context

class ProductListView(ListView):
    template_name = 'product_module/product_list.html'
    model = Product
    context_object_name = 'products'
    ordering = ['-price'] #به ترتیب قرار گیری فیلدها عملیات ordering را انجام میدهد
    paginate_by = 3

    def get_queryset(self):
        query = super(ProductListView, self).get_queryset()
        category_name = self.kwargs.get('cat')
        brand_name = self.kwargs.get('brand')
        if brand_name is not None:
            query = query.filter(brand__url_title__iexact=brand_name, is_active=True)
        if category_name is not None:
            query = query.filter(category__url_title__iexact=category_name, is_active=True)
        return query

    #اعمال یک کوئری برای این listView
    # def get_queryset(self):
    #     base_query = super(ProductListView, self).get_queryset()
    #     data = base_query.filter(is_active=True)
    #     return data

# def product_detail(request, slug):
#     # try:
#     #     product = Product.objects.get(id=product_id)
#     # except:
#     #     raise Http404
#
#     product = get_object_or_404(Product, slug=slug)
#     context = {
#         'product': product
#     }
#     return render(request, 'product_module/product_detail.html', context=context)


# class ProductDetailView(TemplateView):
#     template_name = 'product_module/product_detail.html'
#
#     def get_context_data(self, **kwargs):
#         slug = kwargs['slug']
#         product = Product.objects.get(slug=slug)
#         context = super(ProductDetailView, self).get_context_data()
#         context['product'] = product
#         return context


class ProductDetailView(DetailView):
    template_name = "product_module/product_detail.html"
    model = Product


class AddProductFavorite(View):
    def post(self, request):
        product_id = request.POST['product_id']
        product = Product.objects.get(pk=product_id)
        product.session['product_favorites'] = product_id
        return redirect(product.get_absolute_url())



def product_categories_component(request: HttpRequest):
    product_categories = ProductCategory.objects.filter(is_active=True, is_delete=False)
    context = {
        'categories': product_categories,
    }
    return render(request, 'product_module/components/product_categories_component.html', context=context)


def product_brands_component(request: HttpRequest):
    prodcut_brand = ProductBrand.objects.annotate(proudcts_count=Count('product')).filter(is_active=True)
    context = {
        'brands': prodcut_brand
    }
    return render(request, 'product_module/components/product_brnads_component.html', context=context)