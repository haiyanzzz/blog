#!usr/bin/env python
# -*- coding:utf-8 -*-
from app01 import models
from django.forms import Form
from django.forms import widgets
from django.forms import fields
from django.core.validators import ValidationError
from django.core.validators import RegexValidator
from plulings import xss_pluligs
class RegisterForm(Form):
    username = fields.CharField(
        required=True,
        max_length=16,
        min_length=3,
        error_messages={
            "required": "用户名不能为空",
            "max_length": "长度不能大于16",
            "min_length": "长度不能小于3",
        },
        widget=widgets.TextInput({"placeholder":"请您输入用户名","class":"form-control"})
    )
    password = fields.CharField(
        required=True,
        max_length=16,
        min_length=3,
        error_messages={
            "required": "密码不能为空",
            "max_length": "长度不能大于16",
            "min_length": "长度不能小于3",
        },
        widget=widgets.PasswordInput({"placeholder":"请您输入数字与字母组合的密码","class":"form-control"})
    )
    password_again = fields.CharField(
        required=True,
        max_length=16,
        min_length=3,
        error_messages={
            "required": "密码不能为空",
            "max_length": "长度不能大于16",
            "min_length": "长度不能小于3",
        },
        widget=widgets.PasswordInput({"placeholder": "请您再次输入密码", "class": "form-control"})
    )
    email = fields.EmailField(
        required=True,
        error_messages={
            "required":"邮箱不能为空",
            "invalid":"邮箱格式有误"
        },
        widget = widgets.EmailInput({"placeholder": "请输入您的邮箱", "class": "form-control"})
    )
    tel = fields.CharField(
        required=True,
        max_length=11,
        min_length=11,
        error_messages={
            "required":"手机号码不能为空",
            "max_length":"长度必须是11位，请你正确输入",
            "min_length":"长度必须是11位，请你正确输入",
        },
        validators=[RegexValidator("\d+","密码只能是数字")],
        widget=widgets.TextInput({"placeholder": "请您输入你的电话，要求11位哦", "class": "form-control"})
    )
    nickname = fields.CharField(
        required=True,
        error_messages={
            "required": "昵称不能为空",
        },
        widget=widgets.TextInput({"placeholder": "请输入你的昵称", "class": "form-control"})
    )
    #自定义用户名验证：局部钩子
    def clean_username(self):
        username = self.cleaned_data.get("username")
        valid = models.UserInfo.objects.filter(username = username).first()
        if valid:
            raise ValidationError("用户名已存在")
        return username
    #自定义密码验证：
    def clean_password(self):
        password = self.cleaned_data.get("password")
        if password.isdigit():
            raise ValidationError("密码不能是纯数字")
        else:
            return password
    #自定义全局钩子：验证两次密码是否一致
    def clean(self):
        if self.cleaned_data.get("password") == self.cleaned_data.get("password_again"):
            return self.cleaned_data
        else:
            raise  ValidationError("两次密码不一致")


class ArticleForm(Form):
    title = fields.CharField(max_length=20, error_messages={"required": "不能为空"},widget=widgets.TextInput(attrs={"class":"title_input"}))

    content = fields.CharField(error_messages={"required": "不能为空",}, widget=widgets.Textarea())


    def clean_content(self):
        html_str=self.cleaned_data.get("content")
        clean_content=xss_pluligs.filter_xss(html_str)
        self.cleaned_data["content"]=clean_content
        return self.cleaned_data.get("content")





