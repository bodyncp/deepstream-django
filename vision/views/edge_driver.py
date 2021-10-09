#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/20 10:54
# @Author  : NCP
# @File    : edge_driver.py
# @Software: PyCharm

from django.conf import settings
from stark.service.v1 import StarkHandler, StarkModelForm, Option
from vision import models


class EdgeDriverAddModelForm(StarkModelForm):
    class Meta:
        model = models.EdgeDriver
        fields = ['dname', 'driver_pull', 'bearing_point']


class EdgeDriverChangeModelForm(StarkModelForm):
    class Meta:
        model = models.EdgeDriver
        fields = ['dname', 'driver_pull', 'bearing_point']


class EdgeDriverHandler(StarkHandler):
    list_display = ['dname', 'driver_pull', 'bearing_point']

    search_list = ['dname__contains']

    # 这个方法适用于有关联字段的表
    # search_group = [
    #     Option(field="nick_name"),
    # ]

    def get_model_form_class(self, is_add=False, *args, **kwargs):
        if is_add:
            return EdgeDriverAddModelForm
        return EdgeDriverChangeModelForm

    # 权限粒度控制
    def get_add_btn(self, request, *args, **kwargs):
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if self.get_add_url_name not in permission_dict:
            return None
        return super().get_add_btn(request, *args, **kwargs)

    # 编辑删除控制显示设置
    def get_list_display(self, request, *args, **kwargs):
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)

        value = []
        if self.list_display:
            value.extend(self.list_display)
            if self.get_change_url_name in permission_dict and self.get_delete_url_name in permission_dict:
                value.append(type(self).display_edit_del)
                return value

            elif self.get_change_url_name in permission_dict:
                value.append(type(self).display_edit)
            elif self.get_change_url_name in permission_dict:
                value.append(type(self).display_del)
        return value
