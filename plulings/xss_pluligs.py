#!usr/bin/env python
# -*- coding:utf-8 -*-

# def filter_xss(html_str):
#     valid_tag_list = ["p", "div", "a", "img", "html", "body", "br", "strong", "b"]#所有的合法标签
#
#     valid_dict = {"p": ["id", "class"], "div": ["id", "class"]}   #合法的标签和属性
#     from bs4 import BeautifulSoup
#     soup = BeautifulSoup(html_str,"html.parser")  #soup----相当于document
#     #查找非法标签
#     for ele in soup.find_all():
#         if ele.name not in valid_dict:  #所有的标签名
#             '''如果不在合法的列表里面，就给删除了'''
#             # ele.clear()  #清空
#             ele.decompose()
#         # 查找非法属性
#         else:
#             attrs = ele.atts  # p {"id":12,"class":"d1","egon":"dog"}
#             print(attrs)
#             l = []
#             for k in attrs:
#                 if k not in valid_dict[ele.name]:
#                     l.append(k)
#             for i in l:
#                 del attrs[i]
#     print(soup)
#     return soup.decode()




def filter_xss(html_str):
    valid_tag_list = ["p", "div", "a", "img", "html", "body", "br", "strong", "b"]
    valid_dict = {"img":["src","alt"],"p": ["id", "class"], "div": ["id", "class"]}
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html_str, "html.parser")  # soup  ----->  document
    ######### 改成dict
    for ele in soup.find_all():
        # 过滤非法标签
        if ele.name not in valid_dict:
            ele.decompose()
        # 过滤非法属性
        else:
            attrs = ele.attrs  # p {"id":12,"class":"d1","egon":"dog"}
            l = []
            for k in attrs:
                if k not in valid_dict[ele.name]:
                    l.append(k)
            for i in l:
                del attrs[i]
    print(soup)
    return soup.decode()
