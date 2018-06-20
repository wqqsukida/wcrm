# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# Created by Administrator on 2018/2/6

from flask import Blueprint, render_template, request, redirect, url_for, jsonify, make_response
b_dnspod = Blueprint('b_dnspod', __name__)

from dnspod.domain import Domain
from dnspod import record
from dnspod import dmonitor
from function import MyThread
import time

p = _users.Permission()
log = logs.Loger()

def out_result(status, message):
    if status: # True, errors
        if not message:
            message = "success"
        result = {"code":0, "message":message}
    else:
        result = {"code":1, "message":str(message)}
    return result

@b_dnspod.route('/dnspod',methods=['POST', 'GET'])
@p.is_login
@p.is_user_view
def dnspod():
    '''
    获取dnspod域名列表
    :return:
    '''
    d_obj = Domain()
    group_id = request.values.get("group_id","")
    groups = d_obj.group_list().get('groups',[])
    domain_list = d_obj.list(group_id=group_id)
    result = {}

    status = request.values.get("status", "")
    message = request.values.get("message", "")
    if status.isdigit():
        result = {"code":int(status),"message":message}

    return render_template("dnspod.html",domain_list=domain_list,result=result,groups=groups,group_id=group_id)

@b_dnspod.route('/dnspod/add_domain',methods=['POST', 'GET'])
@p.is_login
@p.is_user_view
def add_domain():
    '''
    添加dnspod域名
    :return:
    '''
    d_obj = Domain()
    result= {}
    # if request.method == "GET":
    #     group_list = d_obj.group_list()
    #     # 获取所有group_id
    #     ids = [{"group_id":g.get("group_id",""),"group_name":g.get("group_name","")}
    #            for g in group_list.get('groups',[])]
    #     # print ids
    #     return jsonify(ids)

    if request.method == "POST":
        domain = request.form.get("domain","")
        group_id = request.form.get("group_id","")
        ismark = request.form.get("ismark","")

        status,data = d_obj.create(domain,group_id,ismark)
        if status:
            result = {"code":0,"message":data['status']['message']}
        else:
            result = {"code":1,"message":data}

        return redirect(url_for("b_dnspod.dnspod",
                                status=result.get("code", ""),
                                message=result.get("message", "")))
    else:
        return jsonify(dict(code=1,message="please use get/post method!"))

@b_dnspod.route('/dnspod/del_domain',methods=['POST', 'GET'])
@p.is_login
@p.is_user_view
def del_domain():
    '''
    删除dnspod域名
    :return:
    '''
    d_obj = Domain()
    result = {}
    if request.method == "GET":
        domain_id = request.values.get("domain_id","")
        status,data = d_obj.remove(domain_id=domain_id)
        if status:
            result = {"code":0,"message":data['status']['message']}
        else:
            result = {"code": 1, "message": data}

        return redirect(url_for("b_dnspod.dnspod",
                                status=result.get("code", ""),
                                message=result.get("message", "")))
    else:
        return jsonify(dict(code=1,message="please use get method!"))

@b_dnspod.route('/dnspod/domain_status',methods=['POST', 'GET'])
@p.is_login
@p.is_user_view
def domain_status():
    '''
    修改域名状态
    :return:
    '''
    d_obj = Domain()
    result = {}
    if request.method == "GET":
        domain_id = request.values.get("domain_id", "")
        status = request.values.get("status", "")
        status_val, data = d_obj.status(domain_id=domain_id, status=status)
        if status_val:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

        return redirect(url_for("b_dnspod.dnspod",
                                status=result.get("code", ""),
                                message=result.get("message", "")))
    else:
        return jsonify(dict(code=1,message="please use get method!"))

@b_dnspod.route('/dnspod/domain_log',methods=['POST','GET'])
@p.is_login
@p.is_user_view
def domain_log():
    '''
    获取域名操作日志：默认100条
    :return:
    '''
    d_obj = Domain()

    if request.method == "GET":
        domain_id = request.values.get("domain_id","")
        status,data = d_obj.log(domain_id=domain_id)
        if status:
            log = '\n'.join(data.get("log", []))
            return jsonify(log)
        else:
            return jsonify(data)
    else:
        return jsonify(dict(code=1,message="please use get method!"))

