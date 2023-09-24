from django.contrib import admin
from order_module import models


# Register your models here.

@admin.register(models.Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['id', 'user']


@admin.register(models.OrderDetail)
class OrderDetail(admin.ModelAdmin):
    list_display = ['id', 'order', 'product']
