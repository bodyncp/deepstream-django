#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2021/9/21 9:29
# @Author  : NCP
# @File    : data_api.py
# @Software: PyCharm

from django.http import JsonResponse, HttpResponse
from django.db.models import Sum
from vision import models
from vision.utils import md5
from machine_vision.settings import AUTH_KEY
import time


def request_url_api(request):
    t = time.strftime("%Y-%m-%d-%H", time.localtime())
    name = request.META.get("HTTP_NAME")
    name = name.encode("latin1").decode("utf-8")
    auth = request.META.get("HTTP_AUTH")
    auth_data = md5.gen_md5(AUTH_KEY+t)
    data_name = models.EdgeDriver.objects.filter(dname=name).first()
    return_data = []

    # 如果设备在web端已经完成注册并通过auth
    if str(data_name) == name and auth_data == auth:
        driver_obj = models.EdgeDriver.objects.filter(dname=name).first()
        data_list = driver_obj.pointinfo_set.all().values_list()
        for data in data_list:
            return_data.append(data)
        return JsonResponse({"code": 200, "msg": "success", "data_list": return_data})
    else:
        return JsonResponse({"code": 403, "msg": "error auth info"})


def person_count_info(request):
    """
    边缘设备post数据接口，需添加head防止外部侵入
    :param request:
    :return:
    """
    t = time.strftime("%Y-%m-%d-%H", time.localtime())
    auth = request.META.get("HTTP_AUTH")
    auth_data = md5.gen_md5(AUTH_KEY+t)
    if auth_data != auth:
        return HttpResponse("error auth info")

    point_name = request.GET.get("point_name")
    if not point_name:
        return HttpResponse("point_name is not found")
    point_in = request.GET.get("point_in")
    if not point_in:
        point_in = 0
    point_out = request.GET.get("point_out")
    if not point_out:
        point_out = 0
    date_time = request.GET.get("date_time")
    # t = time.strftime("%Y-%m-%d-%H", time.localtime())

    pointinfo_exits = models.PersonPostInfo.objects.filter(point_name=point_name)
    if not pointinfo_exits:
        return HttpResponse("bad point name")

    pointinfo_object = models.PersonPostInfo.objects.filter(point_name=point_name, date_time__contains=date_time)

    if pointinfo_object:
        pointinfo_object.update(point_name=point_name, point_in=point_in, point_out=point_out, date_time=date_time)
    else:
        models.PersonPostInfo.objects.create(point_name=point_name, point_in=point_in, point_out=point_out, date_time=date_time)

    return HttpResponse("success")


def data_display_api(request):
    """
    数据可视化
    :param request:
    :return:
    """

    # 当日总数据处理
    t = time.strftime("%Y-%m-%d")
    now_day_count = []
    count_in = models.PersonPostInfo.objects.filter(date_time__contains=t).aggregate(Sum('point_in'))
    count_out = models.PersonPostInfo.objects.filter(date_time__contains=t).aggregate(Sum('point_out'))
    now_day_count.append({"value": count_in["point_in__sum"], "name": "入流量"})
    now_day_count.append({"value": count_out["point_out__sum"], "name": "出流量"})

    # 时段数据处理
    now_day_hour_count = []
    # date_time = time.strftime("%Y-%m-%d-%H", time.localtime())
    data_queryset = models.PersonPostInfo.objects.filter(date_time__icontains=t).values_list().order_by(
        "date_time")
    for data_tuple in data_queryset:
        now_day_hour_count.append(
            {"product": data_tuple[1] + data_tuple[-1][-3:] + "时", '入流量': data_tuple[2], '出流量': data_tuple[3]})
    now_day_hour_count = now_day_hour_count[-8::]

    # 月数据处理
    month_list = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12"]
    month_int_dict_data = {}
    month_out_dict_data = {}
    return_mon_in_data = []
    return_mon_out_data = []
    for i in range(1, 13):
        if i < 10:
            i = "0{}".format(i)
        in_mon_data = models.PersonPostInfo.objects.filter(date_time__contains=t[0:4]+"-{}".format(i)).aggregate(Sum('point_in'))
        if in_mon_data["point_in__sum"]:
            month_int_dict_data[i] = in_mon_data["point_in__sum"]
        else:
            month_int_dict_data[i] = 0

        out_mon_data = models.PersonPostInfo.objects.filter(date_time__contains=t[0:4]+"-{}".format(i)).aggregate(Sum('point_out'))
        if out_mon_data["point_out__sum"]:
            month_out_dict_data[i] = out_mon_data["point_out__sum"]
        else:
            month_out_dict_data[i] = 0

    for k, v in month_int_dict_data.items():
        return_mon_in_data.append(v)

    for k, v in month_out_dict_data.items():
        return_mon_out_data.append(v)

    month_tuple_data = (month_list, return_mon_in_data, return_mon_out_data)

    # 年数据处理
    """
    data_dict = {
        years_data: [(year, in_data, out_data), ...],
    }
    """
    years_dict = {}
    t = t[:4]
    # 从上线开始累计计算3年
    for i in range(0, 3):
        count_in = models.PersonPostInfo.objects.filter(date_time__contains=t).aggregate(Sum('point_in'))
        count_out = models.PersonPostInfo.objects.filter(date_time__contains=t).aggregate(Sum('point_out'))

        if not years_dict.get("years_data"):
            years_dict["years_data"] = [(t, count_in["point_in__sum"], count_out["point_out__sum"])]
        elif count_in["point_in__sum"] != None and count_in["point_out__sum"] != None :
            years_dict["years_data"].append((t, count_in["point_out__sum"], count_out["point_out__sum"]))
        t = int(t) - 1

    # 各点位进出流量
    """
    points_data_list = [(point_name, in, out),...]
    """
    points_data_list = []
    pname_list = models.PointInfo.objects.values("pname")
    for i in pname_list:
        in_out_data = models.PersonPostInfo.objects.filter(point_name=i["pname"]).aggregate(Sum("point_in"), Sum("point_out"))
        points_data_list.append((i["pname"], in_out_data["point_in__sum"], in_out_data["point_out__sum"]))

    return JsonResponse(
        {
            "hour_data": now_day_hour_count,
            "day_data": now_day_count,
            "month_data": month_tuple_data,
            "year_data": years_dict,
            "points_data_list": points_data_list
        },
        json_dumps_params={'ensure_ascii': False},
        content_type="application/json,charset=utf-8"
    )