from django.urls import path, include
import food.views as views

urlpatterns = [
    path('food/add/', views.FoodCreate.as_view()),
    path('food/all/', views.FoodList.as_view()),
    path('food/edit/<int:pk>', views.FoodEdit.as_view()),
    path('category/add/', views.CategoryCreate.as_view()),
    path('category/all/', views.CategoryList.as_view()),
]
