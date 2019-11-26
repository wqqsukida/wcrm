# -*- coding: utf-8 -*-
# Author zwhset

import requests
import copy
# from wcrm.settings import DNSPOD_TOKEN


class Public(object):
    '''公共方法，用于连接以及发送请求到Dnspod'''

    def __init__(self, token='45694,120fff0b9321cfcbb6aeccb647af9131'):
        self.params = dict(login_token=token,
                         format='json',
                         lang='cn',
                         error_on_empty='no')
        self.base_url = 'https://dnsapi.cn/{action}'


    def send(self, action, method='POST', headers={}, params={}):
        '''
        公共发送方法

        @params
            action: 域名动作 exp: 'Domain.Create'
            method: POST or GET
            headers: request发送的请求头信息
            params: 用于与公共self.params进行更新后提交

        @returns
            json
        '''
        url = self.base_url.format(action=action)
        data = copy.deepcopy(self.params)
        data.update(params)

        try:
            if method == 'POST':
                r = requests.post(url, headers=headers, data=data)
            else: # method == 'GET'
                r = requests.get(url, headers=headers, params=data)

            return r.json()
        except:
            raise TypeError("Dnspod requests error.")

    def version(self):
        '''获取版本号'''
        action = 'Info.Version'
        return self.send(action=action)

if __name__ == '__main__':
    p = Public()
    print (p.version())
