#!/usr/bin/env python
# -*-coding:utf-8-*-

#从app模块中即从__init__.py中导入创建的app应用
from app import app
from flask import request,jsonify,make_response
from lib.file_mange import *
import json
import traceback

#建立路由，通过路由可以执行其覆盖的方法，可以多个路由指向同一个方法。

#生成标准的response
def gen_standard_response(response):
    rt = make_response(jsonify(response))
    rt.headers['Access-Control-Allow-Origin'] = '*'
    rt.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET,POST,PUT'
    rt.headers['Access-Control-Allow-Headers'] = 'Content-Type,Content-Length, Authorization, Accept,X-Requested-With'
    return rt

#获取侧边栏配置
@app.route('/api/get_nav_conf', methods=['OPTIONS', 'GET'])
def get_nav_conf():
    response={}
    if request.method == 'OPTIONS':
        return gen_standard_response(response)
    try:
        json_string = get_json_file('config/global.json')
        global_json = json.loads(json_string)
        projects=[]
        methods = []
        #构造项目信息
        for index,proj in enumerate(global_json['projects']):
            p = {}
            p['index'] = '2_' + str(index+1)
            p['projId'] = proj['id']
            p['name'] = proj['pro_name']
            p['sons'] = []
            if proj['case_suits'] != None and len(proj['case_suits'])>0:
                for p_index, son in enumerate(proj['case_suits']):
                    p_son = {}
                    p_son['index'] = p['index'] + '_' + str(p_index +1)
                    p_son['pageId'] = son['suit_id']
                    p_son['name'] = son['name']
                    p['sons'].append(p_son)
            projects.append(p)

        #构造方法信息
        for index,suit in enumerate(global_json['methods']):
            m = {}
            m['index'] = '3_' + str(index+1)
            m['suitId'] = suit['id']
            m['name'] = suit['method_name']
            m['sons'] = []
            if suit['method_suits'] != None and len(suit['method_suits'])>0:
                for s_index, son in enumerate(suit['method_suits']):
                    m_son = {}
                    m_son['index'] = m['index'] + '_' + str(s_index +1)
                    m_son['pageId'] = son['module_id']
                    m_son['name'] = son['module_name']
                    m['sons'].append(m_son)
            methods.append(m)

        #构造返回结果
        response={}
        response['code'] = '1000'
        response['data'] = {}
        response['data']['projects'] = projects
        response['data']['methods'] = methods
        response['msg'] = u'成功获取侧边栏信息！'
    except Exception,e:
        response['code'] = '1001'
        response['msg'] = u'获取侧边栏信息失败！'
        print 'e.message:\t', e.message
        print 'traceback.format_exc():\n%s' % traceback.format_exc()

    # rt = make_response(jsonify(response))
    # rt.headers['Access-Control-Allow-Origin'] = '*'
    # rt.headers['Access-Control-Allow-Methods'] = 'OPTIONS,HEAD,GET'
    return gen_standard_response(response)


#获取设置信息
@app.route('/api/get_setting', methods=['GET'])
def get_setting():
    response = {}
    form = request.form.to_dict()
    return gen_standard_response(response)

#获取所有项目
@app.route('/api/get_all_project', methods=['OPTIONS', 'GET'])
def get_all_project():
    response={}
    if request.method == 'OPTIONS':
        return gen_standard_response(response)
    try:
        json_string = get_json_file('config/global.json')
        global_json = json.loads(json_string)
        projects=[]
        #构造项目信息
        for index,proj in enumerate(global_json['projects']):
            p = {}
            p['index'] = '2_' + str(index+1)
            p['projId'] = proj['id']
            p['name'] = proj['pro_name']
            p['sons'] = []
            if proj['case_suits'] != None and len(proj['case_suits'])>0:
                for p_index, son in enumerate(proj['case_suits']):
                    p_son = {}
                    p_son['index'] = p['index'] + '_' + str(p_index +1)
                    p_son['pageId'] = son['suit_id']
                    p_son['name'] = son['name']
                    p['sons'].append(p_son)
            projects.append(p)

        #构造返回结果
        response={}
        response['code'] = '1000'
        response['data'] = projects
        response['msg'] = u'成功获取所有项目信息！'
    except Exception,e:
        response['code'] = '1001'
        response['msg'] = u'获取所有项目失败！'
        print 'e.message:\t', e.message
        print 'traceback.format_exc():\n%s' % traceback.format_exc()

    return gen_standard_response(response)

