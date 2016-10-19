from django.conf.urls import patterns, include, url
from elmanager.views import *

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'elmanager.views.home', name='home'),
    # url(r'^elmanager/', include('elmanager.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^online/', include('online.urls')),
    url(r'^index/login/$', mylogin),
    url(r'^index/logout/$', mylogout),
    url(r'^index/change_password/$', change_password),
    url(r'^index/register/$', register),

    #function page
    url(r'^index/$', index),
    url(r'^index/monitor/mailtolist/$', configmailtolist),
    url(r'^index/monitor/mailtolist/save_mailto_info/$',save_mailto_info),
    url(r'^index/monitor/mailtolist/add_new_mailto/$',add_new_mailto),
    url(r'^index/monitor/mailtolist/delete_mailto_info/$',delete_mailto_info),
    url(r'^index/monitor/configmonitorlist/$',configmonitorlist),
    url(r'^index/monitor/configmonitorlist/save_monitor_info/$',save_monitor_info),
    url(r'^index/monitor/configmonitorlist/add_new_monitor/$',add_new_monitor),
    url(r'^index/monitor/configmonitorlist/delete_monitor_info/$',delete_monitor_info),
    url(r'^index/monitor/st_heart/$',st_heart),
    url(r'^index/monitor/lasttime_p_basic/$',lasttime_p_basic),
    url(r'^index/monitor/lasttime_p_basic/add_whitelist/$',add_whitelist),
    url(r'^index/monitor/lasttime_p_basic/remove_whitelist/$',remove_whitelist),
    url(r'^index/monitor/acname_p_basic/$',acname_p_basic),
    url(r'^index/monitor/st_information/$',st_information),
    url(r'^index/quanyi/showaccompare/$', showaccompare),
    url(r'^index/quanyi/realcompare/$', realcompare),
    url(r'^index/quanyi/acwantedequlity/$', acwantedequlity),
    url(r'^index/quanyi/acwantedequlitynew/$', acwantedequlitynew),
    url(r'^index/quanyi/acwantedequlityhistory/$', acwantedequlityhistory),
    url(r'^index/quanyi/acwantedequlity/qiu/$', acwantedequlityforqiu),
    url(r'^index/quanyi/acwantedequlitystock/$', acwantedequlitystock),
    url(r'^index/quanyi/acwantedequlitybacktest/$', acwantedequlitybacktest),
    url(r'^index/quanyi/futureaccounttotal/$', futureaccounttotal),
    url(r'^index/quanyi/futureaccountone/$', futureaccountone),
    url(r'^index/dataacquire/adddata/$', adddata),
    url(r'^index/quanyi/account_equity/$', account_equity),
    url(r'^index/quanyi/order_account_equity/$', order_account_equity),
    url(r'^index/quanyi/order_account_equity/save_order_p_basic/$', save_order_p_basic),
    url(r'^index/quanyi/order_account_equity/delete_order_p_follow_info/$', delete_order_p_follow_info),
    url(r'^index/data/fixdata/$',fixdata),
    url(r'^index/data/fixdata/fixdatacrtab/$',fixdatacrtab),
)
