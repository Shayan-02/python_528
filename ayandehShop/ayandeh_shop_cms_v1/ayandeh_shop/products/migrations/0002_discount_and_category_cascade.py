from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("products", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="product",
            name="discount_percent",
            field=models.PositiveSmallIntegerField(
                default=0,
                help_text="برای محصول بدون تخفیف، مقدار صفر وارد کنید.",
                validators=[MinValueValidator(0), MaxValueValidator(100)],
                verbose_name="درصد تخفیف",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="category",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="products",
                to="products.category",
                verbose_name="دسته‌بندی",
            ),
        ),
        migrations.AddConstraint(
            model_name="product",
            constraint=models.CheckConstraint(
                condition=models.Q(("discount_percent__gte", 0), ("discount_percent__lte", 100)),
                name="product_discount_percent_0_100",
            ),
        ),
    ]
