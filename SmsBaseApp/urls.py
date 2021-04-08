from django.conf.urls import url
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from . import views

app_name = 'SmsBaseApp'

# set url with function in view SmsBaseApp
urlpatterns = [
    path('', views.index),
    path('', views.index, name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('news_event/', views.news_event, name='news_event'),
    url(r'^(?P<slug>[-\w]+)/$', views.news_full_detail, name='news_full_detail'),
    url(r"detail/(?P<pk>\d+)/$",views.EventDetail.as_view(), name='event_detail')
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()  
