# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# Created by Administrator on 2017/11/28
from arya.service import v1
from utils.md5 import encrypt
from django.utils.safestring import mark_safe
from . import models
from django.forms import ModelForm
from django.forms import widgets as form_widgets
from django.shortcuts import render,redirect,HttpResponse

######################## 检验是否存在添加，更改，删除权限 ########################
class Permission_Config(object):

    def get_show_add(self):
        code_list = self.request.permission_code_list # list,add,del,edit
        print('当前页面权限：',code_list)
        if 'add' in code_list:
            return True

    def get_list_display(self):
        code_list = self.request.permission_code_list

        result = []
        result.extend(self.list_display)
        # 如果有编辑权限
        if 'edit' in code_list:
            result.append(v1.AryaConfig.row_edit)
        # 如果有删除权限
        if 'del' in code_list:
            result.append(v1.AryaConfig.row_del)

        result.insert(0, v1.AryaConfig.row_checkbox)

        return result

########################### UserInfo ###########################
class UserInfoModelForm(ModelForm):
    class Meta:
        model = models.UserInfo
        fields = "__all__"
        widgets = {
            'username':form_widgets.TextInput(attrs={'class':'form-control'}),
            'password':form_widgets.PasswordInput(attrs={'class':'form-control'}),
            'email':form_widgets.EmailInput(attrs={'class':'form-control'}),
            'auth':form_widgets.Select(attrs={'class':'form-control'}),
        }
        error_messages = {
            'username':{
                'required':'*用户名不能为空'
            },
            'password': {
                'required': '*密码不能为空'
            },
        }

class UserInfoConfig(Permission_Config,v1.AryaConfig):
    '''
    对于用户信息表,因为提交密码时,要加密处理,且要2次确认,
    要重写AryaConfig下的add_view和change_view
    '''
    def add_view(self,request):
        self.request = request
        # self.model_class/ userinfo
        # self.model_class/ usertype
        model_form_cls = self.get_model_form_class()
        url_param = request.GET.get('_getarg')  # 获取前一个页面的页码
        red_url = self.reverse_list_url() + '?' + url_param # 返回列表的url(由列表url+?+page=拼接)
        if request.method == "GET":
            form = model_form_cls()
            return render(request,'arya/add_view.html',{'form':form,'red_url':red_url})
        else:
            form = model_form_cls(data=request.POST)
            if form.is_valid():
                username = request.POST.get("username")
                pwd = request.POST.get("password")
                pwd = encrypt(pwd)
                email = request.POST.get("email",None)
                auth = request.POST.get("auth")
                self.model_class.objects.create(username=username, password=pwd, email=email, auth_id=auth)
                # form.save()
                # 反向生成URL，跳转回列表页面
                return redirect(self.reverse_list_url())
            return render(request, 'arya/add_view.html', {'form': form,'red_url':red_url})

    def change_view(self,request,nid):
        self.request = request
        obj = self.model_class.objects.filter(pk=nid).first()
        # url_param = request.GET.get('_getarg')  # 获取前一个页面的页码
        red_url = self.reverse_list_url() # + '?' + url_param # 返回列表的url(由列表url+?+page=拼接)
        if not obj:
            return redirect(red_url)

        model_form_cls = self.get_model_form_class()
        if request.method == 'GET':
            # 在Input框中显示默认值
            form = model_form_cls(instance=obj)
            return render(request,'arya/change_view.html',{'form':form,'red_url':red_url})
        else:
            form = model_form_cls(instance=obj,data=request.POST)
            if form.is_valid():
                # form.save()
                username = request.POST.get("username")
                pwd = request.POST.get("password")
                pwd = encrypt(pwd)
                email = request.POST.get("email",None)
                auth = request.POST.get("auth")
                self.model_class.objects.filter(pk=nid).update(username=username, password=pwd, email=email, auth_id=auth)

                return redirect(self.reverse_list_url())
            return render(request, 'arya/change_view.html', {'form': form,'red_url':red_url})

    list_display = ['id','username','email','auth']
    model_form_class = UserInfoModelForm
v1.site.register(models.UserInfo,UserInfoConfig)

