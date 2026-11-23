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
        self.cart[product_id]["quantity"] = (
            min(max(1, self.cart[product_id]["quantity"]), product.stock)
            if product.stock
            else 0
        )
        self.save()

    def remove(self, product):
        self.remove_id(product.id)

    def remove_id(self, product_id):
        self.cart.pop(str(product_id), None)
        self.save()

    def save(self):
        self.session[self.SESSION_KEY] = self.cart
        self.session.modified = True

    def __iter__(self):
        product_ids = self.cart.keys()
        products = Product.objects.filter(
            id__in=product_ids,
            is_active=True,
            category__is_active=True,
        ).select_related("category")

        for product in products:
            raw_quantity = self.cart.get(str(product.id), {}).get("quantity", 0)
            try:
                quantity = min(max(0, int(raw_quantity)), product.stock)
            except (TypeError, ValueError):
                quantity = 0
            if quantity < 1:
                continue

            unit_price = product.final_price
            yield {
                "product": product,
                "quantity": quantity,
                "unit_price": unit_price,
                "original_unit_price": product.price,
                "discount_amount": product.discount_amount,
                "discount_percent": product.discount_percent,
                "total_price": unit_price * quantity,
            }

    def __len__(self):
        # Count only products that are currently available to the storefront.
        return sum(item["quantity"] for item in self)

    def get_total_price(self):
        return sum(item["total_price"] for item in self)

    def clear(self):
        self.session.pop(self.SESSION_KEY, None)
        self.session.modified = True
