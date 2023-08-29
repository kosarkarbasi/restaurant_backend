from rest_framework.generics import CreateAPIView
from order.models import Order
from order.serializers import OrderSerializer


class OrderCreate(CreateAPIView):
    model = Order
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]
    serializer_class = OrderSerializer
