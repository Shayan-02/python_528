# Original schema from the first version of the orders application.
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Order",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("full_name", models.CharField(max_length=150, verbose_name="نام و نام خانوادگی")),
                ("phone", models.CharField(max_length=20, verbose_name="شماره تماس")),
                ("address", models.TextField(verbose_name="نشانی")),
                ("postal_code", models.CharField(blank=True, max_length=20, verbose_name="کد پستی")),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("pending", "در انتظار بررسی"),
                            ("processing", "در حال آماده‌سازی"),
                            ("sent", "ارسال شده"),
                            ("delivered", "تحویل شده"),
                            ("cancelled", "لغو شده"),
                        ],
                        default="pending",
                        max_length=20,
                    ),
                ),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("total_price", models.PositiveBigIntegerField(default=0, verbose_name="مبلغ کل (تومان)")),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="orders",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
            options={
                "verbose_name": "سفارش",
                "verbose_name_plural": "سفارش‌ها",
                "ordering": ["-created_at"],
            },
        ),
        migrations.CreateModel(
            name="OrderItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("product_name", models.CharField(max_length=200)),
                ("price", models.PositiveBigIntegerField()),
                ("quantity", models.PositiveIntegerField(default=1)),
                (
                    "order",
                    models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="orders.order"),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="order_items",
                        to="products.product",
                    ),
                ),
            ],
        ),
    ]
