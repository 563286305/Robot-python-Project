# -*- coding: utf-8 -*-
import MySQLdb
from sshtunnel import SSHTunnelForwarder

class ConnDB_RF():
    def a_run_sql_single_no_value(self, ssh_host, ssh_name, ssh_psw, rds_addr, mysql_db, mysql_usr, mysql_psw, sql):
        with SSHTunnelForwarder(
                (ssh_host, 22),
                ssh_username=ssh_name,
                ssh_password=ssh_psw,
                remote_bind_address=(rds_addr, 3306)) as server:
            conn = MySQLdb.connect(
                host='127.0.0.1',
                port=server.local_bind_port,
                user=mysql_usr,
                passwd=mysql_psw,
                db=mysql_db,
                charset='utf8')

            cursor = conn.cursor()
            test_sql = str(sql)
            cursor.execute(test_sql)
            data = cursor.fetchone()
            #data = cursor.fetchall()
            #data = data[0]
            #data_list = list(data)
            #return data_list
            return data

            conn.close()

    def a_run_sql_return_multi_line(self, ssh_host, ssh_name, ssh_psw, rds_addr, mysql_db, mysql_usr, mysql_psw, sql):
        with SSHTunnelForwarder(
                (ssh_host, 22),
                ssh_username=ssh_name,
                ssh_password=ssh_psw,
                remote_bind_address=(rds_addr, 3306)) as server:
            conn = MySQLdb.connect(
                host='127.0.0.1',
                port=server.local_bind_port,
                user=mysql_usr,
                passwd=mysql_psw,
                db=mysql_db,
                charset='utf8')

            cursor = conn.cursor()
            test_sql = str(sql)
            cursor.execute(test_sql)
            data = cursor.fetchall()
            return data

            conn.close()