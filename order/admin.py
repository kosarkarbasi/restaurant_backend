from django.contrib import admin

from order.models import OrderItem, Order, Payment


# Register your models here.
class PaymentInline(admin.TabularInline):
    model = Payment


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ['food', 'quantity', ]


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ['date', ]
    inlines = [PaymentInline, ]
