#!/usr/bin/env python
# -*-coding:utf-8-*-

import json
import hashlib
import os


#读取json文件
def get_json_file(path):
    if not path.endswith(".json"):
        print "文件{}不是json文件".format(path)
        return ''
    if not os.path.exists(path):
        print "文件{}不存在".format(path)
        return None

    with open(path,'r+') as f:
        json_string = f.read()
        if json.loads(json_string):
            return json_string
        else:
            print '读取的不是一个有效的json字符串！'
            return {}


'''
:path 待写入文件路径
:str  待写入字符串
:is_cover 是否覆盖文件
'''
def write_str_into_file(path,str,is_cover=True):
    print '正准备保存数据到{}中>>>>'.format(path)
    try:
        if not os.path.exists(path) or not os.path.isfile(path):
            with open(path,'w') as f:  #如果文件不存在，必须以写的方式打开
                f.write(str)
        else:
            if is_cover == True:
                with open(path,'w') as f:
                    f.write(str)
            else:
                with open(path,'a') as f: #追加写
                    f.write(str)
    except Exception,e:
        print "Func[write_str_into_file] error:%s" %(e)
        raise

#创建目录
def make_dir(path):
    try:
        if os.path.exists(path) and os.path.isdir(path):
            return True
        else:
            os.makedirs(path)
            return True
    except:
        return False

#获取文件MDS值
def get_file_md5(path):
    if not os.path.exists(path):
        print '文件{}不存在'.format(path)
        return None
    elif not os.path.isfile(path) :
        print '文件{}不是一个文件'.format(path)
        return None
    try:
        myhash = hashlib.md5()
        with open(path,'rb') as f:
            while True:
                b = f.read(8096)
                if not b:
                    break
                myhash.update(b)
        return myhash.hexdigest()
    except Exception,e:
        print 'Func[get_file_md5] error,path:{},e:{}'.format(path,e)
        raise


'''
:desc 获取某目录下所有文件绝对路径列表
:param dir_path 目录路径
'''
def get_file_paths_of_dir(file_list,dir_path):
    postfix = set(['xlsx','xls','json'])  # 设置要保存的文件格式
    if not os.path.isdir(dir_path):
        print '{}不是一个目录路径'.format(dir_path)
        return
    try:
        for file in os.listdir(dir_path):   #可以使用os.walk()方法来获取，但是需要用python3才可以
            file_path = os.path.join(dir_path,file).replace('\\','/')  #路径中去除\
            if os.path.isfile(file_path):   #必须是文件绝对路径
                if file.split('.')[-1] in postfix:  #只好获取在集合中后缀的文件路径
                    file_list.append(file_path)
                continue
            if os.path.isdir(file_path):
                get_file_paths_of_dir(file_list,file_path)
    except Exception,e:
        print 'Func[get_file_paths_of_dir] error:{},e:{}'.format(dir_path,e)
        raise


if __name__ == '__main__':
    path = os.getcwd()
    print '当前工作目录为：%s' %path

    print get_json_file('../config/global.json')