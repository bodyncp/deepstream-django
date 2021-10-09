#!/usr/bin/env python
# -*- coding:utf-8 -*-
"""
角色管理
"""
from django.shortcuts import render, redirect, HttpResponse
from stark.utils.pagination import Pagination
from django.urls import reverse

from rbac import models
from rbac.forms.role import RoleModelForm


def role_list(request):
    """
    角色列表
    :param request:
    :return:
    """
    role_queryset = models.Role.objects.all().order_by('-id')
    query_params = request.GET.copy()

    pager = Pagination(
        current_page=request.GET.get('page'),
        all_count=role_queryset.count(),
        base_url=request.path_info,
        query_params=query_params,
        per_page=10
    )

    data_list = role_queryset[pager.start:pager.end]

    user_name = None
    user_name_dict =request.session.get("show_permission")
    if user_name_dict:
        user_name = user_name_dict.get("user_name")

    return render(
        request,
        'rbac/role_list.html',
        {
            'roles': data_list,
            'pager': pager,
            "users": user_name,
            "rest_password": request.session.get("rest_password"),
            "user_edit_href": request.session.get("user_edit_href"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        })


def role_add(request):
    """
    添加角色
    :param request:
    :return:
    """
    if request.method == 'GET':
        form = RoleModelForm()

        user_name = None
        user_name_dict = request.session.get("show_permission")
        if user_name_dict:
            user_name = user_name_dict.get("user_name")

        return render(
            request,
            'rbac/change.html',
            {
                'form': form,
                "users": user_name,
                "rest_password": request.session.get("rest_password"),
                "user_edit_href": request.session.get("user_edit_href"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    form = RoleModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))

    return render(
        request,
        'rbac/change.html',
        {
            'form': form,
            "users": request.session["show_permission"].get("user_name"),
            "rest_password": request.session.get("rest_password"),
            "user_edit_href": request.session.get("user_edit_href"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        })


def role_edit(request, pk):
    """
    编辑角色
    :param request:
    :param pk: 要修改的角色ID
    :return:
    """
    obj = models.Role.objects.filter(id=pk).first()
    if not obj:
        return HttpResponse('角色不存在')
    if request.method == 'GET':
        form = RoleModelForm(instance=obj)
        return render(
            request,
            'rbac/change.html',
            {
                'form': form,
                "users": request.session["show_permission"].get("user_name"),
                "rest_password": request.session.get("rest_password"),
                "user_edit_href": request.session.get("user_edit_href"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    form = RoleModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(reverse('rbac:role_list'))

    return render(
        request,
        'rbac/change.html',
        {
            'form': form,
            "users": request.session["show_permission"].get("user_name"),
            "rest_password": request.session.get("rest_password"),
            "user_edit_href": request.session.get("user_edit_href"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        })


def role_del(request, pk):
    """
    删除角色
    :param request:
    :param pk:
    :return:
    """
    origin_url = reverse('rbac:role_list')
    if request.method == 'GET':
        return render(
            request,
            'rbac/delete.html',
            {
                'cancel': origin_url,
                "users": request.session["show_permission"].get("user_name"),
                "rest_password": request.session.get("rest_password"),
                "user_edit_href": request.session.get("user_edit_href"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    models.Role.objects.filter(id=pk).delete()
    return redirect(origin_url)
