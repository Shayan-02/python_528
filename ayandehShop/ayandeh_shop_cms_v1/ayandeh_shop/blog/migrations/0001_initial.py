import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("products", "0002_discount_and_category_cascade"),
    ]

    operations = [
        migrations.CreateModel(
            name="BlogCategory",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=120, unique=True, verbose_name="نام دسته‌بندی")),
                ("slug", models.SlugField(allow_unicode=True, max_length=140, unique=True)),
                ("description", models.TextField(blank=True, verbose_name="توضیحات")),
                ("is_active", models.BooleanField(default=True, verbose_name="فعال")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
            options={
                "verbose_name": "دسته‌بندی بلاگ",
                "verbose_name_plural": "دسته‌بندی‌های بلاگ",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Tag",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=80, unique=True, verbose_name="نام برچسب")),
                ("slug", models.SlugField(allow_unicode=True, max_length=100, unique=True)),
            ],
            options={
                "verbose_name": "برچسب بلاگ",
                "verbose_name_plural": "برچسب‌های بلاگ",
                "ordering": ["name"],
            },
        ),
        migrations.CreateModel(
            name="Post",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("title", models.CharField(max_length=220, verbose_name="عنوان مقاله")),
                ("slug", models.SlugField(allow_unicode=True, max_length=240, unique=True)),
                ("excerpt", models.CharField(blank=True, max_length=400, verbose_name="خلاصه مقاله")),
                ("content", models.TextField(help_text="متن ساده؛ برای ایجاد پاراگراف، بین خطوط یک سطر خالی قرار دهید.", verbose_name="متن مقاله")),
                ("featured_image", models.ImageField(blank=True, null=True, upload_to="blog/", verbose_name="تصویر شاخص")),
                ("status", models.CharField(choices=[("draft", "پیش‌نویس"), ("published", "منتشرشده")], default="draft", max_length=12, verbose_name="وضعیت انتشار")),
                ("is_featured", models.BooleanField(default=False, verbose_name="مقاله منتخب")),
                ("allow_comments", models.BooleanField(default=True, verbose_name="امکان ثبت دیدگاه")),
                ("published_at", models.DateTimeField(blank=True, null=True, verbose_name="زمان انتشار")),
                ("seo_title", models.CharField(blank=True, max_length=70, verbose_name="عنوان سئو")),
                ("seo_description", models.CharField(blank=True, max_length=170, verbose_name="توضیحات سئو")),
                ("views", models.PositiveIntegerField(default=0, editable=False, verbose_name="بازدید")),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("author", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="blog_posts", to=settings.AUTH_USER_MODEL, verbose_name="نویسنده")),
                ("category", models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name="posts", to="blog.blogcategory", verbose_name="دسته‌بندی")),
                ("related_products", models.ManyToManyField(blank=True, related_name="blog_posts", to="products.product", verbose_name="محصولات مرتبط")),
                ("tags", models.ManyToManyField(blank=True, related_name="posts", to="blog.tag", verbose_name="برچسب‌ها")),
            ],
            options={
                "verbose_name": "مقاله",
                "verbose_name_plural": "مقالات",
                "ordering": ["-published_at", "-created_at"],
                "indexes": [
                    models.Index(fields=["status", "published_at"], name="blog_post_status_pub_idx"),
                    models.Index(fields=["category", "status"], name="blog_post_cat_status_idx"),
                ],
            },
        ),
        migrations.CreateModel(
            name="Comment",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("name", models.CharField(max_length=100, verbose_name="نام")),
                ("email", models.EmailField(max_length=254, verbose_name="ایمیل")),
                ("body", models.TextField(max_length=3000, verbose_name="متن دیدگاه")),
                ("is_approved", models.BooleanField(default=False, verbose_name="تأیید شده")),
                ("created_at", models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")),
                ("post", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="comments", to="blog.post", verbose_name="مقاله")),
            ],
            options={
                "verbose_name": "دیدگاه",
                "verbose_name_plural": "دیدگاه‌ها",
                "ordering": ["created_at"],
                "indexes": [models.Index(fields=["post", "is_approved"], name="blog_comment_post_ok_idx")],
            },
        ),
    ]
