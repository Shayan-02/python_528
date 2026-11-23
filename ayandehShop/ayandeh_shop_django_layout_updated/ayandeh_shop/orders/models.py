from django.conf import settings
from django.db import models

from products.models import Product


class Order(models.Model):
    STATUS_CHOICES = [
        ("pending", "در انتظار بررسی"),
        ("processing", "در حال آماده‌سازی"),
        ("sent", "ارسال شده"),
        ("delivered", "تحویل شده"),
        ("cancelled", "لغو شده"),
    ]
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name="orders")
    full_name = models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")
    phone = models.CharField(max_length=20, verbose_name="شماره تماس")
    address = models.TextField(verbose_name="نشانی")
    postal_code = models.CharField(max_length=20, blank=True, verbose_name="کد پستی")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    total_price = models.PositiveBigIntegerField(default=0, verbose_name="مبلغ کل (تومان)")

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "سفارش"
        verbose_name_plural = "سفارش‌ها"

    def __str__(self):
        return f"سفارش #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    # SET_NULL keeps the historical order line when its product/category is deleted.
    # product_name and price are snapshots captured at checkout.
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="order_items",
    )
    product_name = models.CharField(max_length=200)
    price = models.PositiveBigIntegerField()
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return f"{self.product_name} × {self.quantity}"

    def get_cost(self):
        return self.price * self.quantity
