from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    dependencies = [
        ("orders", "0001_initial"),
        ("products", "0002_discount_and_category_cascade"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orderitem",
            name="product",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="order_items",
                to="products.product",
            ),
        ),
    ]
