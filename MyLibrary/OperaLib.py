# encoding: utf-8
__author__ = 'wuyou'

import sys
import os
import copy
import json
import ConfigParser
config = ConfigParser.ConfigParser()
reload(sys)
sys.setdefaultencoding('utf-8')

class OperaLib(object):
	#根据ini文件section，获取option的键值对，并以字典形式返回
	def gen_dict_by_section(self,file,section):
		config.read(file)
		dict = {}
		options = config.options(section)
		for option in options:
			value = config.get(section, option)
			dict[option] =  value
		return 	dict

	# 给list元素添加后缀，后缀名由posfix_num指定
	def add_list_posfix(self, list, posfix_num):
		new_list = [i + str(posfix_num) for i in list]

		return new_list

	# 将两个列表组成成字典
	def lists_to_dict(self, list1, list2):
		L1 = list1
		L2 = list2
		return dict(zip(L1, L2))

	# 获取列表元素个数
	def get_list_count(self, list):
		count = len(list)
		return count

	# 通过字典的值获取对应Key
	def get_dict_keys(self, d, val):
		return [k for k, v in d.items() if v == val]

	# 生成区间数字列表
	def get_number_list(self, start, end):
		listID = range(int(start), int(end))
		return listID

	# 创建空值字典
	def create_none_value_dict(self, lst):
		dict = {}
		dict1 = dict.fromkeys(lst)
		return dict1

	# 创建文件路径
	def make_dir(self, path):
		a = os.path.exists(path)
		if a:
			pass
		else:
			os.makedirs(path)

	# 生成区间数字列表
	def create_id_list(self, start, end):
		listID = range(int(start), int(end))
		return listID

	# 将两个字典变量合并成一个新的字典
	def dicts_merge(self, dict1, dict2):
		newdict = {}
		for key in dict1.keys():
			for value in dict2.values():
				if key == value:
					ls = dict1[key]
					vkey = ls
					kvalue = get_keys(dict2, value)
					newdict[kvalue[0]] = str(vkey)
		return newdict

	# 删除字典中不在给定列表中的key
	def del_dict_key_value(self, para_name_list, whole_para_name_value_dict):
		lst = para_name_list
		dict = whole_para_name_value_dict
		for k in dict.keys():
			if k not in lst:
				dict.pop(k)
		return dict

	# 通过字典批量修改字典中key的值
	def change_dict_values_by_dict(self, change_dict, to_change_dict):
		d1 = change_dict
		d2 = to_change_dict
		d2.update(d1)
		return d2

	# 依次修改字典中的每一个值
	def change_dict_values_each(self, changed_value, changed_key_list, to_change_dict):
		d1 = dict.fromkeys(changed_key_list, changed_value)
		d2 = to_change_dict
		alist = []
		for k1 in d1.keys():
			d3 = copy.deepcopy(d2)
			d3[k1] = d1[k1]
			alist.append(d3)
		return alist

	# 依次修改字典中的每一个值-特殊字符
	def change_dict_values_each_special(self, changed_value, changed_key_list, to_change_dict):
		d1 = dict.fromkeys(changed_key_list, changed_value)
		d2 = to_change_dict
		data_list = []
		para_list = []
		for k1 in d1.keys():
			d3 = copy.deepcopy(d2)
			d3[k1] = d1[k1]
			data_list.append(d3)
			para_list.append(k1)

		return para_list, data_list

	# 依次修改字典中的每一个值为空
	def change_dict_values_null_each(self, changed_key_list, to_change_dict):
		d1 = dict.fromkeys(changed_key_list)
		d2 = to_change_dict
		data_list = []
		para_list = []
		for k1 in d1.keys():
			d3 = copy.deepcopy(d2)
			d3[k1] = d1[k1]
			data_list.append(d3)
			para_list.append(k1)

		return para_list, data_list

	# 获取自增1
	def plusPlus(self, num):
		plusnum = int(num)
		plusnum += 1
		return plusnum

	# 二位元组转换成字符串
	def two_tuple_to_string(self, two_tup):
		conver_str = "".join(two_tup[0])

		return conver_str

	# 批量获取字典list中的key值并以list形式返回
	def get_dict_list_value_for_key(self, key, dict_list):

		value_list = []

		for i in range(len(dict_list)):
			value = dict_list[i][str(key)]
			value_list.append(value)

		return value_list

	def modify_dict_data(self, change_dict, paras_name_value_dict):

		paras_name_value_dict.update(change_dict)

		return paras_name_value_dict

	def transform_data(self, change_str):
		#如果excel里取下来的值是str格式，json解码转换成字典格式，并捕获异常
		if isinstance(change_str,str) or isinstance(change_str, unicode):
			try:
				change_dict = json.loads(change_str,encoding="utf-8")
			except Exception as ex:
				print('ERROR: Parse change_str %s failed\nDetail: %s ' %(change_str,ex))
				change_dict = {"error": str(ex)}

		# 如果excel里取下来的值是dict格式，则可以直接使用
		elif isinstance(change_str,dict):
			print "change_str is a dict, not the str"
			change_dict = copy.deepcopy(change_str)

		else:
			change_dict = {"error": "NotStrOrDict"}
			type1 = type(change_str)
			print type1

		return change_dict