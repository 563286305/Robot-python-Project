# encoding: utf-8
__author__ = 'wuyou'

import sys
reload(sys)
sys.setdefaultencoding('utf-8')
from GenInputData import GenInputData
from OperaLib import OperaLib
from GenBase import GenBase
from QuerySQL import QuerySQL
from ReadWriteExcel import ReadWriteExcel
from CreateData import CreateData
from Interface import Interface
import suds
import copy

gen = GenInputData()
create = CreateData()
#uu = UserCenter()
oper = OperaLib()
genbase = GenBase()
db = QuerySQL()
#amt = ContractAmt()
#quo = Quota()
excel = ReadWriteExcel()
inf = Interface()


#body体结构格式
#appHouses[]，coownerInfo[]，feeExtraInfoList[]，modelBusinessData[]，recordCarList[]
#recordLoanAttach[]，recordLoanContact[]，recordLoanHouse[]，recordRentList[]，tLonAccountList[]
#customerInfo{}，zhongAnInfo{}，extendMap = {entry[]=,entry[]=}

#基础配置config excel信息
config_excel = r'E:\自动化\05_BUS自动化工具开发\02_接口自动化测试框架\BusAutoTest_Version4\Template\config.xlsx'
config_excel = unicode(config_excel, "utf-8")
para_config_sheet ='para_config'
env1_sheet = 'env_1'
env2_sheet = 'env_2'
env3_sheet = 'env_3'

class RunCase():
	def __init__(self):
		end = excel.get_excel_row_count(config_excel, para_config_sheet)
		self.para_config_dict = excel.get_excel_name_value_dict(config_excel, para_config_sheet, 'A', 'B', 2, end)

		end1 = excel.get_excel_row_count(config_excel, env1_sheet)
		self.env1_dict = excel.get_excel_name_value_dict(config_excel, env1_sheet, 'A', 'B', 2, end1)

		end2 = excel.get_excel_row_count(config_excel, env2_sheet)
		self.env2_dict = excel.get_excel_name_value_dict(config_excel, env2_sheet, 'A', 'B', 2, end2)

		end3 = excel.get_excel_row_count(config_excel, env3_sheet)
		self.env3_dict = excel.get_excel_name_value_dict(config_excel, env3_sheet, 'A', 'B', 2, end3)

#获取用户中心数据
	def get_center_info(self,body):
		centerlist= []
		center = inf.get_user_center_info(body['customerName'], body['certId'])
		uumCustNo = center[0]
		uumUserId = center[1]
		print "User center registering......"
		print "uumCustNo: " + str(uumCustNo)
		print "uumUserId: " + str(uumUserId)
		centerlist.append(uumCustNo)
		centerlist.append(uumUserId)
		return centerlist
#用户中心数据更新到database
	def update_center(self,body,centerinfo):
		print "Updating user center info......"
		if body['modelBusinessData'][0]['propertyMap']['entry'][0]['key'] == 'uumCustNo':
			body['modelBusinessData'][0]['propertyMap']['entry'][0]['value'] = centerinfo[0]
		else:
			print "Update uumCustNo to base failed!"
		if body['modelBusinessData'][0]['propertyMap']['entry'][1]['key'] == 'uumUserId':
			body['modelBusinessData'][0]['propertyMap']['entry'][1]['value'] = centerinfo[1]
		else:
			print "Update uumUserId to base failed!"

		return body
#合同金额试算
	def quo_amt(self,data,env):
		body = data[1]
		# 合同金额试算，得到合同金额
		Amt = inf.get_contract_amt(body,env)
		contractAmt = Amt['contractAmt']
		print "Calculating contractAmt......"
		print "合同金额: " + str(contractAmt)
		return contractAmt
#费用合计试算
	def cal_amtall(self,data,env):
		body = data[1]
		# 费用合计试算
		Amt = inf.get_contract_amt(body,env)
		AmtAll = Amt['fyhj_amt']
		print "Calculating AmtAll......"
		print "费用合计: " + str(AmtAll)
		return AmtAll

	def center_noamt_noquo_db(self,env,data):
		# url = env['url']
		# head = data[0]
		body = data[1]
		centerinfo = self.get_center_info(body)
		body = self.update_center(body,centerinfo)
		print "Send Data: "
		print data
		return data

	def center_amt_quo_db(self,env,data,quo_model):
		# url = env['url']
		# head = data[0]
		body = data[1]
		centerinfo = self.get_center_info(body)
		customerId = centerinfo[1]
		body = self.update_center(body,centerinfo)
		contractAmt = self.quo_amt(data,env)
		(quota_r1, quota_r2) = inf.get_quota_apply_use(quo_model,body, contractAmt,customerId)
		# print quota_r1
		# print quota_r2
		print "Send Data: "
		print data
		return data

	def run_loan_interface(self,env,data):
		url = env['url']
		client = suds.client.Client(url)
		head = data[0]
		body = data[1]
		try:
			result = client.service.recordLoan(head,body)
