from django.core.paginator import Paginator
from django.db.models import BigIntegerField, ExpressionWrapper, F, Q, Value
from django.shortcuts import get_object_or_404, render

from .models import Category, Product


def product_list(request, category_slug=None):
    # A product is public only when both it and its category are active.
    products = Product.objects.filter(
        is_active=True,
        category__is_active=True,
    ).select_related("category")
    categories = Category.objects.filter(is_active=True)
    active_category = None

    if category_slug:
        active_category = get_object_or_404(Category, slug=category_slug, is_active=True)
        products = products.filter(category=active_category)

    query = request.GET.get("q", "").strip()
    if query:
        products = products.filter(
            Q(name__icontains=query)
            | Q(description__icontains=query)
            | Q(category__name__icontains=query)
        )

    # Sort by the actual payable price, not the pre-discount price.
    products = products.annotate(
        _sale_price=ExpressionWrapper(
            F("price") - (F("price") * F("discount_percent") / Value(100)),
            output_field=BigIntegerField(),
        )
    )
    # Optional storefront filters. The range is applied to the payable price
    # after discount, matching the price customers see on product cards.
    min_price_raw = request.GET.get("min_price", "").strip()
    max_price_raw = request.GET.get("max_price", "").strip()
    min_price = int(min_price_raw) if min_price_raw.isdigit() else None
    max_price = int(max_price_raw) if max_price_raw.isdigit() else None

    if min_price is not None:
        products = products.filter(_sale_price__gte=min_price)
    if max_price is not None:
        products = products.filter(_sale_price__lte=max_price)

    discounted_only = request.GET.get("discounted") == "1"
    in_stock_only = request.GET.get("in_stock") == "1"
    if discounted_only:
        products = products.filter(discount_percent__gt=0).exclude(_sale_price=F("price"))
    if in_stock_only:
        products = products.filter(stock__gte=1)

    sort = request.GET.get("sort", "")
    if sort == "price_asc":
        products = products.order_by("_sale_price", "price")
    elif sort == "price_desc":
        products = products.order_by("-_sale_price", "-price")
    elif sort == "newest":
        products = products.order_by("-created_at")

    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    # Preserve active search, sorting and filters when moving between pages.
    pagination_params = request.GET.copy()
    pagination_params.pop("page", None)
    pagination_query = pagination_params.urlencode()

    return render(
        request,
        "products/list.html",
        {
            "page_obj": page_obj,
            "categories": categories,
            "active_category": active_category,
            "query": query,
            "sort": sort,
            "min_price": min_price_raw,
            "max_price": max_price_raw,
            "discounted_only": discounted_only,
            "in_stock_only": in_stock_only,
            "pagination_query": pagination_query,
        },
    )


def product_detail(request, slug):
    product = get_object_or_404(
        Product.objects.select_related("category"),
        slug=slug,
        is_active=True,
        category__is_active=True,
    )
    related = (
        Product.objects.filter(
            category=product.category,
            is_active=True,
            category__is_active=True,
        )
        .exclude(pk=product.pk)[:4]
    )
    return render(request, "products/detail.html", {"product": product, "related": related})
