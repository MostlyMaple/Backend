from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from . import views


urlpatterns = [
    path('', views.apiOverview, name="overview"),
    path('create-item/', views.createItem),
    path('get-items/', views.getItems),
    path('create-discount/', views.createDiscount, name='create-discount'),
    path('upload/', views.updateImage, name='image-upload'),
    path('get-item/<str:pk>/', views.getItem),
    path('update-item/<str:pk>/', views.updateItem),
    path('delete-item/<str:pk>/', views.deleteItem),
    path('get-discount/<str:pk>/', views.getDiscount),
    path('confirm-discount/<str:pk>/', views.confirmDiscount),
    path('update-discount/<str:pk>/', views.updateDiscount),
    path('delete-discount/<str:pk>/', views.deleteDiscount),
    path('get-discounts/', views.getDiscounts),
    path('users/register/', views.registerUser, name='register'),
    path('users/profile/', views.getUserProfile, name='get-user-profile'),
    path('users/update/<str:pk>/', views.updateUser, name='update-user'),
    path('users/', views.getUsers, name='users'),
    path('users/login/', views.MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('users/delete/<str:pk>/', views.deleteUser, name='detele-user'),
    path('users/profile/update/', views.updateUserProfile, name="update-user-profile"),
    path('users/<str:pk>/', views.getUserById, name='get-user-by-id'),
    path('orders/admin/', views.getOrders, name="orders-admin"),
    path('orders/add/', views.addOrderItems, name="orders-add"),
    path('orders/get/', views.getMyOrders, name="orders-get"),
    path('order/<str:pk>/', views.getOrderById, name="order-get"),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
