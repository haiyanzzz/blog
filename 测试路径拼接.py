#!usr/bin/env python
# -*- coding:utf-8 -*-
import os
print(os.path.abspath(__file__))  #E:\blog\测试路径拼接.py
print(os.path.dirname(os.path.abspath(__file__))) #E:\blog
print(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))) #E:\blog
Base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
print(os.path.join(Base,"index","hhh"))