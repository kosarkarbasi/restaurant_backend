import jwt
from datetime import datetime, timedelta
from django.conf import settings
from django.contrib.auth.models import (AbstractBaseUser, PermissionsMixin)
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from smart_selects.db_fields import ChainedForeignKey
from authentication.managers import UserManager


class DiscountCode(models.Model):
    DISCOUNT_TYPES = (('percent', 'percent'), ('cash', 'cash'))
    code = models.CharField(max_length=50)
    type = models.CharField(choices=DISCOUNT_TYPES, max_length=7)


class User(AbstractBaseUser, PermissionsMixin):
    class Type(models.TextChoices):
        CUSTOMER = 'CUSTOMER', 'Customer'
        PERSONNEL = 'PERSONNEL', 'Personnel'
        ADMIN = 'ADMIN', 'Admin'

    type = models.CharField(max_length=50, choices=Type.choices)
    email = models.EmailField(unique=True, null=True, blank=True)
    phone_number = PhoneNumberField(db_index=True, unique=True)
    discount_code = models.ForeignKey(DiscountCode, on_delete=models.CASCADE, null=True, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    # The `USERNAME_FIELD` property tells us which field we will use to log in.
    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    objects = UserManager()

    def __str__(self):
        """
        Returns a string representation of this `User`.

        This string is used when a `User` is printed in the console.
        """
        return str(self.phone_number)

    @property
    def token(self):
        """
        Allows us to get a user's token by calling `user.token` instead of
        `user.generate_jwt_token().

        The `@property` decorator above makes this possible. `token` is called
        a "dynamic property".
        """
        return self._generate_jwt_token()

    def _generate_jwt_token(self):
        """
        Generates a JSON Web Token that stores this user's ID and has an expiry
        date set to 60 days into the future.
        """
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode({
            'id': self.pk,
            'exp': int(dt.strftime('%s'))
        }, settings.SECRET_KEY, algorithm='HS256')

        # return token.decode('utf-8')
        return token


# -------------- managers

class CustomerManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.CUSTOMER)


class PersonnelManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.PERSONNEL)


class AdminManager(models.Manager):
    def get_queryset(self, *args, **kwargs):
        return super().get_queryset(*args, **kwargs).filter(type=User.Type.ADMIN)


# -------------- end managers


class Customer(User):
    base_type = User.Type.CUSTOMER
    objects = CustomerManager()

    class Meta:
        proxy = True
        verbose_name = 'مشتری'
        verbose_name_plural = 'مشتری ها'

    def save(self, *args, **kwargs):
        """
        متد سیو اورراید شده است که هر دفعه نیازی نباشد type را برای یوزرها تعریف کنیم
        """
        if not self.pk:
            self.type = User.Type.CUSTOMER
        return super().save(*args, **kwargs)


class Personnel(User):
    # is_staff = models.BooleanField(default=True)
    base_type = User.Type.PERSONNEL
    objects = PersonnelManager()

    class Meta:
        proxy = True
        # permissions = ('product.add_book',)
        verbose_name = 'کارمند'
        verbose_name_plural = 'کارمندها'

    def save(self, *args, **kwargs):
        """
        متد سیو اورراید شده است که هر دفعه نیازی نباشد type را برای یوزرها تعریف کنیم
        """
        if not self.pk:
            self.type = User.Type.PERSONNEL
        return super().save(*args, **kwargs)


class Admin(User):
    base_type = User.Type.ADMIN
    objects = AdminManager()

    class Meta:
        proxy = True
        verbose_name = 'ادمین'
        verbose_name_plural = 'ادمین ها'

    def save(self, *args, **kwargs):
        """
        متد سیو اورراید شده است که هر دفعه نیازی نباشد type را برای یوزرها تعریف کنیم
        """
        if not self.pk:
            self.type = User.Type.ADMIN
        return super().save(*args, **kwargs)


# -------------- Address Models

class City(models.Model):
    id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=30, unique=True)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Region(models.Model):
    name = models.CharField(max_length=20)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    slug = models.SlugField()

    def __str__(self):
        return self.name


class Address(models.Model):
    """
    مدل آدرس کاربر
    City: شهر
    Region: محله
    full_address: آدرس کامل
    active: اکتیوبودن یا نبودن : True/false
    """

    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, related_name='addresses')
    region = ChainedForeignKey(Region,
                               chained_field="city",
                               chained_model_field="city",
                               show_all=False,
                               auto_choose=True,
                               sort=True,
                               on_delete=models.SET_NULL,
                               null=True)
    full_address = models.TextField(max_length=200)
    active = models.BooleanField(default=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    @property
    def complete_address(self):
        return f'{self.city} - {self.region} - {self.full_address}'

    def __str__(self):
        return f'{self.city} - {self.region} - {self.full_address}'
