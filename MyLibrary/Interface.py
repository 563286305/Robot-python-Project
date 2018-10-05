# encoding: utf-8
__author__ = 'wuyou'
import json
import sys
import time
import suds
import requests

from CreateData import CreateData
from QuerySQL import QuerySQL
from ReadWriteExcel import ReadWriteExcel

excel = ReadWriteExcel()
create = CreateData()
reload(sys)
sys.setdefaultencoding('utf-8')

db = QuerySQL()

class Interface():
#渠道接口
    def inf_channel(self,appId,productId):
        url = 'http://47.94.40.127:7010/intf/inter//trans!server.intf'
        headers = {'Content-Type': 'application/json,charset=UTF-8'}
        head = {"channel": "","extFiled1": "","extFiled2": "","extFiled3": "","secretKey": "",\
                "sysCode": "","transCode": "CF01","transDate": "2017-07-03",\
                "transSerialNo": "23e64a62-39d7-448e-b51b-a2ced9fd6a0b","transTime": "11:21:18",\
                "transType": "T"}
        body = {"batchNo": "322308223272311", "size":"1",\
                "fundList":[{"appId": "926656427" ,"contractAmt": "310","fundChannelId": "9F",\
                             "productId": "417"}]}

        body['batchNo'] = create.get_oldAppId()
        body['fundList'][0]['appId'] = str(appId)
        body['fundList'][0]['productId'] = str(productId)
        data = {'body': body, 'head': head}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print data
        print r.text
        return r
#电子签章
    def inf_dzqz(self,appId):
        url = 'http://47.94.191.238:7086/sign/intf/inter/trans!server.intf'
        headers = {'Content-Type': 'application/json,charset=UTF-8'}
        head = {'transTime': '', 'transSerialNo': '20150723161316', 'transDate': '', 'sysCode': '1019', 'secretKey': '', 'transCode': 'LS02', 'transType': 'T', 'channel': '1019'}
        body = {'signType': '0', 'appId': '926655169'}
        data =  {'head': head , 'body':body}
        r = requests.post(url, data=json.dumps(data), headers=headers)
        print r.text
        return r.json()['sts'],r.json()['msg']
#生成合同接口
    def inf_generateContract(self,appId):
        url = "http://47.94.40.127:7083/webservice/loanService?wsdl"
        client = suds.client.Client(url)
        result = client.service.generateContract(str(appId))
        result = json.loads(result)
        print result['returnCode']
        print result['returnMsg']
        return result['returnCode'],result['returnMsg']

#查看合同接口
    def inf_seeContract(self,appId):
        url = "http://47.94.40.127:7083/webservice/loanService?wsdl"
        client = suds.client.Client(url)
        result = client.service.seeContract(str(appId))
        result = json.loads(result)
        print result['returnCode']
        print result['returnMsg']
        return result['returnCode'],result['returnMsg']

# 获取用户中心接口返回“uuid”，“custNo”
    def get_user_center_info(self, name, id):
        name1 = str(name)
        id1 = str(id)
        contents_part1 = '''http://101.200.87.116:9190/usercenter/new/realNameRegistForBus.do?jSON={'body':{'key':'d20f83ee6933aa1ea047fe5cbd9c1fd5','realName':\''''
        contents_part2 = '''\','idCardNo':\''''
        contents_part3 = '''\','password':'123456','domain':'bus','type':'1'}}'''
        contents = contents_part1 + name1 + contents_part2 + id1 + contents_part3

        r = requests.get(contents)
        # print"center info: "
        #  print r.content

        if r.json()['result'] == 'success' or r.json()['result'] == 'username has existed':
            return r.json()['custNo'], r.json()['uuid']
        else:
			return r.json()['result']

