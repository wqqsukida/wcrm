# -*- coding: utf-8 -*-
from django.shortcuts import render,redirect,HttpResponseRedirect
from django.shortcuts import HttpResponse
import json
import time
from utils.dnspod.domain import Domain
from utils.dnspod import record
from utils.dnspod import dmonitor
from utils.mythread import MyThread
__all__ = ['connect', 'dmonitor', 'domain', 'record', 'user']

RESULT_CODE = {
    -1 : '登陆失败',
    -2 : 'API使用超出限制',
    -3 : '不是合法代理 (仅用于代理接口)',
    -4 : '不在代理名下 (仅用于代理接口)',
    -7 : '无权使用此接口',
    -8 : '登录失败次数过多，帐号被暂时封禁',
    -99 : '此功能暂停开放，请稍候重试',
    1 : '操作成功',
    2 : '只允许POST方法',
    3 : '未知错误',
    6 : '用户ID错误 (仅用于代理接口)',
    7 : '用户不在您名下 (仅用于代理接口)',
    83 : '该帐户已经被锁定，无法进行任何操作',
    85 : '该帐户开启了登录区域保护，当前IP不在允许的区域内',
}

#===================================================================
def dnspod(request):
    '''
    获取dnspod域名列表
    :return:
    '''
    d_obj = Domain()
    group_id = request.GET.get("group_id","")
    groups = d_obj.group_list().get('groups',[])
    domain_list = d_obj.list(group_id=group_id)
    result = {}

    status = request.GET.get("status", "")
    message = request.GET.get("message", "")
    if status.isdigit():
        result = {"code":int(status),"message":message}

    return render(request,"dnspod.html",{"domain_list":domain_list,
                                         "result":result,
                                         "groups":groups,
                                         "group_id":group_id
                                         },using='jinja2')

