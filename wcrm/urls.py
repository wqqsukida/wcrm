"""wcrm URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url,include
from django.contrib import admin
from arya.service import v1
from crm import views
from utils import dnspod

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^arya/', (v1.site.urls, None, 'arya')),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^index/', views.index),
    url(r'^index_v3/', views.index_v3),
    url(r'^403/', views.forbidden),
    url(r'^$', views.index),
    url(r'^machines_dash/', views.machines_dash),
    url(r'^userinfo/', views.userinfo),
    url(r'^get_cert_detail/', views.get_cert_detail),
    url(r'^dnspod/add_domain', dnspod.add_domain),
    url(r'^dnspod/del_domain', dnspod.del_domain),
    url(r'^dnspod/domain_status', dnspod.domain_status),
    url(r'^dnspod/domain_log', dnspod.domain_log),
    url(r'^dnspod/domain_searchenginepush', dnspod.domain_searchenginepush),
    url(r'^dnspod/domain_remark', dnspod.domain_remark),
    url(r'^dnspod/domain_lock', dnspod.domain_lock),
    url(r'^dnspod/domain_changegroup', dnspod.domain_changegroup),
    url(r'^dnspod/domain_addgroup', dnspod.domain_addgroup),
    url(r'^dnspod/domain_modgroup', dnspod.domain_modgroup),
    url(r'^dnspod/domain_delgroup', dnspod.domain_modgroup),
    url(r'^dnspod/', dnspod.dnspod,name='dnspod'),
    url(r'^dnspod_record/add_record', dnspod.add_record),
    url(r'^dnspod_record/del_record', dnspod.del_record),
    url(r'^dnspod_record/mod_record', dnspod.mod_record),
    url(r'^dnspod_record/record_status', dnspod.record_status),
    url(r'^dnspod_record/record_remark', dnspod.record_remark),
    url(r'^dnspod_record/', dnspod.dnspod_record),
    url(r'^dnspod_d/list_subdomain', dnspod.list_subdomain),
    url(r'^dnspod_d/list_subvalue', dnspod.list_subvalue),
    url(r'^dnspod_d/create_monitor', dnspod.create_monitor),
    url(r'^dnspod_d/remove_monitor', dnspod.remove_monitor),
    url(r'^dnspod_d/monitor_info', dnspod.monitor_info),
    url(r'^dnspod_d/modify_monitor', dnspod.modify_monitor),
    url(r'^dnspod_d/setstatus_monitor', dnspod.setstatus_monitor),
    url(r'^dnspod_d/getdowns_monitor', dnspod.getdowns_monitor),
    url(r'^dnspod_d/gethistory_monitor/', dnspod.gethistory_monitor),
    url(r'^dnspod_d/$', dnspod.dnspod_d),
]
