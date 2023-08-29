from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from authentication.models import User, Address, City, Region


class AddressInline(admin.TabularInline):
    model = Address


class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    # form = UserChangeForm
    # add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["phone_number", "email", "type", ]
    # list_filter = ["is_admin"]
    fieldsets = [
        (None, {"fields": ["type", "phone_number", "email", "password"]}),
        ("settings", {"fields": ['discount_code']}),
        ("Permissions", {"fields": ["is_active"]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["email", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["email", "phone_number", ]
    ordering = ["email"]
    filter_horizontal = []
    inlines = [AddressInline]


# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
admin.site.unregister(Group)


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ['name', 'city']


@admin.register(Address)
class AddressAdmin(admin.ModelAdmin):
    list_display = ['region', 'city', 'full_address', 'active', 'user']
