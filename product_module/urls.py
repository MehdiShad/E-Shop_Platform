from . import views
from django.urls import path

urlpatterns = [
    # path('', views.product_list, name="product-list"),
    path('', views.ProductListView.as_view(), name="product-list"),
    path('cat/<cat>', views.ProductListView.as_view(), name="product-categories-list"),
    path('brand/<brand>', views.ProductListView.as_view(), name="product-list-by-brands"),
    # path('<int:product_id>', views.product_detail, name="product-detail"),
    # path('<slug:slug>', views.product_detail, name="product-detail"),
    path('product-favorite', views.AddProductFavorite.as_view(), name="product-favorite"),
    path('<slug:slug>', views.ProductDetailView.as_view(), name="product-detail"),
]

