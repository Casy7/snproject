from .views import *
from django.urls import path
from ChatApp import views

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", UserLogin.as_view(), name="login"),
    path("registration/", Registration.as_view(), name="registration"),
    path("new_hike/", NewHike.as_view(), name="new_hike"),
    path("logout/", Logout.as_view(), name="logout"),
    
]