@b_dnspod.route('/dnspod/domain_searchenginepush', methods=['POST', 'GET'])
@p.is_login
@p.is_user_view
def domain_searchenginepush():
    '''
    是否开启搜索引擎推送
    :return:
    '''
    d_obj = Domain()
    if request.method == "GET":
        domain_id = request.values.get("domain_id","")
        status = request.values.get("status","")
        status_val,data = d_obj.searchenginepush(domain_id=domain_id,status=status)
        if status_val:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

        return redirect(url_for("b_dnspod.dnspod",
                                status=result.get("code", ""),
                                message=result.get("message", "")))
    else:
        return jsonify(dict(code=1,message="please use get method!"))

@b_dnspod.route('/dnspod/domain_remark', methods=['POST', 'GET'])
@p.is_login
@p.is_user_view
def domain_remark():
    '''
    修改域名备注
    :return:
    '''
    d_obj = Domain()
    if request.method == "POST":
        domain_id = request.form.get("domain_id","")
        remark = request.form.get("remark","")
        status,data = d_obj.remark(remark=remark,domain_id=domain_id)
        if status:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

        return redirect(url_for("b_dnspod.dnspod",
                                status=result.get("code", ""),
                                message=result.get("message", "")))
    else:
        return jsonify(dict(code=1,message="please use get method!"))


@b_dnspod.route('/dnspod/domain_lock',methods=['POST','GET'])
@p.is_login
@p.is_user_view
def domain_lock():
    d_obj = Domain()
    if request.method == "POST":
        domain_id = request.form.get("domain_id","")
        days = request.form.get("days","")
        status,data = d_obj.lock(days=days,domain_id=domain_id)
        if status:
            result = {"code": 0, "message": '域名锁定成功，通过解锁码%s解锁，请妥善保管'%data['lock']['lock_code']}
        else:
            result = {"code": 1, "message": data}

        return redirect(url_for("b_dnspod.dnspod",
                                status=result.get("code", ""),
                                message=result.get("message", "")))
    else:
        return jsonify(dict(code=1,message="please use post method!"))

#=====================域名分组================================
@b_dnspod.route('/dnspod/domain_changegroup',methods=['POST', 'GET'])
@p.is_login
@p.is_user_view
def domain_changegroup():
    '''
    设置域名分组
    :return:
    '''
    d_obj = Domain()
    result = {}
    domain_id = request.values.get("domain_id", "")
    group_id = request.values.get("group_id","")
    status, data = d_obj.change_group(domain_id=domain_id,group_id=group_id)

    return jsonify(status)

@b_dnspod.route('/dnspod/domain_addgroup',methods=['POST', 'GET'])
@p.is_login
@p.is_user_view
def domain_addgroup():
    '''
    添加域名分组
    :return:
    '''
    d_obj = Domain()
    group_name = request.form.get("group_name","")

    status, data = d_obj.group_create(group_name)
    if status:
        result = {"code": 0, "message": data['status']['message']}
    else:
        result = {"code": 1, "message": data}

    return redirect(url_for("b_dnspod.dnspod",
                            status=result.get("code", ""),
                            message=result.get("message", "")))

@b_dnspod.route('/dnspod/domain_modgroup',methods=['POST', 'GET'])
@p.is_login
@p.is_user_view
def domain_modgroup():
    '''
    删除域名分组
    :return:
    '''
    d_obj = Domain()
    group_id = request.form.get("group_id","")
    group_name = request.form.get("group_name","")

    status, data = d_obj.group_modify(group_id,group_name)
    if status:
        result = {"code": 0, "message": data['status']['message']}
    else:
        result = {"code": 1, "message": data}

    return redirect(url_for("b_dnspod.dnspod",
                            status=result.get("code", ""),
                            message=result.get("message", "")))


@b_dnspod.route('/dnspod/domain_delgroup',methods=['POST', 'GET'])
@p.is_login
@p.is_user_view
def domain_delgroup():
    '''
    删除域名分组
    :return:
    '''
    d_obj = Domain()
    group_id = request.values.get("group_id","")

    status, data = d_obj.group_remove(group_id)
    if status:
        result = {"code": 0, "message": data['status']['message']}
    else:
        result = {"code": 1, "message": data}

    return redirect(url_for("b_dnspod.dnspod",
                            status=result.get("code", ""),
                            message=result.get("message", "")))

