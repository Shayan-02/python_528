from django import forms

from blog.models import BlogCategory, Post, Tag
from orders.models import Order
from products.models import Category, Product


class DashboardFormMixin:
    """Apply the common CMS form styling without changing model validation."""

    def apply_widgets(self):
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(widget, forms.SelectMultiple):
                widget.attrs.setdefault("class", "form-select cms-multi-select")
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", "form-select")
            else:
                widget.attrs.setdefault("class", "form-control")


class ProductForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Product
        fields = (
            "category", "name", "slug", "sku", "short_description",
            "description", "price", "discount_percent", "stock", "image",
            "is_active", "is_featured",
        )
        widgets = {
            "short_description": forms.TextInput(attrs={"placeholder": "توضیح کوتاه محصول"}),
            "description": forms.Textarea(attrs={"rows": 5}),
            "price": forms.NumberInput(attrs={"min": 0, "step": 1}),
            "discount_percent": forms.NumberInput(attrs={"min": 0, "max": 100}),
            "stock": forms.NumberInput(attrs={"min": 0, "step": 1}),
            "image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
        }
        labels = {
            "category": "دسته‌بندی", "name": "نام محصول", "slug": "نامک (Slug)",
            "sku": "کد کالا", "short_description": "توضیح کوتاه",
            "description": "توضیحات محصول", "price": "قیمت اصلی (تومان)",
            "discount_percent": "درصد تخفیف", "stock": "موجودی",
            "image": "تصویر محصول", "is_active": "نمایش در فروشگاه",
            "is_featured": "محصول پیشنهادی",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = Category.objects.order_by("name")
        self.apply_widgets()


class CategoryForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Category
        fields = ("name", "slug", "description", "is_active")
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
        labels = {
            "name": "نام دسته‌بندی", "slug": "نامک (Slug)",
            "description": "توضیحات", "is_active": "فعال بودن دسته‌بندی",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_widgets()


class OrderStatusForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Order
        fields = ("status",)
        labels = {"status": "وضعیت سفارش"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_widgets()


class PostForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "title", "slug", "excerpt", "content", "featured_image", "category",
            "tags", "related_products", "status", "is_featured", "allow_comments",
            "published_at", "seo_title", "seo_description",
        )
        widgets = {
            "excerpt": forms.Textarea(attrs={"rows": 2}),
            "content": forms.Textarea(attrs={"rows": 12}),
            "featured_image": forms.ClearableFileInput(attrs={"accept": "image/*"}),
            "published_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "seo_description": forms.Textarea(attrs={"rows": 2}),
        }
        labels = {
            "title": "عنوان مقاله", "slug": "نامک (Slug)", "excerpt": "خلاصه مقاله",
            "content": "متن مقاله", "featured_image": "تصویر شاخص",
            "category": "دسته‌بندی بلاگ", "tags": "برچسب‌ها",
            "related_products": "محصولات مرتبط", "status": "وضعیت انتشار",
            "is_featured": "مقاله منتخب", "allow_comments": "امکان ثبت دیدگاه",
            "published_at": "زمان انتشار", "seo_title": "عنوان سئو",
            "seo_description": "توضیحات سئو",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["category"].queryset = BlogCategory.objects.order_by("name")
        self.fields["published_at"].input_formats = ["%Y-%m-%dT%H:%M"]
        self.fields["published_at"].required = False
        self.apply_widgets()
        self.fields["content"].help_text = "برای ایجاد پاراگراف، بین خطوط یک سطر خالی قرار دهید."
        self.fields["tags"].help_text = "برای انتخاب چند برچسب، کلید Ctrl را نگه دارید."
        self.fields["related_products"].help_text = "برای انتخاب چند محصول، کلید Ctrl را نگه دارید."


class BlogCategoryForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = BlogCategory
        fields = ("name", "slug", "description", "is_active")
        widgets = {"description": forms.Textarea(attrs={"rows": 4})}
        labels = {
            "name": "نام دسته‌بندی", "slug": "نامک (Slug)",
            "description": "توضیحات", "is_active": "فعال بودن دسته‌بندی",
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_widgets()


class TagForm(DashboardFormMixin, forms.ModelForm):
    class Meta:
        model = Tag
        fields = ("name", "slug")
        labels = {"name": "نام برچسب", "slug": "نامک (Slug)"}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.apply_widgets()