def add_domain(request):
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
        domain = request.POST.get("domain","")
        group_id = request.POST.get("group_id","")
        ismark = request.POST.get("ismark","")

        status,data = d_obj.create(domain,group_id,ismark)
        if status:
            result = {"code":0,"message":data['status']['message']}
        else:
            result = {"code":1,"message":data}

        return HttpResponseRedirect('/dnspod/?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                           result.get("message", "")))
        # return HttpResponseRedirect(reverse("dnspod",
        #                             kwargs={"status":result.get("code", ""),
        #                                     "message":result.get("message", "")}))
    else:
        return HttpResponse(json.dumps(dict(code=1,message="please use get/post method!")))

def del_domain(request):
    '''
    删除dnspod域名
    :return:
    '''
    d_obj = Domain()
    result = {}
    if request.method == "GET":
        domain_id = request.GET.get("domain_id", "")
        status, data = d_obj.remove(domain_id=domain_id)
        if status:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

        return HttpResponseRedirect('/dnspod/?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                           result.get("message", "")))
    else:
        return HttpResponse(json.dumps(dict(code=1, message="please use get method!")))

def domain_status(request):
    '''
    修改域名状态
    :return:
    '''
    d_obj = Domain()
    result = {}
    if request.method == "GET":
        domain_id = request.GET.get("domain_id", "")
        status = request.GET.get("status", "")
        status_val, data = d_obj.status(domain_id=domain_id, status=status)
        if status_val:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

        return HttpResponseRedirect('/dnspod/?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                           result.get("message", "")))
    else:
        return HttpResponse(json.dumps(dict(code=1, message="please use get method!")))

def domain_log(request):
    '''
    获取域名操作日志：默认100条
    :return:
    '''
    d_obj = Domain()

    if request.method == "GET":
        domain_id = request.GET.get("domain_id", "")
        status, data = d_obj.log(domain_id=domain_id)
        if status:
            log = '\n'.join(data.get("log", []))
            return HttpResponse(json.dumps(log))
        else:
            return HttpResponse(json.dumps(data))
    else:
        return HttpResponse(json.dumps(dict(code=1, message="please use get method!")))

def domain_searchenginepush(request):
    '''
    是否开启搜索引擎推送
    :return:
    '''
    d_obj = Domain()
    if request.method == "GET":
        domain_id = request.GET.get("domain_id", "")
        status = request.GET.get("status", "")
        status_val, data = d_obj.searchenginepush(domain_id=domain_id, status=status)
        if status_val:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

        return HttpResponseRedirect('/dnspod/?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                           result.get("message", "")))
    else:
        return HttpResponse(json.dumps(dict(code=1, message="please use get method!")))

def domain_remark(request):
    '''
    修改域名备注
    :return:
    '''
    d_obj = Domain()
    if request.method == "POST":
        domain_id = request.POST.get("domain_id", "")
        remark = request.POST.get("remark", "")
        status, data = d_obj.remark(remark=remark, domain_id=domain_id)
        if status:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

        return HttpResponseRedirect('/dnspod/?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                           result.get("message", "")))
    else:
        return HttpResponse(json.dumps(dict(code=1, message="please use post method!")))


def domain_lock(request):
    d_obj = Domain()
    if request.method == "POST":
        domain_id = request.POST.get("domain_id", "")
        days = request.POST.get("days", "")
        status, data = d_obj.lock(days=days, domain_id=domain_id)
        if status:
            result = {"code": 0, "message": '域名锁定成功，通过解锁码%s解锁，请妥善保管' % data['lock']['lock_code']}
        else:
            result = {"code": 1, "message": data}

        return HttpResponseRedirect('/dnspod/?status={0}&message={1}'.
                                    format(result.get("code", ""),
                                           result.get("message", "")))
    else:
        return HttpResponse(json.dumps(dict(code=1, message="please use post method!")))

# =====================域名分组================================
def domain_changegroup(request):
    '''
    设置域名分组
    :return:
    '''
    d_obj = Domain()
    result = {}
    domain_id = request.POST.get("domain_id", "")
    group_id = request.POST.get("group_id", "")
    status, data = d_obj.change_group(domain_id=domain_id, group_id=group_id)

    return HttpResponse(json.dumps(status))

def domain_addgroup(request):
    '''
    添加域名分组
    :return:
    '''
    d_obj = Domain()
    group_name = request.POST.get("group_name", "")

    status, data = d_obj.group_create(group_name)
    if status:
        result = {"code": 0, "message": data['status']['message']}
    else:
        result = {"code": 1, "message": data}

    return HttpResponseRedirect('/dnspod/?status={0}&message={1}'.
                                format(result.get("code", ""),
                                       result.get("message", "")))

def domain_modgroup(request):
    '''
    mod域名分组
    :return:
    '''
    d_obj = Domain()
    group_id = request.POST.get("group_id", "")
    group_name = request.POST.get("group_name", "")

    status, data = d_obj.group_modify(group_id, group_name)
    if status:
        result = {"code": 0, "message": data['status']['message']}
    else:
        result = {"code": 1, "message": data}

    return HttpResponseRedirect('/dnspod/?status={0}&message={1}'.
                                format(result.get("code", ""),
                                       result.get("message", "")))

def domain_delgroup(request):
    '''
    删除域名分组
    :return:
    '''
    d_obj = Domain()
    group_id = request.GET.get("group_id", "")

    status, data = d_obj.group_remove(group_id)
    if status:
        result = {"code": 0, "message": data['status']['message']}
    else:
        result = {"code": 1, "message": data}

    return HttpResponseRedirect('/dnspod/?status={0}&message={1}'.
                                format(result.get("code", ""),
                                       result.get("message", "")))
#=====================记录相关================================
def dnspod_record(request):
    '''
    获取dnspod域名的记录列表
    :return:
    '''
    result = {}
    record_list = []
    domain_info = {"id":"","name":""}

    status = request.GET.get("status", "")
    message = request.GET.get("message", "")
    if status.isdigit():
        result = {"code":int(status),"message":message}

    if request.method == "GET":
        domain_id = request.GET.get("domain_id", "")
        r_obj = record.Record(domain_id=domain_id)
        status_val,data = r_obj.list()
        if status_val:
            record_list = data.get("records",[])
            domain_info = data.get("domain",{"id":"","name":""})
        else:
            result = {"code": 1, "message": data}
        types = record.RECORD_TYPE
        lines = record.RECORD_LINE

        return render(request,"dnspod_record.html",
                      {"record_list":record_list,
                      "domain_info":domain_info,
                      "types":types,
                      "lines":lines,
                      "result":result
                      },using='jinja2')
    else:
        return HttpResponse(json.dumps(dict(code=1,message="please use get method!")))

def add_record(request):
    '''
    添加dnspod域名的记录
    :return:
    '''
    if request.method == "POST":
        domain_id = request.POST.get("domain_id", "")
        sub_domain = request.POST.get("sub_domain", "")
        record_type = request.POST.get("record_type", "")
        record_line = request.POST.get("record_line", "")
        value = request.POST.get("value", "")
        mx = request.POST.get("mx", "")
        ttl = request.POST.get("ttl", "")
        status = request.POST.get("status", "")
        weight = request.POST.get("weight", "")

        r_obj = record.Record(domain_id=domain_id)
        try:
            status_val, data = r_obj.create(sub_domain=sub_domain, record_type=record_type,
                                            record_line=record_line, value=value, mx=mx,
                                            ttl=ttl, status=status, weight=weight)
            if status_val:
                result = {"code": 0, "message": data['status']['message']}
            else:
                result = {"code": 1, "message": data}
        except Exception as e:
            result = {"code": 1, "message": e}

        return HttpResponseRedirect('/dnspod_record/?status={0}&message={1}&domain_id={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           domain_id))
    else:
        return HttpResponse(json.dumps(dict(code=1,message="please use post method!")))


def del_record(request):
    '''
    删除dnspod域名的记录
    :return:
    '''
    if request.method == "GET":
        record_id = request.GET.get("record_id", "")
        domain_id = request.GET.get("domain_id", "")
        r_obj = record.Record(domain_id=domain_id)

        status, data = r_obj.remove(record_id)
        try:
            if status:
                result = {"code": 0, "message": data['status']['message']}
            else:
                result = {"code": 1, "message": data}
        except Exception as e:
            result = {"code": 1, "message": e}

        return HttpResponseRedirect('/dnspod_record/?status={0}&message={1}&domain_id={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           domain_id))
    else:
        return HttpResponse(json.dumps(dict(code=1,message="please use get method!")))


def mod_record(request):
    '''
    修改dnspod域名的记录
    :return:
    '''
    if request.method == "GET":  # 获取该条记录的信息
        record_id = request.GET.get("record_id", "")
        domain_id = request.GET.get("domain_id", "")
        r_obj = record.Record(domain_id=domain_id)

        status, data = r_obj.info(record_id)
        if status:
            return HttpResponse(json.dumps(data.get("record",{})))
        else:
            return HttpResponse(json.dumps(data))

    elif request.method == "POST":  # 修改该条记录
        domain_id = request.POST.get("domain_id", "")
        record_id = request.POST.get("record_id", "")
        sub_domain = request.POST.get("sub_domain", "")
        record_type = request.POST.get("record_type", "")
        record_line = request.POST.get("record_line", "")
        value = request.POST.get("value", "")
        mx = request.POST.get("mx", "")
        ttl = request.POST.get("ttl", "")
        status = request.POST.get("status", "")
        weight = request.POST.get("weight", "")

        r_obj = record.Record(domain_id=domain_id)
        try:
            status_val, data = r_obj.modify(record_id=record_id, sub_domain=sub_domain,
                                            record_type=record_type, record_line=record_line,
                                            value=value, mx=mx, ttl=ttl, status=status,
                                            weight=weight)

            if status_val:
                result = {"code": 0, "message": data['status']['message']}
            else:
                result = {"code": 1, "message": data}
        except Exception as e:
            result = {"code": 1, "message": e}

        return HttpResponseRedirect('/dnspod_record/?status={0}&message={1}&domain_id={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           domain_id))
    else:
        return HttpResponse(json.dumps(dict(code=1,message="please use get/post method!")))


def record_status(request):
    '''
    修改记录状态
    :return:
    '''
    if request.method == "GET":
        record_id = request.GET.get("record_id", "")
        domain_id = request.GET.get("domain_id", "")
        status = request.GET.get("status", "")
        r_obj = record.Record(domain_id=domain_id)

        status_val, data = r_obj.status(record_id=record_id, status=status)
        if status_val:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

        return HttpResponseRedirect('/dnspod_record/?status={0}&message={1}&domain_id={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           domain_id))
    else:
        return HttpResponse(json.dumps(dict(code=1,message="please use get method!")))


def record_remark(request):
    '''
    修改记录备注
    :return:
    '''
    if request.method == "POST":
        record_id = request.POST.get("record_id", "")
        domain_id = request.POST.get("domain_id", "")
        remark = request.POST.get("remark", "")
        r_obj = record.Record(domain_id=domain_id)
        try:
            status_val, data = r_obj.remark(record_id=record_id, remark=remark)
            if status_val:
                result = {"code": 0, "message": data['status']['message']}
            else:
                result = {"code": 1, "message": data}
        except Exception as e:
            result = {"code": 1, "message": e}
        return HttpResponseRedirect('/dnspod_record/?status={0}&message={1}&domain_id={2}'.
                                    format(result.get("code", ""),
                                           result.get("message", ""),
                                           domain_id))
    else:
        return HttpResponse(json.dumps(dict(code=1,message="please use post method!")))
#==========================D监控相关===============
def dnspod_d(request):
    result = {}
    monitors = []
    status = request.GET.get("status", "")
    message = request.GET.get("message", "")

    if status.isdigit():
        result = {"code":int(status),"message":message}

    if request.method == "GET":
        dm_obj = dmonitor.DMonitor()
        status_val, data = dm_obj.list()
        if status_val:
            monitors = data.get("monitors",[])
        else:
            result = {"code": 1, "message": data}

        return render(request,"dnspod_monitors.html",
                      {"monitors":monitors,"result":result},using='jinja2')



def list_subdomain(request):
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
    return HttpResponse(json.dumps(d2r_names))


def list_subvalue(request):
    '''
    列出子域名的A记录
    :return:
    '''
    dm_obj = dmonitor.DMonitor()

    domain_id = request.GET.get("domain_id","") or request.POST.get("domain_id", "")

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
        return HttpResponse(json.dumps(sub_domains))
    else:
        record_id = request.POST.get("record_id","")
        for s in sub_domains:
            if s['id'] == record_id:
                # print s
                return HttpResponse(json.dumps(s))


def create_monitor(request):
    '''
    创建监控
    :return:
    '''
    dm_obj = dmonitor.DMonitor()
    result = {}
    if request.method == "POST":
        domain_id = request.POST.get("domain_id","")
        record_id = request.POST.get("record_id","")
        monitor_interval = int(request.POST.get("monitor_interval",""))
        host = request.POST.get("host","")
        port = request.POST.get("port", "")
        monitor_path = request.POST.get("monitor_path","")
        monitor_type = request.POST.get("monitor_type","")
        points = request.POST.get("points","")
        bak_ip = request.POST.get("bak_ip","")

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

    return HttpResponseRedirect('/dnspod_d/?status={0}&message={1}'.
                                format(result.get("code", ""),
                                       result.get("message", "")))


def remove_monitor(request):
    '''
    删除监控
    :return:
    '''
    dm_obj = dmonitor.DMonitor()
    monitor_id = request.GET.get("monitor_id","")
    status,data = dm_obj.remove(monitor_id=monitor_id)
    if status:
        result = {"code": 0, "message": data['status']['message']}
    else:
        result = {"code": 1, "message": data}

    return HttpResponseRedirect('/dnspod_d/?status={0}&message={1}'.
                                format(result.get("code", ""),
                                       result.get("message", "")))


def monitor_info(request):
    '''
    获取监控信息
    :return:
    '''
    dm_obj = dmonitor.DMonitor()
    monitor_id = request.GET.get("monitor_id","")
    status,data = dm_obj.info(monitor_id=monitor_id)
    if status:
        res = data.get("info")
        return HttpResponse(json.dumps(res))
    else:
        return HttpResponse(json.dumps(data))


def modify_monitor(request):
    '''
    修改监控
    :return:
    '''
    #必选参数
    result = {}
    dm_obj = dmonitor.DMonitor()
    if request.method == "POST":
        monitor_id = request.POST.get("monitor_id","")
        host = request.POST.get("host","")
        monitor_path = request.POST.get("monitor_path","")
        port = request.POST.get("port","")
        monitor_interval = int(request.POST.get("monitor_interval",""))
        monitor_type = request.POST.get("monitor_type","")
        points = request.POST.getlist("points")
        bak_ip = request.POST.get("bak_ip","")
        #可选参数
        keep_ttl = request.POST.get("keep_ttl","")
        sms_notice = request.POST.get("sms_notice","")
        email_notice = request.POST.get("email_notice","")
        less_notice = request.POST.get("less_notice", "")
        callback_url = request.POST.get("callback_url","")
        callback_key = request.POST.get("callback_key","")

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

    return HttpResponseRedirect('/dnspod_d/?status={0}&message={1}'.
                                format(result.get("code", ""),
                                       result.get("message", "")))


def setstatus_monitor(request):
    '''
    设置监控状态
    :return:
    '''
    result = {}
    dm_obj = dmonitor.DMonitor()
    if request.method == "GET":
        status =  request.GET.get("status","")
        monitor_id = request.GET.get("monitor_id","")
        status_val,data = dm_obj.set_status(monitor_id=monitor_id,status=status)

        if status_val:
            result = {"code": 0, "message": data['status']['message']}
        else:
            result = {"code": 1, "message": data}

    return HttpResponseRedirect('/dnspod_d/?status={0}&message={1}'.
                                format(result.get("code", ""),
                                       result.get("message", "")))


def getdowns_monitor(request):
    '''
    获取监控警告
    :return:
    '''
    result = {}
    dm_obj = dmonitor.DMonitor()

    if request.method == "GET":
        status,data = dm_obj.get_downs()
        return HttpResponse(json.dumps(data))


def gethistory_monitor(request):
    '''
    获取监控历史
    :return:
    '''
    result = {}
    dm_obj = dmonitor.DMonitor()

    monitor_id = request.GET.get("monitor_id","")
    hours = request.GET.get("hours","")

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

    return render(request,'dnspod_monitor_history.html',
                  {"result":result,
                   "dashs":dashs,
                   "monitor_id":monitor_id,
                   "hours":hours,
                   "record_name":record_name
                   },using='jinja2')