#=====================记录相关================================
@b_dnspod.route('/dnspod_record',methods=['POST', 'GET'])
@p.is_login
@p.is_user_view
def dnspod_record():
    '''
    获取dnspod域名的记录列表
    :return:
    '''
    result = {}
    record_list = []
    domain_info = {"id":"","name":""}

    status = request.values.get("status", "")
    message = request.values.get("message", "")
    if status.isdigit():
        result = {"code":int(status),"message":message}

    if request.method == "GET":
        domain_id = request.values.get("domain_id", "")
        r_obj = record.Record(domain_id=domain_id)
        status_val,data = r_obj.list()
        if status_val:
            record_list = data.get("records",[])
            domain_info = data.get("domain",{"id":"","name":""})
        else:
            result = {"code": 1, "message": data}
        types = record.RECORD_TYPE
        lines = record.RECORD_LINE

        return render_template("dnspod_record.html", record_list=record_list,
                               domain_info=domain_info,types=types,lines=lines,
                               result=result)
    else:
        return jsonify(dict(code=1,message="please use get method!"))

@b_dnspod.route('/dnspod_record/add_record',methods=['POST'])
@p.is_login
@p.is_user_view
def add_record():
    '''
    添加dnspod域名的记录
    :return:
    '''
    if request.method == "POST":
        domain_id = request.form.get("domain_id","")
        sub_domain = request.form.get("sub_domain","")
        record_type = request.form.get("record_type","")
        record_line = request.form.get("record_line","")
        value = request.form.get("value","")
        mx = request.form.get("mx","")
        ttl = request.form.get("ttl","")
        status = request.form.get("status","")
        weight = request.form.get("weight","")

        r_obj = record.Record(domain_id=domain_id)
        try:
            status_val,data = r_obj.create(sub_domain=sub_domain,record_type=record_type,
                                       record_line=record_line,value=value,mx=mx,
                                       ttl=ttl,status=status,weight=weight)
            if status_val:
                result = {"code": 0, "message": data['status']['message']}
            else:
                result = {"code": 1, "message": data}
        except Exception as e:
            result = {"code": 1, "message": e}

        return redirect(url_for("b_dnspod.dnspod_record",domain_id=domain_id,
                                status=result.get("code", ""),
                                message=result.get("message", "")))
    else:
        return jsonify(dict(code=1,message="please use post method!"))

@b_dnspod.route('/dnspod_record/del_record',methods=['POST','GET'])
@p.is_login
@p.is_user_view
def del_record():
    '''
    删除dnspod域名的记录
    :return:
    '''
    if request.method == "GET":
        record_id = request.values.get("record_id","")
        domain_id = request.values.get("domain_id","")
        r_obj = record.Record(domain_id=domain_id)

        status,data = r_obj.remove(record_id)
        try:
            if status:
                result = {"code": 0, "message": data['status']['message']}
            else:
                result = {"code": 1, "message": data}
        except Exception as e:
            result = {"code": 1, "message": e}

        return redirect(url_for("b_dnspod.dnspod_record",domain_id=domain_id,
                                status=result.get("code", ""),
                                message=result.get("message", "")))
    else:
        return jsonify(dict(code=1,message="please use get method!"))

@b_dnspod.route('/dnspod_record/mod_record',methods=['POST','GET'])
@p.is_login
@p.is_user_view
def mod_record():
    '''
    修改dnspod域名的记录
    :return:
    '''
    if request.method == "GET":    # 获取该条记录的信息
        record_id = request.values.get("record_id","")
        domain_id = request.values.get("domain_id","")
        r_obj = record.Record(domain_id=domain_id)

        status,data = r_obj.info(record_id)
        if status:
            return jsonify(data.get("record",{}))
        else:
            return jsonify(data)

    elif request.method == "POST":  # 修改该条记录
        domain_id = request.form.get("domain_id","")
        record_id = request.form.get("record_id","")
        sub_domain = request.form.get("sub_domain","")
        record_type = request.form.get("record_type","")
        record_line = request.form.get("record_line","")
        value = request.form.get("value","")
        mx = request.form.get("mx","")
        ttl = request.form.get("ttl","")
        status = request.form.get("status","")
        weight = request.form.get("weight","")

        r_obj = record.Record(domain_id=domain_id)
        try:
            status_val,data = r_obj.modify(record_id=record_id,sub_domain=sub_domain,
                                           record_type=record_type,record_line=record_line,
                                           value=value,mx=mx,ttl=ttl,status=status,
                                           weight=weight)

            if status_val:
                result = {"code": 0, "message": data['status']['message']}
            else:
                result = {"code": 1, "message": data}
        except Exception as e:
            result = {"code": 1, "message": e}

        return redirect(url_for("b_dnspod.dnspod_record",domain_id=domain_id,
                                status=result.get("code", ""),
                                message=result.get("message", "")))
    else:
        return jsonify(dict(code=1,message="please use get/post method!"))

