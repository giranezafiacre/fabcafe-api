from django.contrib.auth import get_user_model
from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer

from cafeapp.models import Item, Order

User = get_user_model()


class UserSerializer(ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)

    class Meta:
        model = User
        fields = ('phone', 'first_name', 'last_name', 'password', 'image')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(
            validated_data['phone'], validated_data['first_name'], validated_data['last_name'], validated_data['password'])

        return user


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"


class OrderSerializer(ModelSerializer):
    class Meta:
        model = Order
        fields = ('items', 'delivery_time')
