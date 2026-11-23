from datetime import timedelta

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from products.models import Category, Product
from .models import BlogCategory, Comment, Post, Tag


class BlogPublicViewsTests(TestCase):
    def setUp(self):
        self.author = get_user_model().objects.create_user(username="blogger", password="test-password")
        self.category = BlogCategory.objects.create(name="راهنمای خرید", slug="buying-guide")
        self.tag = Tag.objects.create(name="موبایل", slug="mobile")
        self.post = Post.objects.create(
            title="راهنمای خرید گوشی",
            slug="phone-buying-guide",
            excerpt="نکات مهم خرید گوشی",
            content="پاراگراف اول\n\nپاراگراف دوم",
            category=self.category,
            author=self.author,
            status=Post.Status.PUBLISHED,
        )
        self.post.tags.add(self.tag)

    def test_published_post_is_visible_in_blog_list(self):
        response = self.client.get(reverse("blog:list"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_home_page_shows_latest_published_blog_posts(self):
        response = self.client.get(reverse("core:home"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.post.title)

    def test_draft_post_is_not_public(self):
        Post.objects.create(title="پیش‌نویس", slug="draft-post", content="متن")
        response = self.client.get(reverse("blog:list"))
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, "پیش‌نویس")

    def test_scheduled_post_is_not_public_before_publish_time(self):
        Post.objects.create(
            title="مقاله زمان‌بندی‌شده",
            slug="scheduled-post",
            content="متن",
            status=Post.Status.PUBLISHED,
            published_at=timezone.now() + timedelta(days=1),
        )
        response = self.client.get(reverse("blog:list"))
        self.assertNotContains(response, "مقاله زمان‌بندی‌شده")

    def test_inactive_blog_category_hides_its_posts(self):
        self.category.is_active = False
        self.category.save(update_fields=["is_active"])
        self.assertFalse(Post.objects.published().filter(pk=self.post.pk).exists())
        response = self.client.get(reverse("blog:detail", kwargs={"slug": self.post.slug}))
        self.assertEqual(response.status_code, 404)

    def test_category_and_tag_filters(self):
        category_response = self.client.get(self.category.get_absolute_url())
        tag_response = self.client.get(self.tag.get_absolute_url())
        self.assertContains(category_response, self.post.title)
        self.assertContains(tag_response, self.post.title)

    def test_detail_page_increments_views_and_shows_content(self):
        response = self.client.get(self.post.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "پاراگراف اول")
        self.post.refresh_from_db()
        self.assertEqual(self.post.views, 1)

    def test_new_comment_requires_moderation(self):
        response = self.client.post(
            self.post.get_absolute_url(),
            {"name": "کاربر آزمایشی", "email": "test@example.com", "body": "دیدگاه آزمایشی"},
        )
        self.assertEqual(response.status_code, 302)
        comment = Comment.objects.get(post=self.post)
        self.assertFalse(comment.is_approved)
        detail_response = self.client.get(self.post.get_absolute_url())
        self.assertNotContains(detail_response, "دیدگاه آزمایشی")


class BlogRelatedProductsTests(TestCase):
    def test_only_active_products_are_shown_as_related_products(self):
        category = BlogCategory.objects.create(name="آموزش", slug="tutorials")
        post = Post.objects.create(
            title="راهنمای خرید",
            slug="guide",
            content="متن مقاله",
            category=category,
            status=Post.Status.PUBLISHED,
        )
        product_category = Category.objects.create(name="لوازم جانبی", slug="accessories")
        active_product = Product.objects.create(
            category=product_category,
            name="هدفون فعال",
            slug="active-headphone",
            price=1_000_000,
            stock=3,
        )
        inactive_product = Product.objects.create(
            category=product_category,
            name="هدفون غیرفعال",
            slug="inactive-headphone",
            price=1_000_000,
            stock=3,
            is_active=False,
        )
        post.related_products.add(active_product, inactive_product)

        response = self.client.get(post.get_absolute_url())
        self.assertContains(response, "هدفون فعال")
        self.assertNotContains(response, "هدفون غیرفعال")
