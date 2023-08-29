from django.db import models

from authentication.models import User
from food.models import Food


class Order(models.Model):
    DELIVERY_TYPES = (('send', 'send'), ('onPerson', 'onPerson'))

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    description = models.TextField()
    delivery_type = models.CharField(choices=DELIVERY_TYPES, max_length=8)
    address = models.TextField()
    discount_code = models.CharField(null=True, blank=True, max_length=50)
    date = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='order_items')
    food = models.ForeignKey(Food, on_delete=models.CASCADE, related_name='items')
    quantity = models.IntegerField()

    @property
    def price(self):
        return self.food.price * self.quantity


class Payment(models.Model):
    PAYMENT_STATUSES = (('success', 'success'), ('fail', 'fail'), ('loading', 'loading'))
    BANKS = (('saman', 'saman'), ('parsian', 'parsian'))
    PAYMENT_METHODS = (('online', 'online'), ('cash', 'cash'), ('cardReader', 'cardReader'))

    method = models.CharField(choices=PAYMENT_METHODS, max_length=10)
    status = models.CharField(choices=PAYMENT_STATUSES, max_length=7, null=True, blank=True)
    bank_gateway = models.CharField(choices=BANKS, max_length=7, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='payments')

