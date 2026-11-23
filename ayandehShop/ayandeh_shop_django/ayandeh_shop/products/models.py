from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Category(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="نام دسته")
    slug = models.SlugField(max_length=140, unique=True, allow_unicode=True)
    description = models.TextField(blank=True, verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال")

    class Meta:
        ordering = ["name"]
        verbose_name = "دسته‌بندی"
        verbose_name_plural = "دسته‌بندی‌ها"

    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products", verbose_name="دسته‌بندی")
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True)
    sku = models.CharField(max_length=60, blank=True, verbose_name="کد کالا")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="توضیح کوتاه")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    price = models.PositiveBigIntegerField(verbose_name="قیمت (تومان)")
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="تصویر")
    is_active = models.BooleanField(default=True, verbose_name="نمایش در فروشگاه")
    is_featured = models.BooleanField(default=False, verbose_name="پیشنهاد ویژه")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [models.Index(fields=["is_active", "created_at"]), models.Index(fields=["category", "is_active"])]
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})
