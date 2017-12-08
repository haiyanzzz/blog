
from django.http import JsonResponse
from django.shortcuts import render, HttpResponse,redirect
from app01 import models
import json
import os
import datetime
from app01.forms import RegisterForm
from app01.forms import ArticleForm
from django.contrib import auth
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import F, Count, Avg
import json
from django.http import JsonResponse
from django.db import transaction
from django.conf import settings

# ================
from app01.geetest import GeetestLib
pc_geetest_id = "b46d1900d0a894591916ea94ea91bd2c"
pc_geetest_key = "36fc3fe98530eea08dfc6ce76e3d24c4"
mobile_geetest_id = "7c25da6fe21944cfe507d2f9876775a9"
mobile_geetest_key = "f5883f4ee3bd4fa8caec67941de1b903"
# 滑动验证码
def pcgetcaptcha(request):
    user_id = 'test'
    gt = GeetestLib(pc_geetest_id, pc_geetest_key)
    status = gt.pre_process(user_id)
    request.session[gt.GT_STATUS_SESSION_KEY] = status
    request.session["user_id"] = user_id
    response_str = gt.get_response_str()
    return HttpResponse(response_str)
# 滑动验证码
def pcajax_validate(request):

    if request.method == "POST":
        # 验证的验证码
        ret = {"flag": False, "error_msg": None}
        gt = GeetestLib(pc_geetest_id, pc_geetest_key)
        challenge = request.POST.get(gt.FN_CHALLENGE, '')
        validate = request.POST.get(gt.FN_VALIDATE, '')
        seccode = request.POST.get(gt.FN_SECCODE, '')
        status = request.session[gt.GT_STATUS_SESSION_KEY]
        user_id = request.session["user_id"]
        print("status",status)
        if status:
            result = gt.success_validate(challenge, validate, seccode, user_id)
        else:
            result = gt.failback_validate(challenge, validate, seccode)
        if result:  #如果验证验证码正确，就验证用户名是否正确
            username = request.POST.get("username")
            password = request.POST.get("password")

           # 验证用户名和密码
            user = auth.authenticate(username=username, password=password)
            if user:
                # 如果验证成功就让登录
                ret["flag"] = True
                auth.login(request, user)
            else:
                ret["error_msg"] = "用户名和密码错误"
        else:
            ret["error_msg"] = "验证码错误"
        return HttpResponse(json.dumps(ret))
    else:
        return render(request, "login.html")

def login(request):
    '''登录'''
    if request.method=="GET":
        return render(request, "login.html")
    else:
        username = request.POST.get("username")
        password = request.POST.get("password")
        vialdCode = request.POST.get("vialdCode")
        ret = {"flag":False,"error_msg":None}
        if vialdCode.upper() == request.session.get("keep_valid_code").upper():
            user = auth.authenticate(username=username, password=password)
            if user:
                #如果验证成功就让登录
                ret["flag"] = True
                auth.login(request,user)
            else:
                ret["error_msg"] = "用户名和密码错误"
        else:
            ret["error_msg"] = "验证码错误"
    return HttpResponse(json.dumps(ret))

def index(request,*args,**kwargs):
    '''博客系统主页'''
    #验证是不是当前进来的那个用户，如果用户已经登录了就可以看到页面
    # 如果没有登录就不让看见主页面，就直接返回登录页面
    # if not request.user.is_authenticated():
    #     return redirect("/login/")   #index大家都可以看到就不能验证了
    print("-----------",kwargs)  #接收到的是一个字典
    kwargs = kwargs.get("site_article_category")
    print("=======",kwargs)
    if kwargs:
        print("xxxxxxxxxxxxxx")
        article_obj =  models.Article.objects.filter(site_article_category__name=kwargs) # article_list打印的是一个对象  先查看所有的博客
    else:
        article_obj = models.Article.objects.all()#如果没有得到就查询所有的文章
    sit_obj = models.SiteCategory.objects.all()

    # =============分页==============
    paginator = Paginator(article_obj, 3)  # 这里的article_list必须是一个集合对象，把所有的书分页，一页有五个
    current_page = request.GET.get("page",1)  # 得到页数范围,默认有1页
    article_obj = paginator.page(current_page)  # 页码是几显示第几页的内容
    return render(request, "index.html",{"sit_obj": sit_obj,"article_obj": article_obj,"current_page": int(current_page),"paginator": paginator,})

