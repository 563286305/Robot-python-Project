# -*- coding: utf-8 -*-
import MySQLdb
from sshtunnel import SSHTunnelForwarder

class QueryDB_RF():
    def a_connectdb(self,ssh_host, ssh_name, ssh_psw, rds_addr, mysql_db, mysql_usr, mysql_psw):
        server = SSHTunnelForwarder(
            (ssh_host, 22),
			ssh_username=ssh_name,
			ssh_password=ssh_psw,
			remote_bind_address=(rds_addr, 3306))
        server.start()

        serverport = server.local_bind_port
        con = MySQLdb.connect(
                host='127.0.0.1',
                port=server.local_bind_port,
                user=mysql_usr,
                passwd=mysql_psw,
                db=mysql_db,
                charset='utf8')
        return server,con,serverport

    def a_sql_single(self,sql,con):
        cursor = con.cursor()
        cursor.execute(str(sql))
        data = cursor.fetchone()
        return data

    def a_sql_multi(self,sql,con):
        cursor = con.cursor()
        test_sql = str(sql)
        cursor.execute(test_sql)
        data = cursor.fetchall()
        return data

    def Query_application(self,APPID,Envir,con):
        #该函数用于查询工单表相关信息
        sql = "SELECT APPROVE_AMT,APPROVE_LIMIT,YEAR_RATE,MONTH_RATE,LOAN_DATE,\
        PRODUCT_ID,PRODUCT_VERSION,CONTRACT_AMT,MONTH_REPAY_LIMIT,DRAWN_AMT,REPAY_DAY FROM "\
              + Envir['sql_db'] + ".t_lon_application WHERE APP_ID='"+ str(APPID) +"'"

        db_query = self.a_sql_single(sql,con)

        application = {}
        application['APPROVE_AMT'] = str(db_query[0])
        application['APPROVE_LIMIT'] = str(db_query[1])
        application['YEAR_RATE'] = str(db_query[2])
        application['MONTH_RATE'] = str(db_query[3])
        application['LOAN_DATE'] = str(db_query[4][0:10])
        application['PRODUCT_ID'] = str(db_query[5])
        application['PRODUCT_VERSION'] = str(db_query[6])
        application['CONTRACT_AMT'] = str(db_query[7])
        application['MONTH_REPAY_LIMIT'] = str(db_query[8])
        application['DRAWN_AMT'] = str(db_query[9])
        application['REPAY_DAY'] = str(db_query[10])

        return application

    def Query_Risk_Grade(self,APPID,Envir,con):
        #该函数用于查询风险等级

        sql = "SELECT RISK_GRADE FROM " + Envir['sql_db'] +\
              ".t_lon_credit_report WHERE APP_ID='"+ str(APPID) +"' LIMIT 1"

        db_query = self.a_sql_single(sql,con)

        application = {}
        application['RISK_GRADE'] = str(db_query[0])

        return application

    def Query_Comm(self,table,PRODUCT_ID,VERSION,TIMES,Risk_Grade,Envir,con):
        #该函数主要是基础平台相关费率
        #信用管理费费率
        #恒元费用比例
        #保险费费率
        #咨询服务费率
        #贷后管理费费率
        #担保费率（比例）
        sql = "SELECT LEVEL_A,LEVEL_B,LEVEL_C,LEVEL_D,LEVEL_E,LEVEL_A_A,LEVEL_B_B FROM " + Envir['sql_db1'] +"."\
              + str(table) +" WHERE PRODUCT_ID='"+ str(PRODUCT_ID) +"' AND VERSION='"+ str(VERSION) +\
              "' AND TIMES='"+ str(TIMES) +"'"
        db_query = self.a_sql_single(sql,con)

        list_risk_grade = ['A','B','C','D','E','AA','BB']
        for i in range(7):
            if list_risk_grade[i] == Risk_Grade:
                break
        if db_query ==None:
            value =0
        else:
            value =str(db_query[i])

        return value

    def Query_Fee_Amt(self,APPID,FEE_TYPE,Envir,con):
        #查询费用表
        sql = "SELECT FEE_AMT FROM "+ Envir['sql_db'] +".t_loan_fee_info WHERE APP_ID='"+ str(APPID) +\
              "' AND FEE_TYPE='"+ FEE_TYPE +"'"
        db_query = self.a_sql_single(sql,con)
        if db_query ==None:
            value =0
        else:
            value =str(db_query[0])
        return value

    def Query_Repayment_Plan(self,APPID,value,Envir,con):
        #查询还款计划表信息

        sql ="SELECT "
        for i in range(len(value)-1):
            sql =sql + str(value[i]) +","
        sql = sql + value[len(value)-1] +" FROM " + Envir['sql_db'] +".t_rep_repayment WHERE APP_ID='"+ str(APPID) +"'"

        db_query = self.a_sql_multi(sql,con)

        return db_query
