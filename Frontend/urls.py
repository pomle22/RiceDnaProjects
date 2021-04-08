from django.conf.urls import url
from django.urls import path
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
from .views import index,gene,dataManage,sample,profile,json_data,dictfetchall

app_name = 'Frontend'

# set url with function in view Frontend
urlpatterns = [
    path('', index, name='index'),
    path('gene/',gene, name='gene'),
    path('datamanage/',dataManage,name='datamanage'),
    path('sample/',sample,name='sample'),
    path('profile/',profile,name='profile'),
    path('data/', json_data,name='data'),
    # path('data2/', json_data2,name='data2')
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()  







