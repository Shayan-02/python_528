from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST

from products.models import Product
from .cart import Cart


def cart_detail(request):
    cart = Cart(request)
    return render(request, "cart/detail.html", {"cart": cart})


@require_POST
def cart_add(request, product_id):
    product = get_object_or_404(
        Product,
        id=product_id,
        is_active=True,
        category__is_active=True,
    )
    try:
        quantity = int(request.POST.get("quantity", 1))
    except (TypeError, ValueError):
        quantity = 1

    if product.stock < 1:
        messages.error(request, "این محصول در حال حاضر ناموجود است.")
    else:
        Cart(request).add(product, max(1, quantity))
        messages.success(request, "محصول به سبد خرید اضافه شد.")
    return redirect("cart:detail")


@require_POST
def cart_remove(request, product_id):
    Cart(request).remove_id(product_id)
    messages.info(request, "محصول از سبد خرید حذف شد.")
    return redirect("cart:detail")