#			print client.last_sent()
		except suds.transport.TransportError, ex:
			print "TransportError: "+ str(ex)
		except suds.WebFault, ex:
			print "WebFault Error: "+ str(ex)
		except suds.timeout, ex:
			print "Timeout Error: "+ str(ex)
		if result['transHead']['retCode'] == '000000':
			transHead = result['transHead']
			print "实际返回： "
			print result['transHead']
			appId = result['transBody']['entity'][0][0]
			print 'appId: '
			print result['transBody']['entity'][0][0]
			return transHead,appId
		elif result['transHead']['retCode'] == '999999':
			print "实际返回： "
			print result['transHead']
			transHead = result['transHead']
			appId = "null"
			return transHead,appId
#选择环境
	def chose_env(self,envnum):
		if int(envnum) == 3:
			env = self.env3_dict
		if int(envnum) == 2:
			env = self.env2_dict
		if int(envnum) == 1:
			env = self.env1_dict
		return env

	#检查是否需要圈存，N8701需要圈存，N8702不需要圈存
	def check_quo(self,productid,dbinfo):
#		dbinfo['dbname'] ='sit_base_db'
		dbinfo['dbname'] ='test_base_db'
		conlist = db.connectdb(dbinfo)
		server = conlist[0]
		con = conlist[1]
		sql = 'SELECT IS_USE_QUOTA FROM t_prd_quota WHERE product_id = ' + str(productid)
		result = db.get_one_value(con,sql)
		server.stop()
		con.close()
		return result

	#检查圈存类型
	def check_quo_model(self,productid,envinfo):
#		envinfo['dbname'] ='sit_base_db'
		envinfo['dbname'] ='test_base_db'
		conlist = db.connectdb(envinfo)
		server = conlist[0]
		con = conlist[1]
		sql = 'SELECT PRD_FUND_TYPE FROM t_prd_quota WHERE product_id = ' + str(productid)
		result = db.get_one_value(con,sql)
		server.stop()
		con.close()
		return result
#检查是否为自主支付
	def check_self_pay(self,productid,envinfo):
#		envinfo['dbname'] ='sit_base_db'
		envinfo['dbname'] ='test_base_db'
		conlist = db.connectdb(envinfo)
		server = conlist[0]
		con = conlist[1]
		sql = 'SELECT IS_SELF_PAY FROM t_prd_product WHERE PRODUCT_ID=' + str(productid) +' ORDER BY VERSION DESC LIMIT 1'
		print sql
		result = db.get_one_value(con,sql)
		server.stop()
		con.close()
		return result

#更改工单费用信息
	def update_fee(self,data,feename,feevalue):
		body = data[1]
		feelist = body['feeExtraInfoList']
		for fee in feelist:
			if fee['infoName'] == feename:
				fee['infoValue'] = feevalue
		return data

	#根据期数评级在数据库获取各项费率
	def get_platform_rate(self,data,env):
		rate = {}
#		env['dbname'] = 'sit_base_db'
		env['dbname'] ='test_base_db'
		body = data[1]
		riskGrade = body['riskGrade']
		productId = body['productId']
		term = body['loanTerm']
		(server,con,port) = db.connectdb(env)
		#年利率,平息基础利率,咨询服务费,机构服务费,风险备用金,保险费率,担保费率,
		#贷后管理费率,仲裁服务费率,出函费率,打包价年利率,产品包装月利率,
		rate_table = {'yearRate':'t_prd_year_rate', 'approveDstRate':'t_prd_quell_base_rate',\
				'serviceRate':'t_prd_consult_service_rate', 'instServiceRate':'t_prd_inst_service_rate',\
				'riskFundRate':'t_prd_risk_fund','insurance':'t_prd_insurance_rate',\
				'guarantee':'t_prd_guarantee_rate','loanAfterFee':'t_prd_manager_rate',\
				'arbitration':'t_prd_arbitration_rate','letter':'t_prd_letter_rate'}

		rate_dict = {}
		for key in rate_table.keys():
			sql = "SELECT LEVEL_" + riskGrade+" FROM "+ rate_table[key] + " WHERE \
				PRODUCT_ID='"+productId+"' AND times='"+term+"' ORDER BY create_time DESC LIMIT 1"
			rate = db.get_one_value(con, sql)
			rate = str(rate)
			rate_dict[key] = rate

		server.stop()
		con.close()
		return rate_dict