@b_dnspod.route('/dnspod_record/record_status',methods=['POST','GET'])
@p.is_login
@p.is_user_view
def record_status():
    '''
    修改记录状态
    :return:
    '''
    if request.method == "GET":
        record_id = request.values.get("record_id","")
        domain_id = request.values.get("domain_id","")
        status = request.values.get("status","")
        r_obj = record.Record(domain_id=domain_id)

        status_val, data = r_obj.status(record_id=record_id,status=status)
        if status_val:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

        return redirect(url_for("b_dnspod.dnspod_record",domain_id=domain_id,
                                status=result.get("code", ""),
                                message=result.get("message", "")))
    else:
        return jsonify(dict(code=1,message="please use get method!"))

@b_dnspod.route('/dnspod_record/record_remark',methods=['POST','GET'])
@p.is_login
@p.is_user_view
def record_remark():
    '''
    修改记录备注
    :return:
    '''
    if request.method == "POST":
        record_id = request.form.get("record_id","")
        domain_id = request.form.get("domain_id","")
        remark = request.form.get("remark","")
        r_obj = record.Record(domain_id=domain_id)
        try:
            status_val, data = r_obj.remark(record_id=record_id,remark=remark)
            if status_val:
                result = {"code": 0, "message": data['status']['message']}
            else:
                result = {"code": 1, "message": data}
        except Exception as e:
            result = {"code": 1, "message": e}
        return redirect(url_for("b_dnspod.dnspod_record",domain_id=domain_id,
                                status=result.get("code", ""),
                                message=result.get("message", "")))
    else:
        return jsonify(dict(code=1,message="please use post method!"))

#==========================D监控相关===============
@b_dnspod.route('/dnspod_d',methods=['POST','GET'])
@p.is_login
@p.is_user_view
def dnspod_d():
    result = {}
    monitors = []
    status = request.values.get("status", "")
    message = request.values.get("message", "")

    if status.isdigit():
        result = {"code":int(status),"message":message}

    if request.method == "GET":
        dm_obj = dmonitor.DMonitor()
        status_val, data = dm_obj.list()
        if status_val:
            monitors = data.get("monitors",[])
        else:
            result = {"code": 1, "message": data}

        return render_template("dnspod_monitors.html", monitors=monitors,
                               result=result)

@b_dnspod.route('/dnspod_d/list_subdomain',methods=['POST','GET'])
@p.is_login
# @p.is_user_view
def list_subdomain():
    '''
    列出包含A记录的所有子域名
    :return:
    '''
    d_obj = Domain()
    dm_obj = dmonitor.DMonitor()

    domain_list = d_obj.list()

    id_list = [d.get("id") for d in domain_list]

    d2r_names = {}

    # st = time.time()
    li = []
    for did in id_list:
        t = MyThread(dm_obj.list_subdomain,args=(None,did))
        li.append(t)
        t.start()

    for t in li:
        t.join()  # 一定要join，不然主线程比子线程跑的快，会拿不到结果
        status, data = t.get_result()
        if status:
            d_name = data.get("domain",{}).get("name","")
            d_id = data.get("domain",{}).get("id","")
            r_name = data.get("subdomain",[])
            if r_name:
                d2r_names[d_name] = dict(id=d_id,rnames=r_name)
    # et = time.time()
    # print et - st

    # st = time.time()
    # for did in id_list:
    #     status,data = dm_obj.list_subdomain(domain_id=did)
    #     if status:
    #         d_name = data.get("domain",{}).get("name","")
    #         d_id = data.get("domain",{}).get("id","")
    #         r_name = data.get("subdomain",[])
    #         if r_name:
    #             d2r_names[d_name] = dict(id=d_id,rnames=r_name)
    # et = time.time()
    # print et - st

    # print d2r_names
    return jsonify(d2r_names)

