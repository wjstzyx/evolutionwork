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
    url(r'^index/monitor/mailtolist/python_AB_monitor/$',python_AB_monitor),
    url(r'^index/monitor/mailtolist/python_AB_monitor_newalert/$',python_AB_monitor_newalert),
    url(r'^index/monitor/configmonitorlist/$',configmonitorlist),
    url(r'^index/monitor/configmonitorlist/save_monitor_info/$',save_monitor_info),
    url(r'^index/monitor/configmonitorlist/add_new_monitor/$',add_new_monitor),
    url(r'^index/monitor/configmonitorlist/delete_monitor_info/$',delete_monitor_info),
    url(r'^index/monitor/st_heart/$',st_heart),
    url(r'^index/monitor/total_monitor/$',total_monitor),
    url(r'^index/monitor/lasttime_p_basic/$',lasttime_p_basic),
    url(r'^index/monitor/lasttime_p_basic/add_whitelist/$',add_whitelist),
    url(r'^index/monitor/lasttime_p_basic/remove_whitelist/$',remove_whitelist),
    url(r'^index/monitor/acname_p_basic/$',acname_p_basic),
    url(r'^index/monitor/jieti_position_monitor/$',jieti_position_monitor),
    url(r'^index/monitor/jieti_distinct_position/$',jieti_distinct_position),
    url(r'^index/monitor/jieti_st_position/$',jieti_st_position),
    url(r'^index/monitor/st_heart_analysis/$',st_heart_analysis),
    url(r'^index/monitor/distinct_cplus_ab/$',distinct_cplus_ab),    
    url(r'^index/monitor/realshowmonitor/$',realshowmonitor),
    url(r'^index/monitor/rt/$',rt),
    url(r'^index/monitor/rt_newalert/$',rt_newalert),
    url(r'^index/monitor/realshowmonitor_newalert/$',realshowmonitor_newalert), 
    url(r'^index/monitor/realshowmonitor_hulue/$',realshowmonitor_hulue), 
    url(r'^index/monitor/realshowmonitor_huifu/$',realshowmonitor_huifu), 
    url(r'^index/monitor/st_information/$',st_information),
    url(r'^index/quanyi/showaccompare/$', showaccompare),
    url(r'^index/quanyi/acname_distinct_showaccompare/$', acname_distinct_showaccompare),

    url(r'^index/quanyi/realcompare/$', realcompare),
    url(r'^index/quanyi/acwantedequlity/$', acwantedequlity),
    url(r'^index/quanyi/acwantedequlitynew/$', acwantedequlitynew),
    url(r'^index/quanyi/acwantedequlitynew_oneacname/$', acwantedequlitynew_oneacname),
    url(r'^index/quanyi/acwantedequlitynew_jieti/$', acwantedequlitynew_jieti),        
    url(r'^index/quanyi/acwantedequlityhistory/$', acwantedequlityhistory),
    url(r'^index/quanyi/acwantedequlity/qiu/$', acwantedequlityforqiu),
    url(r'^index/quanyi/acwantedequlitystock/$', acwantedequlitystock),
    url(r'^index/quanyi/acwantedequlitybacktest/$', acwantedequlitybacktest),
    url(r'^index/quanyi/stockmapequty/$', stockmapequty),
    url(r'^index/quanyi/map_acname_position/$', map_acname_position),       
    url(r'^index/quanyi/futureaccounttotal/$', futureaccounttotal),
    url(r'^index/quanyi/futureaccountone/$', futureaccountone),
    url(r'^index/quanyi/accountdetail_ac/$', accountdetail_ac), 
    url(r'^index/quanyi/account_lilun_distinct/$', account_lilun_distinct),
    url(r'^index/quanyi/account_lilun_distinct_chart/$', account_lilun_distinct_chart),
    url(r'^index/quanyi/account_lilun_distinct_acname/$', account_lilun_distinct_acname),
    url(r'^index/quanyi/account_lilun_distinct_st/$', account_lilun_distinct_st),
    url(r'^index/dataacquire/adddata/$', adddata),
    url(r'^index/quanyi/account_equity/$', account_equity),
    url(r'^index/quanyi/order_account_equity/$', order_account_equity),
    url(r'^index/quanyi/order_account_equity/save_order_p_basic/$', save_order_p_basic),
    url(r'^index/quanyi/order_account_equity/delete_order_p_follow_info/$', delete_order_p_follow_info),
    url(r'^index/data/fixdata/$',fixdata),
    url(r'^index/data/fixdata/fixdatacrtab/$',fixdatacrtab),
)
