#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/12 11:22
# @Author  : NCP
# @File    : userinfo.py
# @Software: PyCharm

from django.conf import settings
from stark.service.v1 import StarkHandler, StarkModelForm, StarkForm
from vision import models
from vision.utils.md5 import gen_md5
from django import forms
from django.core.exceptions import ValidationError
from django.utils.safestring import mark_safe
from django.conf.urls import url
from django.shortcuts import HttpResponse, render, redirect


class UserInfoAddModelForm(StarkModelForm):
    confirm_password = forms.CharField(label='确认密码')

    class Meta:
        model = models.UserInfoExtent
        fields = ['name', 'password', 'confirm_password', 'phone', 'email', 'level', 'roles']

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        if self.cleaned_data.get("password"):
            password = self.cleaned_data['password']
            self.cleaned_data['password'] = password
            self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


class UserInfoChangeModelForm(StarkModelForm):
    class Meta:
        model = models.UserInfoExtent
        fields = ['name', 'phone', 'email', 'level', 'roles']


class ResetPasswordForm(StarkForm):
    password = forms.CharField(label='密码', widget=forms.PasswordInput)
    confirm_password = forms.CharField(label='确认密码', widget=forms.PasswordInput)

    def clean_confirm_password(self):
        password = self.cleaned_data['password']
        confirm_password = self.cleaned_data['confirm_password']
        if password != confirm_password:
            raise ValidationError('密码输入不一致')
        return confirm_password

    def clean(self):
        password = self.cleaned_data['password']
        self.cleaned_data['password'] = gen_md5(password)
        return self.cleaned_data


class UserInfoHandler(StarkHandler):

    def display_reset_pwd(self, obj=None, is_header=None, *args, **kwargs):
        if is_header:
            return '重置密码'
        reset_url = self.reverse_commons_url(self.get_url_name('reset_pwd'), pk=obj.pk)
        return mark_safe("<a href='%s'>重置密码</a>" % reset_url)

    list_display = [StarkHandler.display_checkbox, 'name', display_reset_pwd]

    search_list = ['name__contains']

    def get_model_form_class(self, is_add=False, *args, **kwargs):
        if is_add:
            return UserInfoAddModelForm
        return UserInfoChangeModelForm

    def reset_password(self, request, pk):
        """
        重置密码的视图函数
        :param request:
        :param pk:
        :return:
        """
        userinfo_object = models.UserInfoExtent.objects.filter(id=pk).first()
        if not userinfo_object:
            return HttpResponse('用户不存在，无法进行密码重置！')
        if request.method == 'GET':
            form = ResetPasswordForm()
            return render(request, 'stark/change.html', {'form': form})
        form = ResetPasswordForm(data=request.POST)
        if form.is_valid():
            userinfo_object.password = form.cleaned_data['password']
            userinfo_object.save()
            return redirect(self.reverse_list_url())
        return render(request, 'stark/change.html', {'form': form})

    def extra_urls(self):
        patterns = [
            url(r'^reset/password/(?P<pk>\d+)/$', self.wrapper(self.reset_password),
                name=self.get_url_name('reset_pwd')),
        ]
        return patterns

    # 权限粒度控制
    def get_add_btn(self, request, *args, **kwargs):
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if self.get_add_url_name not in permission_dict:
            return None
        return super().get_add_btn(request, *args, **kwargs)

    def get_batch_add_btn(self, request, *args, **kwargs):
        permission_dict = request.session.get(settings.PERMISSION_SESSION_KEY)
        if "batch_add_user" not in permission_dict:
            return None
        return super().get_batch_add_btn(request, *args, **kwargs)

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


class UserInfoOneChangeModelForm(StarkModelForm):
    class Meta:
        model = models.UserInfoExtent
        fields = ['name', 'phone', 'email']
        # widgets = {
        #     'level': forms.Select(attrs={'disabled': 'disabled'}),
        #     'show_permission': forms.Select(attrs={'disabled': 'disabled'}),
        #     'company': forms.Select(attrs={'disabled': 'disabled'}),
        #     'roles': forms.Select(attrs={'disabled': 'disabled'}),
        # }


