from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Food(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='foods/', null=True, blank=True)
    category = models.ManyToManyField(Category, blank=True)
    price = models.BigIntegerField()
    description = models.TextField()
    available = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.name} - {self.price if self.available else "not available"}'


class Menu(models.Model):
    date = models.DateTimeField()
    total_price = models.FloatField()