def get_vaildCode_img(request):
    '''验证码图片'''
    # 方式一：这样的方式吧路径写死了，只能是那一张图片
    # import os
    # path = os.path.join(settings.BASE_DIR,"static","image","3.jpg")
    # with open(path,"rb") as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 方式二：每次都显示不同的图片，利用pillow模块，安装一个pillow模块
    # from PIL import Image
    # img = Image.new(mode="RGB",size=(120,40),color="green") #首先自己创建一个图片,参数size=(120,40) 代表长和高
    # f = open("validcode.png","wb")#然后把图片放在一个指定的位置
    # img.save(f,"png")  #保存图片
    # f.close()
    # with open("validcode.png","rb") as f:
    #     data = f.read()
    # return HttpResponse(data)
    # 方式三：
    # 方式二也不怎么好，因为每次都要创建一个保存图片的文件，我们可以不让吧图片保存到硬盘上，
    # 在内存中保存，完了自动清除，那么就引入了方式三：利用BytesIO模块
    # from io import BytesIO
    # from PIL import Image
    # img = Image.new(mode="RGB",size=(120,40),color="blue")
    # f = BytesIO()  #内存文件句柄
    # img.save(f,"png")  #保存文件
    # data = f.getvalue()#打开文件(相当于python中的f.read())
    # return HttpResponse(data)

    # 方式四：1、添加画笔，也就是在图片上写上一些文字
    #         2、并且字体随机，背景颜色随机
    from io import BytesIO
    from PIL import Image,ImageDraw,ImageFont
    import random
    #随机创建图片
    img = Image.new(mode="RGB",size=(120,40),color=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))
    draw = ImageDraw.Draw(img,"RGB")
    # 画干扰线
    for i in range(5):
        x1 = random.randint(0, 120)
        y1 = random.randint(0, 40)
        x2 = random.randint(0, 120)
        y2 = random.randint(0, 40)

        draw.line((x1, y1, x2, y2), fill=(random.randint(0,255),random.randint(0,255),random.randint(0,255)))

    font = ImageFont.truetype("static/font/kumo.ttf",20)  #20表示20像素

    str_list = []  #吧每次生成的验证码保存起来
    # 随机生成五个字符
    for i in range(5):
        random_num = str(random.randint(0, 9))  # 随机数字
        random_lower = chr(random.randint(65, 90))  # 随机小写字母
        random_upper = chr(random.randint(97, 122))  # 随机大写字母
        random_char = random.choice([random_num, random_lower, random_upper])
        print(random_char,"random_char")
        str_list.append(random_char)
        # (5 + i * 24, 10)表示坐标，字体的位置
        draw.text((5+i*24,10),random_char,(random.randint(0,255),random.randint(0,255),random.randint(0,255)),font=font)
    print(str_list,"str_list")
    f = BytesIO()#内存文件句柄
    img.save(f,"png")   #img是一个对象
    data = f.getvalue()  #读取数据并返回至HTML
    valid_str = "".join(str_list)
    print(valid_str,"valid_str")
    request.session["keep_valid_code"] = valid_str   #吧保存到列表的东西存放至session中
    return HttpResponse(data)

def log_out(request):
    '''注销'''
    auth.logout(request)
    return redirect("/login/")

def set_pwd(request):
    '''修改密码'''
    if request.method=="POST":
        oldpassword = request.POST.get("oldpassword")
        newpassword = request.POST.get("newpassword")
        #得到当前登录的用户，判断旧密码是不是和当前的密码一样
        username = request.user  #打印的是当前登录的用户名
        user = models.UserInfo.objects.get(username=username)  #查看用户
        ret = user.check_password(oldpassword)  #检查密码是否正确
        if ret:
            user.set_password(newpassword) #如果正确就给设置一个新密码
            user.save()  #保存
            return redirect("/login/")
        else:
            info = "输入密码有误"
            return render(request,"set_pwd.html",{"info":info})
    return render(request,"set_pwd.html")

def register(request):
    '''注册'''
    if request.method=="GET":
        form = RegisterForm()
        return render(request,"register.html",{"form":form})
    else:
        form = RegisterForm(data=request.POST)
        regresponse = {"user":None,"msg_errors":None}
        if form.is_valid():
            username = form.cleaned_data.get("username")
            password = form.cleaned_data.get("password")
            tel = form.cleaned_data.get("tel")
            email = form.cleaned_data.get("email")
            nickname = form.cleaned_data.get("nickname")
            #如果用户上传图片就把图片设置成当前的图片，如果不是就保持原来设置的图片
            avatar_img=request.FILES.get("avatar_img")
            if avatar_img:
                '''如果用户传了头像，让走传的那个图片'''
                models.UserInfo.objects.create_user(username = username,password=password,tel=tel,avatar=avatar_img,nickname=nickname,email=email)
            else:
                '''如果没有头像就让传默认的'''
                models.UserInfo.objects.create_user(username = username,password=password,tel=tel,nickname=nickname,email=email)
            regresponse["user"] = username
        else:
            print("form.errors",form.errors)
            regresponse["msg_errors"]=form.errors
        return HttpResponse(json.dumps(regresponse))

