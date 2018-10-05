# encoding: utf-8
__author__ = 'wuyou'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from ReadWriteExcel import ReadWriteExcel
from OperaLib import OperaLib
from CreateData import CreateData
excel = ReadWriteExcel()
opra = OperaLib()
gen = CreateData()
#body体结构格式
#appHouses[]，coownerInfo[]，feeExtraInfoList[]，modelBusinessData[]，recordCarList[]
#recordLoanAttach[]，recordLoanContact[]，recordLoanHouse[]，recordRentList[]，tLonAccountList[]
#customerInfo{}，zhongAnInfo{}，extendMap = {entry[]=,entry[]=}

#基础配置config excel信息
#config_excel = r'E:\自动化\05_BUS自动化工具开发\02_接口自动化测试框架\BusAutoTest_Version4\Template\config.xlsx'
#config_excel =config_excel.decode('utf-8')
#config_excel = unicode(config_excel, "utf-8")
default_para_sheet ='default_para'
para_config_sheet ='para_config'

class GenBase():
	#从excel获取name，value信息，以list返回
	def get_default_name_value_list(self,config_excel):
		end = excel.get_excel_row_count(config_excel, default_para_sheet)
		namelist = excel.colname_read_excel_return_list(config_excel, default_para_sheet,'B', 2, end)
		valuelist = excel.colname_read_excel_return_list(config_excel, default_para_sheet,'C', 2, end)
		return namelist,valuelist

	#获取结构名list
	def get_stru_name_list(self,config_excel):
		end = excel.get_excel_row_count(config_excel, default_para_sheet)
		stru_namelist = excel.colname_read_excel_return_list(config_excel, default_para_sheet, 'A', 2, end)
		while 'None' in stru_namelist:
			stru_namelist.remove('None')
		return stru_namelist

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


	#将list放入body体
	def addlist_to_body(self,child,new_dict_list,body_dict):
		tmp = {child: new_dict_list}
		opra.modify_dict_data(tmp,body_dict)
		return body_dict
	#将dict放入body体
	def adddict_to_body(self,child,new_dict,body_dict):
		tmp = {child: new_dict}
		opra.modify_dict_data(tmp,body_dict)
		return body_dict

	#根据结构位置，将结构拼接成dict
	def join_dict(self,namelist,valuelist,stru_index):
		stru_index = int(stru_index)
		stru_namelist = namelist[stru_index]
		stru_valuelist = valuelist[stru_index]
		stru_dict = opra.lists_to_dict(stru_namelist, stru_valuelist)
		return stru_dict

	#更改随机生成的数据，stru_dict_list需要更改的结构list，stru_name_list需要更改的结构名list，有些需要依赖bodydict的值
	def change_generate_data(self,bodydict,stru_dict_list,stru_name_list):
		for i in range(len(stru_dict_list)):
			stru_dict = stru_dict_list[i]
			stru_name = stru_name_list[i]
