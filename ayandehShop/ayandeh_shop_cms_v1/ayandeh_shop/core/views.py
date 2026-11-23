from django.shortcuts import render

from products.models import Category, Product
from blog.models import Post


def home(request):
    categories = Category.objects.filter(is_active=True)[:8]
    visible_products = Product.objects.filter(
        is_active=True,
        category__is_active=True,
    ).select_related("category")
    featured = visible_products.filter(is_featured=True)[:8]
    if not featured:
        featured = visible_products[:8]
    latest = visible_products[:8]
    blog_posts = Post.objects.published().select_related("category", "author")[:3]
    return render(
        request,
        "core/home.html",
        {"categories": categories, "featured": featured, "latest": latest, "blog_posts": blog_posts},
    )
