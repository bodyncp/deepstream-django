#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/17 10:47
# @Author  : NCP
# @File    : account.py
# @Software: PyCharm

from django.shortcuts import render, redirect, HttpResponse
from django.db.models import Sum
from django.http import JsonResponse
from apscheduler.scheduler import Scheduler
from django.core.cache import cache
from django.conf import settings
import paramiko
import sys
import time
from vision import models
from vision.utils.md5 import gen_md5, rtmp_md5
from rbac.service.init_permission import init_permission
from vision.views.userinfo import ResetPasswordForm, UserInfoOneChangeModelForm


# 定时任务初始化
sched = Scheduler()


def login(request):
    """
    用户登录
    :param request:
    :return:
    """

    if request.method == 'GET':
        return render(request, 'login.html')

    user = request.POST.get('user')
    pwd = gen_md5(request.POST.get('pwd', ''))

    # 根据用户名和密码去用户表中获取用户对象
    user = models.UserInfoExtent.objects.filter(name=user, password=pwd).first()

    if not user:
        return render(request, 'login.html', {'msg': '用户名或密码错误'})

    request.session['user_info'] = {'id': user.id, 'name': user.name}

    # 添加用户编辑、重置密码功能
    pk = request.session['user_info'].get("id")
    rest_password_href = "/stark/vision/userinfoextent/reset/password/%s/%s/" % (pk, user.name)
    user_edit_href = "/stark/vision/userinfoextent/change/%s/%s" % (pk, user.name)
    request.session["rest_password"] = rest_password_href
    request.session["user_edit_href"] = user_edit_href

    # 用户项目进出流量统计功能
    count_in = models.PersonPostInfo.objects.aggregate(Sum('point_in'))
    count_out = models.PersonPostInfo.objects.aggregate(Sum('point_out'))

    # 累计入流量
    request.session['queryset_count'] = int(count_in.get("point_in__sum")) if count_in.get("point_in__sum") else 0

    # 累计出流量
    request.session['queryset_count_all'] = int(count_out.get("point_out__sum")) if count_in.get("point_in__sum") else 0

    # 添加用户的查看权限
    request.session["show_permission"] = {"level": user.level, "user_name": user.name}

    # 用户权限信息的初始化
    init_permission_flag = init_permission(user, request)
    if init_permission_flag:
        return redirect('/index/')

    # 判断是否是手机用户
    # is_mobile = checkMobile(request)
    # if init_permission_flag:
    #     if user_role_id[0] != 1 and is_mobile:
    #         return redirect('/m_search_data/')
    #
    #     return redirect('/index/')


def logout(request):
    """
    注销
    :param request:
    :return:
    """
    request.session.delete()
    cache.clear()
    return redirect('/login/')


def index(request):
    """
    携带加密媒体流地址连接
    :param request:
    :return:
    """
    driver_list = []
    play_time = int(time.time())
    play_time = play_time + 60
    driver_queryset_list = models.EdgeDriver.objects.all().values_list()
    rtmp_md5_str = rtmp_md5("/live/test-{}-{}".format(play_time, settings.RTMP_SERVER_KEY))

    for data in driver_queryset_list:
        driver_list.append((data[1], data[2]+"?sign={}-{}".format(play_time, rtmp_md5_str)))

    user = request.session["show_permission"].get("user_name")
    rest_password = request.session["rest_password"]
    user_edit_href = request.session["user_edit_href"]
    return render(
        request,
        'index.html',
        {
            "users": user,
            "rest_password": rest_password,
            "user_edit_href": user_edit_href,
            "driver_list": driver_list,
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        })


# def phone_index(request):
#     return render(request, "phone_index.html")


def reset_password(request, pk, user):
    """
    重置密码的视图函数
    :param request:
    :param pk:
    :return:
    """

    user_edit_href = request.session["user_edit_href"]
    if request.method == 'POST':
        if int(pk) != request.session['user_info'].get("id"):
            return HttpResponse('无法进行密码重置！请联系管理员（ps:除非你想作弊）')

    user_id = request.session['user_info'].get("id")
    userinfo_object = models.UserInfoExtent.objects.filter(id=user_id).first()
    if not userinfo_object:
        return HttpResponse('用户不存在，无法进行密码重置！')

    if request.method == 'GET':
        if int(pk) != request.session['user_info'].get("id"):
            return HttpResponse('用户不存在，无法进行密码重置！')
        form = ResetPasswordForm()
        return render(
            request,
            'stark/change.html',
            {
                'form': form,
                'user_edit_href': user_edit_href,
                "rest_password": request.session.get("rest_password"),
                "queryset_count": request.session.get("queryset_count"),
                "queryset_count_all": request.session.get('queryset_count_all')
            })

    form = ResetPasswordForm(data=request.POST)
    if form.is_valid():
        userinfo_object.password = form.cleaned_data['password']
        userinfo_object.save()
        return redirect('/index/')
    return render(
        request,
        'stark/change.html',
        {
            'form': form,
            "user_edit_href": request.session.get("user_edit_href"),
            "rest_password": request.session.get("rest_password"),
            "queryset_count": request.session.get("queryset_count"),
            "queryset_count_all": request.session.get('queryset_count_all')
        }
    )


