#!usr/bin/env python
# -*- coding:utf-8 -*-
d = {"a":1,"b":3}
# d.pop("a")
# print(d)
print(list(d.keys()))  #['a', 'b']
for i in list(d.keys()):
    print(i)