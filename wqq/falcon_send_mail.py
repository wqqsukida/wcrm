# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# Created by Administrator on 2017/12/21
import requests

host = "http://192.168.67.129:4000/sender/mail"

hearders = {
    "Content-Type": "application/json",
    'tos':'wuyifei@163.com',
    'subject':'test',
    'content':'test',
}

params = {
    'url': host,
    'headers': hearders,
    'timeout': 30
}


res = requests.post(**params)
