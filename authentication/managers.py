from django.contrib.auth.base_user import BaseUserManager


class UserManager(BaseUserManager):
    """
    Django requires that custom users define their own Manager class. By
    inheriting from `BaseUserManager`, we get a lot of the same code used by
    Django to create a `User`.

    All we have to do is override the `create_user` function which we will use
    to create `User` objects.
    """

    def create_user(self, phone_number, type, email=None, password=None):
        """Create and return a `User` with a phone number and password."""
        if phone_number is None:
            raise TypeError('Users must have a phone number.')

        user = self.model(type=type, phone_number=phone_number, email=email)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, phone_number, email, password):
        """
        Create and return a `User` with superuser (admin) permissions.
        """

        if phone_number is None:
            raise TypeError('Users must have a phone number.')

        if email is None:
            raise TypeError('Users must have an email address.')

        if password is None:
            raise TypeError('Superusers must have a password.')

        user = self.create_user(phone_number=phone_number, email=email, password=password,
                                type="ADMIN")
        user.is_superuser = True
        user.is_staff = True
        user.save()

        return user
