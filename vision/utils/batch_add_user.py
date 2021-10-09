#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/10/13 19:37
# @Author  : NCP
# @File    : batch_add_user.py
# @Software: PyCharm

from django.db import connection
from vision.utils.md5 import gen_md5
from django.db import transaction


def func():
    cursor = connection.cursor()
    return cursor


def batch_user(data_list):
    try:
        with transaction.atomic():
            pwd = gen_md5(data_list[1])
            cursor = func()

            # 添加用户
            cursor.execute("insert into vision_userinfoextent(name,password) values(%s,'%s')" % (data_list[0], pwd))
            # 查询新增用户ID，添加用户角色
            cursor.execute("select id from vision_userinfoextent where name='%s'" % data_list[0])
            user_id = cursor.fetchone()
            cursor.execute("select id from rbac_role where title='报表用户'")
            role_id = cursor.fetchone()
            print(user_id, role_id)
            cursor.execute(
                "insert into vision_userinfoextent_roles(userinfoextent_id, role_id) values(%s, %s)" % (user_id[0], role_id[0]))
            cursor.close()
            return True
    except Exception as e:
        print(e)
        return str(e)
