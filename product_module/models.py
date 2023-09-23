from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.utils.text import slugify
from django.urls import reverse


# Create your models here.


class ProductCategory(models.Model):
    title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان')
    url_title = models.CharField(max_length=300, db_index=True, verbose_name='عنوان در url')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'دسته بندی'
        verbose_name_plural = 'دسته بندی ها'


class ProductBrand(models.Model):
    title = models.CharField(max_length=300, verbose_name="نام برند", db_index=True)
    url_title = models.CharField(max_length=300, verbose_name="نام در url", db_index=True)
    is_active = models.BooleanField(verbose_name="فعال / غیرفعال")

    class Meta:
        verbose_name = "برند"
        verbose_name_plural = "برندها"

    def __str__(self):
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=300, verbose_name='نام محصول')
    category = models.ManyToManyField(ProductCategory, related_name="product_categories", verbose_name='دسته بندی ها')
    image = models.ImageField(upload_to='images/products', null=True, blank=True, verbose_name="تصویر محصول")
    brand = models.ForeignKey(ProductBrand, on_delete=models.CASCADE, verbose_name="برند", null=True, blank=True)
    price = models.IntegerField(verbose_name='قیمت')
    # rating = models.IntegerField(validators=[MinValueValidator(1), MaxValueValidator(5)],default=0)
    short_description = models.CharField(max_length=360, null=True, db_index=True,verbose_name='توضیحات کوتاه')
    description = models.TextField(db_index=True, verbose_name='توضیحات اصلی')
    is_active = models.BooleanField(default=False, verbose_name='فعال / غیرفعال')
    slug = models.SlugField(null=True, db_index=True,max_length=200, unique=True, verbose_name='عنوان در url') #hello world _> hello-world
    is_delete = models.BooleanField(verbose_name='حذف شده / نشده')

    def get_absolute_url(self):
        return reverse('product-detail', args=[self.slug])

    def save(self, *args, **kwargs):
        # self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.title} ({self.price})"

    class Meta:
        verbose_name = 'محصول'
        verbose_name_plural = 'محصولات'


class ProductTag(models.Model):
    caption = models.CharField(max_length=300, db_index=True, verbose_name="عنوان")
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='product_tags',verbose_name='تگ های محصول')

    def __str__(self):
        return self.caption

    class Meta:
        verbose_name = 'تگ محصول'
        verbose_name_plural = 'تگ های محصولات'
