from django.db import models
from rbac import models  as rbac_model

class UserInfo(models.Model):
    """
    用户表
    """
    auth = models.OneToOneField(verbose_name='对应用户', to=rbac_model.User,null=True,blank=True)
    username = models.CharField(verbose_name="登录用户名",max_length=32)
    password = models.CharField(verbose_name='密码',max_length=64)
    email = models.CharField(verbose_name="Email",max_length=32,null=True,blank=True)
    class Meta:
        verbose_name_plural = "用户信息表"


class BussinessLine(models.Model):
    '''
    业务线表
    '''
    name = models.CharField(verbose_name="业务线名称",max_length=32)
    description = models.CharField(verbose_name="描述",null=True,max_length=64,blank=True)
    roles = models.ManyToManyField(verbose_name="管理角色",to=rbac_model.Role,blank=True)
    class Meta:
        verbose_name_plural = "业务线表"
    def __str__(self):
        return self.name

class Env(models.Model):
    '''
    主机环境表
    '''
    name = models.CharField(max_length=30)
    class Meta:
        verbose_name_plural = "主机环境表"
    def __str__(self):
        return self.name



class Asset(models.Model):
    '''
    主机表
    '''
    hostname=models.CharField(verbose_name="主机名",max_length=32)
    ip=models.CharField(verbose_name="IP地址",max_length=32)
    port=models.IntegerField(verbose_name="端口号",)
    model=models.CharField(verbose_name="主机类型",null=True,max_length=32,blank=True)
    env=models.ForeignKey(verbose_name="系统环境",to="Env",null=True,blank=True) #外键关联Env
    hardware=models.CharField(verbose_name="硬件配置",null=True,max_length=32,blank=True)
    bussiness=models.ForeignKey(verbose_name="所属业务线",to="BussinessLine")
    class Meta:
        verbose_name_plural = "主机表"
    def __str__(self):
        return self.hostname

class AssetDetail(models.Model):
    '''
    主机详情表
    '''
    asset = models.OneToOneField(Asset) #可以把一对一理解为一种特殊的一对多（多的一方外键为Unique）
    hostname = models.CharField(max_length=32,null=True)
    memory = models.CharField(max_length=32,null=True)
    cpu_model = models.CharField(max_length=32,null=True)
    vender = models.CharField(max_length=32,null=True)
    product = models.CharField(max_length=32,null=True)
    sn = models.CharField(max_length=64,null=True)
    osver = models.CharField(max_length=32,null=True)
    cpu_num = models.CharField(max_length=10,null=True)
    ip = models.CharField(max_length=32)

class DomainTop(models.Model):
    '''
    顶级域名表
    '''
    domain_name = models.CharField(verbose_name="一级域名名称",max_length=255,unique=True)
    creation_date = models.DateTimeField(verbose_name="域名创建时间",null=True,blank=True,default=None)
    expiration_date = models.DateTimeField(verbose_name="域名过期时间",null=True,blank=True,default=None)
    icp_num = models.CharField(verbose_name="ICP备案",max_length=255,null=True,blank=True,default=None)
    gongan_num = models.CharField(verbose_name="公安备案",max_length=255,null=True,blank=True,default=None)
    ssl_creation_date = models.DateField(verbose_name="证书创建时间",null=True,blank=True,default=None)
    ssl_expiration_date = models.DateField(verbose_name="证书过期时间",null=True,blank=True,default=None)
    ssl_brand = models.CharField(verbose_name="证书品牌", max_length=255,null=True,blank=True,default=None)
    ssl_proxy = models.CharField(verbose_name="证书代理", max_length=255,null=True,blank=True,default=None)
    is_public = models.BooleanField(verbose_name="是否是公网域名",default=1) # 1：公网 0：内网