from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import path, re_path

from . import views,view_dashboards ,views_accounts



app_name = 'SmsBaseApp'

# set url with function in view SmsBaseApp
urlpatterns = [
     # main page for all user
     path('smsbackend_admin/', view_dashboards.smsbackend_main_admin,
          name='smsbackend_main_admin'),
     path('smsbackend_curator/', view_dashboards.smsbackend_main_curator,
          name='smsbackend_main_curator'),
          # accouts
     path('manage_accounts/', views_accounts.manage_accounts,
          name="manage_accounts"),
     path('edit_account/?P<user_id>',
          views_accounts.edit_account, name="edit_account"),
     path('view_account/?P<user_id>',
          views_accounts.view_account, name='view_account'),
     path('create_accounts/', views_accounts.create_accounts,
          name="create_accounts"),
     path('active_accounts/', views_accounts.active_accounts,
          name="active_accounts"),
     path('status_message/', views_accounts.status_message,
          name='status_message'),
     re_path(
          r'^user/validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
          views_accounts.activate_account, name='activate_account'),
     re_path(r'^user/reset/password/request/$', views_accounts.password_reset_request,
               name='password_reset_request'),
     re_path(
          r'^user/reset/password/validate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/(?P<date>[0-9A-Za-z_\-]+)/(?P<time>[0-9A-Za-z_\-]+)/$',
          views_accounts.activate_password_reset, name='activate_password_reset'),
     re_path(r'^user/reset/password/change/$', views_accounts.reset_change_password_request,
               name='reset_change_password'),
     re_path(r'^user/change_password/$',
               views_accounts.change_password, name='change_password'),
     path('del_user/?P<username>',
          views_accounts.del_user, name='del_user'),
     path('delete_user_sessions/?P<username>', views_accounts.delete_user_sessions,
          name='delete_user_sessions'),
     path('django_image_and_file_upload_ajax/', views_accounts.django_image_and_file_upload_ajax,
          name='django_image_and_file_upload_ajax'),

     # url for user logged in
     path('profile/', views.profile, name="profile"),
     path('notification/', views.notification, name="notification"),
     path('setting/', views.setting, name="setting"),

     # backup
     path('backup/', views.backup, name="backup"),
     path('backup_database/', views.backup_database,
          name="backup_database"),
     path('backup_web_content/', views.backup_web_content,
          name="backup_web_content"),
          # news & events
     path('create_news/', views.create_news, name="create_news"),
     path('edit_news/<id>/', views.edit_news, name="edit_news"),
     path('view_news/<id>/', views.view_news, name="view_news"),
     path('delete_news/', views.delete_new, name="delete_news"),
     path('manage_news_events_new/', views.manage_news_events_new,
          name="manage_news_events_new"),
     path('manage_news_events/', views.manage_news_events,
          name="manage_news_events"),
     path('load_events/', views.load_events, name="load_events"),
     path('views_events/', views.views_events, name="views_events"),
     path('insert_events/', views.insert_events,
          name="insert_events"),
     path('update_events/', views.update_events,
          name="update_events"),
     path('delete_events/', views.delete_events,
          name="delete_events"),


     path("add_news",views.add_news,name='add_news'),
     url(r"^(?P<slug>[-\w]+)/edit/$",views.edit_post,name='edit_post'),
     
     path("delete_new/",views.delete_new,name="delete_new"),

     path("add_event",views.add_event,name='add_event'),

     url(r"^edit/(?P<pk>\d+)/$",views.edit_event,name="edit_event"),
     path("delete_event/",views.delete_event,name="delete_event"),

     path("add_about",views.add_about,name='add_about'),
     path("about_data_page",views.about_data_page,name='about_data_page'),
     url(r"^edit_about/(?P<pk>\d+)/$",views.edit_about,name='edit_about'),

     # update content
     path('change_content/', views.change_content,
          name="change_content"),

     # logs
     path('logs/', views.logs, name="logs"),

     path('author', views.AuthorList.as_view()),
     path('author/<int:id>', views.AuthorDetail.as_view()),
     path('book', views.BookList.as_view()),
     path('book/<int:id>', views.BookDetail.as_view()),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += staticfiles_urlpatterns()
