from django.contrib import admin
from . import models


# Register your models here.


# method 1:
# admin.site.register(models.Product)

# method 2:

# class ProductAdmin(admin.ModelAdmin):
#     pass
#
# admin.site.register(models.Product, ProductAdmin)

# method 3: use decorator
@admin.register(models.Product)
class ProductAdmin(admin.ModelAdmin):
    # readonly_fields = ['slug']
    prepopulated_fields = {
        'slug': ['title']
    }

    list_display = ['title', 'price', 'is_active', 'is_delete']
    list_filter = ['category', 'is_active']
    list_editable = ['price', 'is_active']


@admin.register(models.ProductBrand)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'url_title']
    list_editable = ['title', 'url_title']


# @admin.register(models.ProductCategory)
# class ProductCategoryAdmin(admin.ModelAdmin):
#     pass
admin.site.register(models.ProductCategory)
admin.site.register(models.ProductTag)


# admin.site.register(models.ProductBrand)


@admin.register(models.ProductVisit)
class ProductBrandAdmin(admin.ModelAdmin):
    list_display = ['id', 'ip']


@admin.register(models.ProductGallery)
class ProductGalleryAdmin(admin.ModelAdmin):
    list_display = ['product']