#新建一个项目
@app.route('/api/add_new_proj', methods=['POST','OPTIONS'])
def add_new_proj():
    response={}
    if request.method == 'OPTIONS':
        return gen_standard_response(response)
    print request.get_data()
    print request.data
    if request.json:  #content_type:application/json
        form = json.loads(request.get_data())
    else:#content_type:application/x-www-form-urlencoded
        form = request.form.to_dict()
    if 'id' in form.keys():
        proj = {}
        proj['id'] = 'p_'+form['id']
        proj['pro_name'] = form['name']
        proj['pro_desc'] = form['desc']
        proj['case_suits'] = []

        m_proj = {}
        m_proj['id'] = 'm_'+form['id']
        m_proj['method_name'] = form['name']
        m_proj['method_suits'] = []

        json_string = get_json_file('config/global.json')
        global_json = json.loads(json_string)
        has_repeat = False  #是否已添加
        if global_json['projects'] != None and len(global_json['projects'])>0:
            for project in global_json['projects']:
                if proj['id'] == project['id']:
                    has_repeat = True
                    break
        if not has_repeat:
            global_json['projects'].append(proj)
            global_json['methods'].append(m_proj)

            #覆盖原数据
            write_str_into_file('config/global.json',json.dumps(global_json,  encoding="UTF-8",indent=4))

            #创建数据目录
            make_dir('data/projects/'+ str(proj['id']))
            #创建用例集和用例映射文件
            write_str_into_file('config/case_suits/{}.json'.format(str(proj['id'])),json.dumps({}, indent=4))

            response = {"code":"1000","msg":u"项目添加成功，id:"+ str(proj['id'])}
        else:
            response = {"code":"1002","msg":u"项目重复，id:"+ str(proj['id'])}
    else:
        response = {"code":"2001","msg":u"缺少关键参数值id"}

    return gen_standard_response(response)


#给项目新增一个测试用例集
@app.route('/api/add_new_case_suit', methods=['POST','OPTIONS'])
def add_new_case_group_for_proj():
    response={}
    if request.method == 'OPTIONS':
        return gen_standard_response(response)
    if request.form.get('proId') and request.form.get('case_suit'):
        proId = request.form.get('proId')
        case_suit = request.form.get('case_suit')
        case_suit = json.loads(case_suit)
        case_suit['id'] = proId + '_' + case_suit['id']


        json_string = get_json_file('config/global.json')
        global_json = json.loads(json_string)
        projs = global_json['projects']

        isAdd = False  #是否已添加
        has_repeat = False
        has_proj=False #proId是否存在
        for proj in projs:
            if proId == proj['id']:
                has_proj=True
                if proj['case_suits'] != None and len(proj['case_suits'])>0:
                    for suit in proj['case_suits']:
                        if suit['suit_id'] == case_suit['id']:
                            has_repeat = True
                            response = json.dumps({"code":'1002',"msg":u"测试用例集不能重复添加！case id重复："+suit['suit_id']})
                            break
                else:
                    proj['case_suits']=[]

                temp_suit = {}
                temp_suit['suit_id'] = case_suit['id']
                temp_suit['name'] = case_suit['name']
                temp_suit['desc'] = case_suit['desc']
                proj['case_suits'].append(temp_suit) #添加用例集
                isAdd=True
                #覆盖元数据
                write_str_into_file('config/global.json',json.dumps(global_json, indent=4))
                #初始化配置文件
                write_str_into_file('config/case_suits/{}.json'.format(str(proj['id'])),json.dumps({temp_suit['suit_id']:[]}, encoding="UTF-8",indent=4))
                response = {"code":'1000',"msg":u"测试用例集添加成功！"}
                break

        if not has_proj:
            response = {"code":'1003',"msg":u"proId匹配不上！proId="+proId}
        elif not isAdd and (not has_repeat):
            response = {"code":'1001',"msg":u"测试用例集添加失败！"}

    else:
        response = {"code":"2001","msg":u"缺少关键参数值proId或case_suit！"}

    return gen_standard_response(response)


