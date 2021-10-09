#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/2/17 21:07
# @Author  : NCP
# @File    : download.py
# @Software: PyCharm

from stark.service.v1 import queryset_dict
from django.http import StreamingHttpResponse
import pandas as pd
from collections import OrderedDict


def download_file(request, *args, **kwargs):
    new_data_queryset = queryset_dict["download_data"]

    # 打开excel
    writer = pd.ExcelWriter(str("download_data")+".xls")
    data_dict = OrderedDict()
    # print(new_data_queryset._meta.fields)
    for data_obj in new_data_queryset:
        if not data_dict.get("统计点位名称"):
            data_dict["统计点位名称"] = [data_obj.point_name]
        else:
            data_dict["统计点位名称"].append(data_obj.point_name)

        if not data_dict.get("进入流量"):
            data_dict["进入流量"] = [data_obj.point_in]
        else:
            data_dict["进入流量"].append(data_obj.point_in)

        if not data_dict.get("出去流量"):
            data_dict["出去流量"] = [data_obj.point_out]
        else:
            data_dict["出去流量"].append(data_obj.point_out)

        if not data_dict.get("统计时间"):
            data_dict["统计时间"] = [data_obj.date_time]
        else:
            data_dict["统计时间"].append(data_obj.date_time)

    df1 = pd.DataFrame(data=data_dict)
    df1.to_excel(writer, sheet_name='sheet1')
    writer.save()


    file = open(str("download_data")+".xls", 'rb')
    response = StreamingHttpResponse(file)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="%s.xls"' % str("download_data")
    return response
