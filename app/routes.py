#!/usr/bin/env python
# -*-coding:utf-8-*-

#从app模块中即从__init__.py中导入创建的app应用
from app import app
from flask import Flask
from flask import request

#建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。

#获取侧边栏配置
@app.route('/get_nav_conf')
def get_nav_conf():
    return "Hello,World!"

#更新侧边栏配置
@app.route('/submit_nav_conf',methods=['POST'])
def submit_nav_conf(json):
    form = request.form.to_dict()
    return "侧边栏配置更新成功了！"

if __name__ == '__main__':
    pass