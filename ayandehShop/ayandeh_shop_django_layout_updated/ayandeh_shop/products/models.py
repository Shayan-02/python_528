from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Q
from django.urls import reverse


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
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
        verbose_name="دسته‌بندی",
    )
    name = models.CharField(max_length=200, verbose_name="نام محصول")
    slug = models.SlugField(max_length=220, unique=True, allow_unicode=True)
    sku = models.CharField(max_length=60, blank=True, verbose_name="کد کالا")
    short_description = models.CharField(max_length=300, blank=True, verbose_name="توضیح کوتاه")
    description = models.TextField(blank=True, verbose_name="توضیحات")
    price = models.PositiveBigIntegerField(verbose_name="قیمت اصلی (تومان)")
    discount_percent = models.PositiveSmallIntegerField(
        default=0,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        verbose_name="درصد تخفیف",
        help_text="برای محصول بدون تخفیف، مقدار صفر وارد کنید.",
    )
    stock = models.PositiveIntegerField(default=0, verbose_name="موجودی")
    image = models.ImageField(upload_to="products/", blank=True, null=True, verbose_name="تصویر")
    is_active = models.BooleanField(default=True, verbose_name="نمایش در فروشگاه")
    is_featured = models.BooleanField(default=False, verbose_name="پیشنهاد ویژه")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        indexes = [
            models.Index(fields=["is_active", "created_at"], name="products_pr_dce09b_idx"),
            models.Index(fields=["category", "is_active"], name="products_pr_c25f4a_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(discount_percent__gte=0) & Q(discount_percent__lte=100),
                name="product_discount_percent_0_100",
            ),
        ]
        verbose_name = "محصول"
        verbose_name_plural = "محصولات"

    def __str__(self):
        return self.name

    @property
    def discount_amount(self):
        """Amount deducted from the original price, in toman."""
        return (self.price * self.discount_percent) // 100

    @property
    def final_price(self):
        """Price payable by the customer after applying the discount."""
        return self.price - self.discount_amount

    @property
    def has_discount(self):
        return self.discount_percent > 0 and self.discount_amount > 0

    def get_absolute_url(self):
        return reverse("products:detail", kwargs={"slug": self.slug})