#圈存额度
    def get_quota_apply_use(self,quo_model,datadict, contractAmt, customerId):
        url1 = 'http://123.56.226.129:7030/quota/httpInf/apply'
        url2 = 'http://123.56.226.129:7030/quota/httpInf/use'
        headers = {'Content-Type': 'application/json,charset=UTF-8'}

        name = datadict['customerName']
        cardId = datadict['certId']
        channelValue = datadict['saleChannel']
        appId = datadict['oldAppId']
        if quo_model == 'B17302':
            operateType = 'credit'
        if quo_model == 'B17301':
            operateType = 'cash'

        channelOrderId = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        channelOrderId += channelOrderId

        head = {'functionCode': 'apply013', 'sysId': '1030', 'requestId': '9aa09a7a8b6147ca854ced61a2a99b28'}
        body = {'name': str(name), 'customerId': str(customerId), 'cardType': 'B1301', 'cardId': str(cardId), 'modelValue': 'PU00001', 'creditQuota': '7000', 'cashQuota': '7000', 'channelValue': str(channelValue), 'channelOrderId': '12345678000001'}
        data = {'body': body, 'head': head}

        r = requests.post(url1, data=json.dumps(data), headers=headers)

        head1 = {'functionCode': 'use001', 'sysId': '1030', 'requestId': '9aa09a7a8b6147ca854ced61a2a99b28'}
        body1 = {'appId': str(appId), 'channelValue': str(channelValue), 'modelValue': 'PU00001', 'operateType': operateType, 'quota': str(contractAmt), 'channelOrderId': str(channelOrderId), 'businessType': 'QB0002', 'cardId': str(cardId), 'cardType': 'B1301', 'userType': 'QU0001'}
        data1 = {'body': body1, 'head': head1}

        r1 = requests.post(url2, data=json.dumps(data1), headers=headers)

        return r.text, r1.text
#根据风险等级，到数据库查平台的风险备用金率（系统自己算合同金额时，取的是平台数据，脚本和它保持一致）
    def get_serviceRate(self,data,env):
        env['dbname'] = 'sit_base_db'
        riskGrade = data['riskGrade']
        productId = data['productId']
        term = data['loanTerm']
        (server,con,port) = db.connectdb(env)
        sqlcommand = "SELECT LEVEL_" + riskGrade+" FROM t_prd_consult_service_rate WHERE \
        PRODUCT_ID='"+productId+"' AND times='"+term+"' ORDER BY create_time DESC LIMIT 1"

        serviceRate = db.get_one_value(con, sqlcommand)

        server.stop()
        con.close()
        return serviceRate

    def get_riskFundRate(self, data, env):
        env['dbname'] = 'sit_base_db'
        riskGrade = data['riskGrade']
        productId = data['productId']
        term = data['loanTerm']
        (server, con, port) = db.connectdb(env)
        sqlcommand = "SELECT LEVEL_" + riskGrade + " FROM t_prd_risk_fund WHERE \
        PRODUCT_ID='" + productId + "' AND times='" + term + "' ORDER BY create_time DESC LIMIT 1"
        print sqlcommand
        riskFundRate = db.get_one_value(con, sqlcommand)

        server.stop()
        con.close()
        return riskFundRate

