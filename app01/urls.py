"""day博客应用项目 URL Configuration

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
from app01 import views
urlpatterns = [
    #吧用户名作为路径匹配   注意：#匹配规则少的要放在上面
    url(r'^poll/$', views.poll),
    url(r'^comment/$', views.comment),
    url(r'^backendIndex/$', views.backendIndex),
    url(r'^addArticle/$', views.addArticle),
    url(r'^commenttree/(?P<article_id>\d+)$', views.commentTree),
    url(r'^(?P<username>.*)/articles/(?P<article_id>\d+)/$', views.article_detail),


    url(r'^(?P<username>.*)/(?P<condition>category|tag|data)/(?P<para>.*)/$', views.homesite),
    url(r'^(?P<username>.*)/$', views.homesite, name='aaa'),
]
