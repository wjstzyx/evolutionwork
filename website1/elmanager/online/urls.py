from django.conf.urls import patterns, url
from online import views

 
urlpatterns = patterns('',
    url(r'^$', views.login, name='login'),
    url(r'^login/$',views.login,name = 'login'),
    url(r'^regist/$',views.regist,name = 'regist'),
    url(r'^indexuser/$',views.indexuser,name = 'indexuser'),
    url(r'^logout/$',views.logout,name = 'logout'),
)