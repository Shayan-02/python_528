from django.contrib.auth import get_user_model
from django.test import TestCase

from orders.models import Order, OrderItem
from .models import Category, Product


class ProductPricingTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="موبایل", slug="mobile")
        self.product = Product.objects.create(
            category=self.category,
            name="گوشی آزمایشی",
            slug="test-phone",
            price=12_500_000,
            discount_percent=20,
            stock=3,
        )

    def test_discount_calculation(self):
        self.assertEqual(self.product.discount_amount, 2_500_000)
        self.assertEqual(self.product.final_price, 10_000_000)
        self.assertTrue(self.product.has_discount)

    def test_zero_discount_keeps_original_price(self):
        self.product.discount_percent = 0
        self.product.save(update_fields=["discount_percent"])
        self.assertEqual(self.product.final_price, self.product.price)
        self.assertFalse(self.product.has_discount)

    def test_inactive_category_hides_but_does_not_delete_products(self):
        self.category.is_active = False
        self.category.save(update_fields=["is_active"])

        self.assertTrue(Product.objects.filter(pk=self.product.pk).exists())
        self.assertFalse(
            Product.objects.filter(pk=self.product.pk, is_active=True, category__is_active=True).exists()
        )

        self.category.is_active = True
        self.category.save(update_fields=["is_active"])
        self.assertTrue(
            Product.objects.filter(pk=self.product.pk, is_active=True, category__is_active=True).exists()
        )

    def test_deleting_category_deletes_products_but_keeps_order_snapshot(self):
        user = get_user_model().objects.create_user(username="shopper", password="test-password")
        order = Order.objects.create(
            user=user,
            full_name="خریدار آزمایشی",
            phone="09120000000",
            address="تهران",
            total_price=self.product.final_price,
        )
        order_item = OrderItem.objects.create(
            order=order,
            product=self.product,
            product_name=self.product.name,
            price=self.product.final_price,
            quantity=1,
        )

        self.category.delete()

        self.assertFalse(Product.objects.filter(pk=self.product.pk).exists())
        order_item.refresh_from_db()
        self.assertIsNone(order_item.product)
        self.assertEqual(order_item.product_name, "گوشی آزمایشی")
        self.assertEqual(order_item.price, 10_000_000)


class ProductListingFilterTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="لپ‌تاپ", slug="laptop")
        self.discounted_product = Product.objects.create(
            category=self.category,
            name="لپ‌تاپ تخفیف‌دار",
            slug="discounted-laptop",
            price=2_000_000,
            discount_percent=50,
            stock=4,
        )
        self.regular_product = Product.objects.create(
            category=self.category,
            name="لپ‌تاپ عادی",
            slug="regular-laptop",
            price=2_000_000,
            stock=0,
        )

    def product_names(self, response):
        return {product.name for product in response.context["page_obj"].object_list}

    def test_price_range_filters_using_payable_price_after_discount(self):
        response = self.client.get("/products/", {"min_price": 1_500_000})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product_names(response), {"لپ‌تاپ عادی"})

    def test_discounted_filter_only_returns_discounted_products(self):
        response = self.client.get("/products/", {"discounted": "1"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product_names(response), {"لپ‌تاپ تخفیف‌دار"})

    def test_in_stock_filter_only_returns_available_products(self):
        response = self.client.get("/products/", {"in_stock": "1"})

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.product_names(response), {"لپ‌تاپ تخفیف‌دار"})

    def test_sort_toolbar_is_separate_from_category_filter_panel(self):
        response = self.client.get("/products/")
        html = response.content.decode()

        self.assertEqual(response.status_code, 200)
        self.assertIn('class="sort-toolbar"', html)
        self.assertIn('class="product-filters"', html)
        self.assertLess(html.index('class="sort-toolbar"'), html.index('class="product-filters"'))
