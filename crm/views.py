from django.shortcuts import render,redirect,HttpResponseRedirect
from django.shortcuts import HttpResponse
from django.db.models import Q
from rbac.models import *
from rbac.service.init_permission import init_permission
import json
import paramiko
from utils.md5 import encrypt
from django.forms import Form,fields,widgets
from wqq.ops_base import *
from .models import *
from django.urls import reverse
############################取消装饰器在中间件里验证登录session##############
def auth(func):
    '''
    验证session装饰器函数
    '''
    def wrapper(request,*args,**kwargs):
        user_dict = request.session.get('is_login', None)  # 获取会话保存到数据库的字典
        if user_dict:
            res=func(request,user_dict,*args,**kwargs)
            return res
        else:
            return redirect('/login/')
    return wrapper
###########################################################################
def forbidden(request):
    return render(request,'403.html')

class LoginForm(Form):
    username = fields.CharField(
        required=True,
        error_messages={'required':'*用户名不能为空'},
        widget=widgets.TextInput(attrs={'class':'form-control',
                                        'type':'text',
                                        'id':'inputUsername3',
                                        'placeholder':'Username',
                                        'name':'username'
                                        })
    )
    password = fields.CharField(
        required=True,
        error_messages={'required': '*密码不能为空'},
        widget = widgets.PasswordInput(attrs={'class':'form-control',
                                        'id':'inputPassword3',
                                        'placeholder':'Password',
                                        'name':'password'
                                        })
    )

def login(request):
    '''
    login登录验证函数
    '''
    if request.method == "GET":
        form = LoginForm()
        return render(request,'login.html',{'form':form})
    else:
        response = {'status': True, 'data': None, 'msg': None}
        form = LoginForm(request.POST)
        if form.is_valid():
            user = request.POST.get('username',None)  #获取input标签里的username的值 None：获取不到不会报错
            pwd = request.POST.get('password',None)
            pwd = encrypt(pwd) #md5加密密码字符串
            user_obj = UserInfo.objects.filter(username=user, password=pwd).first()

            if user_obj:
                role = user_obj.auth.roles.values('title')
                # print(role)
                if role:
                    role = role.first().get('title')
                else:
                    role = '访客'
                request.session['is_login'] = {'user': user,'role':role} #仅作为登录后用户名和身份显示session
                init_permission(user_obj.auth,request)
                response['data']={}
            else:
                response['status'] = False
                response['msg']={'password':['*用户名或者密码错误']}
        else:
            response['status']=False
            response['msg']=form.errors
        # print(response)
        return HttpResponse(json.dumps(response))

def logout(request):
    '''
    logout删除session函数
    '''
    request.session.clear() #删除session
    return HttpResponseRedirect('/login/')

def index(request):
    '''
    index页面函数
    '''
    user_dict = request.session.get('is_login', None)
    username = user_dict['user']
    user_role = user_dict['role']
    # print('---当前登录用户/角色--->',username,user_role)
    return render(request,'index.html',locals())


def index_v3(request):
    return render(request,'index_v3.html')
from django.template.loader import render_to_string
def machines_dash(request):
    result = {}
    dashs = {}
    c = OpsMachineInfo()
    in_ip = request.GET.get('ip')
    step_time = request.GET.get("step_time", "1800")
    if step_time.isdigit():
        step_time = int(step_time)
    else:
        step_time = 1800

    if not in_ip:
        result = {"code":1,"message":"未提供IP地址"}
        # return render_to_string('machines_dash.html', context={'result':result, 'dashs':dashs, 'step_time':step_time}, request=request, )
        return render(request,'machines_dash.html',{'result':result, 'dashs':dashs, 'step_time':step_time},using='jinja2')

    dashs = c.dash(in_ip, step_time)
    if not dashs:
        result = {"code":1,"message":"此台机器未进行监控"}
        # return render_to_string('machines_dash.html', context={'result':result, 'dashs':dashs, 'step_time':step_time}, request=request, )
        return render(request,'machines_dash.html',{'result':result, 'dashs':dashs, 'step_time':step_time},using='jinja2')

    # return render_to_string('machines_dash.html', context={'result':result, 'dashs':dashs, 'step_time':step_time}, request=request, )
    return render(request,'machines_dash.html',{'result':result, 'dashs':dashs, 'step_time':step_time},using='jinja2')

def userinfo(request):
    return (json.dumps(dict(code=0, message="用户信息页面")))



from utils import get_cert
def get_cert_detail(request):
    '''
    获取域名证书信息方法
    :param request:
    :return:
    '''
    domain_detail ={}
    if request.method == "POST":

        domain = request.POST.get('domain').strip()
        #print(domain)
        domain_detail['val'] = get_cert.get_cert(domain)
        #print(domain_detail)

    return HttpResponse(json.dumps(domain_detail),content_type="application/json")

from utils.dnspod.domain import Domain
from utils.dnspod import record
from utils.dnspod import dmonitor
#========================================================================
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