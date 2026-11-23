from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from orders.models import Order, OrderItem
from products.models import Category, Product


class CMSAccessTests(TestCase):
    def test_customer_cannot_open_cms(self):
        user = get_user_model().objects.create_user(username="customer", password="safe-password")
        self.client.force_login(user)
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 403)

    def test_staff_can_open_cms_dashboard(self):
        staff = get_user_model().objects.create_user(
            username="manager", password="safe-password", is_staff=True
        )
        self.client.force_login(staff)
        response = self.client.get(reverse("dashboard:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "داشبورد مدیریت")


class CMSCategoryManagementTests(TestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user(
            username="manager", password="safe-password", is_staff=True
        )
        self.client.force_login(self.staff)
        self.category = Category.objects.create(name="لپ‌تاپ", slug="laptop")
        self.product = Product.objects.create(
            category=self.category,
            name="لپ‌تاپ آزمایشی",
            slug="test-laptop",
            price=25_000_000,
            stock=2,
        )

    def test_deactivating_category_hides_without_deleting_products(self):
        response = self.client.post(reverse("dashboard:category_toggle", args=[self.category.pk]))
        self.assertEqual(response.status_code, 302)
        self.category.refresh_from_db()
        self.assertFalse(self.category.is_active)
        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
        self.assertEqual(self.client.get(reverse("products:list")).context["page_obj"].paginator.count, 0)

    def test_reactivating_category_shows_products_again(self):
        self.category.is_active = False
        self.category.save(update_fields=["is_active"])
        self.client.post(reverse("dashboard:category_toggle", args=[self.category.pk]))
        self.category.refresh_from_db()
        self.assertTrue(self.category.is_active)
        self.assertEqual(self.client.get(reverse("products:list")).context["page_obj"].paginator.count, 1)

    def test_delete_category_deletes_products_but_preserves_order_snapshot(self):
        user = get_user_model().objects.create_user(username="buyer", password="safe-password")
        order = Order.objects.create(
            user=user, full_name="خریدار", phone="09120000000", address="تهران",
            total_price=self.product.final_price,
        )
        line = OrderItem.objects.create(
            order=order, product=self.product, product_name=self.product.name,
            price=self.product.final_price, quantity=1,
        )
        response = self.client.post(reverse("dashboard:category_delete", args=[self.category.pk]))
        self.assertEqual(response.status_code, 302)
        self.assertFalse(Category.objects.filter(pk=self.category.pk).exists())
        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
        line.refresh_from_db()
        self.assertIsNone(line.product)
        self.assertEqual(line.product_name, "لپ‌تاپ آزمایشی")
        self.assertEqual(line.price, 25_000_000)


class CMSUserManagementTests(TestCase):
    def setUp(self):
        self.staff = get_user_model().objects.create_user(
            username="manager", password="safe-password", is_staff=True
        )
        self.customer = get_user_model().objects.create_user(
            username="customer", password="safe-password"
        )
        self.client.force_login(self.staff)

    def test_staff_can_deactivate_and_reactivate_customer(self):
        url = reverse("dashboard:user_toggle", args=[self.customer.pk])
        self.client.post(url)
        self.customer.refresh_from_db()
        self.assertFalse(self.customer.is_active)
        self.client.post(url)
        self.customer.refresh_from_db()
        self.assertTrue(self.customer.is_active)

    def test_staff_cannot_deactivate_another_staff_account(self):
        other_staff = get_user_model().objects.create_user(
            username="other-manager", password="safe-password", is_staff=True
        )
        self.client.post(reverse("dashboard:user_toggle", args=[other_staff.pk]))
        other_staff.refresh_from_db()
        self.assertTrue(other_staff.is_active)
