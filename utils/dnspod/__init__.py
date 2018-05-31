# -*- coding: utf-8 -*-
# Author zwhset

__all__ = ['connect', 'dmonitor', 'domain', 'record', 'user']

RESULT_CODE = {
    -1 : '登陆失败',
    -2 : 'API使用超出限制',
    -3 : '不是合法代理 (仅用于代理接口)',
    -4 : '不在代理名下 (仅用于代理接口)',
    -7 : '无权使用此接口',
    -8 : '登录失败次数过多，帐号被暂时封禁',
    -99 : '此功能暂停开放，请稍候重试',
    1 : '操作成功',
    2 : '只允许POST方法',
    3 : '未知错误',
    6 : '用户ID错误 (仅用于代理接口)',
    7 : '用户不在您名下 (仅用于代理接口)',
    83 : '该帐户已经被锁定，无法进行任何操作',
    85 : '该帐户开启了登录区域保护，当前IP不在允许的区域内',
}