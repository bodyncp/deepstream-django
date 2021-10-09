#!/usr/bin/env python
# -*- coding:utf-8 -*-
import hashlib


def gen_md5(origin):
    """
    md5加密
    :param origin:
    :return:
    """
    ha = hashlib.md5(b'jk3usodfjwkrsdf')
    ha.update(origin.encode('utf-8'))
    return ha.hexdigest()


def rtmp_md5(origin):
    """
    rtmp流地址加密访问
    :param origin:
    :return:
    """
    ha = hashlib.md5()
    ha.update(origin.encode(encoding='utf-8'))
    return ha.hexdigest()