# -*- coding: utf-8 -*-
# Author zwhset

'''
Dnspod 域名接口，函数命令与Dnspod尽是保持一致
'''

from utils.dnspod import connect,record
# from record import RECORD_TYPE

BAK_RULE = ['pass', 'pause', 'pause2', 'auto'] # 不支持备用IP
NOTICE_RULE = ['me', 'share'] # 不使用

class DMonitor(connect.Public):

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

    def list_subdomain(self, domain=None, domain_id=None):
        '''列出包含A记录的子域名'''
        action = 'Monitor.Listsubdomain'

        params = {}
        if not (domain or domain_id):
            raise ValueError("params error, domain or domain_id not fund.")

        if domain:
            params['domain'] = domain
        else:
            params['domain_id'] = domain_id

        return self.check_res(self.send(action=action, params=params))

    def list_sub_value(self, domain=None, domain_id=None, subdomain="@"):
        '''列出子域名的A记录'''
        action = 'Monitor.Listsubvalue'

        params = {}
        if not (domain or domain_id):
            raise ValueError("params error, domain or domain_id not fund.")

        if domain:
            params['domain'] = domain
        else:
            params['domain_id'] = domain_id

        if not subdomain:
            raise ValueError("params error, need subdomain param")
        params['subdomain'] = subdomain


        return self.check_res(self.send(action=action, params=params))

    def list(self, domain=None, domain_id=None):
        '''监控列表'''
        action = 'Monitor.List'
        params = {}
        if domain:
            params['domain'] = domain
        else:
            params['domain_id'] = domain_id

        return self.check_res(self.send(action=action, params=params))

    def create(self, domain_id, record_id, port=80,
               monitor_interval=60, host=None, monitor_type="http",
               monitor_path="/", points="random", bak_ip="auto",
               keep_ttl="yes", sms_notice="me", email_notice="me",
               less_notice="no", callback_url="", callback_key=""):
        '''监控添加'''

        action = 'Monitor.Create'
        params = {}

        yn = ['yes', 'no']
        monitor_intervals =[180, 360, 600]
        monitor_types = ['http', 'https']

        #self._check_int(domain_id)
        params['domain_id'] = domain_id

        #self._check_int(record_id)
        params['record_id'] = record_id

        #self._check_port(port)
        params['port'] = port

        if monitor_interval not in monitor_intervals:
            raise ValueError("params monitor_interval need in [180, 360, 600]")
        self._check_int(monitor_interval)
        params['monitor_interval'] = monitor_interval

        if not host:
            raise ValueError("params host not fund")
        params['host'] = host

        if monitor_type not in monitor_types:
            raise ValueError("params monitor_type not in ['http', 'https']")
        params['monitor_type'] = monitor_type

        if not monitor_path:
            raise ValueError("params monitor_path not fund")
        params['monitor_path'] = monitor_path

        if not points:
            raise ValueError("params points not fund")
        params['points'] = points

        if bak_ip not in BAK_RULE:
            raise ValueError("params bak_ip not in ['pass', 'pause', 'pause2', 'auto']")
        params['bak_ip'] = bak_ip

        if keep_ttl not in yn:
            raise ValueError("params bak_ip not in ['yes', 'no']")
        params['keep_ttl'] = keep_ttl

        if sms_notice:
            params['keep_ttl'] = sms_notice

        if email_notice:
            params['email_notice'] = email_notice

        if less_notice:
            if less_notice not in yn:
                raise ValueError("params less_notice not in ['yes', 'no']")
            params['less_notice'] = less_notice

        if callback_url:
            params['callback_url'] = callback_url

        if callback_key:
            params['callback_key'] = callback_key
        res = self.send(action=action, params=params)
        # print res
        return self.check_res(res)

    def modify(self, monitor_id, port=80,
               monitor_interval=60, host=None, monitor_type="http",
               monitor_path="/", points="random", bak_ip="auto",
               keep_ttl="yes", sms_notice="me", email_notice="me",
               less_notice="no", callback_url="", callback_key=""):
        '''监控修改'''

        action = 'Monitor.Modify'
        params = {}

        yn = ['yes', 'no']
        monitor_intervals =[180, 360, 600]
        monitor_types = ['http', 'https']

        # self._check_int(monitor_id)
        params['monitor_id'] = monitor_id

        # self._check_port(port)
        params['port'] = port

        if monitor_interval not in monitor_intervals:
            raise ValueError("params monitor_interval need in [180, 360, 600]")
        self._check_int(monitor_interval)
        params['monitor_interval'] = monitor_interval

        if not host:
            raise ValueError("params host not fund")
        params['host'] = host

        if monitor_type not in monitor_types:
            raise ValueError("params monitor_type not in ['http', 'https']")
        params['monitor_type'] = monitor_type

        if not monitor_path:
            raise ValueError("params monitor_path not fund")
        params['monitor_path'] = monitor_path

        if not points:
            raise ValueError("params points not fund")
        params['points'] = points

        if bak_ip not in BAK_RULE:
            raise ValueError("params bak_ip not in ['pass', 'pause', 'pause2', 'auto']")
        params['bak_ip'] = bak_ip

        if keep_ttl not in yn:
            raise ValueError("params keep_ttl not in ['yes', 'no']")
        params['keep_ttl'] = keep_ttl

        if sms_notice:
            params['keep_ttl'] = sms_notice

        if email_notice:
            params['email_notice'] = email_notice

        if less_notice:
            if less_notice not in yn:
                raise ValueError("params less_notice not in ['yes', 'no']")
            params['less_notice'] = less_notice

        if callback_url:
            params['callback_url'] = callback_url

        if callback_key:
            params['callback_key'] = callback_key

        return self.check_res(self.send(action=action, params=params))

    def remove(self, monitor_id):
        '''监控删除'''
        action = 'Monitor.Remove'
        params = {}

        # self._check_int(monitor_id)
        params['monitor_id'] = monitor_id

        return self.check_res(self.send(action=action, params=params))

    def info(self, monitor_id):
        '''获取监控信息'''
        action = 'Monitor.Info'
        params = {}

        # self._check_int(monitor_id)
        params['monitor_id'] = monitor_id

        return self.check_res(self.send(action=action, params=params))

    def set_status(self, monitor_id, status='enabled'):
        '''设置监控状态'''
        action = 'Monitor.Setstatus'
        params = {}

        statuses = ['enabled', 'disabled']

        # self._check_int(monitor_id)
        params['monitor_id'] = monitor_id

        if status not in statuses:
            raise ValueError("params less_notice not in ['enabled', 'disabled']")
        params['status'] = status

        return self.check_res(self.send(action=action, params=params))

    def get_history(self, monitor_id, hours=1):
        '''获取监控历史'''
        action = 'Monitor.Gethistory'
        params = {}

        # self._check_int(monitor_id)
        params['monitor_id'] = monitor_id

        # self._check_int(hours)
        params['hours'] = hours

        return self.check_res(self.send(action=action, params=params))

    def user_desc(self):
        '''获取监控概况'''
        action = 'Monitor.Userdesc'
        params = {}

        return self.send(action=action, params=params)

    def get_downs(self, offset=0, length=100):
        '''获取监控警告'''
        action = 'Monitor.Getdowns'
        params = {}

        self._check_int(offset)
        self._check_int(length)

        # 如果区间给定错误
        if not offset >= length:
            length += offset
        params['offset'] = offset
        params['length'] = length

        return self.check_res(self.send(action=action, params=params))

    '''内部方法'''
    def _check_port(self, port):
        '''检测端口合法'''
        if isinstance(port, int):
            port = int(port)
            if not 1 <= port <= 65535:
                raise ValueError("params port 1 <= port <= 65535")
        else:
            raise ValueError("params port need int ")

    def _check_int(self, value):
        if not isinstance(value, int):
            raise ValueError("params value '{0}' need int".format(value))

if __name__ == '__main__':
    import json
    d = DMonitor()
    domain = 'python-ldap.org' # id = 64187088
    domain_id = 64187088
    monitor_id = 4515586
    '''读测试'''
    # ret = d.list_subdomain(domain)
    # print json.dumps(ret, indent=4)
    #
    # ret = d.list_sub_value(domain)
    # print json.dumps(ret, indent=4)
    #
    # ret = d.list(domain_id=domain_id)
    # print json.dumps(ret, indent=4)

    # ret = d.info(monitor_id)
    # print json.dumps(ret, indent=4)

    # ret = d.get_history(monitor_id)
    # print json.dumps(ret, indent=4)

    # ret = d.user_desc()
    # print json.dumps(ret, indent=4)

    # ret = d.get_downs()
    # print json.dumps(ret, indent=4)

    '''修改测试'''