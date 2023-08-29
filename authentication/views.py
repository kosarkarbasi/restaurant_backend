from django.http import JsonResponse
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveUpdateAPIView, ListCreateAPIView, CreateAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from authentication.models import User, Address, City, Region
from authentication.renderers import UserJSONRenderer
from authentication.serializers import RegistrationSerializer, LoginSerializer, UserSerializer, AddressSerializer, \
    CitySerializer, RegionSerializer


class RegistrationAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = RegistrationSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_201_CREATED)


class LoginAPIView(APIView):
    permission_classes = (AllowAny,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = LoginSerializer

    def post(self, request):
        user = request.data.get('user', {})
        serializer = self.serializer_class(data=user)
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated,)
    renderer_classes = (UserJSONRenderer,)
    serializer_class = UserSerializer

    def retrieve(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = self.serializer_class(
            request.user, data=serializer_data, partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)


class UserList(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class CityList(ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class RegionList(ListCreateAPIView):
    queryset = Region.objects.all()
    serializer_class = RegionSerializer


class AddressCreate(CreateAPIView):
    model = Address
    serializer_class = AddressSerializer


def check_user_existence(request):
    if request.method == 'POST':
        phone_number = request.POST.get('phone_number')
        if phone_number:
            existence = User.objects.filter(phone_number=phone_number).exists()
            return JsonResponse({'existence': existence}, status=status.HTTP_200_OK, safe=False)
