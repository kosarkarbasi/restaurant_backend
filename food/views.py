from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView

from food.models import Food, Category
from food.serializers import FoodSerializer, CategorySerializer


class FoodCreate(CreateAPIView):
    model = Food
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]
    serializer_class = FoodSerializer


class FoodList(ListAPIView):
    model = Food
    queryset = Food.objects.all()
    serializer_class = FoodSerializer


class FoodEdit(UpdateAPIView):
    model = Food
    queryset = Food.objects.all()
    serializer_class = FoodSerializer
    lookup_field = 'pk'


class CategoryCreate(CreateAPIView):
    model = Category
    # permission_classes = [
    #     permissions.IsAuthenticated
    # ]
    serializer_class = CategorySerializer


class CategoryList(ListAPIView):
    model = Category
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
