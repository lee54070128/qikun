#!/usr/bin/env python
# -*-coding:utf-8-*-
import hashlib

#判断一个字符串是否为none火控
def defaultIfEmpty(string,defaultStr):
    return defaultStr if string==None or string == "" else string

#计算字符串的md5值
def md5(string):
    if(not isinstance(string,str)):
        print str,"不是字符串"
        return None
    m = hashlib.md5()
    m.update(string)
    return m.hexdigest()

if __name__ == '__main__':
    pass
