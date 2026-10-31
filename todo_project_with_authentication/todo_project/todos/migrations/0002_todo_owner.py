import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("todos", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="todo",
            name="owner",
            field=models.ForeignKey(
                blank=True,
                editable=False,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="todos",
                to=settings.AUTH_USER_MODEL,
            ),
        ),
    ]
