# services.py
from .models import Order, OrderItem
from products.models import Product


def create_order(data):
    order = Order.objects.create(user=data["user"], total_price=0)
    for item in data["items"]:
        order_item = OrderItem.objects.create(
            order=order,
            product=Product.objects.get(id=item["product"]),
            quantity=item["quantity"],
            price=item["product"].price * item["quantity"],
        )
        order.total_price += item["product"].price * item["quantity"]
    order.save()
    return order
