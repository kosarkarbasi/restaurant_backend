from django.urls import path
import authentication.views as views

app_name = 'authentication'
urlpatterns = [
    path('users/signup/', views.RegistrationAPIView.as_view()),
    path('users/login/', views.LoginAPIView.as_view()),
    path('user/', views.UserRetrieveUpdateAPIView.as_view()),
    path('users/all/', views.UserList.as_view()),
    path('user/exist/', views.check_user_existence),

    path('address/create/', views.AddressCreate.as_view()),
    path('city/all/', views.CityList.as_view()),
    path('region/all/', views.RegionList.as_view()),
]
