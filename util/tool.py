#coding=utf-8
import datetime
import json
def time_today(time=None):
    if time==None:
        return datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        return time.strftime('%Y-%m-%d')
import re