def homesite(request,username,**kwargs):
    '''个人站点'''
    # print(request.user.username)
    # print(username)
    #查看当前用户
    current_user = models.UserInfo.objects.filter(username=username).first()
    print("current_user==========",current_user,type(current_user))
    print("request.user.username======",request.user.username,type(request.user.username))
    # print(current_user.blog)
    if not current_user:
        return render(request, "msg_error.html")
    else:
        #查看当前用户昵称
        # print("=====",current_user)
        #查看当前用户的所有文章的所有标签
        # tags_obj= current_user.article_set.all().values("tags__name")
        #查看标签归档
        from django.db.models import Count
        current_blog = current_user.blog
        print(current_blog)
        print(models.Tag.objects.filter(blog=current_blog))  #拿到的是每一个个人站点的标签
        tag_obj = models.Tag.objects.all().filter(blog=current_blog).annotate(count=Count("article__id")).values_list("name","count")
        print("as",tag_obj)
        #查看当前用户的分类归档
        category_obj = models.Classfication.objects.filter(blog=current_blog).annotate(count=Count("article__title")).values_list("title","count")
        #查询当前用户的文章
        article_list = current_user.article_set.all()
        #查询当前用户的日期归档
        # print(models.Article.objects.all().filter(user=current_user).extra(select={"filter_create_date":"strftime('%%Y/%%m',create_time)"}).values_list("filter_create_date").annotate(Count("title")))
        data_obj = models.Article.objects.all().filter(user=current_user).extra(select={"filter_create_date":"strftime('%%Y/%%m',create_time)"}).values_list("filter_create_date").annotate(Count("title"))


        #跳转时的操作
        # print(kwargs)
        if kwargs:
            if kwargs.get("condition")=="category":
                article_list = models.Article.objects.all().filter(user=current_user,classify__title=kwargs.get("para"))
            elif kwargs.get("condition")=="tag":
                article_list= models.Article.objects.filter(user=current_user,tags__name=kwargs.get("para"))
                print("======",article_list)
            elif kwargs.get("condition")=="data":
                year,month = kwargs.get("para").split("/")
                article_list = models.Article.objects.all().filter(user=current_user,create_time__year=year,create_time__month=month)

                # =============分页==============
        return render(request, "homesite.html",locals())

def article_detail(request,username,article_id):
    '''点击文章标题跳转的具体文章'''
    article_obj = models.Article.objects.filter(id=article_id).first()
    current_user = models.UserInfo.objects.filter(username=username).first()
    from django.db.models import Count
    current_blog = current_user.blog  #当前用户的博客
    # print("xxxxx",current_blog)
    # print(models.Tag.objects.all().filter(blog=current_blog))  #拿到的是每一个个人站点的标签
    tag_obj = models.Tag.objects.all().filter(blog=current_blog).annotate(count=Count("article__id")).values_list("name", "count")
    # 查看当前用户的分类归档
    category_obj = models.Classfication.objects.all().filter(blog=current_blog).annotate(count=Count("article__id")).values_list("title", "count")
    # 查询当前用户的文章
    article_list = current_user.article_set.all()
    # 查询当前用户的日期归档
    # print(models.Article.objects.all().filter(user=current_user).extra(select={"filter_create_date":"strftime('%%Y/%%m',create_time)"}).values_list("filter_create_date").annotate(Count("title")))
    data_obj = models.Article.objects.all().filter(user=current_user).extra(select={"filter_create_date": "strftime('%%Y/%%m',create_time)"}).values_list("filter_create_date").annotate(Count("title"))
    comment_obj  = models.Comment.objects.filter(article_id=article_id)
    for i in comment_obj:
        print(i.comment_set.all().values("content"))
    obj = render(request, "article_detail.html", locals())
    obj.set_cookie("next_path",request.path)
    obj.set_cookie("username",request.user.username)
    print(obj,"========obj=========")
    return obj

