from django.urls import path
from . import views

urlpatterns = [
        path('', views.home, name='home'),
        path('login/', views.login_view, name='login'),
        path('signup/', views.signup_view, name='signup'),
        path('logout/', views.logout_view, name='logout'),
        path('menu/', views.menu, name='menu'),
        path('add_to_cart/<int:item_id>/', views.add_to_cart, name='add_to_cart'),
        path('cart/', views.view_cart, name='view_cart'),
        path('confirm_order/', views.confirm_order, name='confirm_order'),
        path('order_confirmation/', views.order_confirmation, name='order_confirmation'),
        path('profile/', views.user_profile, name='user_profile'),
        path('adjust_quantity/<int:item_id>/<str:action>/', views.adjust_quantity, name='adjust_quantity'),
        path('remove_item/<int:item_id>/', views.remove_item, name='remove_item'),


    ]


