from .views import *
from django.urls import path
from ChatApp import views

urlpatterns = [
    path("", HomePage.as_view(), name="home"),
    path("login/", UserLogin.as_view(), name="login"),
    path("registration/", Registration.as_view(), name="registration"),
    path("new_hike/", NewHike.as_view(), name="new_hike"),
    path("logout/", Logout.as_view(), name="logout"),
    path("all_hikes/", AllHikes.as_view(), name="all_hikes"),
    path('hike/<int:id>/', SetHike.as_view(), name="hike"),
    path('map/<int:id>/', MapOfHike.as_view(), name="map"),
    path('editor/<int:id>/', HikeEditor.as_view(), name="editor"),
]