from django.urls import path
import order.views as views

urlpatterns = [
    path('order/create/', views.OrderCreate.as_view()),
]