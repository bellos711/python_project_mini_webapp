from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('admin/', views.admin_login_view, name='adminloginpage'),
    path('adminauthenticate/',views.authenticateadmin),
    path('admin/homepage/', views.adminhomepageview, name='adminhomepage'),
    path('adminlogout/', views.logoutadmin),
    path('addhamburger/', views.add_hamburger),
    path('deletehamburger/<int:hamburger_id>', views.delete_hamburger),
    path('', views.homepage_view, name="homepage"),
    path('register/', views.register),
    path('userlogin/', views.user_login_view),
    path('authenticate/', views.login_user),
    path('customer/main/', views.customer_page),
    path('customer/logout', views.logout_user),
    path('placeorder/', views.place_order),
    path('customer/customerorders/', views.customer_orders),
    path('adminorders/', views.admin_orders),
    path('acceptorder/<int:order_id>/', views.accept_order),
    path('declineorder/<int:order_id>/', views.decline_order),
]