#			print stru_name
			if stru_name == 'body':
				stru_dict['approveSuggestAmt'] = gen.get_float_number(100, 100, 0)
				stru_dict['career'] = gen.get_career_choice('F123130103')
				stru_dict['certId'] = gen.get_eighteen_certId(23, 50, 18)
				stru_dict['certType'] = gen.get_certType_choice('B1301')
				stru_dict['companyPhone'] = gen.get_phone(11)
				stru_dict['customerName'] = gen.get_chinese_name(1)
				stru_dict['customerSex'] = gen.get_customerSex_choice()
				stru_dict['degree'] = gen.get_degree_choice()
				stru_dict['email'] = gen.get_normal_email('qq', 'com')
				stru_dict['liveAddress'] = gen.get_liveAddress_choice()
				stru_dict['loanPurpose'] = gen.get_loanPurpose_choice()
				stru_dict['marry'] = gen.get_marry_choice()
				stru_dict['oldAppId'] = gen.get_oldAppId()
				stru_dict['phone'] = gen.get_phone(11)
				stru_dict['livePhone'] = gen.get_phone(11)
				stru_dict['qq'] = gen.get_int_number(1111111, 99999999)
				stru_dict['receiveName'] = stru_dict['customerName']
				stru_dict['company'] = stru_dict['customerName']
				stru_dict['receiveOpen'] = gen.get_accBankName_choice()
				stru_dict['receiveBankCard'] = gen.get_accBankCard_choice(stru_dict['receiveOpen'])
				stru_dict['receiveBranch'] = gen.get_accBankBranch_choice(stru_dict['receiveOpen'])
				stru_dict['repayOpen'] = gen.get_accBankName_choice()
				stru_dict['repayBankCard'] = gen.get_accBankCard_choice(stru_dict['repayOpen'])
				stru_dict['repayBranch'] = gen.get_accBankBranch_choice(stru_dict['repayOpen'])
				stru_dict['repayName'] = stru_dict['customerName']
				stru_dict['riskGrade'] = gen.get_riskGrade_choice('A')
				stru_dict['score'] = gen.get_int_number(1, 100)
				stru_dict['totalAmount'] = gen.get_int_number(500, 500)
			if stru_name in ['tLonAccountList0','tLonAccountList1','tLonAccountList2']:
				if stru_name == 'tLonAccountList0':
					stru_dict['extendFieldString'] = '{"B1309": "952441222", "B1310": "124441", "B1311": "95244222"}'
				if stru_name == 'tLonAccountList1':
					stru_dict['extendFieldString'] = '{"B1309": "9524422", "B1310": "121", "B1311": "952441222"}'
				if stru_name == 'tLonAccountList2':
					stru_dict['extendFieldString'] = '{"B1309": "9524422", "B1310": "121", "B1311": "952441222"}'
				stru_dict['accBankName'] = gen.get_accBankName_choice()
				stru_dict['accBankBranch'] = gen.get_accBankBranch_choice(stru_dict['accBankName'])
				stru_dict['accProvince'] = gen.get_accProvince_choice()
				stru_dict['accCity'] = gen.get_accCity_choice(1000)
				stru_dict['accBankCard'] = gen.get_accBankCard_choice(stru_dict['accBankName'])
				stru_dict['accOwnName'] = bodydict['customerName']
				stru_dict['accAccountName'] = bodydict['customerName']
				stru_dict['accCorpRep'] = bodydict['customerName']
				stru_dict['accOwnPhone'] = bodydict['phone']
				stru_dict['accCertType'] = gen.get_certType_choice('B1301')
				stru_dict['accOwnIdCard'] = bodydict['certId']
				stru_dict['accountType'] = '01'
				stru_dict['trusteeType'] = 'B134003'
				stru_dict['accBankCardBindId'] = gen.get_accBankCardBindId()
				stru_dict['orgnCreditCode'] = '12563'
			if stru_name == 'recordLoanContact':
				stru_dict['contactName'] = gen.get_chinese_name(1)
				stru_dict['contactPhone'] = gen.get_phone(11)
			if stru_name == 'coownerInfo':
				stru_dict['certId'] = gen.get_eighteen_certId(22, 50, 18)
		return	stru_dict_list

	#拼接简单的list类型的结构，如：（ appHouses：[{},{}] ）
	def join_list(self,namelist,valuelist,struindexlist):
		list=[]
		for i in range(len(struindexlist)):
			dict = self.join_dict(namelist, valuelist, struindexlist[i])
			list.append(dict)
		return list

	#获取结构名-结构位置信息的字典
	def get_stru_index(self,config_excel):
		stru_index_dict = {}
		stru_namelist = self.get_stru_name_list(config_excel)
		for i in range(len(stru_namelist)):
			stru_index_dict[stru_namelist[i]] = stru_namelist.index(stru_namelist[i])
		return stru_index_dict

	def create_modelBusinessData_list(self,namelist,valuelist,stru_index_dict):
		modelBusinessData_list = []
		stru_name_list = ['modelBusinessData_modelId26','modelBusinessData_modelId37',\
		                  'modelBusinessData_modelId38','modelBusinessData_modelId39', \
		                  'modelBusinessData_modelId47','modelBusinessData_modelId72',\
		                  'modelBusinessData_modelId51','modelBusinessData_modelId52',\
		                  'modelBusinessData_modelId56','modelBusinessData_modelId83',\
		                  'modelBusinessData_modelId60','modelBusinessData_modelId61',\
		                  'modelBusinessData_modelId64','modelBusinessData_modelId65',\
		                  'modelBusinessData_modelId66','modelBusinessData_modelId74', \
		                  'modelBusinessData_modelId83', 'modelBusinessData_modelId86', \
		                  'modelBusinessData_modelId87', 'modelBusinessData_modelId88']
		for name in stru_name_list:
			dict = self.create_modelBusinessData_dict(namelist,valuelist,name,stru_index_dict[name])
			if name == 'modelBusinessData_modelId26':
				dict['propertyMap']['entry'][4]['value'] = gen.get_oldAppId()
			if name == 'modelBusinessData_modelId74':
				dict['propertyMap']['entry'][1]['value'] = gen.get_oldAppId()
			if name == 'modelBusinessData_modelId39':
				dict['propertyMap']['entry'][10]['value'] = gen.get_oldAppId()
			modelBusinessData_list.append(dict)

		return modelBusinessData_list

	def create_modelBusinessData_dict(self,namelist,valuelist,stru_name,stru_index):
		modelBusinessData_dict = {}
		id = (stru_name.split('Id'))[1]
		modelBusinessData_dict['modelId'] = id
		entrydict = self.create_entry_dict(namelist, valuelist, stru_index)
		modelBusinessData_dict['propertyMap'] = entrydict
		return modelBusinessData_dict

	def create_entry_dict(self,namelist,valuelist,stru_index):
		entrylist = []
		keylist = namelist[stru_index]
		valuelist = valuelist[stru_index]
		for i in range(len(keylist)):

			entrydict = {}
			entrydict['key'] = keylist[i]
			entrydict['value'] = valuelist[i]
			entrylist.append(entrydict)
		entrydict = {'entry':entrylist}
		return entrydict


	#拼接head数据
	def join_head(self,namelist,valuelist,headindex):
		headdict = self.join_dict(namelist,valuelist,headindex)
		return headdict

	#拼接body数据
	def join_body(self,namelist,valuelist,stru_index_dict):
		#拼接basebody数据，change_generate_data更改body需要随机生成的数据
		body_dict = self.join_dict(namelist,valuelist,stru_index_dict['body'])
		body_dictlist = self.change_generate_data(body_dict,[body_dict],['body'])
		body_dict = body_dictlist[0]

		appHouses_dictlist = self.join_list(namelist,valuelist,[stru_index_dict['appHouses']])
		customerInfo_dict = self.join_dict(namelist,valuelist,stru_index_dict['customerInfo'])
		coownerInfo_dictlist = self.join_list(namelist,valuelist,[stru_index_dict['coownerInfo']])
		coownerInfo_dictlist = 	self.change_generate_data(body_dict,coownerInfo_dictlist,['coownerInfo'])

		feeindexlist = [stru_index_dict['feeExtraInfoList0'],stru_index_dict['feeExtraInfoList1'], \
		                stru_index_dict['feeExtraInfoList2'],stru_index_dict['feeExtraInfoList3'], \
		                stru_index_dict['feeExtraInfoList4'],stru_index_dict['feeExtraInfoList5'], \
		                stru_index_dict['feeExtraInfoList6'],stru_index_dict['feeExtraInfoList7'], \
		                stru_index_dict['feeExtraInfoList8'],stru_index_dict['feeExtraInfoList9'], \
		                stru_index_dict['feeExtraInfoList10'],stru_index_dict['feeExtraInfoList11'],\
						stru_index_dict['feeExtraInfoList12'],stru_index_dict['feeExtraInfoList13'],\
						stru_index_dict['feeExtraInfoList14'],stru_index_dict['feeExtraInfoList15'],\
						stru_index_dict['feeExtraInfoList16']]

		feeExtraInfoList_dictlist = self.join_list(namelist,valuelist,feeindexlist)

		modelBusinessData_dictlist =  self.create_modelBusinessData_list(namelist,valuelist,stru_index_dict)

		recordCarList_dictlist = self.join_list(namelist, valuelist, [stru_index_dict['recordCarList']])

		Attachindexlist = [stru_index_dict['recordLoanAttach0'],stru_index_dict['recordLoanAttach1'], \
		                   stru_index_dict['recordLoanAttach2'],stru_index_dict['recordLoanAttach3'],\
						   stru_index_dict['recordLoanAttach4'],stru_index_dict['recordLoanAttach5'],\
						   stru_index_dict['recordLoanAttach6'],stru_index_dict['recordLoanAttach7'],\
						   stru_index_dict['recordLoanAttach8']]
		recordLoanAttach_dictlist = self.join_list(namelist, valuelist, Attachindexlist)
		recordLoanContact_dictlist = self.join_list(namelist, valuelist, [stru_index_dict['recordLoanContact']])
		recordLoanContact_dictlist = self.change_generate_data(body_dict,recordLoanContact_dictlist,['recordLoanContact'])



		recordRentList_dictlist = self.join_list(namelist, valuelist, [stru_index_dict['recordRentList']])
		zhongAnInfo_dict = self.join_dict(namelist, valuelist, stru_index_dict['zhongAnInfo'])

		accountindexlist = [stru_index_dict['tLonAccountList0'],stru_index_dict['tLonAccountList1'],\
		                    stru_index_dict['tLonAccountList2']]
		accountnamelist = ['tLonAccountList0','tLonAccountList1','tLonAccountList2']
		tLonAccountList_dictlist = self.join_list(namelist, valuelist, accountindexlist)
		tLonAccountList_dictlist = 	self.change_generate_data(body_dict,tLonAccountList_dictlist,accountnamelist)

		self.addlist_to_body('appHouses',appHouses_dictlist,body_dict)
		self.adddict_to_body('customerInfo', customerInfo_dict, body_dict)
		self.addlist_to_body('coownerInfo', coownerInfo_dictlist, body_dict)
		self.addlist_to_body('feeExtraInfoList', feeExtraInfoList_dictlist, body_dict)
		self.addlist_to_body('modelBusinessData', modelBusinessData_dictlist, body_dict)
		self.addlist_to_body('recordCarList', recordCarList_dictlist, body_dict)
		self.addlist_to_body('recordLoanAttach', recordLoanAttach_dictlist, body_dict)
		self.addlist_to_body('recordLoanContact', recordLoanContact_dictlist, body_dict)
		self.addlist_to_body('recordRentList', recordRentList_dictlist, body_dict)
		self.adddict_to_body('zhongAnInfo', zhongAnInfo_dict, body_dict)
		self.addlist_to_body('tLonAccountList', tLonAccountList_dictlist, body_dict)

		return body_dict

	def gen_basedata(self, num,config_excel):
		datalist = []
		#num为拼接数据的条数
		for i in range(num):
			#excel获取namelist和valuelist
			list = self.get_default_name_value_list(config_excel)
			namelist = self.get_stru_list(list[0])
			valuelist = self.get_stru_list(list[1])

			#获取结构位置信息字典
			stru_index_dict = self.get_stru_index(config_excel)

			#拼接head数据
			head_dict = self.join_head(namelist,valuelist,stru_index_dict['head'])
			#拼接body数据
			body_dict = self.join_body(namelist,valuelist,stru_index_dict)

			#将拼好的数据放入list中
			datalist.append([head_dict, body_dict])
		return 	datalist


if __name__ == '__main__':
	genbase = GenBase()
	# a = genbase.get_default_name_value_list()
	# namelist = a[0]
	# print 'namelist len: '+str(len(namelist))
	# valuelist = a[1]
	# print 'valuelist len: ' + str(len(valuelist))
	#
	# b = genbase.get_stru_list(namelist)
	# print b
	# c = genbase.get_stru_list(valuelist)
	# print c

	basedata = genbase.gen_basedata(2)
	print basedata
#	url = 'http://123.57.48.237:7082/webservice/loanService?wsdl'