#更新进件数据中的各项费率（改成和基础平台相同值）
	def update_feerate(self,data,plantform):
		body = data[1]
		if body.has_key('approveDstRate'):
			body['approveDstRate'] = plantform['approveDstRate']
		if body.has_key('yearRate'):
			body['yearRate'] = plantform['yearRate']
		return data
	def case_term_risk(self,envno,productidlist):
		#环境选择，获取url和数据库信息
		env = self.chose_env(envno)
		print "Env: " + str(envno)
		resultdict_list = []
		appidlist = []

		#获取测试用例excel和sheet
		point_file = self.para_config_dict['testpoint_file']
		point_file =point_file.decode('utf-8')
		point_sheet = self.para_config_dict['testpoint_sheet']

		result_file = self.para_config_dict['testpoint_result_file']
		result_file =result_file.decode('utf-8')
		result_sheet = self.para_config_dict['testpoint_result_sheet']

		excel.copyExcel(point_file, result_file)

		#根据给出的产品list循环进件
		for product in productidlist:
			print "****************************************************"
			#如果list中有子list，证明为子产品，子产品需要使用相同的用户分别进件
			resultdict = {}
			if isinstance(product, list):
				for productid in product:

					#检测产品在excel参数表中的位置，是否需要圈存
					quolist = self.check_product(productid, env)
					colname = quolist[0]
					quo_result = quolist[1]
					quo_model = quolist[2]
					point_colname = quolist[3]
					self_pay = quolist[4]

					#根据产品获取测试点变更参数list， 以及是否运行该用例list
					end = excel.get_excel_row_count(point_file, point_sheet)
					index_list = excel.colname_read_excel_return_list(point_file, point_sheet,'A', 2, end)
					point_str_list = excel.colname_read_excel_return_list(point_file, point_sheet,'F', 2, end)
					valuelist = excel.colname_read_excel_return_list(point_file, point_sheet,point_colname, 2, end)

					#删除不运行的用例
					for i in range(len(valuelist)):
						if valuelist[i] == 'None':
							point_str_list[i] = 'None'
							index_list[i] =  'None'
					while 'None' in point_str_list:
						point_str_list.remove('None')
						index_list.remove('None')

					#获取需要运行的测试例数量，并生成相应数量的基础数据
					case_num = len(point_str_list)
					basedatalist = genbase.gen_basedata(case_num,config_excel)

					for i in range(case_num):
						#复制基础数据
						basedata = basedatalist[i]
						basedatanew = copy.deepcopy(basedata)
						#两个子产品使用相同的用户数据，但是前端第三方工单号不能相同
						basedatanew[1]['oldAppId'] = create.get_oldAppId()
						print "Updating parameter ......"
						basedatanew = gen.change_all(colname, basedatanew,config_excel,para_config_sheet)

						#将测试点参数 更新到 进件参数中
						point_dict = oper.transform_data(point_str_list[i])
						oper.modify_dict_data(point_dict,basedatanew[1])

						if self_pay == 'N8701':
							#是自主支付,根据期数评级，更改进件参数的各费率
							plantform = self.get_platform_rate(basedatanew,env)
							basedatanew = self.update_feerate(basedatanew,plantform)
							#计算费用合计，更改进件参数B6655等于费用合计
							amtall = self.cal_amtall(basedatanew,env)
							basedatanew = self.update_fee(basedatanew,'B6655',amtall)

						if quo_result == 'N8702':
							#不需要圈存
							basedatanew = self.center_noamt_noquo_db(env, basedatanew)
						if quo_result == 'N8701':
							#需要圈存
							basedatanew = self.center_amt_quo_db(env, basedatanew, quo_model)
						result = self.run_loan_interface(env,basedatanew)

						print "Result : "
						print str(result)
						if str(len(result))=='2':
							appid = result[1]
							if appid != 'null':
								appidlist.append(appid)
						if result[0]['retCode'] == '000000':
							result_finnal = 'PASS'
						else:
							result_finnal = 'FAILED'
						resultdict[index_list[i]] = result_finnal
					excel.resultdictAddExcel(result_file, result_sheet, resultdict, point_colname)
					resultdict_list.append(resultdict)
			# 如果list中没有子list，则单独进件
			else:
				print "****************************************************"
				productid = product
				# 检测产品在excel参数表中的位置，是否需要圈存，以及圈存模式
				quolist = self.check_product(productid, env)
				colname = quolist[0]
				quo_result = quolist[1]
				quo_model = quolist[2]
				point_colname = quolist[3]
				self_pay = quolist[4]

				#根据产品获取测试点变更参数list， 以及是否运行该用例list
				end = excel.get_excel_row_count(point_file, point_sheet)
				index_list = excel.colname_read_excel_return_list(point_file, point_sheet,'A', 2, end)
				point_str_list = excel.colname_read_excel_return_list(point_file, point_sheet,'F', 2, end)
				valuelist = excel.colname_read_excel_return_list(point_file, point_sheet,point_colname, 2, end)

				#删除不运行的用例
				for i in range(len(valuelist)):
					if valuelist[i] == 'None':
						point_str_list[i] = 'None'
						index_list[i] =  'None'
				while 'None' in point_str_list:
					point_str_list.remove('None')
					index_list.remove('None')

				#获取需要运行的测试例数量，并生成相应数量的基础数据
				case_num = len(point_str_list)
				basedatalist = genbase.gen_basedata(case_num,config_excel)

				for i in range(case_num):
					#复制基础数据
					basedata = basedatalist[i]
					basedatanew = copy.deepcopy(basedata)

					# 根据excel表中的进件参数更改basedata
					basedatanew = copy.deepcopy(basedata)
					print "Updating parameter ......"
					basedatanew = gen.change_all(colname, basedatanew,config_excel,para_config_sheet)
					#将测试点参数 更新到 进件参数中
					point_dict = oper.transform_data(point_str_list[i])
					oper.modify_dict_data(point_dict,basedatanew[1])
					if self_pay == 'N8701':
						#是自主支付,根据期数评级，更改进件参数的各费率
						plantform = self.get_platform_rate(basedatanew,env)
						basedatanew = self.update_feerate(basedatanew,plantform)
						#计算费用合计，更改进件参数B6655等于费用合计
						amtall = self.cal_amtall(basedatanew,env)
						basedatanew = self.update_fee(basedatanew,'B6655',amtall)

					if quo_result == 'N8702':
						# 不需要圈存
						basedatanew = self.center_noamt_noquo_db(env, basedatanew)
					if quo_result == 'N8701':
						# 需要圈存：
						basedatanew = self.center_amt_quo_db(env, basedatanew, quo_model)
					# rate = self.get_platform_rate(basedatanew,env)
					# print rate

					result = self.run_loan_interface(env,basedatanew)
					print "Result : "
					print str(result)
					if str(len(result))=='2':
						appid = result[1]
						if appid != 'null':
							appidlist.append(appid)
					if result[0]['retCode'] == '000000':
						result_finnal = 'PASS'
					else:
						result_finnal = 'FAILED'
					resultdict[index_list[i]] = result_finnal
				excel.resultdictAddExcel(result_file, result_sheet, resultdict, point_colname)
				resultdict_list.append(resultdict)
		return resultdict_list,appidlist

