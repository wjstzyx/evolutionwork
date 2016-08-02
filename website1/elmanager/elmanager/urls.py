from django.conf.urls import patterns, include, url
from elmanager.views import *

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'elmanager.views.home', name='home'),
    # url(r'^elmanager/', include('elmanager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # url(r'^admin/', include(admin.site.urls)),
    url(r'^index/$', index),
    url(r'^index/monitor/mailtolist/$', configmailtolist),
    url(r'^index/monitor/mailtolist/save_mailto_info/$',save_mailto_info),
    url(r'^index/monitor/mailtolist/add_new_mailto/$',add_new_mailto),
    url(r'^index/monitor/mailtolist/delete_mailto_info/$',delete_mailto_info),
    url(r'^index/monitor/configmonitorlist/$',configmonitorlist),
    url(r'^index/monitor/configmonitorlist/save_monitor_info/$',save_monitor_info),
    url(r'^index/monitor/configmonitorlist/add_new_monitor/$',add_new_monitor),
    url(r'^index/monitor/configmonitorlist/delete_monitor_info/$',delete_monitor_info),
    url(r'^index/quanyi/showaccompare/$', showaccompare),
    url(r'^index/quanyi/realcompare/$', realcompare),
    url(r'^index/quanyi/acwantedequlity/$', acwantedequlity),
    url(r'^index/quanyi/acwantedequlitynew/$', acwantedequlitynew),
    url(r'^index/quanyi/acwantedequlity/qiu/$', acwantedequlityforqiu),
    url(r'^index/quanyi/acwantedequlitystock/$', acwantedequlitystock),
    url(r'^index/quanyi/acwantedequlitybacktest/$', acwantedequlitybacktest),
    url(r'^index/dataacquire/adddata/$', adddata),
)
