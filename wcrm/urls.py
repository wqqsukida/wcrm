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


urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^arya/', (v1.site.urls, None, 'arya')),
    url(r'^login/', views.login),
    url(r'^logout/', views.logout),
    url(r'^index/', views.index),
    url(r'^index_v3/', views.index_v3),
    url(r'^403/', views.forbidden),
    url(r'^machines_dash/', views.machines_dash),
    url(r'^userinfo/', views.userinfo),
    url(r'^get_cert_detail/', views.get_cert_detail),
    url(r'^dnspod/add_domain', views.add_domain),
    url(r'^dnspod/', views.dnspod,name='dnspod'),
    url(r'^dnspod_record/', views.dnspod_record),
    url(r'^dnspod_d/$', views.dnspod_d),
    url(r'^dnspod_d/gethistory_monitor/', views.gethistory_monitor),
]