########################### Asset ###########################
class AssetModelForm(ModelForm):
    class Meta:
        model = models.Asset
        fields = "__all__"
        widgets = {
            'hostname':form_widgets.TextInput(attrs={'class':'form-control'}),
            'ip':form_widgets.TextInput(attrs={'class':'form-control'}),
            'port':form_widgets.TextInput(attrs={'class':'form-control'}),
            'model':form_widgets.TextInput(attrs={'class':'form-control'}),
            'env':form_widgets.Select(attrs={'class':'form-control'}),
            'hardware':form_widgets.TextInput(attrs={'class':'form-control'}),
            'bussiness':form_widgets.Select(attrs={'class':'form-control'}),
        }
        error_messages = {
            'hostname':{
                'required':'*主机名不能为空'
            },
            'ip': {
                'required': '*IP不能为空'
            },
            'port': {
                'required': '*端口不能为空'
            },
        }

class NewChangeList(v1.ChangeList):
    def table_body(self):
        table_data = []
        for obj in self.queryset:
            row = []
            for str_func in self.list_display:
                if isinstance(str_func, str):
                    if str_func == 'ip':
                        url = '/machines_dash?ip=' + getattr(obj, str_func)
                        col = mark_safe('<a href="{0}">{1}</a>'.format(url,getattr(obj, str_func)))
                    else:
                        col = getattr(obj, str_func)
                else:
                    col = str_func(self.config, obj)
                row.append(col)
            table_data.append(row)
        # print(table_data)
        return table_data

class AssetConfig(Permission_Config,v1.AryaConfig):
    list_display = ['hostname', 'ip', 'port', 'model','env','hardware','bussiness']
    model_form_class = AssetModelForm

    search_list = [
        {'k':'hostname__contains','type':None},
        {'k':'ip__contains','type':None},
        {'k':'port__contains','type':None},
        {'k':'model__contains','type':None},
        {'k':'env__name__contains','type':None},
        {'k':'hardware__contains','type':None},
        {'k':'bussiness__name__contains','type':None},
    ]
    def changelist_view(self,request):

        # UserInfoConfig对象 =  self
        # UserTypeConfig对象 =  self
        self.request = request
        if request.method == "POST":
            action_item_name = request.POST.get('select_ac') # multi_init /multi_delete
            if action_item_name:
                func = getattr(self,action_item_name)
                if func(request): # 执行action函数,若return，则无权限
                    return redirect('/403')

        from django.db.models import Q
        condition = Q()
        search_q = request.GET.get('q')
        search_list = self.get_search_list() # [name__contains,pwd]

        if search_q and search_list:
            for field in search_list:
                temp = Q()
                convert_type = field.get('type')
                if convert_type:
                    try:
                        search_q = convert_type(search_q)
                    except Exception as e:
                        continue
                temp.children.append((field.get('k'),search_q))
                condition.add(temp,'OR')
        # 在这里进行业务线过滤得到最后的queryset,admin除外
        user_dict = request.session.get('is_login', None)
        if user_dict['user']=='admin':
            queryset = self.model_class.objects.filter(condition)
        else:
            queryset = self.model_class.objects.filter(condition,bussiness__roles__user__userinfo__username=user_dict['user'])

        cl = NewChangeList(self,queryset)

        from django.http.request import QueryDict
        url_obj = QueryDict(mutable=True)
        url_obj['_getarg'] = request.GET.urlencode()
        # print(url_obj.urlencode())
        url_param = url_obj.urlencode()

        return render(request,'arya/changelist.html',{'cl':cl,'url_param':url_param})

    def multi_delete(self,request):
        pk_list = request.POST.getlist('pk')
        # print(request.permission_code_list)
        if 'del' in request.permission_code_list:
            self.model_class.objects.filter(id__in=pk_list).delete()
        else:
            return '没有权限！'

    multi_delete.text = '批量删除'
    actions = [multi_delete,]

v1.site.register(models.Asset, AssetConfig)

########################### BussinessLine ###########################
class BussinessLineModelForm(ModelForm):
    class Meta:
        model = models.BussinessLine
        fields = "__all__"
        widgets = {
            'name':form_widgets.TextInput(attrs={'class':'form-control'}),
            'description':form_widgets.TextInput(attrs={'class':'form-control'}),
            'roles':form_widgets.SelectMultiple(attrs={'class':'form-control'}),
        }
        error_messages = {
            'name':{
                'required':'*名称不能为空'
            },
        }

class BussinessLineConfig(Permission_Config,v1.AryaConfig):

    def show_roles(self,row=None,is_header=None):
        if is_header:
            return "管理角色"
        data = []
        class_list = row.roles.all()
        for item in class_list:
            data.append(item.__str__())
        return ','.join(data)

    list_display = ['name','description',show_roles]
    model_form_class = BussinessLineModelForm

v1.site.register(models.BussinessLine, BussinessLineConfig)