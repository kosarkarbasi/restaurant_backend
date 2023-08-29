import json

from rest_framework import serializers

from food.models import Category, Food


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class FoodSerializer(serializers.ModelSerializer):
    category = serializers.SlugRelatedField(slug_field='name', queryset=Category.objects.all(), many=True)

    class Meta:
        model = Food
        fields = ['id', 'name', 'price', 'description', 'available', 'category', 'image']

    def create(self, validated_data):
        categories = validated_data.get('category')
        food = super().create(validated_data)
        food.category.set(categories)
        return food
