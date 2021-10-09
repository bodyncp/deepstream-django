#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/20 10:43
# @Author  : NCP
# @File    : person_count.py
# @Software: PyCharm

from django.conf import settings
from stark.service.v1 import StarkHandler, get_m2m_text, StarkModelForm, StarkForm, Option
from vision import models


class PersonPostInfoModelForm(StarkModelForm):

    class Meta:
        model = models.PersonPostInfo
        fields = ['point_name', 'point_in', 'point_out', 'date_time']


class PersonPostInfoChangeModelForm(StarkModelForm):
    class Meta:
        model = models.PersonPostInfo
        fields = ['point_name', 'point_in', 'point_out']


class PersonPostInfoHandler(StarkHandler):

    list_display = [StarkHandler.display_checkbox, 'point_name', 'point_in', 'point_out', 'date_time']

    search_list = ['point_name__contains']

    def get_model_form_class(self, is_add=False, *args, **kwargs):
        if is_add:
            return PersonPostInfoModelForm
        return PersonPostInfoChangeModelForm

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

    def action_multi_remove(self, request, *args, **kwargs):
        """
        批量移除
        :return:
        """
        current_user_id = request.session['user_info']['id']
        pk_list = request.POST.getlist('pk')
        self.model_class.objects.filter(id__in=pk_list).delete()

    action_multi_remove.text = "批量删除"

    action_list = [action_multi_remove]

