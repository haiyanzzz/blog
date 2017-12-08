# #!usr/bin/env python
# # -*- coding:utf-8 -*-
#
# #吧pid为NULL的筛选出来,说明就是根评论，有值就是子评论
# comment_list=[
# 	 {'id': 154, 'content': '发个', 'farther_comment_id': None},
# 	 {'id': 155, 'content': '你好啊', 'farther_comment_id': None},
# 	 {'id': 156, 'content': '嘻嘻', 'farther_comment_id': 155},
# 	 {'id': 157, 'content': '哎呦', 'farther_comment_id': 156},
# 	 {'id': 158, 'content': '不错。继续加油', 'farther_comment_id': None},
# 	 {'id': 159, 'content': '运往直前', 'farther_comment_id': None},
# 	 {'id': 160, 'content': '加油啦', 'farther_comment_id': 159},
# 	 {'id': 161, 'content': '爱你啊', 'farther_comment_id': 159},
# 	 {'id': 162, 'content': '@undefined\n的说的得分是', 'farther_comment_id': None}
# ]
# # ===========放一个字典，吧id提出来，并且在每一个字典中加一个"children_comment":[]键值对==========
# comment_dict = {}
# for comment in comment_list:
# 	comment["children_comment"] = []
# 	comment_dict[comment["id"]]=comment
# print(comment_dict)   #{1:{"":"","":""},2:{"":"","":""},3:{}}
# # print(comment_list)
# # =================找父级id==================
# comment_tree=[]
# for comment in comment_list:
# 	pid = comment["farther_comment_id"]
# 	if pid:
# 		comment_dict[pid]["children_comment"].append(comment)
# 	else:
# 		'''如果pid为none的时候找一个列表存起来'''
# 		comment_tree.append(comment)
# # print(comment_tree)
#
#
# '''
# comment_tree:
# [
#     {
#         'id': 154,
#         'content': '发个',
#         'farther_comment_id': None,
#         'children_comment': [
#
#         ]
#     },
#     {
#         'id': 155,
#         'content': '你好啊',
#         'farther_comment_id': None,
#         'children_comment': [
#             {
#                 'id': 156,
#                 'content': '嘻嘻',
#                 'farther_comment_id': 155,
#                 'children_comment': [
#                     {
#                         'id': 157,
#                         'content': '哎呦',
#                         'farther_comment_id': 156,
#                         'children_comment': [
#
#                         ]
#                     }
#                 ]
#             }
#         ]
#     },
#     {
#         'id': 158,
#         'content': '不错。继续加油',
#         'farther_comment_id': None,
#         'children_comment': [
#
#         ]
#     },
#     {
#         'id': 159,
#         'content': '运往直前',
#         'farther_comment_id': None,
#         'children_comment': [
#             {
#                 'id': 160,
#                 'content': '加油啦',
#                 'farther_comment_id': 159,
#                 'children_comment': [
#
#                 ]
#             },
#             {
#                 'id': 161,
#                 'content': '爱你啊',
#                 'farther_comment_id': 159,
#                 'children_comment': [
#
#                 ]
#             }
#         ]
#     },
#     {
#         'id': 162,
#         'content': '@undefined\n的说的得分是',
#         'farther_comment_id': None,
#         'children_comment': [
#
#         ]
#     }
# ]
# '''
#
#
#

comment_list=[
	 {'id': 154, 'content': '发个', 'farther_comment_id': None},
	 {'id': 155, 'content': '你好啊', 'farther_comment_id': None},
	 {'id': 156, 'content': '嘻嘻', 'farther_comment_id': 155},
	 {'id': 157, 'content': '哎呦', 'farther_comment_id': 156},
	 {'id': 158, 'content': '不错。继续加油', 'farther_comment_id': None},
	 # {'id': 160, 'content': '加油啦', 'farther_comment_id': 159},
]
resault_dict = {}
for i in comment_list:
	i["children_comment"] = []
	resault_dict[i["id"]] = i
# print(resault_dict)
# resault_dict={
# 	154: {'id': 154, 'content': '发个', 'farther_comment_id': None, 'children_comment': []},
# 	155: {'id': 155, 'content': '你好啊', 'farther_comment_id': None, 'children_comment': []},
# 	156: {'id': 156, 'content': '嘻嘻', 'farther_comment_id': 155, 'children_comment': []},
# 	157: {'id': 157, 'content': '哎呦', 'farther_comment_id': 156, 'children_comment': []},
# 	158: {'id': 158, 'content': '不错。继续加油', 'farther_comment_id': None, 'children_comment': []},
# 	160: {'id': 160, 'content': '加油啦', 'farther_comment_id': 159, 'children_comment': []}
# }
#拿到字典以后找farther_comment_id为NULL的
print(resault_dict)
result_list = []
for j in comment_list:
	pid = j['farther_comment_id']
	if pid:
		resault_dict[pid]['children_comment'].append(j)
	else:
		result_list.append(j)

print(result_list)


# for j in comment_list:   #你在前面的字典的时候就已经给每一个comment里增加了一个children_comment空列表，这时候你在遍历的时候也已经改变了，因为他们用的是用一个引用，一个变了，另一个也跟着变了
# 	pid = j["farther_comment_id"]
# 	if pid :#如果pid有值
# 		resault_dict[pid]["children_comment"].append(j)#找到他对应的pid,并且添加在children_comment列表里面
# 	else:
# 		result_list.append(j)# 没有的话就先存放在一个列表里面
# print(result_list)

