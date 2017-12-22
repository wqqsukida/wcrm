# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# Created by Administrator on 2017/12/18
import sys
import json
import time
import requests
from wcrm import settings

class OpsMachineInfo():
    def dash(self, in_ip, step_time=1800):
        f = FalconBase()
        status, data = f.req_api(directiry="/api/v1/graph/endpoint?q={0}".format(in_ip), method="get")
        print (status,data)
        if not status or not data:
            return {}
        point_id = data[0]["id"]    # 得到eid

        status, counters = f.req_api(directiry="/api/v1/graph/endpoint_counter?eid={0}".format(point_id), method="get")
        if not status:
            return {}
        counters = [ counter["counter"] for counter in counters ]    # 得到具体监控项

        end_time = int(time.time()) # 必须要整形
        start_time = end_time - step_time # 30分钟

        payload = {
           "step": 60,
           "start_time": start_time,
           "hostnames": [in_ip,],
           "end_time": end_time,
           "counters": counters,
           "consol_fun": "AVERAGE"
           }
        # 得到指定监控项的历史记录
        status, data = f.req_api(directiry="/api/v1/graph/history", method="post", payload=payload)
        if not status:
            return {}

        # ===============格式化数据==========================================
        data = dict([ (iter["counter"], iter["Values"] ) for iter in data ])

        for key in data:
            values = data[key]
            data[key] = [ {"timestamp": time.strftime('%H:%M',time.localtime(k["timestamp"])), "value": k["value"] }  for k in values if k["value"] ]

        data["in_ip"] = in_ip

        return data

class FalconBase(object):
    """  从获取falcon中获取监控原始数据  """

    def __init__(self):
        """ get connect info & auth header. """
        # try:
        #     with open('config.yaml') as falcon_conf:
        #         y = yaml.load(falcon_conf)
        #         username = y['OpenFalcon']['username']
        #         password = y['OpenFalcon']['sig']
        #         host = y['OpenFalcon']['host']
        # except IOError:
        #     with open('../config.yaml') as falcon_conf:
        #         y = yaml.load(falcon_conf)
        #         username = y['OpenFalcon']['username']
        #         password = y['OpenFalcon']['sig']
        #         host = y['OpenFalcon']['host']

        self.user = settings.user
        self.passwd = settings.sig
        self.domain = settings.domain
        api_token = '{"name":"'+self.user+'", "sig":"'+self.passwd+'"}'
        self.falcon_header = {
            "Apitoken": api_token,
            "X-Forwarded-For": "127.0.0.1",
            "Content-Type": "application/json",
            "name": self.user,
            "sig": self.passwd
        }

    def req_api(self, directiry, method, payload=None):
        """
        :param directiry:  falcon api path
        :param method:  request method , get or post
        :param payload:  request data
        :return:  json data
        """
        params = {
            'url': self.domain + directiry,
            'headers': self.falcon_header,
            'timeout': 30
        }
        if payload:
            params['data'] = json.dumps(payload)
        try:
            if method == 'get':
                res = requests.get(**params)
            elif method == 'post':
                res = requests.post(**params)
            else:
                return False, 'request method error.'

            return True, json.loads(res.text)
        except Exception as e:
            return False, str(e)

    def endpoint_list(self):
        """ list all endpoint """
        directiry = '/api/v1/graph/endpoint?q=172.*'
        status, message = self.req_api(directiry=directiry, method='get')
        if status:
            return [_i['endpoint'] for _i in message if '.' in _i['endpoint']]