def user_edit_one(request, pk, user):
    """
    单用户编辑功能
    :param request:
    :param pk:
    :return:
    """

    rest_password = request.session["rest_password"]
    user_id = request.session['user_info'].get("id")
    if int(pk) != user_id:
        return HttpResponse('要修改的数据和传入数据不匹配！')

    userinfo_object = models.UserInfoExtent.objects.filter(id=user_id).first()
    if not userinfo_object:
        return HttpResponse('要修改的数据不存在，请重新选择！')

    model_form_class = UserInfoOneChangeModelForm
    if request.method == 'GET':
        form = model_form_class(instance=userinfo_object)
        return render(
            request,
            'stark/one_user_change.html',
            {'form': form, "rest_password": rest_password,
             "user_name": request.session["show_permission"].get("user_name"),
             "user_edit_href": request.session.get("user_edit_href"),
             "queryset_count": request.session.get("queryset_count"),
             "queryset_count_all": request.session.get('queryset_count_all')
             }
        )
    else:
        form = model_form_class(data=request.POST, instance=userinfo_object)
        if form.is_valid():
            response = userinfo_object.save()
            # 在数据库保存成功后，跳转回列表页面(携带原来的参数)。
            return response or redirect('/index/')
        return render(
            request,
            'stark/one_user_change.html',
            {'form': form,
             "rest_password": rest_password,
             "user_name": request.session["show_permission"].get("user_name"),
             "user_edit_href": request.session.get("user_edit_href"),
             "queryset_count": request.session.get("queryset_count"),
             "queryset_count_all": request.session.get('queryset_count_all')
             }
        )


def data_display(request):
    rest_password = request.session["rest_password"]
    return render(request, "stark/data_display.html",
                  {
                      "rest_password": rest_password,
                      "user_name": request.session["show_permission"].get("user_name"),
                      "user_edit_href": request.session.get("user_edit_href"),
                      "queryset_count": request.session.get("queryset_count"),
                      "queryset_count_all": request.session.get('queryset_count_all')
                  },
                  )


@sched.interval_schedule(seconds=5)
def check_driver_status():
    ip_addr_list = models.EdgeDriverSsh.objects.values_list("ssh_addr")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    if ip_addr_list:
        for addr in ip_addr_list:
            try:
                ssh.connect('{}'.format(addr[0]), username='ncp', password='123123', timeout=5)
                models.EdgeDriverSsh.objects.filter(ssh_addr__contains=addr[0]).update(driver_status=1)
                cmd_python = 'ps -ef | grep python3'
                _, stdout, stderr = ssh.exec_command(cmd_python)
                data = stdout.readlines()
                if data:
                    for i in data:
                        if "python3 enrty.py" in i:
                            models.EdgeDriverSsh.objects.filter(ssh_addr__contains=addr[0]).update(program_status=1)
                            break
                        else:
                            models.EdgeDriverSsh.objects.filter(ssh_addr__contains=addr[0]).update(program_status=2)

                cmd_node = 'ps -ef | grep node'
                _, stdout, stderr = ssh.exec_command(cmd_node)
                data = stdout.readlines()
                if data:
                    for i in data:
                        if "node app.js" in i:
                            models.EdgeDriverSsh.objects.filter(ssh_addr__contains=addr[0]).update(rtmp_server_status=1)
                            break
                        else:
                            models.EdgeDriverSsh.objects.filter(ssh_addr__contains=addr[0]).update(rtmp_server_status=2)

            except Exception as e:
                models.EdgeDriverSsh.objects.filter(ssh_addr__contains=addr[0]).update(driver_status=2)
                models.EdgeDriverSsh.objects.filter(ssh_addr__contains=addr[0]).update(rtmp_server_status=2)
                models.EdgeDriverSsh.objects.filter(ssh_addr__contains=addr[0]).update(program_status=2)

    ssh.close()


sched.start()