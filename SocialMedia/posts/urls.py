from django.contrib import admin
from django.urls import path
from django.conf import settings
from .views import userPost
from django.conf.urls.static import static

urlpatterns = [
    path('', userPost,name='userpost'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)