from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer
from rest_framework import status
from rest_framework.response import Response


class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer

    class Meta:
        model = OrderItem
        fields = ["product", "quantity"]
        read_only_fields = ["price"]


class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Order
        fields = ["total_price", "status", "created_at", "items"]
        read_only_fields = ["total_price", "status", "created_at"]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        total_price = 0
        for item in items_data:
            total_price += item["product"].price * item["quantity"]
        order = Order.objects.create(
            user=self.context["request"].user, total_price=total_price
        )
        print(len(items_data))
        for item_data in items_data:
            item_data["price"] = item_data["product"].price * item_data["quantity"]
            item_data["product"] = item_data["product"].pk
            item = OrderItemSerializer(data=item_data)
            if item.is_valid():
                item.save(order=order)
            else:
                return Response(item.errors, status=status.HTTP_400_BAD_REQUEST)
        return order
