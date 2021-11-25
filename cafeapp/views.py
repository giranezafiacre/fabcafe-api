from django.contrib.auth import get_user_model
from django.db.models.base import Model
from django.shortcuts import render

from cafeapp.serializers import UserSerializer
from rest_framework import views, response, decorators, parsers, permissions, authentication,filters,generics,status,viewsets

User=get_user_model()
# Create your views here.
class CreateUserAPIView(generics.CreateAPIView):
    serializer_class = UserSerializer
    # permission_classes = [permissions.AllowAny]
    def perform_create(self,serializer):
        serializer.save()

class LoginUserAPIView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]
    queryset = User.objects.all()
