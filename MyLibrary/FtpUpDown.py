# encoding: utf-8
__author__ = 'zhengyong'

from ftplib import FTP
import os
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import ftplib
import codecs

class FtpUpDown():

	# 下载文件
	def ftp_file_down(self, host, username, password, remote_path_down, file_name):
		basedir = os.getcwd()
		print basedir
		os.chdir(basedir)
		ftpfolder = '../amt_file'
		if os.path.exists(ftpfolder):
			pass
		else:
			os.makedirs(ftpfolder)
		os.chdir(ftpfolder)

		ftp = FTP()
		ftp.set_debuglevel(2)
		ftp.connect(host=host, port='21')
		ftp.login(user=username, passwd=password)
		ftp.cwd(remote_path_down)
		bufsize = 1024
		file_handler = open(file_name, 'wb').write
		ftp.retrbinary('RETR %s' % os.path.basename(file_name), file_handler, bufsize)
		ftp.set_debuglevel(0)
		ftp.quit()

		os.chdir(basedir)

	def find_n_sub_str(self, src, pos, start):
		sub = '|'
		index = src.find(sub, start)
		if index != -1 and int(pos) > 0:
			return self.find_n_sub_str(src, int(pos) - 1, index + 1)
		return index


	# 修改单行
	def modify_single(self, file_name, mark_num, str_content):

		# os.chdir('C:\\Users\\Zhengy\\Desktop\\aaa\\')
		file1 = open(file_name, 'r+')

		file1.seek(0, 0)
		r_str = file1.readlines()

		num = self.find_n_sub_str(r_str[0], int(mark_num)-1, 0)

		r_str_new = r_str[0][:int(num+1)] + str_content + r_str[0][int(num+1):]

		file1.seek(0, 0)
		file1.write(r_str_new)
		file1.close()



	# 修改多行
	def modify_repeatedly(self, file_name, mark_num, str_content):

		file1 = open(file_name, 'r+')

		file1.seek(0, 0)
		r_str = file1.readlines()

		count = len(r_str)

		r_str_new_list = []

		for i in range(count):

			num = self.find_n_sub_str(r_str[i], int(mark_num) - 1, 0)

			r_str_new = r_str[i][:int(num+1)] + str(str_content) + r_str[i][int(num+1):]

			r_str_new_list.append(r_str_new)

		file1.seek(0, 0)
		file1.writelines(r_str_new_list)
		file1.close()

	# 上传文件
	def ftp_file_up(self, host, username, password, remote_path_up, file_name):

		ftp = FTP()
		ftp.set_debuglevel(2)
		ftp.connect(host=host, port='21')
		ftp.login(user=username, passwd=password)
		ftp.cwd(remote_path_up)
		bufsize = 1024
		file_handler = open(file_name, 'rb')
		ftp.storbinary('STOR %s' % os.path.basename(file_name), file_handler, bufsize)
		ftp.set_debuglevel(0)
		file_handler.close()
		ftp.quit()

if __name__ == '__main__':
	con = FtpUpDown()
	con.ftp_file_down('182.92.118.156','test_p2p','u7s3dpdT','/zhangwu','1000_08_01_0_20180323143802422.txt')

	con.modify_repeatedly('../amt_file/1000_08_01_0_20180323143802422.txt', '4', 'P2P10062|')
#

#	con.modify_repeatedly('amt_file/1000_08_01_0_20180323143802422', '4', 'P2P10062|')