#重复批量进件
	def repeat_input(self,envno,productidlist,times):
		appidall=[]
		i = int(times)
		while i > 0:
			(result,appidlist) = self.case_normal_input(envno,productidlist)
			appidall.extend(appidlist)
			i = i-1
		print "生成成功的工单数量： " + str(len(appidall))
		print "工单appid： " , appidall
		return appidall

#正常进件
	def case_normal_input(self,envno,productidlist):
		#环境选择，获取url和数据库信息
		env = self.chose_env(envno)
		print "Env: " + str(envno)

		#根据给出的productid list 生成相应数量的basedata
		num = len(productidlist)
		print "Generating basedata ...... "
		basedatalist = genbase.gen_basedata(num,config_excel)

		appidlist = []

		#根据给出的产品list循环进件
		for i in range(num):
			basedata = basedatalist[i]

			#如果list中有子list，证明为子产品，子产品需要使用相同的用户分别进件
			if isinstance(productidlist[i], list):

				for j in range(len(productidlist[i])):
					print "****************************************************"
					productid = productidlist[i][j]
					#检测产品在excel参数表中的位置，是否需要圈存
					quolist = self.check_product(productid, env)
					colname = quolist[0]
					quo_result = quolist[1]
					quo_model = quolist[2]
					self_pay = quolist[4]
					#根据excel表中的参数更改basedata
					basedatanew = copy.deepcopy(basedata)
					#两个子产品使用相同的用户数据，但是前端第三方工单号不能相同
					basedatanew[1]['oldAppId'] = create.get_oldAppId()
					print "Updating parameter ......"
					basedatanew = gen.change_all(colname, basedatanew,config_excel,para_config_sheet)
					if self_pay == 'N8701':
						#是自主支付,根据期数评级，更改进件参数的各费率
						plantform = self.get_platform_rate(basedatanew,env)
						basedatanew = self.update_feerate(basedatanew,plantform)
						#计算费用合计，更改进件参数B6655等于费用合计
						amtall = self.cal_amtall(basedatanew,env)
						basedatanew = self.update_fee(basedatanew,'B6655',amtall)
					if quo_result == 'N8702':
						#不需要圈存
						basedatanew = self.center_noamt_noquo_db(env, basedatanew)
					if quo_result == 'N8701':
						#需要圈存
						basedatanew = self.center_amt_quo_db(env, basedatanew, quo_model)

					all = self.run_loan_interface(env,basedatanew)
					print "result len: " + str(all)
					if str(len(all))=='2':
						result = all[0]
						appid = all[1]
						if appid != 'null':
							appidlist.append(appid)

					else:
						result = all[0]

				#	print 'appId' + str(result['transBody']['entity'][0][0])

			# 如果list中没有子list，则单独进件
			else:
				print "****************************************************"
				productid = productidlist[i]
				# 检测产品在excel参数表中的位置，是否需要圈存，以及圈存模式
				quolist = self.check_product(productid, env)
				colname = quolist[0]
				quo_result = quolist[1]
				quo_model = quolist[2]
				self_pay = quolist[4]

				# 根据excel表中的参数更改basedata
				basedatanew = copy.deepcopy(basedata)
				print "Updating parameter ......"
				basedatanew = gen.change_all(colname, basedatanew,config_excel,para_config_sheet)
				if self_pay == 'N8701':
					#是自主支付,根据期数评级，更改进件参数的各费率
					plantform = self.get_platform_rate(basedatanew,env)
					basedatanew = self.update_feerate(basedatanew,plantform)
					#计算费用合计，更改进件参数B6655等于费用合计
					amtall = self.cal_amtall(basedatanew,env)
					basedatanew = self.update_fee(basedatanew,'B6655',amtall)

				if quo_result == 'N8702':
					# 不需要圈存
					basedatanew = self.center_noamt_noquo_db(env, basedatanew)
				if quo_result == 'N8701':
					# 需要圈存：
					basedatanew = self.center_amt_quo_db(env, basedatanew, quo_model)

				all = self.run_loan_interface(env,basedatanew)
				print "result len: " + str(all)
				if str(len(all))=='2':
					result = all[0]
					appid = all[1]
					if appid != 'null':
						appidlist.append(appid)
				else:
					result = all[0]

		return result,appidlist

	def check_product(self,productid,envinfo):
		# print self.para_config_dict
		input_file = self.para_config_dict['para_file']
		input_file =input_file.decode('utf-8')
		input_sheet = self.para_config_dict['para_sheet']
		product_index_dict = excel.get_cell_index(input_file, input_sheet,1)
		product = 'product_' + str(productid)
		#判断产品所在进件excel位置
		input_colname = product_index_dict[str(product)]

		#判断产品所在测试点excel位置
		point_file = self.para_config_dict['testpoint_file']
		point_file =point_file.decode('utf-8')
		point_sheet = self.para_config_dict['testpoint_sheet']
		point_index_dict = excel.get_cell_index(point_file, point_sheet,1)
		product = 'product_' + str(productid)
		if point_index_dict.has_key(product):
			point_colname = point_index_dict[product]
		else:
			point_colname = 'NULL'
		#判断是否圈存
		quo_result = self.check_quo(productid, envinfo)
		#判断圈存类型
		quo_model_result = self.check_quo_model(productid, envinfo)
		#判断是否为自主支付产品
		self_pay = self.check_self_pay(productid, envinfo)

		print "Checking product info ......"
		print "Productid: " +str(productid)
		print "input_colname: " + input_colname
		print '是否需要圈存： ' + quo_result
		print '圈存类型： ' + quo_model_result
		print '是否自主支付： ' + self_pay
		return input_colname, quo_result,quo_model_result,point_colname,self_pay

if __name__ == '__main__':
	run = RunCase()
	url = ''
	# productidlist = [137,298,379,380,[403,404],[406,407],408,[409,410],\
	# 				411,[412,413],414,[415,416],417,[430,431],\
	# 				432,[433,434],435,436,438,[439,440,441],442,\
	# 				448,449,450,451,455,456,457]

#	productidlist = [[403,404],[430,431],433,442,432]
	productidlist = [404]
	# print productidlist[0]
	# a = isinstance(productidlist[0], list)
	# print a
#	result = run.case_term_risk(1, productidlist)
	result = run.case_normal_input(1, productidlist)
#	result = run.repeat_input(1,productidlist,3)




