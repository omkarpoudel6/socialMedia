"""SocialMedia URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from users.views import login_view,register_view,User_profile,Logout
from posts.views import Home

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',Home,name='home'),
    path('login/',login_view,name='login'),
    path('register/',register_view,name='register'),
    path('profile/',User_profile,name='profile'),
    path('logout/',Logout,name='logout'),

    path('posts/',include('posts.urls',namespace='posts')),
    path('friends/',include("users.urls"))
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
