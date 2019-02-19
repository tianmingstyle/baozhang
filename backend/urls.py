"""baozhang URL Configuration

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
from django.conf.urls import url
from django.contrib import admin
from backend import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'index.html', views.index),
    url(r'trouble-list.html', views.trouble_list),
    url(r'trouble-create.html', views.trouble_create),
    url(r'trouble-list-(?P<nid>\d+)-edit.html', views.trouble_edit),
    url(r'trouble-list-(?P<nid>\d+)-delete.html', views.trouble_delete),
    url(r'trouble-kill-list.html', views.trouble_kill_list),
    url(r'trouble-(?P<nid>\d+)-detail.html', views.trouble_detail),
    url(r'trouble-kill-(?P<nid>\d+).html', views.trouble_kill),
    url(r'trouble-kill-(?P<nid>\d+)-solution.html', views.trouble_kill_solution),
    url(r'highchartstest.html', views.highchartstest),
    url(r'highcharts-data-by-ajax.html', views.highcharts_data_by_ajax),

]