def poll(request):
    '''点赞和点灭操作'''
    pollresponse = {"state": True, "is_repeat": None}  # 如果state为True代表访问成功，is_repeat为是否重复

    article_id = request.POST.get("article_id")
    user_id = request.user.nid
    is_positive = request.POST.get("is_positive")
    print("===========",is_positive)
    # print(article_id,user_id)
    print("user",request.user.username)
    # if models.Article_poll.objects.filter(user_id=user_id,article_id=article_id):
    #     #如果这条记录存在，就不能在提交了，这是没有建联合唯一的时候实现的方法，有了联合唯一就不用判断了
    #     pollresponse["state"] = False
    #     pollresponse["is_repeat"] = True
    # else:
    try:
        '''解决联合唯一的问题，如果是联合唯一你一创建就会报错，捕获一下走except的内容'''
        if is_positive=="1":  #点赞
            with transaction.atomic():
                print("========")
                # 当有人点赞的时候数据库的数据肯定会多一条
                models.Article_poll.objects.create(user_id=user_id,article_id=article_id)
                # 并且点赞数加1
                models.Article.objects.filter(id=article_id).update(up_count=F("up_count")+1)
        else: #点灭
            with transaction.atomic():
                print("=======zzzz")
                # 当有人点赞的时候数据库的数据肯定会多一条
                models.Article_poll.objects.create(user_id=user_id, article_id=article_id)
                # 并且点赞数加1
                models.Article.objects.filter(id=article_id).update(down_count=F("down_count")+1)
    except:
            pollresponse["state"] = False
            pollresponse["is_repeat"] = True
    return HttpResponse(json.dumps(pollresponse))

def comment(request):
    '''文章评论和评论的评论操作'''
    comment_response = {"flag":True}
    if not request.user.is_authenticated():
        comment_response["flag"] = False
        return HttpResponse(json.dumps(comment_response))
    else:
        article_id = request.POST.get("article_id")
        user_id = request.user.nid
        content=request.POST.get("content")
        farther_comment_id = request.POST.get("farther_comment_id")
        print(farther_comment_id,"==========")
        #用户输入的数据存到评论表
        if farther_comment_id:
            with transaction.atomic():
                '''如果父级评论有值就是对评论进行评论：子评论'''
                comment_obj = models.Comment.objects.create(content=content, user_id=user_id, article_id=article_id,farther_comment_id=farther_comment_id)
                comment_response["create_time"] = str(comment_obj.time)
                print("啦啦",models.Comment.objects.filter(article_id=article_id))
                print(comment_response)
                comment_response["parent_comment_username"] = comment_obj.farther_comment.user.username

                comment_response["parent_comment_content"] = comment_obj.farther_comment.content
        else:
            '''否则就是对文章进行评论：根评论'''
            with transaction.atomic():
                '''创建事务，如果出错回滚。下面两个要么同时生成，要么一个都不生成'''
                comment_obj = models.Comment.objects.create(content=content,user_id=user_id,article_id=article_id)
                # 评论数增加1
                models.Article.objects.filter(id=article_id).update(comment_count=F("comment_count")+1)
        comment_response["create_time"] = str(comment_obj.time)
        comment_response["comment_id"] = comment_obj.id
        # print(comment_response)
        return JsonResponse(comment_response)


def commentTree(request,article_id):
    # print('\033[35m=====\033[0m%s'%commentTree)
    '''结构化评论树'''
    comment_list = models.Comment.objects.filter(article_id=article_id).values("id","content","farther_comment_id")


    # ===========放一个字典，吧id提出来，并且在每一个字典中加一个"children_comment":[]键值对==========
    comment_dict = {}
    for comment in comment_list:
        comment["children_comment"] = []
        comment_obj = models.Comment.objects.filter(id=comment["id"]).first()
        comment["comment_time"] = str(comment_obj.time)
        comment["parent_comment_content"] = comment_obj.content
        comment["parent_comment_username"] = comment_obj.user.username
        comment_dict[comment["id"]] = comment
    # print(comment_dict)   #{1:{"":"","":""},2:{"":"","":""},3:{}}
    # print(comment_list)
    # =================找父级id==================
    comment_tree = []
    for comment in comment_list:
        pid = comment["farther_comment_id"]
        if pid:
            comment_dict[pid]["children_comment"].append(comment)
        else:
            '''如果pid为none的时候找一个列表存起来'''
            comment_tree.append(comment)
    print('\033[35m=====>>>\033[0m%s' % comment_tree)
    return HttpResponse(json.dumps(comment_tree))

def backendIndex(request):
    '''后台管理主页，记得要加上文章的跳转路径，这里的路径拼接有问题'''
    print("*******",request.user,type(request.user))#******* haiyan <class 'django.utils.functional.SimpleLazyObject'> 只是一个类实例对象
    print("+++++++",request.user.username,type(request.user.username))#+++++++ haiyan <class 'str'>
    article_obj = models.Article.objects.filter(user=request.user).all()
    return render(request,"backendIndex.html",{"article_obj":article_obj})

