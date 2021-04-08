from django.urls import include, path,re_path
from . import views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf.urls.static import static
from django.conf import settings
app_name = 'Users'
#set name url with function in views  manage user
urlpatterns = [
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('logout/', views.logout, name='logout'),
    path('status_message/', views.status_message, name='status_message'),
    re_path(r'^user/validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',views.activate_account, name='activate_account'),
    re_path(r'^user/reset/password/request/$', views.password_reset_request,name='password_reset_request'),
    re_path(r'^user/reset/password/validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<date>[0-9A-Za-z_\-]+)/(?P<time>[0-9A-Za-z_\-]+)/$',views.activate_password_reset, name='activate_password_reset'),
    re_path(r'^user/reset/password/change/$', views.reset_change_password_request,name='reset_change_password'),
    re_path(r'^user/change_password/$', views.change_password,name='change_password'),
    re_path(r'^totp/create/$', views.TOTPCreateView.as_view(), name='totp-create'),
    re_path(r'^totp/login/(?P<token>[0-9]{6})/$', views.TOTPVerifyView.as_view(), name='totp-login'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
