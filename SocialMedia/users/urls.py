from django.contrib import admin
from django.urls import path
from django.conf import settings
from .views import view_friends_profile
from django.conf.urls.static import static

urlpatterns = [
    # path('/myposts', userPost,name='userpost'),
    path('view_friends_profile/<int:id>/',view_friends_profile,name='view_friends_profile')
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)