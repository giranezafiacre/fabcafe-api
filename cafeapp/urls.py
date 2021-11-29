from django.contrib import admin
from django.urls import path,include


from cafeapp.views import CreateUserAPIView, ItemCreateAPIView, ItemDetailAPIView, ListItemsAPIView, ListUsersAPIView, OrderDetailAPIView, UserDetailAPIView, createOrderAPIView
urlpatterns = [
    path('register/', CreateUserAPIView.as_view(),name='register'),
    path('auth/', include('rest_auth.urls')), 
    path('user/<int:pk>/',UserDetailAPIView.as_view(),name='user-detail'),
    path('users',ListUsersAPIView.as_view(),name='all-users'),
    path('item/',ItemCreateAPIView.as_view(),name='create-item'),
    path('item/<int:pk>/',ItemDetailAPIView.as_view(),name='item-detail'),
    path('items/',ListItemsAPIView.as_view(),name='all-items'),
    path('order/',createOrderAPIView.as_view(),name='create-item'),
    path('order/<int:pk>/',OrderDetailAPIView.as_view(),name='order-detail'),
    
]