# 各项金额试算接口（合同金额，费用合计等）
    def get_contract_amt(self, data, env):
        amd_dict = {}
        print "Calculating Amt ......"
        url = 'http://123.57.48.237:7082/intf/external/trans!server.intf'
        headers = {'Content-Type': 'application/json,charset=UTF-8'}
        term = data['loanTerm']
        productId = data['productId']
        riskGrade = data['riskGrade']

        if str(productId) == '413' or str(productId) == '416' or str(productId) == '137':
            approveAmt = '0'
        else:
            approveAmt = data['approveSuggestAmt']

        channel = data['saleChannel']
        appId = data['oldAppId']
        if data.has_key('feeExtraInfoList'):
            feelist = data['feeExtraInfoList']
        else:
            feelist = []
        instServiceRate = '0.05'
        if data.has_key('approveDstRate'):
            quellRate = str(data['approveDstRate'])
        else:
            quellRate = '0.09'
        if data.has_key('yearRate'):
            yearRate = str(data['yearRate'])
        else:
            yearRate = '0'
        if data.has_key('repayDay'):
            repayDay = data['repayDay']
        else:
            repayDay = '20'

        serviceRate = self.get_serviceRate(data, env)
        riskFundRate = self.get_riskFundRate(data, env)

        print "loanTerm : " + str(term)
        print "riskGrade : " + str(riskGrade)
        print "approveAmt : " + str(approveAmt)
        print "channel : " + str(channel)
        print "approveDstRate : " + str(quellRate)
        print "yearRate : " + str(yearRate)
        print "repayDay : " + str(repayDay)
        print "serviceRate : " + str(serviceRate)
        print "riskFundRate : " + str(riskFundRate)

        if len(feelist) == 0:
			extroInfo = '{}'
        else:
			for i in range(len(feelist)):
				if feelist[i].has_key('infoName') and feelist[i]['infoName'] == 'B6638':
					infoName = 'B6638'
					infoValue = feelist[i]['infoValue']
					extroInfo = "{\"extroOther\":\"{\\\"riskFundRate\\\":\\\""+str(riskFundRate)+"\\\",\\\"serviceRate\\\":\\\""+str(serviceRate)+"\\\"}\",\"feeList\":\"{\\\"" + infoName + "\\\":\\\"" + infoValue + "\\\"}\"}"
					break
				else:
					extroInfo = '{}'
        currentDate = time.strftime('%Y%m%d', time.localtime(time.time()))
        transSerialNo = time.strftime('%Y%m%d%H%M%S', time.localtime(time.time()))
        currentTime = time.strftime('%H%M%S', time.localtime(time.time()))

        head = {'channel': channel, 'sysCode': '14', 'transCode': '02', 'transDate': currentDate, 'transSerialNo': transSerialNo, 'transTime': currentTime, 'transType': 'RS'}
        paraMap = {'term': str(term), 'productId': productId, 'riskGrade': riskGrade, \
				   'yearRate':yearRate,'instServiceRate': instServiceRate,'contractAmt': '0', \
				   'approveAmt': str(approveAmt), 'quellRate': quellRate,\
		           'repayDay': repayDay, 'extroInfo': extroInfo}


        body = {'appId': appId, 'paraMap': paraMap}
        data = {'body': body, 'head': head}

        print "*******************************"
        print data
        print "*******************************"
        r = requests.post(url, data=json.dumps(data), headers=headers)
        if r.json()['sts'] == '000000':
            print r.content
            #合同金额
            contractAmt = r.json()['data']['contractAmt']
            amd_dict['contractAmt']=contractAmt
            #费用合计
            for i in range(len(r.json()['data']['feeInfoList'])):
                feetype = r.json()['data']['feeInfoList'][i]['feeType']
                if feetype == 'B6629':
                    fyhj_amt = r.json()['data']['feeInfoList'][i]['feeAmt']
                    amd_dict['fyhj_amt']=fyhj_amt
                if feetype == 'B6628':
                    qdfwf_amt = r.json()['data']['feeInfoList'][i]['feeAmt']
                    amd_dict['qdfwf_amt']=qdfwf_amt
        else:
            print r.content
            amd_dict['msg']=r.json()['msg']

        return amd_dict

