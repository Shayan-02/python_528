from django.shortcuts import render
from products.models import Category, Product

def home(request):
    categories = Category.objects.filter(is_active=True)[:8]
    featured = Product.objects.filter(is_active=True, is_featured=True).select_related("category")[:8]
    if not featured:
        featured = Product.objects.filter(is_active=True).select_related("category")[:8]
    latest = Product.objects.filter(is_active=True).select_related("category")[:8]
    return render(request, "core/home.html", {
        "categories": categories, "featured": featured, "latest": latest,
    })
