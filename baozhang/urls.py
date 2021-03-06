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
from django.conf.urls import url, include
from django.contrib import admin
from web import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^all/(?P<article_type_id>\d+).html', views.index, name='home'),
    url(r'^register', views.register),
    url(r'^login', views.login),
    url(r'^logout', views.logout),
    url(r'^get_content', views.get_content),
    url(r'^(?P<suffix>\w+)/get_mycontent', views.get_mycontent),
    url(r'^(?P<suffix>\w+)/(?P<article_id>\d+).html', views.get_mycontent, name="article_content"),
    url(r'^$', views.index),
    url(r'^backmanage.html$', views.backmanage),
    url(r'^cktest.html', views.cktest),
    url(r'^(?P<username>\w+)/management', views.backmanage),
    url(r'^(?P<username>\w+)/(?P<condition>((article)|(classification)|(tag)))', views.backmanage),
    url(r'^cktestmain', views.cktestmain),
    url(r'^(?P<what>(un)*likes).html', views.likesOrunlikes),
    url(r'^(?P<suffix>\w+).html', views.blog),
    url(r'^(?P<suffix>\w+)/(?P<condition>((tag)|(category)|(date)))/(?P<condition_id>\w+-*\w*).html', views.blog),
    url(r'^backend', include('backend.urls'))
]
