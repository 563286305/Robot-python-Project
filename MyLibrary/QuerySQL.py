# -*- coding: utf-8 -*-
'''
Created on 2018.01.24
@author: wuyou
'''

import MySQLdb
from sshtunnel import SSHTunnelForwarder
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



class QuerySQL():

	def connectssh(self,dbinfo):
		server = SSHTunnelForwarder(
				(dbinfo['ssh_host'], 22),
				ssh_username = dbinfo['ssh_usr'],
				ssh_password = dbinfo['ssh_psw'],
				remote_bind_address=(dbinfo['sql_addr'], int(dbinfo['sql_port'])))
		server.start()
		return server

	def stopssh(self,server):
		server.stop()

	def connectdb(self,dbinfo):

		server = SSHTunnelForwarder(
				(dbinfo['ssh_host'], 22),
				ssh_username = dbinfo['ssh_usr'],
				ssh_password = dbinfo['ssh_psw'],
				remote_bind_address=(dbinfo['sql_addr'], int(dbinfo['sql_port'])))
		server.start()
		serverport = server.local_bind_port
		con = MySQLdb.connect(host='127.0.0.1',
#							   port=server.local_bind_port,
							   port=serverport,
							   user=dbinfo['sql_usr'],
							   passwd=dbinfo['sql_psw'],
		                       db=dbinfo['dbname'],
							   charset='utf8')
		return server,con,serverport


	def get_one_value(self,db,sqlcommand):
		cursor = db.cursor()
		cursor.execute(sqlcommand)

		result = cursor.fetchall()
		if result == ():
			result = '0'
		else:
			result = result[0][0]
		return result

if __name__ == '__main__':
	run = QuerySQL()
	dbinfo = {'ssh_host':'123.57.48.237',\
	          'ssh_usr':'read',\
	          'ssh_psw':'jFF111',\
	          'sql_addr':'rdsiuzzzqiuzzzq.mysql.rds.aliyuncs.com',\
	          'sql_port':3306,\
	          'sql_usr':'sit_user01',\
	          'sql_psw':'j*IHNifVbxCJ',\
	          'dbname':'sit_base_db'}
	sqlcommand = 'SELECT PRD_FUND_TYPE FROM t_prd_quota WHERE product_id = 137'
	conlist = run.connectdb(dbinfo)
	server = conlist[0]
	con = conlist[1]
	result = run.get_one_value(con,sqlcommand)
	server.stop()
	con.close()
	print result