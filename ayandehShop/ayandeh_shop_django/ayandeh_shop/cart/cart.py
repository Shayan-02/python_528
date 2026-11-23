from decimal import Decimal
from products.models import Product

class Cart:
    SESSION_KEY = "ayandeh_cart"

    def __init__(self, request):
        self.session = request.session
        self.cart = self.session.get(self.SESSION_KEY, {})

    def add(self, product, quantity=1, override=False):
        product_id = str(product.id)
        if product_id not in self.cart:
            self.cart[product_id] = {"quantity": 0}
        if override:
            self.cart[product_id]["quantity"] = quantity
        else:
            self.cart[product_id]["quantity"] += quantity
        self.cart[product_id]["quantity"] = min(
            max(1, self.cart[product_id]["quantity"]), product.stock
        ) if product.stock else 0
        self.save()

    def remove(self, product):
        self.cart.pop(str(product.id), None)
        self.save()

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def __iter__(self):
        ids = self.cart.keys()
        products = Product.objects.filter(id__in=ids, is_active=True)
        for product in products:
            item = self.cart[str(product.id)]
            quantity = min(item["quantity"], product.stock)
            if quantity < 1:
                continue
            yield {
                "product": product,
                "quantity": quantity,
                "total_price": product.price * quantity,
            }

    def __len__(self):
        return sum(item["quantity"] for item in self.cart.values())

    def get_total_price(self):
        return sum(item["quantity"] * Product.objects.get(pk=int(pid)).price
                   for pid, item in self.cart.items()
                   if Product.objects.filter(pk=int(pid), is_active=True).exists())

    def clear(self):
        self.session.pop(self.SESSION_KEY, None)
        self.session.modified = True
