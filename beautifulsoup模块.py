#!usr/bin/env python
# -*- coding:utf-8 -*-

html_doc = """

<html>
 <head>
  <title>
   The Dormouse's story
  </title>
 </head>
 <body>
  <p class="title">
   <b>
    The Dormouse's story
   </b>
  </p>
  <div id="d1" class="d1">
    <b>
    The Dormouse's story2
    </b></div>
  <p class="story">
   Once upon a time there were three little sisters; and their names were
   <a class="sister0" href="http://example.com/elsie" id="link1">
    Elsie
   </a>
   ,
   <a class="sister1" href="http://example.com/lacie" id="link2">
    Lacie
   </a>
   and
   <a class="sister2" href="http://example.com/tillie" id="link3">
    Tillie
   </a>
   ;
and they lived at the bottom of a well.
  </p>
   <script>alert(1234)</script>
  <p class="story sister2">
   ...
  </p>
 </body>
</html>
"""
# 第一步:实例化对象
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_doc,"html.parser")
# 第二步：美化
print(soup.prettify())
# 第三步:查找标签
print(soup.a)  #只能找到符合条件的第一个标签
print(soup.find("a")) #只能找到符合条件的第一个标签
print(soup.find_all("a"))  #找到所有的a标签
print(soup.a["class"])  #找到a标签的class属性
print(soup.find_all(name="a"))#找所有标签名是a标签的
print(soup.find_all(attrs={"class":"sister1"}))#找属性是class=sister1的
print(soup.find_all(name="a",attrs={"class":"sister1"}))#找a标签并且属性是class=sister1的

# ===========================
for ele_a in soup.find_all("a"):
    print(ele_a.attrs)  #找出a标签的所有的属性
    print(ele_a["href"])  #找出所有的a标签的href属性
    print(ele_a["class"])  #找出所有的a标签的class属性

for ele_a in soup.find_all("a"):
    print(ele_a.attrs)  #找出a标签的所有属性
    del ele_a["class"]  #删除a标签的class属性
#
for ele_a in soup.find_all("a"):
    print(ele_a)  #找出a标签


for ele in soup.find_all():
    if ele.attrs:
        '''如果有属性'''
        if ele.attrs.get("class"):
            '''如果得到class属性'''
            print(ele.attrs)
            del ele["class"]
print(soup)


for ele_a in soup.find_all("script"):
    print(ele_a.string)  #所有a标签的文本
    print(ele_a.text)    #所有a标签的文本
    ele_a.string.replace_with("//别瞎玩")  #替换a标签的文本
print(soup)


