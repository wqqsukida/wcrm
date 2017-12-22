# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# Created by Administrator on 2017/12/15
import json
import time
import requests

in_ip = '192.168.67.130'
user = 'root'
sig = '5dfd815de3ce11e7b107000c298269bc'
domain = 'http://192.168.67.129:8080'
api_token = '{"name":"' + user + '", "sig":"' + sig + '"}'
directiry = "/api/v1/graph/endpoint?q={0}".format(in_ip)

falcon_header = {
            "Apitoken": api_token,
            "X-Forwarded-For": "127.0.0.1",
            "Content-Type": "application/json",
            "name": user,
            "sig": sig
        }

params = {
    'url': domain + directiry,
    'headers': falcon_header,
    'timeout': 30
}
res1 = requests.get(**params)
data1 = json.loads(res1.text)
print('得到eid',data1)
#=========================================================================
point_id = data1[0]["id"]
directiry="/api/v1/graph/endpoint_counter?eid={0}".format(point_id)
params = {
    'url': domain + directiry,
    'headers': falcon_header,
    'timeout': 30
}
res2 = requests.get(**params)
data2 = json.loads(res2.text)
print('得到具体监控项',data2)
#=========================================================================
counters = [ counter["counter"] for counter in data2 ]

end_time = int(time.time()) # 必须要整形
start_time = end_time - 1800 # 30分钟
directiry="/api/v1/graph/history"
params = {
    'url': domain + directiry,
    'headers': falcon_header,
    'timeout': 30
}

payload = {
    "step": 60,
    "start_time": start_time,
    "hostnames": [in_ip, ],
    "end_time": end_time,
    "counters": counters,
    "consol_fun": "AVERAGE"
}
params['data'] = json.dumps(payload)

res3 = requests.post(**params)
data3 = json.loads(res3.text)
# print('得到指定监控项的历史记录',data3)

data = dict([(iter["counter"], iter["Values"]) for iter in data3])

#===============格式化数据==========================================
for key in data:
    values = data[key]
    data[key] = [{"timestamp": time.strftime('%H:%M', time.localtime(k["timestamp"])), "value": k["value"]} for k in
                 values if k["value"]]

data["in_ip"] = in_ip

print('得到指定监控项的历史记录',data)