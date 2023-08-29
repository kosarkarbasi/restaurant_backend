from django.contrib import admin
from food.models import Category, Food, Menu


# Register your models here.
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", ]


@admin.register(Food)
class FoodAdmin(admin.ModelAdmin):
    list_display = ["name", "price", "description", "available"]


@admin.register(Menu)
class MenuAdmin(admin.ModelAdmin):
    list_display = ["date", "total_price"]
