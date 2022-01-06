import base64
from datetime import datetime
from django.contrib.auth import get_user_model
from django.http.response import FileResponse
from cafeapp.models import Item, Order, OrderItem, Table, Transaction
from cafeapp.permissions import IsAdminOrReadOnly, IsOrderItemOwner, IsOrderOwnerOrReadOnly, IsOwnerOrReadOnly
from cafeapp.process_payment import process_payment, verify_payment
from cafeapp.serializers import ItemSerializer, OrderItemSerializer, OrderSerializer, UserSerializer, tableSerializers
from rest_framework import views, response, permissions, authentication, filters, generics, status
from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view
import json

User = get_user_model()
# Create your views here.


class CreateUserAPIView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save()


class ListUsersAPIView(generics.ListAPIView):
    """list of all users"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['phone', 'fullname']


class UserDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOwnerOrReadOnly, permissions.IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'


class UserView(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = UserSerializer
    def get(self, request):
        user = request.user
        return response.Response({
            'id':user.id,
            'fullname': user.fullname,
            'image': user.image.url,
            'staff':user.staff,
        })


class ItemCreateAPIView(generics.CreateAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer

    def perform_create(self, serializer):
        serializer.save()


class ItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsAdminOrReadOnly]
    queryset = Item.objects.all()
    serializer_class = ItemSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'


class ListItemsAPIView(generics.ListAPIView):
    """list of all Items"""
    queryset = Item.objects.filter(quantity__gt=0)
    serializer_class = ItemSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['name', 'category']
    paginate_by = 12


class ListOrdersAPIView(generics.ListAPIView):
    """list of all Items"""
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['user', 'item', 'order_time_date']


class createOrderItemAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer

    def perform_create(self, serializer):
        serializer.save()


class OrderItemDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOrderItemOwner, permissions.IsAuthenticated]
    queryset = OrderItem.objects.all()
    serializer_class = OrderItemSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'


class viewUserOrderAPIView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = OrderItemSerializer

    def get_queryset(self):
        return OrderItem.objects.filter(cart__user=self.request.user)
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ['item', 'price']

class PlaceOrderAPIView(views.APIView):
   authentication_classes = [authentication.TokenAuthentication]
   permission_classes = [permissions.IsAuthenticated]
   queryset = Order.objects.all()
   def get(self,request):
       if(Order.objects.filter(user=request.user, paid=False)):
           order = Order.objects.filter(
                    user=request.user, paid=False)[0]
           serializer = OrderSerializer(instance=order)
           return response.Response(serializer.data)
       else:
            return response.Response(data={"no order available"},status=status.HTTP_204_NO_CONTENT)

   def put(self,request):
       if(Order.objects.filter(user=request.user, paid=False)):
            
            if not 'delivery_time' in request.data:
               return response.Response(data={"please specify delivery time"},status=status.HTTP_400_BAD_REQUEST) 

            order = Order.objects.filter(
                    user=request.user, paid=False)[0]
            order.ordered=True
            orderItems = OrderItem.objects.filter(cart=order)
            sum = 0
            for orderItem in orderItems:
                    price = orderItem.item.price*orderItem.quantity
                    sum += price
            order.totalPay = sum
            serializer = OrderSerializer(
                instance=order, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return response.Response(serializer.data)
       else:
            return response.Response(data={"this order may be ordered or paid arleady"},status=status.HTTP_208_ALREADY_REPORTED)



class OrderDetailAPIView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [IsOrderOwnerOrReadOnly]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'

    def update(self, request, *args, **kwargs):
        object_id = int(
            [i for i in str(self.request.path).split('/') if i][-1])
        order = get_object_or_404(Order, id=object_id)
        order.ordered=True
        order.delivery_time=self.request.data.get('delivery_time')
        orderItems = OrderItem.objects.filter(cart=order)
        sum = 0
        for orderItem in orderItems:
            price = orderItem.item.price*orderItem.quantity
            sum += price
        order.totalPay = sum
        if order.ordered == True and order.paid == True:
            return response.Response(data={'this order has already been paid'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer = self.get_serializer(
                instance=order, data=self.request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_update(serializer)

            return response.Response(serializer.data)


class cleanOrdersAPIView(generics.DestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.filter(paid=True)
    serializer_class = OrderSerializer(many=True)

    def delete(self, request, *args, **kwargs):
        selectOrders = Order.objects.filter(paid=bool(kwargs['paid']))
        if selectOrders.count() > 0:
            selectOrders.delete()
            return response.Response("deleted", status=status.HTTP_204_NO_CONTENT)
        return response.Response("Unable to find any order paid.", status=status.HTTP_404_NOT_FOUND)


class HistorRecordsAPIView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['order_time_date']


class pay_by_MoMoAPI(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    order = None

    def get(self, request):
        user = request.user
        if(Order.objects.filter(user=user, paid=False, ordered=True)):
            order = Order.objects.filter(user=user, paid=False)[0]
            data = process_payment(order.totalPay, user.phone, user.fullname)
            print(data)
            if(data['status'] == 'success'):
                return response.Response(data=data)
            else:
                return response.Response(data={"there is some errors retry later"})
        else:
            return response.Response(data={"you have not placed order for this order"}, status=status.HTTP_404_NOT_FOUND)


class verify_Payment(views.APIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]

    def post(self, request):
        # print('hi',request.POST['phone'])
        data = request.POST
        if not 'phone' in data:
            return response.Response(data={'please enter phone field'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            user = get_object_or_404(User, phone=request.POST['phone'])
            if(Order.objects.filter(user=user, paid=False)):
                order = Order.objects.filter(user=user, paid=False)[0]
                if 'flwref' in request.POST:
                    data = verify_payment(request.POST['flwref'])
                    if data['status'] == 'success':
                        if data['data']['amount'] == order.totalPay:
                            order.paid = True
                            order.save()
                            return response.Response(data=data, status=status.HTTP_200_OK)
                        return response.Response(data={'you did not pay the exact amount of order'}, status=status.HTTP_200_OK)
                    else:
                        return response.Response(data=data, status=status.HTTP_404_NOT_FOUND)
                else:
                    return response.Response(data={'message': "please fill payment"}, status=status.HTTP_400_BAD_REQUEST)


class addTableAPIView(generics.CreateAPIView):
    permission_classes = [permissions.IsAuthenticated]
    queryset = Table.objects.all()
    serializer_class = tableSerializers
     
    def perform_create(self, serializer):
        serializer.save(reserved_by=self.request.user)


class tableDetail(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAuthenticated, IsAdminOrReadOnly]
    queryset = Table.objects.all()
    serializer_class = tableSerializers
    lookup_field = 'id'
    lookup_url_kwarg = 'pk'


class ListTableAPIView(generics.ListAPIView):
    authentication_classes = [authentication.TokenAuthentication]
    permission_classes = [permissions.IsAdminUser]
    serializer_class = tableSerializers
    queryset = Table.objects.all()
    filter_backends = [filters.SearchFilter]
    search_fields = ['requested_on']

class ListUserTableAPIView(generics.ListAPIView):
    authentication_classes = [authentication.SessionAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = tableSerializers
    queryset = Table.objects.all()
    def get(self, request, *args, **kwargs):
        data=Table.objects.filter(reserved_by=self.request.user)
        return response

@api_view(['POST'])
def payment_response(request):
    if request.method == 'POST':
        request_json = json.loads(request.body)
        if request_json['status'] == 'successful':
            user = get_object_or_404(
                User, phone=request_json['customer']['phone'])
            if(Order.objects.filter(user=user, paid=False)):
                order = Order.objects.filter(user=user, paid=False)[0]
                # Transaction.objects.create()
                if order.totalPay == request_json['amount']:
                    order.paid = True
                    order.save()
                print(request_json, '\n___________________\norder:', order.paid)
        print(request_json)
        return response.Response(data=request_json, status=status.HTTP_200_OK)
