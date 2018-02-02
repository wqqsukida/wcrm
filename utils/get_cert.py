# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# Created by Administrator on 2018/1/30
import json
import requests
from bs4 import BeautifulSoup

def get_cert(domain):
    '''
    发起request获取证书详细信息
    :param domain:
    :return:
    '''
    url = "http://web.chacuo.net/netsslcheck"

    post_data = {
        "data": domain,
        "type": "sslcheck",
        "arg": "p=443",
    }

    headers = {
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8'
    }
    res = requests.post(url=url, data=post_data, headers=headers)
    res.encoding = "utf-8"
    html = json.loads(res.text)
    html_doc = html["data"][0]

    soup = BeautifulSoup(html_doc, features="lxml")
    tag = soup.find(name='td', attrs={'class': 'alert alert-info bold f14'}, text='证书信息')

    if tag:
        cert_list = tag.parent.find_all_next(name='tr')[0:10]
        cert_list = [str(i) for i in cert_list]
        return cert_list
