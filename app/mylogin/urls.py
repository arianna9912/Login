from django.urls import path

from mylogin.auth.authentication import Login

from django.contrib.auth.views import LogoutView, LoginView
from django.urls import path

from mylogin.views import home

urlpatterns = [

    path('auth/', Login.as_view(), name='auth'),
    path('home/',home,name='home'),
    path('login/', LoginView.as_view(), name='login'),


]
