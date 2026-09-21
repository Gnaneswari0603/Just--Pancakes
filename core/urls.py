from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    path('menu/', views.menu, name='menu'),

    path('cart/', views.cart, name='cart'),

    path('update_cart/', views.update_cart, name='update_cart'),

    path('checkout/', views.checkout, name='checkout'),

    path(
        'success/',
        views.success,
        name='success'
    ),

    path(
        'payment/<int:order_id>/',
        views.payment_page,
        name='payment_page'
    ),

    path(
        'online_payment/<int:order_id>/',
        views.online_payment,
        name='online_payment'
    ),

    path(
        'verify_payment/',
        views.verify_payment,
        name='verify_payment'
    ),
]