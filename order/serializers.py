from rest_framework import serializers
from food.models import Food
from order.models import Order, OrderItem, Payment


class PaymentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Payment
        fields = ['status', 'bank_gateway']


class OrderItemSerializer(serializers.ModelSerializer):
    food = serializers.SlugRelatedField(slug_field='name', queryset=Food.objects.all())

    class Meta:
        model = OrderItem
        fields = ['food', 'quantity']

    def create(self, validated_data):
        foods = validated_data.get('food')
        order_item = super().create(validated_data)
        order_item.food.set(foods)
        return order_item


class OrderSerializer(serializers.ModelSerializer):
    order_items = OrderItemSerializer(many=True)  # 🖘 use the OrderItemSerializer directly
    payments = PaymentSerializer()

    def create(self, validated_data):
        items_data = validated_data.pop('order_items')
        checkouts_data = validated_data.pop('payments')
        order = Order.objects.create(**validated_data)
        if not order.payments.filter(status='success').exists():
            order.payments.create(order=order, **checkouts_data)
        else:
            raise serializers.ValidationError('noch noch noch...')
        for item_data in items_data:
            OrderItem.objects.create(order=order, **item_data)

        return order

    class Meta:
        model = Order
        fields = ['description',
                  'delivery_type',
                  'address',
                  'discount_code',
                  'date',
                  'order_items',
                  'payments']
