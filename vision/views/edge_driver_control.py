#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/29 14:00
# @Author  : NCP
# @File    : edge_driver_control.py
# @Software: PyCharm

from django import forms
from django.conf import settings
from stark.service.v1 import StarkHandler, StarkModelForm, get_choice_text
from vision import models


class EdgeDriverSshAddModelForm(StarkModelForm):
    class Meta:
        model = models.EdgeDriverSsh
        fields = ['ssh_addr', 'driver_status', 'rtmp_server_status', 'program_status', 'driver_name']

        widgets = {
            'driver_status': forms.Select(attrs={'class': 'form-control'}),
            'program_status': forms.Select(attrs={'class': 'form-control'}),
        }


class EdgeDriverSshChangeModelForm(StarkModelForm):
    class Meta:
        model = models.EdgeDriverSsh
        fields = ['ssh_addr', 'driver_status', 'rtmp_server_status', 'program_status', 'driver_name']

        widgets = {
            'driver_status': forms.Select(attrs={'class': 'form-control'}),
            'program_status': forms.Select(attrs={'class': 'form-control'}),
        }


class EdgeDriverSshHandler(StarkHandler):
    list_display = ['ssh_addr', get_choice_text('设备状态', 'driver_status'), get_choice_text('流服务器状态', 'rtmp_server_status'), get_choice_text('程序状态', 'program_status'), 'driver_name']

    def get_model_form_class(self, is_add=False, *args, **kwargs):
        if is_add:
            return EdgeDriverSshAddModelForm
        return EdgeDriverSshChangeModelForm

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