from django.contrib import admin
from django.urls import path
from django.conf import settings
from .views import view_friends_profile,Friends,AddFriend,AcceptFriendRequest
from django.conf.urls.static import static

app_name='users'

urlpatterns = [
    # path('/myposts', userPost,name='userpost'),
    path('',Friends,name='friends'),
    path('view_friends_profile/<int:id>/',view_friends_profile,name='view_friends_profile'),
    path('addfriend/',AddFriend,name='addfriend'),
    path('acceptfriendrequest/',AcceptFriendRequest,name='acceptfriendrequest')
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)