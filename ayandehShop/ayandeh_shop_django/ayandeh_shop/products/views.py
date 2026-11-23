from django.db.models import Q
from django.shortcuts import get_object_or_404, render
from django.core.paginator import Paginator
from .models import Product, Category

def product_list(request, category_slug=None):
    products = Product.objects.filter(is_active=True).select_related("category")
    categories = Category.objects.filter(is_active=True)
    active_category = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=active_category)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query) |
            Q(description__icontains=query) |
            Q(category__name__icontains=query)
        )

    sort = request.GET.get("sort", "")
    if sort == "price_asc":
        products = products.order_by("price")
    elif sort == "price_desc":
        products = products.order_by("-price")
    elif sort == "newest":
        products = products.order_by("-created_at")

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "products/list.html", {
        "page_obj": page_obj, "categories": categories,
        "active_category": active_category, "query": query, "sort": sort,
    })

def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug, is_active=True
    )
    related = Product.objects.filter(category=product.category, is_active=True).exclude(pk=product.pk)[:4]
    return render(request, "products/detail.html", {"product": product, "related": related})
