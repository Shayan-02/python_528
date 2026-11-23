from django.contrib import admin
from django.utils.html import format_html

from .models import Category, Product


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "category",
        "formatted_price",
        "discount_percent",
        "formatted_final_price",
        "stock",
        "is_active",
        "is_featured",
    )
    list_filter = ("category", "is_active", "is_featured")
    search_fields = ("name", "sku", "description")
    list_editable = ("discount_percent", "stock", "is_active", "is_featured")
    prepopulated_fields = {"slug": ("name",)}

    @admin.display(description="قیمت اصلی", ordering="price")
    def formatted_price(self, obj):
        return f"{obj.price:,} تومان"

    @admin.display(description="قیمت با تخفیف")
    def formatted_final_price(self, obj):
        return f"{obj.final_price:,} تومان"
