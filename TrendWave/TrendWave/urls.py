"""
URL configuration for TrendWave project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from restapp.views import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/',productsview.as_view(),name='api'),
    path('',products,name='products'),
    path('product/<int:id>/', product_detail, name='product'),
    path('clothes/',clothes.as_view(),name='clothes'),
    path('cloth/',cloth,name='cloth'),
    path('electronics/',electronics.as_view(),name='electronics'),
    path('electron/',electron,name='electron'),
    path('furniture/',furniture.as_view(),name='furniture'),
    path('wood_furniture/',wood_furniture,name='wood_furniture'),
    path('shoes/',shoes.as_view(),name='shoes'),
    path('shoe/',func_shoes,name='shoe'),
    path('other/',other.as_view(),name='other'),
    path('otheritems/',other_items,name='otheritems'),
    path('usersapi/',usersview.as_view()),
    path('register/',register,name='register'),
    path('clear-cache/', clear_cache_view, name='clear_cache'),
    path('login/',login,name='login'),
    path('logout/',logout,name='logout'),
    path('profile/',profile,name='profile'),
    path('cart/',cart,name='cart'),
    path('cart-view/',cart_view,name='cart-view'),
    path('buy/<int:id>/',buy,name='buy'),
    path('create-checkout-session/', create_checkout_session, name='create_checkout_session'),
    

]
