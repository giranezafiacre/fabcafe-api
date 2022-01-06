from datetime import datetime
from django.contrib.auth import get_user_model
from django.db import models
from django.db.models import fields
from rest_framework import serializers
from rest_framework.serializers import ModelSerializer, Serializer

from cafeapp.models import Item, Order, OrderItem, Table
import datetime

User = get_user_model()



class OrderItemSerializer(ModelSerializer):
    item_name = serializers.CharField(source='item.name', read_only=True)
    item_image=serializers.ImageField(source='item.image', read_only=True)
    item_description=serializers.CharField(source='item.description', read_only=True)
    class Meta:
        model = OrderItem
        fields = ('id','item', 'item_name','item_image', 'price', 'quantity','item_description','availability')

    def create(self, validated_data):
        """create a new user"""

        item = validated_data['item']
        quantity = validated_data['quantity']

        try:
            request = self.context.get('request', None)
            if(Order.objects.filter(user=request.user, paid=False)):
                search_order = Order.objects.filter(
                    user=request.user, paid=False)[0]
                item = Item.objects.get(id=item.id)
                item.quantity -= quantity
                item.save()
                totalPay = item.price * quantity
                totalPay += search_order.totalPay
                search_order.totalPay = totalPay
                search_order.save()
                order_item = OrderItem.objects.create(
                    cart=search_order,
                    item=item,
                    quantity=quantity)
                return order_item

            else:
                item = Item.objects.get(id=item.id)
                totalPay = item.price * quantity
                new_order = Order.objects.create(user=request.user,
                                                 delivery_time=datetime.datetime.now(), totalPay=totalPay)
                order_item = OrderItem.objects.create(
                    cart=new_order,
                    item=item,
                    quantity=quantity)
                return order_item

        except Exception as e:
            error = {'message': ",".join(e.args) if len(
                e.args) > 0 else 'Unknown Error'}
            raise serializers.ValidationError(error)


class OrderSerializer(ModelSerializer):
    ordered_items = OrderItemSerializer(many=True,read_only=True)
    username=serializers.CharField(source='user.fullname', read_only=True)
    class Meta:
        model = Order
        fields = ['id', 'username', 'totalPay', 'delivery_time','paid', 'order_time_date','ordered','delivered','ordered_items',]

    
    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError({
    'delivery_time_error':"You have to specify delivery time"})
        time =attrs['delivery_time']
        if datetime.datetime.now().time() > time:
            raise serializers.ValidationError({
    'delivery_time_error':"You have to specify time later than now"})
        return super().validate(attrs)

    def update(self, instance, validated_data):
        instance.ordered=True
        print(validated_data)
        instance.save()
        return instance

class UserSerializer(ModelSerializer):
    password = serializers.CharField(
        style={'input_type': 'password'}, write_only=True)
    image = serializers.ImageField(default='../static/img/anonymous.jpg')
    order=OrderSerializer(many=True, read_only=True)
    class Meta:
        model = User
        fields = ('id','phone', 'fullname', 'password', 'image','order','trustworthy','staff')
        extra_kwargs = {'password': {'write_only': True},'trustworthy': {'read_only': True},'staff': {'read_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)            

        return user


class ItemSerializer(ModelSerializer):
    class Meta:
        model = Item
        fields = "__all__"

class tableSerializers(ModelSerializer):
    username=serializers.CharField(source='reserved_by.fullname', read_only=True)
    time_needed = models.DateTimeField(auto_now_add=False)
    time_needed = serializers.DateTimeField(format=None,input_formats=['%Y-%m-%dT%H:%M:%SZ',])
    class Meta:
       model = Table
       fields = ['id','number_of_persons','reserved_by','availability','requested_on','time_needed','username']
    def validate(self, attrs):
        if not attrs:
            raise serializers.ValidationError({
    'delivery_time_error':"You have to specify delivery time"})
        time =attrs['time_needed']
        from django.utils import timezone
        now = timezone.now()
        if now > time:
            raise serializers.ValidationError({
    'delivery_time_error':"You have to specify time later than now"})
        return super().validate(attrs)
