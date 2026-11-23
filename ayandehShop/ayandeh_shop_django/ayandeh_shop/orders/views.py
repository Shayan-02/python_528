from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from products.models import Product
from cart.cart import Cart
from .forms import OrderCreateForm
from .models import Order, OrderItem

@login_required
def order_create(request):
    cart = Cart(request)
    items = list(cart)
    if not items:
        messages.warning(request, "سبد خرید شما خالی است.")
        return redirect("products:list")

    if request.method == "POST":
        form = OrderCreateForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    order = form.save(commit=False)
                    order.user = request.user
                    order.total_price = 0
                    order.save()
                    total = 0
                    for item in items:
                        product = Product.objects.select_for_update().get(pk=item["product"].pk)
                        quantity = item["quantity"]
                        if quantity < 1 or product.stock < quantity:
                            raise ValueError(f"موجودی {product.name} کافی نیست.")
                        product.stock -= quantity
                        product.save(update_fields=["stock"])
                        OrderItem.objects.create(
                            order=order, product=product,
                            product_name=product.name,
                            price=product.price, quantity=quantity
                        )
                        total += product.price * quantity
                    order.total_price = total
                    order.save(update_fields=["total_price"])
            except (ValueError, Product.DoesNotExist) as exc:
                messages.error(request, str(exc) or "ثبت سفارش انجام نشد.")
                return redirect("cart:detail")
            cart.clear()
            messages.success(request, "سفارش شما با موفقیت ثبت شد.")
            return redirect("orders:detail", order_id=order.id)
    else:
        form = OrderCreateForm()
    return render(request, "orders/create.html", {"form": form, "cart": items})

@login_required
def order_detail(request, order_id):
    order = get_object_or_404(Order.objects.prefetch_related("items"), pk=order_id, user=request.user)
    return render(request, "orders/detail.html", {"order": order})

@login_required
def order_list(request):
    orders = Order.objects.filter(user=request.user)
    return render(request, "orders/list.html", {"orders": orders})
