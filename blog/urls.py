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
from django.contrib import admin
from app01 import views
from django.conf import settings
from django.views.static import serve
from app01.views import pcajax_validate
from app01.views import pcgetcaptcha
urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^login/$', views.login),
    url(r'^index/', views.index),
    url(r'^uploadFile/$', views.uploadFile),
    url(r'^$', views.index),
    url(r'^get_vaildCode_img/$', views.get_vaildCode_img),
    url(r'^log_out/$', views.log_out),

    url(r'^register/$', views.register),
    #media配置
    url(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
    url(r'^set_pwd/$', views.set_pwd),

    url(r'^cate/(?P<site_article_category>.*)/', views.index),
    url(r'^blog/', include('app01.urls')),

    #滑动验证码
    url(r'^pc-geetest/register', pcgetcaptcha, name='pcgetcaptcha'),
    url(r'^pc-geetest/ajax_validate', pcajax_validate, name='pcajax_validate'),
    #CBV模式
    url(r'^login_cbv/$', views.Login_cbv.as_view()),
    url(r'^querytest/$', views.querytest),

]