def addArticle(request):
    '''添加图书的操作，kindeditor编辑器的应用'''
    if request.method == "POST":
        print(12213)
        form = ArticleForm(data=request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            cate = request.POST.get("cate")
            tag = request.POST.getlist("tag")
            article_obj = models.Article.objects.create(title=title,summary=content[0:30],create_time=datetime.datetime.now(),user=request.user,classify_id = cate)
            models.Article_detail.objects.create(content=content,article=article_obj)
            if tag:
                for i in tag:   #[2,4]
                    models.Article2tag.objects.create(tag_id=i,article_id=article_obj.id)
            # 如果数据正确就把数据插入到数据库
        else:
            pass
        return HttpResponse("添加成功")
    else:
        form = ArticleForm()
        print("--------")
        #查询当前站点的所有分类的名字
        cate_list = models.Classfication.objects.all().filter(blog__user=request.user)
        for i in cate_list:
            print("??????",i)
        #查询当前站点的所有标签
        tag_list = models.Tag.objects.all().filter(blog__user=request.user)

        return render(request,"addArticle.html",{"form":form,"cate_list":cate_list,"tag_list":tag_list})

def uploadFile(request):
    '''上传图片路径'''
    print(request.path)  #返回的是当前请求的路径
    print(request.FILES)  #<MultiValueDict: {'imgFile': [<InMemoryUploadedFile: 44643.gif (image/gif)>]}>
    file_obj = request.FILES.get("imgFile")  #得到用户上传的文件对象
    filename = file_obj.name  #那到文件的文件名
    path = os.path.join(settings.MEDIA_ROOT,"upload_article_img",filename) #拼接一个路径吧文件保存进去，一般上传文件的路径保存在media中
    print("======",path)
    with open(path,"wb") as f:#吧文件保存在本地
        for line in file_obj:
            f.write(line)
    response = {
        "error":0,
        "url":"/media/upload_article_img/"+filename+"/"   #前端图片文件预览
    }

    return HttpResponse(json.dumps(response))   #需要注意的是上传文件返回的是一个json字符串

# cbv模式
from django.views import View
class Login_cbv(View):
   def get(self,request):  #如果是get请求需要执行的代码
       return render(request,"login_cbv.html")
   def post(self,request): #如果是post请求需要执行的代码
       return HttpResponse(".....")
   def delete(self,request):
       pass

# 优化查询
def querytest(request):
    #查询所有的文章
    # ret = models.Article.objects.all()
    #惰性机制：不用不求
    # for i in ret:
    #     print(i.title)  #如果我把这个注释了，只有   ret = models.Article.objects.all()
    #                     # 就不会走sql,什么时候用它什么时候走数据库
    # if ret :   #在这里用了，就走sql
    #     print("ok")
    # print(ret[2])  #也会走sql

    # 缓存机制
    # ret2 = models.Article.objects.all().iterator()  #吧所有的数据做成一个迭代器对象，什么时候用什么时候拿，不用不拿
    #这时有两个for循环的时候，会打印两边，sql语句会走一遍
    # for i in ret2:
    #     print(i.title)
    # for i in ret2:
    #     print(i.title)
    # 每一个queryset都会有一个缓存机制，当你下次访问的时候会去缓存里面拿

    #优化查询有两种，一种是iterator() ，一种是exists()：
    # if ret2.exists():
    #     print("ok")

# ===================================
    # 查询 主键等于2的文章的所属分类名称

    # ret=models.Article.objects.filter(id=2).values("classify__title")
    # print(ret)   #

    # obj = models.Article.objects.get(id=2)
    # print(obj.classify.title)   #走两次数据库，基于对象的属于子查询，基于双下划线的属于连表查询

    # obj = models.Article.objects.select_related("classify").get(id=2)   #现在就会查询一次了
    # print(obj.classify.title)
    #查询所有书的分类标题
    obj_list=models.Article.objects.select_related("user").select_related("classify").all()
    for obj in obj_list:
        print(obj,"2222222",type(obj))
        print(obj.classify.title)

    # obj_list = models.Article.objects.select_related("user","classify").all()
    # for obj in obj_list:
    #     print(obj.classify.title)
    # 要看需求查的数据多不多，如果一次的话就没有必要了

    # obj_list = models.Article.objects.select_related("category").select_related("user").all()
    # for obj in obj_list:
    #     print(obj.user.title)
    return HttpResponse("ok")
