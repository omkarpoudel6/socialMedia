from django.contrib import admin
from django.urls import path
from django.conf import settings
from .views import userPost,like_post
from django.conf.urls.static import static

app_name='posts'

urlpatterns = [
    path('', userPost,name='userpost'),
    path('like/',like_post,name='like-post')
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)