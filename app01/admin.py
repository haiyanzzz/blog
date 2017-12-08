from django.contrib import admin
from app01 import models
# Register your models here.
admin.site.register(models.UserInfo)
admin.site.register(models.Article)
admin.site.register(models.Article_detail)
admin.site.register(models.Blog)
admin.site.register(models.Article2tag)
admin.site.register(models.Comment)
admin.site.register(models.Classfication)
admin.site.register(models.Tag)
admin.site.register(models.Article_poll)
admin.site.register(models.Comment_poll)
admin.site.register(models.SiteCategory)
admin.site.register(models.SiteArticleCategory)