@b_dnspod.route('/dnspod_d/list_subvalue',methods=['POST','GET'])
@p.is_login
# @p.is_user_view
def list_subvalue():
    '''
    列出子域名的A记录
    :return:
    '''
    dm_obj = dmonitor.DMonitor()

    domain_id = request.values.get("domain_id","")

    status, data = dm_obj.list_subdomain(domain_id=domain_id)
    sub_domains = []

    dic = {}
    st = time.time()
    if status:
        r_name = data.get("subdomain",[])
        for r in r_name:
            t = MyThread(dm_obj.list_sub_value,args=(None,domain_id,r))
            dic[r] = t
            t.start()
        for k,v in dic.items():
            v.join()  # 一定要join，不然主线程比子线程跑的快，会拿不到结果
            status, data = v.get_result()
            if status:
                s = dict(record_name=k,domain_name= data.get("domain").get("name"),
                         id=data.get("records")[0].get("id"),points=data.get("points").get("list"))
                sub_domains.append(s)
    et = time.time()
    # print et - st

    # st = time.time()
    # if status:
    #     r_name = data.get("subdomain",[])
    #     for r in r_name:
    #         status, data = dm_obj.list_sub_value(domain_id=domain_id,subdomain=r)
    #         if status:
    #             s = dict(record_name=r,domain_name= data.get("domain").get("name"),
    #                      id=data.get("records")[0].get("id"),points=data.get("points").get("list"))
    #             sub_domains.append(s)
    # et = time.time()
    # print et - st

    if request.method == "GET":
        return jsonify(sub_domains)
    else:
        record_id = request.values.get("record_id","")
        for s in sub_domains:
            if s['id'] == record_id:
                # print s
                return jsonify(s)

@b_dnspod.route('/dnspod_d/create_monitor',methods=['POST','GET'])
@p.is_login
@p.is_user_view
def create_monitor():
    '''
    创建监控
    :return:
    '''
    dm_obj = dmonitor.DMonitor()
    result = {}
    if request.method == "POST":
        domain_id = request.form.get("domain_id","")
        record_id = request.form.get("record_id","")
        monitor_interval = int(request.form.get("monitor_interval",""))
        host = request.form.get("host","")
        port = request.form.get("port", "")
        monitor_path = request.form.get("monitor_path","")
        monitor_type = request.form.get("monitor_type","")
        points = request.form.get("points","")
        bak_ip = request.form.get("bak_ip","")

        # print domain_id,record_id,monitor_interval,host,port,monitor_path, monitor_type,points,bak_ip
        try:
            status,data = dm_obj.create(domain_id=domain_id,record_id=record_id,monitor_interval=monitor_interval,
                                        host=host,port=port,monitor_path=monitor_path,
                                        monitor_type=monitor_type,points=points,bak_ip=bak_ip)
            if status:
                result = {"code": 0, "message": data['status']['message']}
            else:
                result = {"code": 1, "message": data}
        except Exception as e:
            result = {"code": 1, "message": e}

    return redirect(url_for("b_dnspod.dnspod_d",
                            status=result.get("code", ""),
                            message=result.get("message", "")))

@b_dnspod.route('/dnspod_d/remove_monitor',methods=['POST','GET'])
@p.is_login
@p.is_user_view
def remove_monitor():
    '''
    删除监控
    :return:
    '''
    dm_obj = dmonitor.DMonitor()
    monitor_id = request.values.get("monitor_id","")
    status,data = dm_obj.remove(monitor_id=monitor_id)
    if status:
        result = {"code": 0, "message": data['status']['message']}
    else:
        result = {"code": 1, "message": data}

    return redirect(url_for("b_dnspod.dnspod_d",
                            status=result.get("code", ""),
                            message=result.get("message", "")))

