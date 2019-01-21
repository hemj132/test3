#coding:utf-8
from util.operation_excel import OperationExcel
import data_config
from util.operation_json import OperetionJson
from util.connect_db import OperationMysql
from util import tool
from case import case_def
import re

global str, str1
str = '123'
str1 = '223'
class GetData:
    def __init__(self):
        self.opera_excel = OperationExcel()

    #去获取excel行数,就是我们的case个数
    def get_case_lines(self):
        return self.opera_excel.get_lines()

    #获取是否执行
    def get_is_run(self,row):
        flag = None
        col = int(data_config.get_run())
        run_model = self.opera_excel.get_cell_value(row,col)
        if run_model == 'yes':
            flag = True
        else:
            flag = False
        return flag

    #是否携带header
    def is_header(self,row):
        col = int(data_config.get_header())
        header = self.opera_excel.get_cell_value(row,col)
        if header != '':
            if header == 'write':
                return header
            elif header == 'yes':
                op_json = OperetionJson('../dataconfig/cookie.json')
                # cookie = op_json.get_data('apsid')
                # cookies = {
                # 	'apsid':cookie
                # }
                cookies = op_json.get_data('header')
                # cookies = {
                # 	'token':cookie,
                #
                # }
                return cookies
            else:
                return None

        else:
            return None

    #获取请求方式
    def get_request_method(self,row):
        col = int(data_config.get_run_way())
        request_method = self.opera_excel.get_cell_value(row,col)
        return request_method

    #获取url
    def get_request_url(self,row):
        col = int(data_config.get_url())
        url = self.opera_excel.get_cell_value(row,col)


        return self.find_def(url)


    #获取请求数据
    def get_request_data(self,row):
        col = int(data_config.get_data())
        data = self.opera_excel.get_cell_value(row,col)

        if data == '':
            return None
        if re.match('{.+}', data, re.M | re.I)==None:
            opera_json = OperetionJson()
            data = opera_json.get_data(data)

        return  self.find_def(data)

    #通过获取关键字拿到data数据
    def get_data_for_json(self,row):
        opera_json = OperetionJson()
        print row
        request_data = opera_json.get_data(self.get_request_data(row))
        return request_data

    #获取预期结果
    def get_expcet_data_for_excel(self,row):
        col = int(data_config.get_expect())
        expect = self.opera_excel.get_cell_value(row,col)
        if expect == '':
            return None
        return expect

    #通过sql获取预期结果
    def get_expcet_data_for_mysql(self,row):
        op_mysql = OperationMysql()
        sql = self.get_expcet_data_for_excel(row)
        res = op_mysql.search_one(sql)
        # return res.decode('unicode-escape')
        return res
    def get_expcet_data(self,row):
        expect = self.get_expcet_data_for_excel(row)
        if expect == "":
            return None
        if re.match('select.+from',expect,re.M|re.I)==None:
            return expect
        else:
            op_mysql = OperationMysql()
            return op_mysql.search_one(expect)
    def write_result(self,row,value):
        col = int(data_config.get_result())
        self.opera_excel.write_value(row,col,value)

    #获取依赖数据的key
    def get_depend_key(self,row):
        col = int(data_config.get_data_depend())
        depent_key = self.opera_excel.get_cell_value(row,col)
        if depent_key == "":
            return None
        else:
            return depent_key

    #判断是否有case依赖
    def is_depend(self,row):
        col = int(data_config.get_case_depend())
        depend_case_id = self.opera_excel.get_cell_value(row,col)
        if depend_case_id == "":
            return None
        else:
            return depend_case_id

    #获取数据依赖字段
    def get_depend_field(self,row):
        col = int(data_config.get_field_depend())
        data = self.opera_excel.get_cell_value(row,col)
        if data == "":
            return None
        else:
            return data
    #是否有方法参数，目前每条只支持1个 ${}
    def find_def(self,param):
        #print type(param)
        #字典暂不处理
        if type(param)==dict:
            return param


        param =param.encode("utf-8")
        pattern1 = re.compile(r"(.*)\${(.+?)}(.*)")
        matcher1 = re.search(pattern1, param)

        if matcher1==None:
            return param
        else:
            defs= matcher1.group(2)
            matcher2= re.search('(.+)\((.*?)\)', defs)
            if matcher2==None:
                returns = getattr(case_def, defs)()
                return matcher1.group(1) + returns + matcher1.group(3)
            modus = re.search('(.+)\((.*?)\)', defs).group(1)
            paramers = re.search('(.+)\((.*?)\)', defs).group(2)
            paramers=tuple(paramers.split(','))
            returns=getattr(case_def, modus)(*paramers)
            print locals()
            return matcher1.group(1)+returns+matcher1.group(3)
if __name__ == '__main__':
    data= GetData()

    print locals()['str']

    print data.find_def('${dragonlong(str,str1)}')

