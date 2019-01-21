#coding=utf-8
import datetime
import json
def time_today(time=None):
    if time==None:
        return datetime.datetime.now().strftime('%Y-%m-%d')
    else:
        return time.strftime('%Y-%m-%d')
def dragonlong(*args):
    print eval(args[0])

    print args[1]

