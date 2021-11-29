from django.contrib.auth import get_user_model
from django.db.models import query
from django.db.models.base import Model
from django.shortcuts import render
from cafeapp.models import Item, Order
from cafeapp.permissions import IsAdminOrReadOnly, IsOrderOwnerOrReadOnly, IsOwnerOrReadOnly

from cafeapp.serializers import ItemSerializer, OrderSerializer, UserSerializer
from rest_framework import views, response, decorators, parsers, permissions, authentication,filters,generics,status,viewsets

User=get_user_model()
# Create your views here.
class CreateUserAPIView(generics.CreateAPIView):
    queryset =User.objects.all()
    serializer_class = UserSerializer
    def perform_create(self,serializer):
        serializer.save()
class ListUsersAPIView(generics.ListAPIView):
    """list of all users"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['phone','first_name']


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes=[IsOwnerOrReadOnly]
    queryset =User.objects.all()
    serializer_class = UserSerializer
    lookup_field ='id'
    lookup_url_kwarg='pk'

class ItemCreateAPIView(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes=[permissions.IsAdminUser]
    queryset=Item.objects.all()
    serializer_class = ItemSerializer
    def perform_create(self,serializer):
        serializer.save()

class ItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes=[IsAdminOrReadOnly]
    queryset =Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field ='id'
    lookup_url_kwarg='pk'

class ListItemsAPIView(generics.ListAPIView):
    """list of all Items"""
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter,filters.OrderingFilter]
    search_fields = ['name','category']

class createOrderAPIView(generics.CreateAPIView):
    permission_classes=[permissions.IsAuthenticated]
    queryset=Order.objects.all()
    serializer_class = OrderSerializer
    def perform_create(self,serializer):
        serializer.save()

class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes=[IsOrderOwnerOrReadOnly]
    queryset=Order.objects.all()
    serializer_class = ItemSerializer
    lookup_field ='id'
    lookup_url_kwarg='pk'


