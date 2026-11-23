from django.conf import settings
from django.db import models
from django.db.models import Q
from django.utils import timezone
from django.urls import reverse


class BlogCategory(models.Model):
    name = models.CharField(max_length=120, unique=True, verbose_name="نام دسته‌بندی")
    slug = models.SlugField(max_length=140, unique=True, allow_unicode=True)
    description = models.TextField(blank=True, verbose_name="توضیحات")
    is_active = models.BooleanField(default=True, verbose_name="فعال")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "دسته‌بندی بلاگ"
        verbose_name_plural = "دسته‌بندی‌های بلاگ"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:category", kwargs={"slug": self.slug})


class Tag(models.Model):
    name = models.CharField(max_length=80, unique=True, verbose_name="نام برچسب")
    slug = models.SlugField(max_length=100, unique=True, allow_unicode=True)

    class Meta:
        ordering = ["name"]
        verbose_name = "برچسب بلاگ"
        verbose_name_plural = "برچسب‌های بلاگ"

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("blog:tag", kwargs={"slug": self.slug})


class PostQuerySet(models.QuerySet):
    def published(self):
        """Return posts that are published and whose optional category is active."""
        return self.filter(
            status=Post.Status.PUBLISHED,
            published_at__lte=timezone.now(),
        ).filter(Q(category__isnull=True) | Q(category__is_active=True))


class Post(models.Model):
    class Status(models.TextChoices):
        DRAFT = "draft", "پیش‌نویس"
        PUBLISHED = "published", "منتشرشده"

    title = models.CharField(max_length=220, verbose_name="عنوان مقاله")
    slug = models.SlugField(max_length=240, unique=True, allow_unicode=True)
    excerpt = models.CharField(max_length=400, blank=True, verbose_name="خلاصه مقاله")
    content = models.TextField(verbose_name="متن مقاله", help_text="متن ساده؛ برای ایجاد پاراگراف، بین خطوط یک سطر خالی قرار دهید.")
    featured_image = models.ImageField(upload_to="blog/", blank=True, null=True, verbose_name="تصویر شاخص")
    category = models.ForeignKey(
        BlogCategory,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="posts",
        verbose_name="دسته‌بندی",
    )
    tags = models.ManyToManyField(Tag, blank=True, related_name="posts", verbose_name="برچسب‌ها")
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        related_name="blog_posts",
        verbose_name="نویسنده",
    )
    related_products = models.ManyToManyField(
        "products.Product",
        blank=True,
        related_name="blog_posts",
        verbose_name="محصولات مرتبط",
    )
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.DRAFT, verbose_name="وضعیت انتشار")
    is_featured = models.BooleanField(default=False, verbose_name="مقاله منتخب")
    allow_comments = models.BooleanField(default=True, verbose_name="امکان ثبت دیدگاه")
    published_at = models.DateTimeField(blank=True, null=True, verbose_name="زمان انتشار")
    seo_title = models.CharField(max_length=70, blank=True, verbose_name="عنوان سئو")
    seo_description = models.CharField(max_length=170, blank=True, verbose_name="توضیحات سئو")
    views = models.PositiveIntegerField(default=0, editable=False, verbose_name="بازدید")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = PostQuerySet.as_manager()

    class Meta:
        ordering = ["-published_at", "-created_at"]
        indexes = [
            models.Index(fields=["status", "published_at"], name="blog_post_status_pub_idx"),
            models.Index(fields=["category", "status"], name="blog_post_cat_status_idx"),
        ]
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if self.status == self.Status.PUBLISHED and self.published_at is None:
            self.published_at = timezone.now()
            update_fields = kwargs.get("update_fields")
            if update_fields is not None:
                kwargs["update_fields"] = set(update_fields) | {"published_at"}
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("blog:detail", kwargs={"slug": self.slug})


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="comments", verbose_name="مقاله")
    name = models.CharField(max_length=100, verbose_name="نام")
    email = models.EmailField(verbose_name="ایمیل")
    body = models.TextField(max_length=3000, verbose_name="متن دیدگاه")
    is_approved = models.BooleanField(default=False, verbose_name="تأیید شده")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ثبت")

    class Meta:
        ordering = ["created_at"]
        indexes = [models.Index(fields=["post", "is_approved"], name="blog_comment_post_ok_idx")]
        verbose_name = "دیدگاه"
        verbose_name_plural = "دیدگاه‌ها"

    def __str__(self):
        return f"{self.name} - {self.post.title}"
