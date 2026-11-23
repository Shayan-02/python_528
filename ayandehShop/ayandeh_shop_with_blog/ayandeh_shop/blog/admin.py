from django.contrib import admin
from .models import BlogCategory, Comment, Post, Tag


@admin.register(BlogCategory)
class BlogCategoryAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "is_active", "created_at")
    list_filter = ("is_active",)
    list_editable = ("is_active",)
    search_fields = ("name", "description")
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ("name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ("title", "category", "author", "status", "is_featured", "published_at", "views")
    list_filter = ("status", "is_featured", "allow_comments", "category", "published_at")
    list_editable = ("status", "is_featured")
    search_fields = ("title", "excerpt", "content", "seo_title", "seo_description")
    prepopulated_fields = {"slug": ("title",)}
    filter_horizontal = ("tags", "related_products")
    autocomplete_fields = ("author",)
    date_hierarchy = "published_at"
    readonly_fields = ("views", "created_at", "updated_at")
    fieldsets = (
        ("محتوا", {"fields": ("title", "slug", "excerpt", "content", "featured_image", "category", "tags", "author")} ),
        ("انتشار", {"fields": ("status", "published_at", "is_featured", "allow_comments")} ),
        ("محصولات مرتبط", {"fields": ("related_products",)}),
        ("سئو", {"fields": ("seo_title", "seo_description"), "classes": ("collapse",)}),
        ("آمار و زمان‌ها", {"fields": ("views", "created_at", "updated_at"), "classes": ("collapse",)}),
    )

    def save_model(self, request, obj, form, change):
        if not obj.author_id:
            obj.author = request.user
        super().save_model(request, obj, form, change)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("name", "post", "is_approved", "created_at")
    list_filter = ("is_approved", "created_at")
    list_editable = ("is_approved",)
    search_fields = ("name", "email", "body", "post__title")
    readonly_fields = ("created_at",)
    actions = ("approve_comments", "reject_comments")

    @admin.action(description="تأیید دیدگاه‌های انتخاب‌شده")
    def approve_comments(self, request, queryset):
        queryset.update(is_approved=True)

    @admin.action(description="لغو تأیید دیدگاه‌های انتخاب‌شده")
    def reject_comments(self, request, queryset):
        queryset.update(is_approved=False)
