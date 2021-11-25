from django.contrib import admin
from django.urls import path,include

from cafeapp.views import CreateUserAPIView, LoginUserAPIView

urlpatterns = [
    path('register/', CreateUserAPIView.as_view(),name='register'),
    path('auth/', include('rest_auth.urls')), 
]
