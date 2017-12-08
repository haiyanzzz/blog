from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser
# Create your models here.
class UserInfo(AbstractUser):   #settings  ：AUTH_USER_MODEL ="应用名称.UserInfo"
    '''用户信息表'''
    nid = models.BigAutoField(primary_key=True)
    nickname =models.CharField(max_length=32,verbose_name="昵称")
    tel = models.IntegerField(verbose_name="电话",unique=True,null=True,blank=True)
    email = models.CharField(max_length=64,verbose_name="邮箱")
    avatar = models.FileField(verbose_name="头像",upload_to="avatar",default="avatar/default.png")
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)

    class Meta:
        verbose_name_plural = "用户信息表"
    def __str__(self):
        return self.username

class Blog(models.Model):
    '''个人站点表'''
    title = models.CharField(max_length=32,verbose_name="个人博客标题")
    site = models.CharField(verbose_name='个人博客后缀', max_length=32,unique=True)
    theme = models.CharField(max_length=32,verbose_name="博客主题")
    user = models.OneToOneField(to="UserInfo", verbose_name="所属用户")
    class Meta:
        '''通过admin录入数据的时候个中文显示'''
        verbose_name_plural = "个人站点表"

    def __str__(self):
        return self.title

class Article(models.Model):
    '''
    文章表
    '''
    title = models.CharField(max_length=64,verbose_name="文章标题")
    summary = models.CharField(max_length=244, verbose_name="文章概要")
    create_time = models.DateTimeField(verbose_name="创建时间",auto_now_add=True)
    update_time = models.DateTimeField(verbose_name="修改时间",auto_now=True)
    up_count = models.IntegerField(verbose_name="点赞数",default=0)
    down_count = models.IntegerField(verbose_name="点灭数",default=0)
    comment_count = models.IntegerField(verbose_name="评论数",default=0)
    read_count = models.IntegerField(verbose_name="阅读数",default=0)

    user = models.ForeignKey(to="UserInfo",verbose_name="所属作者",null=True,blank=True)
    classify = models.ForeignKey(to="Classfication",verbose_name="所属类别",null=True,blank=True)
    tags = models.ManyToManyField(to="Tag",through="Article2tag",through_fields=('article', 'tag'),verbose_name="所属标签")
    site_article_category = models.ForeignKey(to="SiteArticleCategory",verbose_name="所属文章分类",null=True,blank=True)
    class Meta:
        verbose_name_plural = "文章表"
    def __str__(self):
        return self.title

class Article_detail(models.Model):
    '''文章细节表'''
    article = models.OneToOneField(to="Article",verbose_name="所属文章")
    content =models.TextField(verbose_name="文章内容")

    class Meta:
        verbose_name_plural = "文章细节表"
    def __str__(self):
        return self.content

class SiteCategory(models.Model):
    '''网站分类表'''
    name = models.CharField(max_length=32,verbose_name="分类名")
    class Meta:
        verbose_name_plural="网站分类表"
    def __str__(self):
        return self.name

class SiteArticleCategory(models.Model):
    '''网站文章分类表'''
    name = models.CharField(max_length=32,verbose_name="分类名")
    sitecategory = models.ForeignKey(to="SiteCategory",verbose_name="所属网站")

    class Meta:
        verbose_name_plural = "网站文章分类表"
    def __str__(self):
        return self.name

class Tag(models.Model):
    '''标签表'''
    name = models.CharField(max_length=32,verbose_name="标签名")
    blog = models.ForeignKey(to="Blog",verbose_name="所属博客")
    class Meta:
        verbose_name_plural = "标签表"

    def __str__(self):
        return self.name

class Article2tag(models.Model):
    article = models.ForeignKey(verbose_name="文章",to="Article")
    tag = models.ForeignKey(verbose_name="标签",to="Tag")
    class Meta:
        verbose_name="文章和标签关系表"
        '''联合唯一'''
        unique_together = [
            ("article","tag")
        ]
    def __str__(self):
        return self.article.title + "  "+self.tag.name
class Comment(models.Model):
    '''评论表'''
    time = models.DateTimeField(verbose_name="评论时间",auto_now_add=True)
    content = models.CharField(max_length=265,verbose_name="评论内容")
    up_count = models.IntegerField(default=0,verbose_name="评论点赞数")
    user = models.ForeignKey(to="UserInfo",verbose_name="评论人",null=True,blank=True)
    article = models.ForeignKey(to="Article",verbose_name="评论文章",null=True,blank=True)
    farther_comment = models.ForeignKey(to="Comment",verbose_name="父级评论",null=True,blank=True)
    # farther_comment = models.ForeignKey("self",verbose_name="父级评论",null=True,blank=True)

    class Meta:
        verbose_name_plural = "评论表"
class Article_poll(models.Model):
    '''文章点赞表'''
    time = models.DateTimeField(verbose_name="点赞时间",auto_now_add=True)
    article = models.ForeignKey(to="Article",verbose_name="点赞文章",null=True,blank=True)   #一个文章可以有多个赞
    user = models.ForeignKey(to="UserInfo",verbose_name="点赞人",null=True,blank=True)
    is_positive = models.BooleanField(default=1,verbose_name="点赞或踩")

    class Meta:
        '''联合唯一'''
        unique_together = ("user", "article",)
        verbose_name_plural = "文章点赞表"
    def __str__(self):
        return self.user.username

class Comment_poll(models.Model):
    '''评论点赞表'''
    time=models.DateTimeField(verbose_name="点赞时间",auto_now_add=True)
    # is_positive = models.BooleanField(verbose_name="点赞或踩",default=1)
    user = models.ForeignKey(to="UserInfo",verbose_name="点赞用户",null=True,blank=True)
    comment = models.ForeignKey(to="Comment",verbose_name="点赞所属评论",null=True,blank=True)   #一个评论可以有多个赞

    class Meta:
        '''联合唯一'''
        unique_together = ("user","comment",)
        verbose_name_plural = "评论点赞表"


class Classfication(models.Model):
    '''博主个人文章分类表'''
    title = models.CharField(max_length=32, verbose_name="分类标题")
    blog = models.ForeignKey(to="Blog",verbose_name="所属博客")

    class Meta:
        verbose_name = 'classfication'
        verbose_name_plural = '分类表'
        ordering = ['title']

    def __str__(self):
        return self.title