#给用例集添加一个用例
@app.route('/api/add_new_case', methods=['POST','OPTIONS'])
def add_new_case_for_suit():
    response={}
    if request.method == 'OPTIONS':
        return gen_standard_response(response)
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
                    write_str_into_file('data/projects/'+ str(projId)+'/'+case_suit['case_name'],form, encoding="UTF-8", indent=4)
                    response = {"code":'1000',"msg":u"测试用例添加成功！"}
            else:
                response = {"code":"2002","msg":u"缺测试集和用例映射关系文件异常！"}

        else:
            response = {"code":"2001","msg":u"缺少关键参数值proId或suit_id！"}

        return gen_standard_response(response)
    except Exception,e:
        print 'e.message:\t', e.message
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        response = json.dumps({"code":'1001',"msg":u"测试用例添加失败！"})
        return gen_standard_response(response)

#获取一个用例的详细信息
@app.route('/api/get_case_detail', methods=['GET'])
def get_case_detail():
    response={}
    try:
        if request.args.get('proId') and request.args.get('case_id'):
            projId = request.args.get('proId')
            case_id = request.args.get('case_id')
            json_string = get_json_file('data/projects/'+ str(projId)+'/'+case_id + '.json')
            response = {"code":"1000","msg":u"用例获取成功！",'case':json.loads(json_string)}
        else:
            response = {"code":"2001","msg":u"缺少关键参数值proId或case_id！"}
        return gen_standard_response(response)
    except Exception,e:
        print 'e.message:\t', e.message
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        response = {"code":'1001',"msg":u"测试用例获取失败！"}
        return gen_standard_response(response)


#编辑一个用例
@app.route('/api/edit_case', methods=['POST','OPTIONS'])
def edit_case():
    response = {}
    if request.method == 'OPTIONS':
        return gen_standard_response(response)
    try:
        print request.form.to_dict
        if request.form.get('proId') and request.form.get('case_id'):
            projId = request.form.get('proId')
            case_id = request.form.get('case_id')
            form = request.form.get('case')
            #保存case数据文件
            write_str_into_file('data/projects/'+ str(projId)+'/'+case_id+'.json',form, indent=4)
            response = {"code":'1000',"msg":u"测试用例修改成功！"}
        else:
            response = {"code":"2001","msg":u"缺少关键参数值proId或case_id！"}
        return gen_standard_response(response)
    except Exception,e:
        print 'e.message:\t', e.message
        print 'traceback.format_exc():\n%s' % traceback.format_exc()
        response = {"code":'1001',"msg":u"测试用例修改失败！"}
        return gen_standard_response(response)


#添加一个辅助方法集（项目）
@app.route('/api/add_methods_suit', methods=['POST','OPTIONS'])
def add_new_methods_group():
    response = {}
    if request.method == 'OPTIONS':
        return gen_standard_response(response)
    pass


#增加一个辅助方法
@app.route('/api/add_new_method', methods=['POST','OPTIONS'])
def add_new_method_for_group():
    response = {}
    if request.method == 'OPTIONS':
        return gen_standard_response(response)


#修改一个辅助方法
@app.route('/api/edit_method', methods=['POST','OPTIONS'])
def edit_method():
    if request.method == 'OPTIONS':
        return {}

#获取辅助方法详细信息
@app.route('/api/get_method_detail', methods=['GET'])
def get_method_detail():
    pass

if __name__ == '__main__':
    pass