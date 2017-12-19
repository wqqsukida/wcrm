# -*- coding: UTF-8 -*-
#!/usr/bin/env python
# Created by Administrator on 2017/12/18
from __future__ import absolute_import  # Python 2 only

from django.contrib.staticfiles.storage import staticfiles_storage
from django.urls import reverse

from jinja2 import Environment


def environment(**options):
    env = Environment(**options)
    env.globals.update({
        'static': staticfiles_storage.url,
        'url': reverse,
    })
    return env