"""
URL configuration for AzuraCastRecognition project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('login', views.login, name='login'),
    path('manual_detection', views.manual_detection, name='manual_detection'),
    path('auth/', include('social_django.urls', namespace='social')),
    path('accounts/', include('allauth.urls')),
    path("preview_tweet/<str:type>", views.preview_tweet, name="preview_tweet"),
    path("post_tweet", views.post_tweet, name="post_tweet")
]
