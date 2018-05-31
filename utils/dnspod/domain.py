# -*- coding: utf-8 -*-
# Author zwhset
'''
DnsPod Domain API
result:
    {
        'status' : {
            'code' : '1',
            'message' : '4.6'
        }
    }
成功与否判断status的code即可，如果为1则成功。
'''

from utils.dnspod.connect import Public

DOMAIN_TYPE = {
    'all'       : '所有域名',
    'mine'      : '我的域',
    'share'     :'共享给我的域名',
    'ismark'    : '星标域名',
    'pause'     : '暂停域名',
    'vip'       : 'VIP域名',
    'recent'    : '最近操作过的域名',
    'share_out' : '我共享出去的域名'
}
DOMAIN_MARK_TYPE = ['yes', 'no']

class Domain(Public):

    def __init__(self):
        super(Domain, self).__init__()

    def check_res(self, send_res):
        try:
            ret_code =  int(send_res['status']['code'])
        except:
            ret_code = None

        if ret_code == 1:
            return True,send_res
        else:
            try:
                return False, send_res.get('status', {}).get('message', None) or send_res
            except Exception as e:
                return False, send_res

    def create(self, domain, group_id=None, is_mark=None):
        '''添加域名'''
        action = 'Domain.Create'

        params = {}
        if group_id:
            params['group_id'] = group_id
        if is_mark:
            is_mark = is_mark.lower()
            if is_mark not in DOMAIN_MARK_TYPE:
                return ValueError, "params error, is_mark need in ['yes', 'no']"
            else:
                params['is_mark'] = is_mark
        params['domain'] = domain

        return self.check_res(self.send(action=action, params=params))

    def list(self, type=None, offset=None, length=None,
             group_id=None, keyword=None):
        '''域名列表'''
        action = 'Domain.List'

        params = {}
        if type:
            type = type.lower()
            if type not in DOMAIN_TYPE:
                raise ValueError("params error, domain type error.")
        if keyword:
            params['keyword'] = keyword
        if offset:
            params['offset'] = offset
            params['length'] = length
        if group_id:
            params['group_id'] = group_id

        bool_val ,re = self.check_res(self.send(action=action, params=params))
        if bool_val:
            res = re.get("domains",[])
        else:
            res = re
        return res

    def remove(self, domain=None, domain_id=None):
        '''删除域名'''
        action = 'Domain.Remove'

        params = {}
        if not (domain or domain_id):
            raise ValueError("params error, domain or domain_id not fund.")

        if domain:
            params['domain'] = domain
        else:
            params['domain_id'] = domain_id

        return self.check_res(self.send(action=action, params=params))

    def status(self, domain=None, domain_id=None, status=None):
        '''设置域名状态'''
        action = 'Domain.Status'

        params = {}
        if not (domain or domain_id):
            raise ValueError("params error, domain or domain_id not fund.")

        if domain:
            params['domain'] = domain
        else:
            params['domain_id'] = domain_id

        status_type = ['enable', 'disable']
        if status:
            status = status.lower()
            if status not in status_type:
                raise ValueError("params error, status need in ['enable', 'disable']")
            params['status'] = status

        return self.check_res(self.send(action=action, params=params))

    def info(self, domain=None, domain_id=None):
        '''获取域名信息'''
        action = 'Domain.Info'

        params = {}
        if not (domain or domain_id):
            raise ValueError("params error, domain or domain_id not fund.")

        if domain:
            params['domain'] = domain
        else:
            params['domain_id'] = domain_id

        return self.send(action=action, params=params)

    def log(self, domain=None, domain_id=None, offset=None, length=100):
        '''域名日志'''
        action = 'Domain.Log'

        params = {}
        if not (domain or domain_id):
            raise ValueError("params error, domain or domain_id not fund.")

        if domain:
            params['domain'] = domain
        else:
            params['domain_id'] = domain_id

        if offset:
            params['offset'] = offset
        params['length'] = length

        return self.check_res(self.send(action=action, params=params))

    def group_list(self):
        '''域名分组域名'''
        action = 'Domaingroup.List'
        return self.send(action=action)

    def group_create(self, group_name):
        '''创建域名分组'''
        action = 'Domaingroup.Create'

        params = dict(group_name=group_name)
        return self.check_res(self.send(action=action, params=params))

    def group_modify(self, group_id, group_name):
        '''修改域名分组的组名'''
        action = 'Domaingroup.Modify'

        params = dict(group_id=group_id, group_name=group_name)
        return self.check_res(self.send(action=action, params=params))

    def group_remove(self, group_id):
        '''删除域名分组'''
        action = 'Domaingroup.Remove'

        params = dict(group_id=group_id)
        return self.check_res(self.send(action=action, params=params))

    def change_group(self, group_id, domain_id=None, domain=None):
        '''设置域名分组'''
        action = 'Domain.Changegroup'

        params = {}
        if not (domain or domain_id):
            raise ValueError("params error, domain or domain_id not fund.")

        if domain:
            params['domain'] = domain
        else:
            params['domain_id'] = domain_id

        params['group_id'] = group_id

        return self.check_res(self.send(action=action, params=params))

    def ismark(self,is_mark, domain_id=None, domain=None):
        '''设置域名星标'''
        action = 'Domain.Ismark'

        params = {}
        if not (domain or domain_id):
            raise ValueError("params error, domain or domain_id not fund.")

        if domain:
            params['domain'] = domain
        else:
            params['domain_id'] = domain_id

        is_mark = is_mark.lower()
        if is_mark not in DOMAIN_MARK_TYPE:
            raise ValueError("params error, is_mark need in ['yes', 'no']")

        return self.send(action=action, params=params)

    def remark(self, remark, domain_id=None, domain=None):
        '''设置域名备注'''
        action = 'Domain.Remark'

        params = {}
        if not (domain or domain_id):
            raise ValueError("params error, domain or domain_id not fund.")

        if domain:
            params['domain'] = domain
        else:
            params['domain_id'] = domain_id
        params['remark'] = remark

        return self.check_res(self.send(action=action, params=params))

    def purview(self, domain_id=None, domain=None):
        '''获取域名权限'''
        action = 'Domain.Purview'

        params = {}
        if not (domain or domain_id):
            raise ValueError("params error, domain or domain_id not fund.")

        if domain:
            params['domain'] = domain
        else:
            params['domain_id'] = domain_id

        return self.send(action=action, params=params)

    def acquire(self, domain):
        '''域名取回获取WHOIS邮箱列表'''
        action = 'Domain.Purview'

        params = dict(domain=domain)

        return self.send(action=action, params=params)

    def searchenginepush(self,domain_id,status):
        '''是否开启搜索引擎推送'''
        action = 'Domain.Searchenginepush'

        params = dict(domain_id=domain_id,status=status)

        return self.check_res(self.send(action=action,params=params))

    def lock(self,domain_id,days):
        '''锁定域名'''
        action = 'Domain.Lock'

        params = dict(domain_id=domain_id,days=days)

        return self.check_res(self.send(action=action,params=params))