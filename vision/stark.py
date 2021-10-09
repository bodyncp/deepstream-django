#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2020/3/10 10:16
# @Author  : NCP
# @File    : stark.py
# @Software: PyCharm

from stark.service.v1 import site
from vision import models
from vision.views.userinfo import UserInfoHandler
from vision.views.point_info import PointInfoHandler
from vision.views.edge_driver import EdgeDriverHandler
from vision.views.person_count import PersonPostInfoHandler
from vision.views.edge_driver_control import EdgeDriverSshHandler


site.register(models.UserInfoExtent, UserInfoHandler)
site.register(models.PointInfo, PointInfoHandler)
site.register(models.EdgeDriver, EdgeDriverHandler)
site.register(models.PersonPostInfo, PersonPostInfoHandler)
site.register(models.EdgeDriverSsh, EdgeDriverSshHandler)