#Just for test
if __name__ == '__main__':
    inf = Interface()
    data12 = {'orgCode': '120001', 'intustry': 'B1017', 'instCode': '110807', 'customerInfo': {'hisLoanType': 'F1201', 'incomeSource': 'B20301', 'monthlyIncome': 'B20201', 'hasLoan': 'N8702'}, 'customerSex': 'N0202', 'qq': 61701620, 'zhongAnInfo': {}, 'marry': 'B0505', 'tLonAccountList': [{'accAccountName': u'\u6276\u7533\u666f', 'accOwnIdCard': '589459197105208090', 'trusteeType': 'B134003', 'accCertType': 'B1301', 'accBankName': '0309', 'accOwnPhone': '15895991791', 'extendFieldString': '{"B1310":"1q21e32fdhb","B1311":"asdmsdcvs","B1309":"asdsafwlef"}', 'accOwnName': u'\u6276\u7533\u666f', 'accProvince': '\xe5\xa4\xa9\xe6\xb4\xa5\xe5\xb8\x82', 'accBankBranch': '\xe5\x85\xb4\xe4\xb8\x9a\xe9\x93\xb6\xe8\xa1\x8c', 'uumCustNo': '20170109gerenkaih1110521', 'accBankCardBindId': 296018923132L, 'accountType': '01', 'accBankCard': '622908328546701352', 'accType': 'B6802', 'accCity': 1000, 'accCorpRep': u'\u6276\u7533\u666f'}, {'accAccountName': u'\u6276\u7533\u666f', 'accOwnIdCard': '589459197105208090', 'trusteeType': 'B134003', 'accCertType': 'B1301', 'accBankName': '0105', 'accOwnPhone': '15895991791', 'extendFieldString': '{"B1310":"1q21e32fdhb","B1311":"asdmsdcvs","B1309":"asdsafwlef"}', 'accOwnName': u'\u6276\u7533\u666f', 'accProvince': '\xe6\xb9\x96\xe5\x8c\x97\xe7\x9c\x81', 'accBankBranch': '\xe4\xb8\xad\xe5\x9b\xbd\xe5\xbb\xba\xe8\xae\xbe\xe9\x93\xb6\xe8\xa1\x8c', 'uumCustNo': '20170109gerenkaih1110521', 'accBankCardBindId': 714861127604L, 'accountType': '01', 'accBankCard': '6227001935076453820', 'accType': 'B6803', 'accCity': 1000, 'accCorpRep': u'\u6276\u7533\u666f'}, {'accOwnIdCard': '589459197105208090', 'trusteeType': 'B134003', 'accCertType': 'B1301', 'accBankName': '0102', 'accOwnPhone': '15895991791', 'extendFieldString': '{"B1310":"1q21e32fdhb","B1311":"asdmsdcvs","B1309":"asdsafwlef"}', 'accOwnName': u'\u6276\u7533\u666f', 'accProvince': '\xe6\xb9\x96\xe5\x8d\x97\xe7\x9c\x81', 'accBankBranch': '\xe5\xb7\xa5\xe8\xa1\x8c', 'uumCustNo': '20170109gerenkaih1110556', 'accBankCardBindId': 592095893915L, 'accountType': '01', 'accBankCard': '6222024100020675134', 'accType': 'B6801', 'accCity': 1000, 'accCorpRep': u'\u6276\u7533\u666f'}], 'feeExtraInfoList': [{'infoName': 'B6655', 'infoValue': 69.04}, {'infoName': 'B11405', 'infoValue': '0.5'}, {'infoName': 'B6606', 'infoValue': '120'}], 'loanPurposeOther': 'F1101', 'saleChannel': '1055', 'score': '90', 'email': 'kw8MHweN6@qq.com', 'recordLoanAttach': [{'attachName': 'sdhjs', 'fileType': 'png', 'attachType': '11001539', 'fileId': '93'}, {'attachName': 'QQ\xe6\x88\xaa\xe5\x9b\xbe20161114160212.png', 'fileType': 'png', 'attachType': '11001004', 'fileId': '0eb661bc-7105-446f-bef0-818c7d295f82'}], 'companyPhone': '18949683325', 'degree': 'B0304', 'certId': '589459197105208090', 'liveAddress': '\xe6\xb9\x96\xe5\x8c\x97\xe7\x9c\x81\xe6\xad\xa6\xe6\xb1\x89\xe5\xb8\x82', 'livePhone': '18189137638', 'approveDstRate': '0.006300', 'duty': 'B2901', 'customerName': u'\u6276\u7533\u666f', 'modelBusinessData': [{'propertyMap': {'entry': [{'key': 'uumCustNo', 'value': u'201803291235585864499528174'}, {'key': 'uumUserId', 'value': u'892d5820-9894-4919-9725-254b1fa406cf'}]}, 'modelId': '26'}, {'propertyMap': {'entry': [{'key': 'nationality', 'value': '\xe4\xb8\xad\xe5\x9b\xbd'}, {'key': 'certifiCountry', 'value': '\xe7\xbe\x8e\xe5\x9b\xbd'}, {'key': 'workStatus', 'value': 'F16101'}, {'key': 'debitCardNum', 'value': '0'}, {'key': 'creditCardNum', 'value': '0'}, {'key': 'programApply', 'value': '\xe6\x95\xb4\xe8\x84\xb8\xe5\x9e\x8b'}, {'key': 'payTransNo', 'value': 'nF5moJfxt'}, {'key': 'rechargeType', 'value': 'B8010'}]}, 'modelId': '39'}, {'propertyMap': {'entry': [{'key': 'companyAddress', 'value': '\xe5\x8c\x97\xe4\xba\xac\xe4\xb8\xb0\xe5\x8f\xb0\xe7\xbe\x8e\xe5\xae\xb9\xe6\x95\xb4\xe5\xbd\xa2'}, {'key': 'legalPersonPhone', 'value': '13501201020'}, {'key': 'legalPersonCertId', 'value': '140101198303060617'}, {'key': 'legalPersonName', 'value': '\xe5\xbc\xa0\xe7\xbe\x8e\xe7\xbe\x8e'}, {'key': 'hospitalName', 'value': '\xe5\x8c\x97\xe4\xba\xac\xe7\xac\xac\xe4\xba\x8c\xe4\xba\xba\xe6\xb0\x91\xe5\x8c\xbb\xe9\x99\xa2'}]}, 'modelId': '47'}], 'borrowerType': 'B154001', 'company': u'\u6276\u7533\u666f', 'certType': 'B1301', 'phone': '15895991791', 'loanTerm': '12', 'recordLoanContact': [{'contactPhone': '15796336262', 'contactRelation': 'F1004', 'contactName': u'\u84b2\u59ec\u6021'}], 'career': 'F123150201', 'oldAppId': 'nAHDes0JH', 'loanPurpose': 'F1108', 'productId': '432', 'approveSuggestAmt': '2000', 'appayDate': '2019-11-24', 'yearRate': '0.07500000000', 'companyAddress': '\xe7\xbb\xbf\xe5\x8d\xa1\xe5\xb0\x86\xe5\x86\x9b\xe5\xba\x9c\xe8\x83\xa1\xe7\xba\xa2\xe4\xb8\xba\xe5\x90\xa6', 'riskGrade': 'A'}
    data18 = {'orgCode': '120001', 'intustry': 'B1017', 'instCode': '110807', 'customerInfo': {'hisLoanType': 'F1201', 'incomeSource': 'B20301', 'monthlyIncome': 'B20201', 'hasLoan': 'N8702'}, 'customerSex': 'N0202', 'qq': 31713068, 'zhongAnInfo': {}, 'marry': 'B0504', 'tLonAccountList': [{'accAccountName': u'\u97e6\u97ec\u5bcc', 'accOwnIdCard': '710910199508205358', 'trusteeType': 'B134003', 'accCertType': 'B1301', 'accBankName': '0301', 'accOwnPhone': '15332288411', 'extendFieldString': '{"B1310":"1q21e32fdhb","B1311":"asdmsdcvs","B1309":"asdsafwlef"}', 'accOwnName': u'\u97e6\u97ec\u5bcc', 'accProvince': '\xe8\xb4\xb5\xe5\xb7\x9e\xe7\x9c\x81', 'accBankBranch': '\xe5\x8c\x97\xe4\xba\xac\xe5\x88\x86\xe8\xa1\x8c', 'uumCustNo': '20170109gerenkaih1110521', 'accBankCardBindId': 357704701384L, 'accountType': '01', 'accBankCard': '6222620910135472806', 'accType': 'B6802', 'accCity': 1000, 'accCorpRep': u'\u97e6\u97ec\u5bcc'}, {'accAccountName': u'\u97e6\u97ec\u5bcc', 'accOwnIdCard': '710910199508205358', 'trusteeType': 'B134003', 'accCertType': 'B1301', 'accBankName': '0102', 'accOwnPhone': '15332288411', 'extendFieldString': '{"B1310":"1q21e32fdhb","B1311":"asdmsdcvs","B1309":"asdsafwlef"}', 'accOwnName': u'\u97e6\u97ec\u5bcc', 'accProvince': '\xe5\x8c\x97\xe4\xba\xac\xe5\xb8\x82', 'accBankBranch': '\xe5\xb7\xa5\xe8\xa1\x8c', 'uumCustNo': '20170109gerenkaih1110521', 'accBankCardBindId': 663682821900L, 'accountType': '01', 'accBankCard': '6222024100067153284', 'accType': 'B6803', 'accCity': 1000, 'accCorpRep': u'\u97e6\u97ec\u5bcc'}, {'accOwnIdCard': '710910199508205358', 'trusteeType': 'B134003', 'accCertType': 'B1301', 'accBankName': '0303', 'accOwnPhone': '15332288411', 'extendFieldString': '{"B1310":"1q21e32fdhb","B1311":"asdmsdcvs","B1309":"asdsafwlef"}', 'accOwnName': u'\u97e6\u97ec\u5bcc', 'accProvince': '\xe6\xb1\x9f\xe8\x8b\x8f\xe7\x9c\x81', 'accBankBranch': '\xe4\xb8\xad\xe5\x9b\xbd\xe5\x85\x89\xe5\xa4\xa7\xe9\x93\xb6\xe8\xa1\x8c', 'uumCustNo': '20170109gerenkaih1110556', 'accBankCardBindId': 265056381390L, 'accountType': '01', 'accBankCard': '6226638884136072', 'accType': 'B6801', 'accCity': 1000, 'accCorpRep': u'\u97e6\u97ec\u5bcc'}], 'feeExtraInfoList': [{'infoName': 'B6655', 'infoValue': 'null'}, {'infoName': 'B11405', 'infoValue': '0.5'}, {'infoName': 'B6606', 'infoValue': '120'}], 'loanPurposeOther': 'F1101', 'saleChannel': '1055', 'score': '90', 'email': 'QHtyovhlB@qq.com', 'recordLoanAttach': [{'attachName': 'sdhjs', 'fileType': 'png', 'attachType': '11001539', 'fileId': '93'}, {'attachName': 'QQ\xe6\x88\xaa\xe5\x9b\xbe20161114160212.png', 'fileType': 'png', 'attachType': '11001004', 'fileId': '0eb661bc-7105-446f-bef0-818c7d295f82'}], 'companyPhone': '13092747795', 'degree': 'B0303', 'certId': '710910199508205358', 'liveAddress': '\xe6\xb1\x9f\xe8\x8b\x8f\xe7\x9c\x81\xe5\x8d\x97\xe4\xba\xac\xe5\xb8\x82', 'livePhone': '18574127069', 'approveDstRate': '0.006300', 'duty': 'B2901', 'customerName': u'\u97e6\u97ec\u5bcc', 'modelBusinessData': [{'propertyMap': {'entry': [{'key': 'uumCustNo', 'value': u'201803291430099535737943821'}, {'key': 'uumUserId', 'value': u'634189ef-6af1-4f22-91a4-a54688b25b1f'}]}, 'modelId': '26'}, {'propertyMap': {'entry': [{'key': 'nationality', 'value': '\xe4\xb8\xad\xe5\x9b\xbd'}, {'key': 'certifiCountry', 'value': '\xe7\xbe\x8e\xe5\x9b\xbd'}, {'key': 'workStatus', 'value': 'F16101'}, {'key': 'debitCardNum', 'value': '0'}, {'key': 'creditCardNum', 'value': '0'}, {'key': 'programApply', 'value': '\xe6\x95\xb4\xe8\x84\xb8\xe5\x9e\x8b'}, {'key': 'payTransNo', 'value': 'tgbL3ZOks'}, {'key': 'rechargeType', 'value': 'B8010'}]}, 'modelId': '39'}, {'propertyMap': {'entry': [{'key': 'companyAddress', 'value': '\xe5\x8c\x97\xe4\xba\xac\xe4\xb8\xb0\xe5\x8f\xb0\xe7\xbe\x8e\xe5\xae\xb9\xe6\x95\xb4\xe5\xbd\xa2'}, {'key': 'legalPersonPhone', 'value': '13501201020'}, {'key': 'legalPersonCertId', 'value': '140101198303060617'}, {'key': 'legalPersonName', 'value': '\xe5\xbc\xa0\xe7\xbe\x8e\xe7\xbe\x8e'}, {'key': 'hospitalName', 'value': '\xe5\x8c\x97\xe4\xba\xac\xe7\xac\xac\xe4\xba\x8c\xe4\xba\xba\xe6\xb0\x91\xe5\x8c\xbb\xe9\x99\xa2'}]}, 'modelId': '47'}], 'borrowerType': 'B154001', 'company': u'\u97e6\u97ec\u5bcc', 'certType': 'B1301', 'phone': '15332288411', 'loanTerm': u'24', 'recordLoanContact': [{'contactPhone': '15338654447', 'contactRelation': 'F1004', 'contactName': u'\u4faf\u4f26\u5de7'}], 'career': 'F12325', 'oldAppId': 'lci439d5G', 'loanPurpose': 'F1112', 'productId': '432', 'approveSuggestAmt': '2000', 'appayDate': '2019-11-24', 'yearRate': '0.10000000000', 'companyAddress': '\xe7\xbb\xbf\xe5\x8d\xa1\xe5\xb0\x86\xe5\x86\x9b\xe5\xba\x9c\xe8\x83\xa1\xe7\xba\xa2\xe4\xb8\xba\xe5\x90\xa6', 'riskGrade': u'A'}
    env = {'sql_usr': 'sit_user01', 'dzqz_url': 'http://47.94.191.238:7086', 'user_center_url': 'http://101.200.87.116:9190', 'ssh_host': '47.94.40.127', 'sql_port': '3306', 'url': 'http://47.94.40.127:7084/webservice/loanService?wsdl', 'ssh_usr': 'appuser', 'ssh_psw': '5zt4BRJ8', 'txhp_url': 'http://47.94.40.127:7082', 'scht_url': 'http://47.94.40.127:7083', 'web_url': 'http://47.94.40.127:7000/product/system/login!selectPage.action', 'sql_psw': 'j*IHNifVbxCJ', 'sql_db': 'test_loan_db', 'sql_addr': 'rdsiuzzzqiuzzzq.mysql.rds.aliyuncs.com'}

#    result = inf.inf_seeContract('926656508')
#    result = inf.get_contract_amt(data18,env)
#    result = inf.inf_channel('926671516','403')
    result = inf.inf_generateContract('926671520')



