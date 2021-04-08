"""BaseProject URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from rest_framework.documentation import include_docs_urls
from django.urls import path, re_path
from django.conf.urls import url ,include
from two_factor.urls import urlpatterns as tf_urls

urlpatterns = [

    path('admin/', admin.site.urls),
    path('tutorialbot/', include('tutorialbot.urls')),
    path('Users/', include(('Users.urls'))),
    path('social/', include('social_django.urls')),
    path('docs/', include_docs_urls()),
    # path('home/',include('SmsBaseApp.urls')),
    # path('SmsBackEnd/', include(('SmsBackEnd.urls'))),
    path('', include(('Frontend.urls'))),
    re_path(r'^api/', include('Users.urls')),
    



    
]
   

