from .views import *
from django.urls import path
from django.conf.urls import url
from ChatApp import views
from FreeFallProject import settings
from django.contrib.staticfiles.urls import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

urlpatterns = [
    path("home/", HomePage.as_view(), name="home"),
    path("", AllHikes.as_view(), name="all_hikes"),
    path("login/", UserLogin.as_view(), name="login"),
    path("registration/", Registration.as_view(), name="registration"),
    path("new_hike/", NewHike.as_view(), name="new_hike"),
    path("logout/", Logout.as_view(), name="logout"),
    path("all_hikes/", AllHikes.as_view(), name="all_hikes"),
    path('hike/<int:id>/', SetHike.as_view(), name="hike"),
    path('map/<int:id>/', MapOfHike.as_view(), name="map"),
    path('create_map/<int:id>/', CreateMap.as_view(), name="create_map"),
    path('editor/<int:id>/', HikeEditor.as_view(), name="editor"),
    path('my_account/', MyAccount.as_view(), name="my_account"),
        url('does_user_exist/',DoesUserExist.as_view(), name='does_user_exist'),
    # staticfiles_urlpatterns(),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()