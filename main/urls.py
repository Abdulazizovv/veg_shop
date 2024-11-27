from django.urls import path
from . import views


urlpatterns = [
    path('', views.index, name='index'),
    path('register/', views.register_user, name='register_user'),
    path('login/', views.login_user, name='login_user'),
    path('vegetables/', views.vegetables, name='vegetables'),
    path('fruits/', views.fruits, name='fruits'),
    path('product/<int:product_id>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile, name='profile'),
    path('product/buy/', views.buy_product, name="buy_product"),
    path('orders/', views.orders, name="orders"),
    path('about/', views.about, name='about'),
    path('logout/', views.logout_user, name="logout"),
]