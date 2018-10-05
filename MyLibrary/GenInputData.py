# encoding: utf-8
__author__ = 'wuyou'
import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from GenBase import GenBase
from ReadWriteExcel import ReadWriteExcel
from OperaLib import OperaLib
genbase = GenBase()
excel = ReadWriteExcel()
opra = OperaLib()

#body体结构格式
#appHouses[]，coownerInfo[]，feeExtraInfoList[]，modelBusinessData[]，recordCarList[]
#recordLoanAttach[]，recordLoanContact[]，recordLoanHouse[]，recordRentList[]，tLonAccountList[]
#customerInfo{}，zhongAnInfo{}，extendMap = {entry[]=,entry[]=}

#基础配置config excel信息
# config_excel = r'E:\自动化\05_BUS自动化工具开发\02_接口自动化测试框架\BusAutoTest_Version4\Template\config.xlsx'
# config_excel = unicode(config_excel, "utf-8")
# para_config_sheet ='para_config'

class GenInputData():

	# def __init__(self):
	# 	end = excel.get_excel_row_count(config_excel, para_config_sheet)
	# 	self.para_config_dict = excel.get_excel_name_value_dict(config_excel, para_config_sheet, 'A', 'B', 2, end)
	#
	def get_name_value_dict(self,config_excel,para_config_sheet):
		end = excel.get_excel_row_count(config_excel, para_config_sheet)
		para_config_dict = excel.get_excel_name_value_dict(config_excel, para_config_sheet, 'A', 'B', 2, end)
		return para_config_dict

	def change_point_body(self,colname,data,config_excel,para_config_sheet):
		para_config_dict = self.get_name_value_dict(config_excel,para_config_sheet)
		file = para_config_dict['testpoint_file']
		file =file.decode('utf-8')
		sheet = para_config_dict['testpoint_sheet']
		namevaluelist = self.get_default_name_value_list(file,sheet,'F',colname)
		change_str_list = namevaluelist[0]
		valuelist = namevaluelist[1]


	#从para excel获取name，value信息，以list返回
	def get_default_name_value_list(self,file,sheet,col1,col2):
		end = excel.get_excel_row_count(file, sheet)
		namelist = excel.colname_read_excel_return_list(file, sheet,col1, 2, end)
		valuelist = excel.colname_read_excel_return_list(file, sheet,col2, 2, end)
		return namelist,valuelist

	#将整列list，以tag分隔，变成小的structure list
	def get_stru_list(self,list):
		structureall_list = []
		liststr = ' '.join(list)
		structurestrlist = liststr.split(' tag')
		for i in range(len(structurestrlist)):
			structurelist = structurestrlist[i].split(' ')
			while '' in structurelist:
				structurelist.remove('')
			if structurelist != []:
				structureall_list.append(structurelist)
		return 	structureall_list

	def change_body(self,ex_namelist, ex_valuelist,ex_struindex_dict,body):

		excel_bodydict = self.join_dict(ex_namelist, ex_valuelist, ex_struindex_dict['body'])
		basebody = self.changedict_to_base(excel_bodydict,body)

		# 按照excel更改appHouses结构
		ex_appHouses_dictlist = self.join_list(ex_namelist,ex_valuelist,[ex_struindex_dict['appHouses']])
		basebody = self.changelist_to_base(ex_appHouses_dictlist, body, 'appHouses')

		#更改customerInfo结构
		ex_customerInfo_dict = self.join_dict(ex_namelist, ex_valuelist, ex_struindex_dict['customerInfo'])
		basebody = self.change_dictstru_to_base(ex_customerInfo_dict, body,'customerInfo')

		# 更改coownerInfo结构
		ex_coownerInfo_dictlist = self.join_list(ex_namelist, ex_valuelist, [ex_struindex_dict['coownerInfo']])
		basebody = self.changelist_to_base(ex_coownerInfo_dictlist, body, 'coownerInfo')

		# 更改feeExtraInfoList结构
		feeindexlist = [ex_struindex_dict['feeExtraInfoList0'],ex_struindex_dict['feeExtraInfoList1'], \
		                ex_struindex_dict['feeExtraInfoList2'],ex_struindex_dict['feeExtraInfoList3'], \
		                ex_struindex_dict['feeExtraInfoList4'],ex_struindex_dict['feeExtraInfoList5'], \
		                ex_struindex_dict['feeExtraInfoList6'],ex_struindex_dict['feeExtraInfoList7'], \
		                ex_struindex_dict['feeExtraInfoList8'],ex_struindex_dict['feeExtraInfoList9'], \
		                ex_struindex_dict['feeExtraInfoList10'],ex_struindex_dict['feeExtraInfoList11'],\
						ex_struindex_dict['feeExtraInfoList12'],ex_struindex_dict['feeExtraInfoList13'],\
						ex_struindex_dict['feeExtraInfoList14'],ex_struindex_dict['feeExtraInfoList15'],\
						ex_struindex_dict['feeExtraInfoList16']]

		ex_feeExtraInfoList_dictlist = self.join_list(ex_namelist,ex_valuelist,feeindexlist)
		basebody = self.changelist_to_base(ex_feeExtraInfoList_dictlist, body, 'feeExtraInfoList')

		# 更改modelBusinessData结构  复杂
		stru_name_list = ['modelBusinessData_modelId26','modelBusinessData_modelId37',\
		                  'modelBusinessData_modelId38','modelBusinessData_modelId39', \
		                  'modelBusinessData_modelId47','modelBusinessData_modelId72',\
		                  'modelBusinessData_modelId51','modelBusinessData_modelId52', \
		                  'modelBusinessData_modelId56','modelBusinessData_modelId83',\
		                  'modelBusinessData_modelId60','modelBusinessData_modelId61',\
		                  'modelBusinessData_modelId64','modelBusinessData_modelId65',\
		                  'modelBusinessData_modelId66','modelBusinessData_modelId74', \
		                  'modelBusinessData_modelId83', 'modelBusinessData_modelId86', \
		                  'modelBusinessData_modelId87', 'modelBusinessData_modelId88']
		modelindexlist = []
		for name in stru_name_list:
			modelindexlist.append(ex_struindex_dict[name])

		ex_modelBusinessData_dictlist = self.join_list(ex_namelist, ex_valuelist, modelindexlist)
		basebody = self.change_modelBusinessData(ex_modelBusinessData_dictlist,body)

		# 更改recordCarList结构
		ex_recordCarList_dictlist = self.join_list(ex_namelist, ex_valuelist, [ex_struindex_dict['recordCarList']])
		basebody = self.changelist_to_base(ex_recordCarList_dictlist, body, 'recordCarList')

		# 更改recordLoanAttach结构
		Attachindexlist = [ex_struindex_dict['recordLoanAttach0'],ex_struindex_dict['recordLoanAttach1'], \
		                   ex_struindex_dict['recordLoanAttach2'],ex_struindex_dict['recordLoanAttach3'],\
						   ex_struindex_dict['recordLoanAttach4'],ex_struindex_dict['recordLoanAttach5'],\
						   ex_struindex_dict['recordLoanAttach6'],ex_struindex_dict['recordLoanAttach7'],\
						   ex_struindex_dict['recordLoanAttach8']]

		ex_recordLoanAttach_dictlist = self.join_list(ex_namelist, ex_valuelist, Attachindexlist)
		basebody = self.changelist_to_base(ex_recordLoanAttach_dictlist, body, 'recordLoanAttach')

		# 更改recordLoanContact结构
		ex_recordLoanContact_dictlist = self.join_list(ex_namelist, ex_valuelist, [ex_struindex_dict['recordLoanContact']])
		basebody = self.changelist_to_base(ex_recordLoanContact_dictlist, body, 'recordLoanContact')

		# 更改recordRentList结构
		ex_recordRentList_dictlist = self.join_list(ex_namelist, ex_valuelist, [ex_struindex_dict['recordRentList']])
		basebody = self.changelist_to_base(ex_recordRentList_dictlist, body, 'recordRentList')

		# 更改zhongAnInfo结构
		ex_zhongAnInfo_dict = self.join_dict(ex_namelist, ex_valuelist, ex_struindex_dict['zhongAnInfo'])
		basebody = self.change_dictstru_to_base(ex_zhongAnInfo_dict, body, 'zhongAnInfo')

		# 更改tLonAccountList结构
		accountindexlist = [ex_struindex_dict['tLonAccountList0'],ex_struindex_dict['tLonAccountList1'], \
		                    ex_struindex_dict['tLonAccountList2']]
		ex_tLonAccountList_dictlist = self.join_list(ex_namelist, ex_valuelist, accountindexlist)

		basebody = self.changelist_to_base(ex_tLonAccountList_dictlist, body, 'tLonAccountList')

		return basebody

	def change_modelBusinessData(self,exceldictlist,body):

		for i in range(len(exceldictlist)):
			list2 = body['modelBusinessData'][i]['propertyMap']['entry']
			dict1 = exceldictlist[i]
			for j in range(len(list2)):
				cutedict = list2[j]
				if dict1[cutedict['key']] != 'None' and dict1[cutedict['key']] != 'yes':
					cutedict['value'] = dict1[cutedict['key']]
				if dict1[cutedict['key']] == 'None':
					del cutedict['key']
					del cutedict['value']
			while {} in list2:
				list2.remove({})
			if list2 == []:
				del body['modelBusinessData'][i]['propertyMap']
				del body['modelBusinessData'][i]['modelId']

		while {} in body['modelBusinessData']:
			(body['modelBusinessData']).remove({})

		return body


	def join_dict(self, namelist, valuelist, stru_index):
		stru_index = int(stru_index)
		# print "aaaaaaaaaa"
		# print namelist
		# print valuelist
		# print stru_index
		stru_namelist = namelist[stru_index]
		stru_valuelist = valuelist[stru_index]
		stru_dict = opra.lists_to_dict(stru_namelist, stru_valuelist)
		return stru_dict

	#拼接简单的list类型的结构，如：（ appHouses：[{},{}] ）
	def join_list(self,namelist,valuelist,struindexlist):
		list=[]
		for i in range(len(struindexlist)):
			dict = self.join_dict(namelist, valuelist, struindexlist[i])
			list.append(dict)
		return list

	#字典类型的结构更改，如head，bodybase
	def changedict_to_base(self,dict1,dict2):
		for para in dict1.keys():
			if dict1[para] != 'None' and dict1[para] != 'yes':
				dict2[para] = dict1[para]
			if dict1[para] == 'None':
				del dict2[para]
		return dict2

	# 套接字典类型的结构更改，如 （custominfo： {}）
	def change_dictstru_to_base(self,exceldict,body,struname):
		dict1 = exceldict
		dict2 = body[struname]

		for para in dict1.keys():
			if dict1[para] != 'None' and dict1[para] != 'yes':
				dict2[para] = dict1[para]
			if dict1[para] == 'None':
				del dict2[para]
		return body

	#简单的list类型的结构更改
	def changelist_to_base(self,exceldictlist,body,struname):
		baselist = body[struname]
		for i in range(len(exceldictlist)):
			dict1 = exceldictlist[i]
			dict2 = baselist[i]
			for para in dict1.keys():
				if dict1[para] != 'None' and dict1[para] != 'yes':
					dict2[para] = dict1[para]
				if dict1[para] == 'None':
					del dict2[para]
		while {} in baselist:
			baselist.remove({})
		if baselist == []:
			del body[struname]
		return body

	#获取结构名-结构位置信息的字典
	def get_stru_index(self,config_excel,para_config_sheet):
		stru_index_dict = {}
		stru_namelist = self.get_stru_name_list(config_excel,para_config_sheet)
		for i in range(len(stru_namelist)):
			stru_index_dict[stru_namelist[i]] = stru_namelist.index(stru_namelist[i])
		return stru_index_dict

	#获取结构名list
	def get_stru_name_list(self,config_excel,para_config_sheet):
		para_config_dict = self.get_name_value_dict(config_excel,para_config_sheet)
		file = para_config_dict['para_file']
		file =file.decode('utf-8')
		sheet = para_config_dict['para_sheet']
		stru_cloname = para_config_dict['structure']

		end = excel.get_excel_row_count(file, sheet)
		stru_namelist = excel.colname_read_excel_return_list(file, sheet,stru_cloname, 2, end)

		while 'None' in stru_namelist:
			stru_namelist.remove('None')
		return stru_namelist

	def change_all(self,colname,basedata,config_excel,para_config_sheet):
		para_config_dict = self.get_name_value_dict(config_excel,para_config_sheet)
		file = para_config_dict['para_file']
		file =file.decode('utf-8')
		#file = unicode(file, "utf-8")
		sheet = para_config_dict['para_sheet']
		#获取base数据的head和body
		head = basedata[0]
		body = basedata[1]

		# 获取结构位置信息字典
		ex_struindex_dict = self.get_stru_index(config_excel,para_config_sheet)

		# excel获取namelist和valuelist
		list = self.get_default_name_value_list(file,sheet,'B',colname)
		ex_namelist = self.get_stru_list(list[0])
		ex_valuelist = self.get_stru_list(list[1])

		#按照excel更改head结构
		ex_head_dict = self.join_dict(ex_namelist, ex_valuelist, ex_struindex_dict['head'])
		basehead = self.changedict_to_base(ex_head_dict,head)

		# 按照excel更改body结构
		basebody = self.change_body(ex_namelist, ex_valuelist, ex_struindex_dict, body)

		return basehead,basebody

if __name__ == '__main__':
	gen = GenInputData()
	url = 'http://123.57.48.237:7082/webservice/loanService?wsdl'
	# config = gen.get_para_config()
	# print config
	basedata = genbase.gen_basedata(1)
	basedata = basedata[0]
	print basedata
	data = gen.change_all('P',basedata)
	basehead = data[0]
	basebody = data[1]
	print data

	# client = suds.client.Client(url)
	# result = client.service.recordLoan(basehead, basebody)
	# print client.last_sent()
	# print result





