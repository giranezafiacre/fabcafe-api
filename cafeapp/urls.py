from django.contrib import admin
from django.urls import path, include
from cafeapp.views import (CreateUserAPIView, HistorRecordsAPIView, ItemCreateAPIView,
                           ItemDetailAPIView, ListItemsAPIView, ListOrdersAPIView, ListTableAPIView,
                           ListUsersAPIView, OrderDetailAPIView, OrderItemDetailAPIView, PlaceOrderAPIView, UserDetailAPIView, UserView, addTableAPIView, cleanOrdersAPIView,
                           createOrderItemAPIView, pay_by_MoMoAPI, payment_response, tableDetail, verify_Payment, viewUserOrderAPIView)
urlpatterns = [
    path('register/', CreateUserAPIView.as_view(), name='register'),
    path('auth/', include('rest_auth.urls')),
    path('user/<int:pk>/', UserDetailAPIView.as_view(), name='user-detail'),
    path('users/', ListUsersAPIView.as_view(), name='all-users'),
    path('get-logged-in-user/', UserView.as_view(), name='current_user'),
    path('item/', ItemCreateAPIView.as_view(), name='create-item'),
    path('item/<int:pk>/', ItemDetailAPIView.as_view(), name='item-detail'),
    path('items/', ListItemsAPIView.as_view(), name='all-items'),
    path('add-to-cart/', createOrderItemAPIView.as_view(), name='add-item'),
    path('change-order-item/<int:pk>/',
         OrderItemDetailAPIView.as_view(), name='change-order-item'),
    path('view-my-order/', viewUserOrderAPIView.as_view(), name='view-my-order'),
    path('place-order/', PlaceOrderAPIView.as_view(), name='order-detail'),
    path('order/<int:pk>/', OrderDetailAPIView.as_view(), name='order-detail'),
    path('pay-order/', pay_by_MoMoAPI.as_view(), name='pay_with_MoMo'),
    path('orders/', ListOrdersAPIView.as_view(), name='list orders'),
    path('verify-payment/', verify_Payment.as_view(), name='pay_with_MoMo'),
    path('clean-orders/<str:paid>/',
         cleanOrdersAPIView.as_view(), name='clean-orders'),
    path('historical-records/', HistorRecordsAPIView.as_view(), name='historic'),
    path('add-table/', addTableAPIView.as_view(), name='add-table'),
    path('view-tables/', ListTableAPIView.as_view(), name='list-tables'),
    path('table-detail/<int:pk>/', tableDetail.as_view(), name='table-detail'),
    path('callback/', payment_response, name='payment_response')
]
