#coding:utf-8
import requests
import json
from operation_json import OperetionJson


class OperationHeader:

	def __init__(self,response):
		self.response = json.loads(response)

	def get_response_url(self):
		'''
		获取登录返回的token的url
		'''

		url = self.response['token']

		return url

	def get_cookie(self):
		'''
		获取cookie的jar文件
		'''
		url = self.get_response_url()+"&callback=jQuery21008240514814031887_1508666806688&_=1508666806689"
		cookie = requests.get(url).cookies
		return cookie

	def write_cookie(self):
		cookie = requests.utils.dict_from_cookiejar(self.get_cookie())
		op_json = OperetionJson()
		op_json.write_data(cookie)

	def get_token(self):
		token = self.response['token']
		token = {"header":{"token":token,
						   # "Content-Type": "application/json;charset=UTF-8"
						   }}
		return token
	def write_header(self):
		op_json = OperetionJson()
		op_json.write_data(self.get_token())


