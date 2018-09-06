#!/usr/bin/env python
# -*-coding:utf-8-*-

#从app模块中即从__init__.py中导入创建的app应用
from app import app
from flask import request
from lib.file_mange import *
import json

#建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。

#获取侧边栏配置
@app.route('/get_nav_conf')
def get_nav_conf():
    json_string = get_json_file('config/global.json')
    global_json = json.loads(json_string)
    response = {}
    response=json_string
    return response


#更新侧边栏配置
@app.route('/submit_nav_conf', methods=['POST'])
def submit_nav_conf():
    form = request.form.to_dict()
    return "侧边栏配置更新成功了！"


#新建一个项目
@app.route('/add_new_proj', methods=['POST'])
def add_new_proj():
    if request.form.get('id'):
        form = request.form.to_dict()

        proj = {}
        proj['id'] = 'p_'+form['id']
        proj['name'] = form['name']
        proj['desc'] = form['desc']
        proj['case_suits'] = None

        json_string = get_json_file('config/global.json')
        global_json = json.loads(json_string)
        has_repeat = False  #是否已添加
        for project in global_json['projects']:
            if proj['id'] == project['id']:
                has_repeat = True
                break
        if not has_repeat:
            global_json['project'].append(proj)

            #覆盖原数据
            write_str_into_file('config/global.json',json.dumps(global_json))

            #创建数据目录
            make_dir('data/projects/'+ str(proj['id']))
            #创建用例集和用例映射文件
            write_str_into_file('config/case_suits/{}.json'.format(str(proj['id'])),json.dumps({}))

            content = json.dumps({"code":"1000","msg":"项目添加成功，id:"+ str(proj['id'])})
        else:
            content = json.dumps({"code":"1002","msg":"项目重复，id:"+ str(proj['id'])})
    else:
        content = json.dumps({"code":"2001","msg":"缺少关键参数值id"})
    return content


#给项目新增一个测试用例集
@app.route('/add_new_case_group', methods=['POST'])
def add_new_case_group_for_proj():
    if request.form.get('proId') and request.form.get('case_suit'):
        proId = request.form.get('proId')
        case_suit = request.form.get('case_suit')
        case_suit = json.loads(case_suit)
        case_suit['id'] = proId + '_' + case_suit['id']


        json_string = get_json_file('config/global.json')
        global_json = json.loads(json_string)
        projs = global_json['project']

        isAdd = False  #是否已添加
        for proj in projs:
            if proId == proj['id']:
                has_repeat = False
                for suit in proj['case_suits']:
                    if suit['suit_id'] == case_suit['id']:
                        has_repeat = True
                        response = json.dumps({"code":'1002',"msg":"测试用例集不能重复添加！case id重复："+suit['suit_id']})
                        break

                temp_suit = {}
                temp_suit['suit_id'] = case_suit['id']
                temp_suit['name'] = case_suit['name']
                temp_suit['desc'] = case_suit['desc']
                proj['case_suits'].append(temp_suit) #添加用例集
                isAdd=True
                #覆盖元数据
                write_str_into_file('config/global.json',json.dumps(global_json))
                #初始化配置文件
                write_str_into_file('config/case_suits/{}.json'.format(str(proj['id'])),json.dumps({temp_suit['suit_id']:[]}))
                response = json.dumps({"code":'1000',"msg":"测试用例集添加成功！"})
                break

        if (not isAdd) and (not has_repeat):
            response = json.dumps({"code":'1001',"msg":"测试用例集添加失败！"})

    else:
        response = json.dumps({"code":"2001","msg":"缺少关键参数值proId或case_suit！"})

    return response


#给用例集添加一个用例
@app.route('/add_new_case', methods=['POST'])
def add_new_case_for_group():
    try:
        if request.form.get('proId') and request.form.get('suit_id'):
            projId = request.form.get('proId')
            suit_id = request.form.get('suit_id')
            form = request.form.get('case')
            case_suit = json.loads(form)


            json_string = get_json_file('config/case_suits/{}.json'.format(projId))
            if json_string is not None and json_string != '':
                pro_json = json.loads(json_string)
                if suit_id in pro_json.keys():

                    pro_json[suit_id].append(case_suit['case_name'])  #添加测试集和用例映射关系
                    #保存case数据文件
                    write_str_into_file('data/projects/'+ str(projId)+'/'+case_suit['case_name'],form)
                    response = json.dumps({"code":'1000',"msg":"测试用例添加成功！"})
            else:
                response = json.dumps({"code":"2002","msg":"缺测试集和用例映射关系文件异常！"})

        else:
            response = json.dumps({"code":"2001","msg":"缺少关键参数值proId或suit_id！"})
        return response
    except:
        response = json.dumps({"code":'1001',"msg":"测试用例添加失败！"})
        return response


#获取一个用例的详细信息
@app.route('/get_case_detail', methods=['GET'])
def get_case_detail():
    try:
        print request.form.to_dict
        if request.args.get('proId') and request.args.get('case_id'):
            projId = request.args.get('proId')
            case_id = request.args.get('case_id')
            json_string = get_json_file('data/projects/'+ str(projId)+'/'+case_id + '.json')
            response = json.dumps({"code":"1000","msg":"用例获取成功！",'case':json.loads(json_string)})
        else:
            response = json.dumps({"code":"2001","msg":"缺少关键参数值proId或case_id！"})
        return response
    except:
        response = json.dumps({"code":'1001',"msg":"测试用例获取失败！"})
        return response


#编辑一个用例
@app.route('/edit_case', methods=['POST'])
def edit_case():
    try:
        print request.form.to_dict
        if request.form.get('proId') and request.form.get('case_id'):
            projId = request.form.get('proId')
            case_id = request.form.get('case_id')
            form = request.form.get('case')
            #保存case数据文件
            write_str_into_file('data/projects/'+ str(projId)+'/'+case_id+'.json',form)
            response = json.dumps({"code":'1000',"msg":"测试用例修改成功！"})
        else:
            response = json.dumps({"code":"2001","msg":"缺少关键参数值proId或case_id！"})
        return response
    except:
        response = json.dumps({"code":'1001',"msg":"测试用例修改失败！"})
        return response


#添加一个辅助方法集（项目）
@app.route('/add_methods_group', methods=['POST'])
def add_new_methods_group():
    pass


#增加一个辅助方法
@app.route('/add_new_method', methods=['POST'])
def add_new_method_for_group():
    pass


#修改一个辅助方法
@app.route('/edit_method', methods=['POST'])
def edit_method():
    pass

if __name__ == '__main__':
    pass