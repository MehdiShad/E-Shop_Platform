from django.db import models
from account_module.models import User
from product_module.models import Product


# Create your models here.


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.PROTECT, verbose_name='کاربر')
    is_paid = models.BooleanField(verbose_name='نهایی شده/ نشده')
    payment_date = models.DateField(null=True, blank=True, verbose_name='تاریخ پرداخت')

    def calculate_total_price(self):
        total_cart_amount = 0
        for order_detail in self.orderdetail_set.all():
            if self.is_paid:
                total_cart_amount += order_detail.count * order_detail.final_price
            else:
                total_cart_amount += order_detail.count * order_detail.product.price

        return total_cart_amount

    def __str__(self):
        return str(self.user)

    class Meta:
        verbose_name = 'سبد خرید'
        verbose_name_plural = 'سبدهای خرید کاربران'


class OrderDetail(models.Model):
    order = models.ForeignKey(Order, on_delete=models.PROTECT, verbose_name='سبد خرید')
    product = models.ForeignKey(Product, on_delete=models.PROTECT, verbose_name='محصول')
    final_price = models.IntegerField(null=True, blank=True, verbose_name='فیمت نهایی تکی محصول')
    count = models.IntegerField(verbose_name='تعداد')

    def get_total_price(self):
        return self.count * self.product.price

    def __str__(self):
        return str(self.order)

    class Meta:
        verbose_name = 'جزییات سبد خرید'
        verbose_name_plural = 'لیست جزییات سبدهای خرید'
