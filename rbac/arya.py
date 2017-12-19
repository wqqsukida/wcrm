from arya.service import v1
from . import models
from django.forms import ModelForm
from django.forms import widgets as form_widgets

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

########################### User ###########################
class UserModelForm(ModelForm):
    class Meta:
        model = models.User
        fields = "__all__"
        widgets = {
            'name':form_widgets.TextInput(attrs={'class':'form-control'}),
            'roles':form_widgets.SelectMultiple(attrs={'class':'form-control'}),
        }
        error_messages = {
            'name':{
                'required':'*用户名不能为空'
            }
        }

class UserConfig(Permission_Config,v1.AryaConfig):
    def show_roles(self,row=None,is_header=None):
        if is_header:
            return "拥有角色"
        data = []
        class_list = row.roles.all()
        for item in class_list:
            data.append(item.__str__())

        return ','.join(data)

    list_display = ['name',show_roles]
    model_form_class = UserModelForm
v1.site.register(models.User,UserConfig)

########################### Role ###########################
class RoleModelForm(ModelForm):
    class Meta:
        model = models.Role
        fields = "__all__"
        widgets = {
            'title':form_widgets.TextInput(attrs={'class':'form-control'}),
            'permissions':form_widgets.SelectMultiple(attrs={'class':'form-control'}),
        }
        error_messages = {
            'title':{
                'required':'*角色名不能为空'
            }
        }

class RoleConfig(Permission_Config,v1.AryaConfig):
    def show_permissions(self,row=None,is_header=None):
        if is_header:
            return "拥有权限"
        data = []
        class_list = row.permissions.all()
        for item in class_list:
            data.append(item.__str__())

        return ','.join(data)
    list_display = ['title',show_permissions]
    model_form_class = RoleModelForm
v1.site.register(models.Role,RoleConfig)

########################### Permission ###########################
class PermissionModelForm(ModelForm):
    class Meta:
        model = models.Permission
        fields = "__all__"
        widgets = {
            'title':form_widgets.TextInput(attrs={'class':'form-control'}),
            'url':form_widgets.TextInput(attrs={'class':'form-control'}),
            'menu_gp':form_widgets.Select(attrs={'class':'form-control'}),
            'code':form_widgets.TextInput(attrs={'class':'form-control'}),
            'group':form_widgets.Select(attrs={'class':'form-control'}),
        }
        error_messages = {
            'title':{
                'required':'*权限名不能为空'
            },
            'url':{
                'required': '*url不能为空'
            },
            'code': {
                'required': '*code不能为空'
            },
        }

class PermissionConfig(Permission_Config,v1.AryaConfig):
    list_display = ['title','url','code','menu_gp','group']
    model_form_class = PermissionModelForm
    search_list = [
        {'k':'title__contains','type':None},
        {'k':'url__contains','type':None},
        {'k':'code__contains','type':None},
        {'k':'menu_gp__title__contains','type':None},
        {'k':'group__caption__contains','type':None},
    ]


    def multi_delete(self,request):
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()
    multi_delete.text = '批量删除'

    actions = [multi_delete,]

v1.site.register(models.Permission,PermissionConfig)

########################### Group ###########################
class GroupModelForm(ModelForm):
    class Meta:
        model = models.Group
        fields = "__all__"
        widgets = {
            'caption':form_widgets.TextInput(attrs={'class':'form-control'}),
            'menu':form_widgets.Select(attrs={'class':'form-control'}),
        }
        error_messages = {
            'caption':{
                'required':'*组名不能为空'
            }
        }

class GroupConfig(Permission_Config,v1.AryaConfig):
    list_display = ['caption','menu']
    model_form_class = GroupModelForm
v1.site.register(models.Group,GroupConfig)

########################### Menu ###########################
class MenuModelForm(ModelForm):
    class Meta:
        model = models.Menu
        fields = "__all__"
        widgets = {
            'title':form_widgets.TextInput(attrs={'class':'form-control'}),
        }
        error_messages = {
            'title':{
                'required':'*菜单名不能为空'
            }
        }

class MenuConfig(Permission_Config,v1.AryaConfig):
    list_display = ['title',]
    model_form_class = MenuModelForm
v1.site.register(models.Menu,MenuConfig)




