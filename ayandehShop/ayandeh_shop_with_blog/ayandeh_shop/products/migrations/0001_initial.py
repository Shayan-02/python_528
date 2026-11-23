# Original schema from the first version of the products application.
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Category",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True, verbose_name="نام دسته")),
                ("slug", models.SlugField(allow_unicode=True, max_length=140, unique=True)),
                ("description", models.TextField(blank=True, verbose_name="توضیحات")),
                ("is_active", models.BooleanField(default=True, verbose_name="فعال")),
            ],
            options={
                "verbose_name": "دسته‌بندی",
                "verbose_name_plural": "دسته‌بندی‌ها",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=200, verbose_name="نام محصول")),
                ("slug", models.SlugField(allow_unicode=True, max_length=220, unique=True)),
                ("sku", models.CharField(blank=True, max_length=60, verbose_name="کد کالا")),
                ("short_description", models.CharField(blank=True, max_length=300, verbose_name="توضیح کوتاه")),
                ("description", models.TextField(blank=True, verbose_name="توضیحات")),
                ("price", models.PositiveBigIntegerField(verbose_name="قیمت (تومان)")),
                ("stock", models.PositiveIntegerField(default=0, verbose_name="موجودی")),
                ("image", models.ImageField(blank=True, null=True, upload_to="products/", verbose_name="تصویر")),
                ("is_active", models.BooleanField(default=True, verbose_name="نمایش در فروشگاه")),
                ("is_featured", models.BooleanField(default=False, verbose_name="پیشنهاد ویژه")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "category",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.PROTECT,
                        related_name="products",
                        to="products.category",
                        verbose_name="دسته‌بندی",
                    ),
                ),
            ],
            options={
                "verbose_name": "محصول",
                "verbose_name_plural": "محصولات",
                "ordering": ["-created_at"],
                "indexes": [
                    models.Index(fields=["is_active", "created_at"], name="products_pr_dce09b_idx"),
                    models.Index(fields=["category", "is_active"], name="products_pr_c25f4a_idx"),
                ],
            },
        ),
    ]
