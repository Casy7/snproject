from .views import *
from django.urls import path
from django.conf.urls import url
from FreeFallApp import views
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
    path("posts/", Posts.as_view(), name="posts"),
    path("all_hikes/", AllHikes.as_view(), name="all_hikes"),
    path('hike/<int:id>/', SetHike.as_view(), name="hike"),
    path('post/<int:id>/', SetPost.as_view(), name="post"),
    path('hike/<int:id>/about', About.as_view(), name="about"),
    path('map/<int:id>/', MapOfHike.as_view(), name="map"),
    path('create_map/<int:id>/', CreateMap.as_view(), name="create_map"),
    path('discussion/<int:id>/', Discussion.as_view(), name="discussion"),
    path('editor/<int:id>/', HikeEditor.as_view(), name="editor"),
    path('account/<str:username>/', Account.as_view(), name="account"),
    path("hike_filter/", HikeFilter.as_view(), name="hike_filter"),
    url('does_user_exist/', DoesUserExist.as_view(), name='does_user_exist'),
    url('send_notification_choice/', NotificationResult.as_view(),
        name='send_notification_choice'),
    url('get_user_notifications/', SendNotifications.as_view(),
        name='get_user_notifications'),
    url('change_map/', ChangeMap.as_view(), name='change_map'),
    url('get_filtered_hikes', FilterHikes.as_view(), name='get_filtered_hikes'),
    url('send_comment', AddComment.as_view(), name='send_comment'),
    url('upload_hike_image/', UploadHikeImage.as_view(), name='upload_hike_image'),
    url('invite_users/', InviteUsers.as_view(), name='invite_users'),
    
    path('account_editor/', AccountEditor.as_view(), name="account_editor"),


    # staticfiles_urlpatterns(),
    # static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
