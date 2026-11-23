from django.contrib import admin

from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    fields = ("product_name", "formatted_price", "quantity")
    readonly_fields = fields

    @admin.display(description="قیمت واحد")
    def formatted_price(self, obj):
        return f"{obj.price:,} تومان"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "full_name", "formatted_total_price", "status", "created_at")
    list_filter = ("status", "created_at")
    search_fields = ("full_name", "phone", "user__username")
    list_editable = ("status",)
    inlines = [OrderItemInline]

    @admin.display(description="مبلغ کل", ordering="total_price")
    def formatted_total_price(self, obj):
        return f"{obj.total_price:,} تومان"
