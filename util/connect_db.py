#coding:utf-8
import pymysql
import json
class OperationMysql:
	def __init__(self):
		self.conn = pymysql.connect(
			host='192.168.199.162',
			port=3306,
			user='root',
			passwd='root',
			db='game_api_developmentv3',
			charset='utf8',

			)
		self.cur = self.conn.cursor()

	#查询一条数据
	def search_one(self,sql):
		self.cur.execute(sql)
		result = self.cur.fetchone()
		self.conn.close()

		return result

if __name__ == '__main__':
	op_mysql = OperationMysql()
	res = op_mysql.search_one("SELECT *from users limit 1;")
	print res
