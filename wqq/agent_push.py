# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# Created by Administrator on 2017/12/20
#!/usr/bin/env python
#!-*- coding:utf8 -*-

import requests
import time
import json
import random
import os


while True:
    time.sleep(20)
    payload_list = []
    ts = int(time.time())
    print (ts)
    endpoint = os.popen('echo $HOSTNAME').read().strip()
    value = random.randint(1,100)
    temp_dict = {
        "endpoint": endpoint,
        "metric": "feng-count",
        "timestamp": ts,
        "step": 60,
        "value":value ,
        "counterType": "GAUGE",
        "tags": "idc_test",
    }
    payload_list.append(temp_dict)
    requests.post("http://127.0.0.1:1988/v1/push", data=json.dumps(payload_list))