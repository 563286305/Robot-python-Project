# -*- coding: utf-8 -*-
from QueryDB_RF import QueryDB_RF
from OperateExcel import OperateExcel
import re
B = OperateExcel()

#Template文件夹路径
Template_path = r'E:/自动化/05_BUS自动化工具开发/02_接口自动化测试框架/BusAutoTest_Version4/Contract/Template/config.xlsx'
Template_path = unicode(Template_path, "utf-8")
Template = r'E:/自动化/05_BUS自动化工具开发/02_接口自动化测试框架/BusAutoTest_Version4/Contract/Template/'
#Result文件夹路径
Result_path = r'E:/自动化/05_BUS自动化工具开发/02_接口自动化测试框架/BusAutoTest_Version4/Result/Contract_result.xlsx'
Result_path = unicode(Result_path, "utf-8")

class Contract_RF():

    def __init__(self):
        pass

    def Contract_Check(self,Envir,*list_appid):

        # 读取excel中环境配置
        # env_1 测试环境
        # env_2 准生产环境
        # env_3 联调环境

        list1 = B.a_colsReadExcel2(Template_path, Envir, 0)
        list2 = B.a_colsReadExcel2(Template_path, Envir, 1)
        dict_env = B.a_listToDict(list1, list2)
        A = QueryDB_RF()

        # 费用的循环写入计数
        q = 1
        # 还款计划的循环写入计数
        t = 1

        #将存放结果的excel文件清空
        B.a_remove_sheet_allvalue(Result_path)

        #链接数据库
        (server,con,serverport)= A.a_connectdb(dict_env['ssh_host'], dict_env['ssh_usr'], dict_env['ssh_psw'],dict_env['sql_addr'], dict_env['sql_db'], dict_env['sql_usr'], dict_env['sql_psw'])

        # 循环每个工单号
        for appid in list_appid:
            # 入参值list
            value = []
            # 费用出参值list
            value1 = []
            # 数据库费用值
            value2 = []
            # 费用比较结果
            fee_result = []
            fee_result.append('APPID')
            fee_result.append(appid)
            # execel还款计划list值
            plan_value = []

            # 查询工单表和风险等级
            application = A.Query_application(appid,dict_env,con)
            Risk_Grade = A.Query_Risk_Grade(appid,dict_env,con)

            # 读取入参的配置和位置
            parameter = B.a_colsReadExcel2(Template_path, application['PRODUCT_ID'], 0)
            position = B.a_colsReadExcel2(Template_path, application['PRODUCT_ID'], 1)

            # 该循环是获取入参的值
            for i in range(1, len(parameter)):
                if parameter[i] == 'APPROVE_AMT' or parameter[i] == 'APPROVE_LIMIT' or parameter[i] =='LOAN_DATE' \
                        or parameter[i] == 'YEAR_RATE' or parameter[i] == 'MONTH_RATE' or parameter[i] =='REPAY_DAY':
                    value.append(application[parameter[i]])
                if parameter[i] == 'RISK_GRADE':
                    value.append(Risk_Grade[parameter[i]])
                if re.match(r'B66', parameter[i]):
                    fee_query = A.Query_Fee_Amt(appid, parameter[i],dict_env,con)
                    value.append(fee_query)
                if parameter[i] == 't_prd_risk_fund' or parameter[i] == 't_prd_consult_service_rate' or parameter[i] == \
                        't_prd_inst_service_rate' or parameter[i] == 't_prd_insurance_rate' or parameter[i] == \
                        't_prd_manager_rate' or parameter[i] =='t_prd_guarantee_rate':
                    base_query = A.Query_Comm(parameter[i], application['PRODUCT_ID'], application['PRODUCT_VERSION'],
                                              application['APPROVE_LIMIT'], Risk_Grade['RISK_GRADE'],dict_env,con)
                    value.append(base_query)

            # 判断合同计算器名称
            id_list = B.a_colsReadExcel2(Template_path, '合同计算器名称对照表', 0)
            for j in range(len(id_list)):
                if id_list[j] == application['PRODUCT_ID']:
                    name = B.a_rowsReadExcel2(Template_path, '合同计算器名称对照表', j)
                    break

            # 拼接合同计算器文件路径
            comtract_path = Template + name[1]

            # 按照位置列表循环写入计算器
            for k in range(1, len(position)):
                B.a_cellAddExcel(comtract_path,name[2],position[k],value[k-1])

            # 刷新
            #B.a_refreshExcel(comtract_path)

            # 读取出参参数和位置
            parameter1 = B.a_colsReadExcel2(Template_path, application['PRODUCT_ID'], 2)
            position1 = B.a_colsReadExcel2(Template_path, application['PRODUCT_ID'], 3)

            # 根据位置按照顺序取值，存入list
            for m in range(1, len(position1)):
                read_value = B.a_cellReadExcel(comtract_path, name[2], position1[m])
                if read_value != None:
                    read_value = "%.2f" % read_value
                value1.append(read_value)

            # 根据出参配置取数据库值
            for n in range(1, len(parameter1)):
                if parameter1[n] == 'CONTRACT_AMT' or parameter1[n] == 'MONTH_REPAY_LIMIT' or parameter1[n] =='DRAWN_AMT':
                    value2.append(application[parameter1[n]])
                if re.match(r'B66', parameter1[n]):
                    fee_query = A.Query_Fee_Amt(appid, parameter1[n],dict_env,con)
                    value2.append(fee_query)

            # 比较
            for p in range(1, len(parameter1)):
                if float(value1[p - 1]) == float(value2[p - 1]):
                    comparison_result = 'PASS'
                else:
                    comparison_result = 'FAIL'

                fee_result.append(parameter1[p])
                fee_result.append(value1[p - 1])
                fee_result.append(value2[p - 1])
                fee_result.append(comparison_result)

            # 结果循环回写保存
            B.a_listAddExcel(Result_path, 'fee_result', q, 1, *fee_result)
            q += 1

            # 读取还款计划出参参数和位置
            parameter2 = B.a_colsReadExcel2(Template_path, application['PRODUCT_ID'], 4)
            position2 = B.a_colsReadExcel2(Template_path, application['PRODUCT_ID'], 5)
            del parameter2[0]
            del position2[0]

            # 查询数据库还款计划信息
            plan_query = A.Query_Repayment_Plan(appid, parameter2,dict_env,con)

            # 读取excel还款计划信息
            for x in range(len(position2)):
                begin_row_line = position2[x][1:]
                begin_col_name = position2[x][:1]
                end_row_line = int(begin_row_line) + int(len(plan_query))
                read_plan_value = B.a_cellListReadExcel(comtract_path, name[2], begin_col_name, begin_row_line,
                                                      end_row_line)
                if parameter2[x] == 'PLAN_REPAY_DATE':
                    for y in range(len(plan_query)):
                        read_plan_value[y] = read_plan_value[y][0:10]
                    plan_value.append(read_plan_value)
                elif parameter2[x] == 'STAGE':
                    plan_value.append(read_plan_value)
                else:
                    for z in range(len(plan_query)):
                        read_plan_value[z] = "%.2f" % float(read_plan_value[z])
                    plan_value.append(read_plan_value)

            # 读取的exec还款计划转置
            plan_value = map(list, zip(*plan_value))

            # 还款计划比较
            for r in range(len(plan_query)):
                # 还款计划每行比较结果
                plan_eachrow_result = []
                plan_eachrow_result.append(appid)
                for s in range(len(parameter2)):
                    if parameter2[s] == 'STAGE' or parameter2[s] == 'PLAN_REPAY_DATE':
                        if plan_value[r][s] == plan_query[r][s]:
                            comparison_result = 'PASS'
                        else:
                            comparison_result = 'FAIL'
                    else:
                        if float(plan_value[r][s]) == float(plan_query[r][s]):
                            comparison_result = 'PASS'
                        else:
                            comparison_result = 'FAIL'
                    plan_eachrow_result.append(parameter2[s])
                    plan_eachrow_result.append(plan_value[r][s])
                    plan_eachrow_result.append(str(plan_query[r][s]))
                    plan_eachrow_result.append(comparison_result)

                # 还款计划每行比较结果写入excel结果文件
                B.a_listAddExcel(Result_path, 'plan_result', t, 1, *plan_eachrow_result)
                t += 1
        server.stop()
        con.close()

if __name__ == '__main__':
    con = Contract_RF()
    con.Contract_Check('env_1','926656659')