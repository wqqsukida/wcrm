# -*- coding: utf-8 -*-
# Author zwhset

from utils.dnspod.connect import Public

RECORD_LINE = ['默认', '国内', '国外', '电信', '联通', '教育网',
               '移动', '百度', '谷歌', '搜搜', '有道', '必应',
               '搜狗', '奇虎', '搜索引擎']
RECORD_TYPE = ['A', 'CNAME', 'MX', 'TXT', 'NS', 'AAAA', 'SRV']
RECORD_MIN_MX = 0
RECORD_MAX_MX = 20
RECORD_MIN_TTL = 600
RECORD_MIN_WEIGHT = 1
RECORD_MAX_WEIGHT = 100

class Record(Public):
    '''
    DNSPOD请求参数：
        公共参数
        domain_id 域名ID, 必选
        domain_id 或 domain, 分别对应域名ID和域名, 提交其中一个即可
        sub_domain 主机记录, 如 www，可选，如果不传，默认为 @
        record_type 记录类型，通过API记录类型获得，大写英文，比如：A, 必选
        record_line 记录线路，通过API记录线路获得，中文，比如：默认
        record_line_id 线路的ID，通过API记录线路获得，英文字符串，比如：‘10=1’
            record_line 和 record_line_id 二者传其一即可，系统优先取 record_line_id】
        value 记录值, 如 IP:200.200.200.200, CNAME: cname.dnspod.com., MX: mail.dnspod.com., 必选
        mx {1-20} MX优先级, 当记录类型是 MX 时有效，范围1-20, MX记录必选
        ttl {1-604800} TTL，范围1-604800，不同等级域名最小值不同, 可选
        status [“enable”, “disable”]，记录初始状态，默认为”enable”，如果传入”disable”，解析不会生效，
            也不会验证负载均衡的限制，可选
        weight 权重信息，0到100的整数，可选。仅企业 VIP 域名可用，0 表示关闭，
            留空或者不传该参数，表示不设置权重信息
    '''

    def __init__(self, domain_id=None, domain=None):
        super(Record, self).__init__()

        if not(domain_id or domain):
            raise ValueError("params error, need domain_id or domain name")

        self.domain = domain
        self.domain_id = domain_id

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

    def create(self, sub_domain='@', record_type='A',
               record_line='默认', record_line_id=None,
               value=None, mx=None, ttl=RECORD_MIN_TTL, status='enable', weight=None):
        '''添加域名记录'''
        action = 'Record.Create'

        params = {}
        if self.domain:
            params['domain'] = self.domain
        else:
            params['domain_id'] = self.domain_id

        # if not record_line or not record_line_id:
        #     raise ValueError, "params error, need record_line or record_id"
        if record_line:
            params['record_line'] = record_line
        else:
            params['record_line_id'] = record_line_id

        if mx:
            mx = int(mx)
            if not RECORD_MIN_MX <= mx <= RECORD_MAX_MX:
                raise  ValueError("params error, mx in {0}-{1}".format(RECORD_MIN_MX, RECORD_MAX_MX))
            params['mx'] = mx

        if ttl:
            ttl = int(ttl)
            if ttl < RECORD_MIN_TTL:
                raise ValueError("params error, ttl >= {0}".format(RECORD_MIN_TTL))
            params['ttl'] = ttl

        if status:
            if status not in ['enable', 'disable']:
                raise ValueError("params error, status in ['enable', 'disable']")
            params['status'] = status

        if weight:
            weight = int(weight)
            if not RECORD_MIN_WEIGHT <= weight <= RECORD_MAX_WEIGHT:
                raise ValueError("params error, weight in {0}-{1}".format(RECORD_MIN_WEIGHT, RECORD_MAX_WEIGHT))
            params['weight'] = weight

        if sub_domain:
            params['sub_domain'] = sub_domain

        if record_line in RECORD_LINE:
            params['record_line'] = record_line
        else:
            params['record_line'] = '默认'

        if record_type in RECORD_TYPE:
            params['record_type'] = record_type
        else:
            raise ValueError('params error, record_type type error.')

        if not value:
            raise ValueError("params error, need params value")
        params['value'] = value

        return self.check_res(self.send(action=action, params=params))

    def list(self, keyword=None, offset=None, length=20, sub_domain=None):
        '''获取记录列表'''
        action = 'Record.List'

        params = {}
        if self.domain:
            params['domain'] = self.domain
        else:
            params['domain_id'] = self.domain_id

        if keyword:
            params['keyword'] = keyword
        if offset:
            params['offset'] = offset
            params['length'] =length
        if sub_domain:
            params['sub_domain'] = sub_domain


        status ,data = self.check_res(self.send(action=action, params=params))

        return status,data

    def modify(self, record_id, sub_domain='@', record_type='A',
               record_line='默认', record_line_id=None,
               value=None, mx=None, ttl=600, status='enable', weight=None):
        '''修改域名记录'''
        action = 'Record.Modify'

        params = {}
        if self.domain:
            params['domain'] = self.domain
        else:
            params['domain_id'] = self.domain_id

        # if not record_line or not record_line_id:
        #     raise ValueError, "params error, need record_line or record_id"
        if record_line:
            params['record_line'] = record_line
        else:
            params['record_line_id'] = record_line_id

        if mx:
            mx = int(mx)
            if not RECORD_MIN_MX <= mx <= RECORD_MAX_MX:
                raise ValueError("params error, mx in {0}-{1}".format(RECORD_MIN_MX, RECORD_MAX_MX))
            params['mx'] = mx

        if ttl:
            ttl = int(ttl)
            if ttl < RECORD_MIN_TTL:
                raise ValueError("params error, ttl >= {0}".format(RECORD_MIN_TTL))
            params['ttl'] = ttl

        if status:
            if status not in ['enable', 'disable']:
                raise ValueError("params error, status in ['enable', 'disable']")
            params['status'] = status

        if weight:
            weight = int(weight)
            if not RECORD_MIN_WEIGHT <= weight <= RECORD_MAX_WEIGHT:
                raise ValueError("params error, weight in {0}-{1}".format(RECORD_MIN_WEIGHT, RECORD_MAX_WEIGHT))
            params['weight'] = weight

        if sub_domain:
            params['sub_domain'] = sub_domain

        if record_line in RECORD_LINE:
            params['record_line'] = record_line
        else:
            params['record_line'] = '默认'

        if record_type in RECORD_TYPE:
            params['record_type'] = record_type
        else:
            raise ValueError('params error, record_type type error.')

        if not value:
            raise ValueError("params error, need params value")
        params['value'] = value
        params['record_id'] = record_id

        return self.check_res(self.send(action=action, params=params))

    def remove(self, record_id):
        '''删除域名记录'''
        action = 'Record.Remove'

        params = {}
        if self.domain:
            params['domain'] = self.domain
        else:
            params['domain_id'] = self.domain_id
        params['record_id'] = record_id

        return self.check_res(self.send(action=action, params=params))

    def ddns(self, record_id, domain_id=None, domain=None,
             record_line=None, record_line_id=None, value=None):
        '''更新动态DNS记录'''
        action = 'Record.Ddns'
        pass

    def remark(self, record_id, remark=None):
        '''修改记录备注'''
        action = 'Record.Remark'

        params = {}
        if self.domain:
            params['domain'] = self.domain
        else:
            params['domain_id'] = self.domain_id

        # if not remark:
        #     raise ValueError, "params error, params remark not fund."
        params['remark'] = remark
        params['record_id'] = record_id

        return self.check_res(self.send(action=action, params=params))

    def info(self, record_id):
        '''获取记录信息'''
        action = 'Record.Info'

        params = {}
        if self.domain:
            params['domain'] = self.domain
        else:
            params['domain_id'] = self.domain_id
        params['record_id'] = record_id

        return self.check_res(self.send(action=action, params=params))

    def status(self, record_id,status):
        '''设置记录状态'''
        action = 'Record.Status'

        params = {}

        if self.domain:
            params['domain'] = self.domain
        else:
            params['domain_id'] = self.domain_id
        params['record_id'] = record_id
        params['status'] = status
        return self.check_res(self.send(action=action, params=params))


if __name__ == '__main__':
    r = Record(domain_id=45175079)
    ret = r.list()
    if ret.get('status', {}).get('message', None):
        print (ret.get('status', {}).get('message', None))
    print (ret)