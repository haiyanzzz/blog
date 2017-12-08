# #!usr/bin/env python
# # -*- coding:utf-8 -*-
from django import template
import datetime
from django.utils.safestring import mark_safe
#由于没有计算时间差的过滤器 ，所以我们的自己定义一个，如下
register = template.Library()  # register的名字是固定的,不可改变
@register.filter  #过滤器
def yuanlingtime(createtime):
    #计算时间差：当前的时间减去创建的时间
    now_time = datetime.datetime.now()
    user_create_time = datetime.datetime(year=createtime.year,month=createtime.month,day=createtime.day,hour=createtime.hour,minute=createtime.minute,second=createtime.second)
    ret = now_time-user_create_time
    print("---------",ret)  #5 days, 15:51:47.855688
    print(type(ret))  #<class 'datetime.timedelta'>
    return mark_safe(str(ret)[:-17])  #mark_dafe只是做一个安全机制，和safe过滤器一样，安全之后返回
# print(datetime.datetime(year=2017,month=2,day=5))  #2017-02-05 00:00:00