@b_dnspod.route('/dnspod_d/monitor_info',methods=['POST','GET'])
@p.is_login
# @p.is_user_view
def monitor_info():
    '''
    获取监控信息
    :return:
    '''
    dm_obj = dmonitor.DMonitor()
    monitor_id = request.values.get("monitor_id","")
    status,data = dm_obj.info(monitor_id=monitor_id)
    if status:
        res = data.get("info")
        return jsonify(res)
    else:
        return jsonify(data)

@b_dnspod.route('/dnspod_d/modify_monitor',methods=['POST','GET'])
@p.is_login
@p.is_user_view
def modify_monitor():
    '''
    修改监控
    :return:
    '''
    #必选参数
    result = {}
    dm_obj = dmonitor.DMonitor()
    if request.method == "POST":
        monitor_id = request.form.get("monitor_id","")
        host = request.form.get("host","")
        monitor_path = request.form.get("monitor_path","")
        port = request.form.get("port","")
        monitor_interval = int(request.form.get("monitor_interval",""))
        monitor_type = request.form.get("monitor_type","")
        points = request.form.getlist("points")
        bak_ip = request.form.get("bak_ip","")
        #可选参数
        keep_ttl = request.form.get("keep_ttl","")
        sms_notice = request.form.get("sms_notice","")
        email_notice = request.form.get("email_notice","")
        less_notice = request.form.get("less_notice", "")
        callback_url = request.form.get("callback_url","")
        callback_key = request.form.get("callback_key","")

        # print monitor_id,monitor_interval,host,port,monitor_path, monitor_type,points,bak_ip,keep_ttl,\
        #     sms_notice,email_notice,less_notice,callback_url,callback_key

        status,data = dm_obj.modify(monitor_id=monitor_id,host=host,monitor_path=monitor_path,
                                    port=port,monitor_interval=monitor_interval,monitor_type=monitor_type,
                                    points=points,bak_ip=bak_ip,
                                    keep_ttl=keep_ttl,sms_notice=sms_notice,email_notice=email_notice,
                                    less_notice=less_notice,callback_url=callback_url,callback_key=callback_key)
        if status:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

    return redirect(url_for("b_dnspod.dnspod_d",
                            status=result.get("code", ""),
                            message=result.get("message", "")))

@b_dnspod.route('/dnspod_d/setstatus_monitor',methods=['POST','GET'])
@p.is_login
@p.is_user_view
def setstatus_monitor():
    '''
    设置监控状态
    :return:
    '''
    result = {}
    dm_obj = dmonitor.DMonitor()
    if request.method == "GET":
        status =  request.values.get("status","")
        monitor_id = request.values.get("monitor_id","")
        status_val,data = dm_obj.set_status(monitor_id=monitor_id,status=status)

        if status_val:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

    return redirect(url_for("b_dnspod.dnspod_d",
                            status=result.get("code", ""),
                            message=result.get("message", "")))

@b_dnspod.route('/dnspod_d/getdowns_monitor',methods=['POST','GET'])
@p.is_login
# @p.is_user_view
def getdowns_monitor():
    '''
    获取监控警告
    :return:
    '''
    result = {}
    dm_obj = dmonitor.DMonitor()

    if request.method == "GET":
        status,data = dm_obj.get_downs()
        return jsonify(data)

@b_dnspod.route('/dnspod_d/gethistory_monitor',methods=['POST','GET'])
@p.is_login
# @p.is_user_view
def gethistory_monitor():
    '''
    获取监控历史
    :return:
    '''
    result = {}
    dm_obj = dmonitor.DMonitor()

    monitor_id = request.values.get("monitor_id","")
    hours = request.values.get("hours","")

    status,data = dm_obj.get_history(monitor_id=monitor_id,hours=hours) # 默认获取24小时

    if status:
        result = {"code": 0, "message": data['status']['message']}
        dashs = data.get("monitor_history",[])
        record_name = data['record']['sub_domain'] + '.' + data['domain']['domain']
    else:
        result = {"code": 1, "message": data}
        dashs = []
        record_name = ""
    # return jsonify(dashs)

    return render_template('dnspod_monitor_history.html',result=result,dashs=dashs,
                           monitor_id=monitor_id,hours=hours,record_name = record_name)