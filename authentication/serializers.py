from django.contrib.auth import authenticate
from phonenumber_field.serializerfields import PhoneNumberField
from rest_framework import serializers
from authentication.models import User, Address, City, Region


class RegistrationSerializer(serializers.ModelSerializer):
    """Serializers registration requests and creates a new user."""

    # Ensure passwords are at least 8 characters long, no longer than 128
    # characters, and can not be read by the client.
    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    # The client should not be able to send a token along with a registration
    # request. Making `token` read-only handles that for us.
    token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        # List all the fields that could possibly be included in a request
        # or response, including fields specified explicitly above.
        fields = ['email', 'phone_number', 'password', 'token', 'type']

    def create(self, validated_data):
        # Use the `create_user` method we wrote earlier to create a new user.
        return User.objects.create_user(**validated_data)


class LoginSerializer(serializers.Serializer):
    phone_number = PhoneNumberField(max_length=255)
    email = serializers.CharField(max_length=255, read_only=True)
    password = serializers.CharField(max_length=128, write_only=True)
    token = serializers.CharField(max_length=255, read_only=True)
    address = serializers.CharField(max_length=1000, read_only=True)

    def validate(self, data):
        phone_number = data.get('phone_number', None)
        password = data.get('password', None)

        if phone_number is None:
            raise serializers.ValidationError(
                'A phone_number is required to log in.'
            )

        if password is None:
            raise serializers.ValidationError(
                'A password is required to log in.'
            )

        user = authenticate(username=phone_number, password=password)

        if user is None:
            raise serializers.ValidationError(
                'A user with this phone number and password was not found.'
            )

        if not user.is_active:
            raise serializers.ValidationError(
                'This user has been deactivated.'
            )

        return {
            'phone_number': phone_number,
            'email': user.email,
            'token': user.token,
            'address': list({'pk': address.pk, 'address': address.complete_address, 'active': f'{address.active}'}
                            for address in Address.objects.filter(user=user)),
        }


class UserSerializer(serializers.ModelSerializer):
    """Handles serialization and deserialization of User objects."""

    password = serializers.CharField(
        max_length=128,
        min_length=8,
        write_only=True
    )

    class Meta:
        model = User
        fields = ('email', 'phone_number', 'address', 'password', 'token',)
        read_only_fields = ('token',)

    def update(self, instance, validated_data):
        """Performs an update on a User."""
        password = validated_data.pop('password', None)

        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance


class AddressSerializer(serializers.ModelSerializer):
    city = serializers.SlugRelatedField(slug_field='name', queryset=City.objects.all())
    region = serializers.SlugRelatedField(slug_field='name', queryset=Region.objects.all())
    user = serializers.SlugRelatedField(slug_field='phone_number', queryset=User.objects.all())

    class Meta:
        model = Address
        fields = ['city', 'region', 'full_address', 'active', 'user']

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data['user'] = str(instance.user)
        return data


class CitySerializer(serializers.ModelSerializer):
    class Meta:
        model = City
        fields = '__all__'


class RegionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Region
        fields = '__all__'
