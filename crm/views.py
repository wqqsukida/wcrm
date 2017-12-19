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