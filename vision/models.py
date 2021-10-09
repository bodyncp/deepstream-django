from django.db import models
from rbac.models import UserInfo

# Create your models here.


class UserInfoExtent(UserInfo):
    """
    管理人员信息扩展
    """
    phone = models.CharField(verbose_name='联系方式', max_length=32, unique=True, blank=True, null=True)
    level_choices = (
        (1, 'T1'),
        (2, 'T2'),
        (3, 'T3'),
    )
    level = models.IntegerField(verbose_name='级别', choices=level_choices, blank=True, null=True)

    def __str__(self):
        return self.name


class PointInfo(models.Model):
    """
    前端点位表
    """
    pname = models.CharField(verbose_name="点位名称", max_length=32, unique=True)
    pull_address = models.CharField(verbose_name="拉流地址", max_length=128, unique=True)
    driver = models.ForeignKey(verbose_name="承载AI设备", to="EdgeDriver", on_delete=models.DO_NOTHING)

    def __str__(self):
        return self.pname


class EdgeDriver(models.Model):
    """
    边缘设备表
    """
    dname = models.CharField(verbose_name="设备名称", max_length=32, unique=True)
    driver_pull = models.CharField(verbose_name="网页拉流地址", default="ws://<input_ip>:8000/live/test", blank=True, null=True, max_length=64)
    bearing_point = models.CharField(verbose_name="承载点位", max_length=64)

    def __str__(self):
        return self.dname


class PersonPostInfo(models.Model):
    """
    人流统计表
    """
    point_name = models.CharField(verbose_name="统计点位名称", max_length=32)
    point_in = models.CharField(verbose_name="进入流量", max_length=32)
    point_out = models.CharField(verbose_name="出去流量", max_length=32)
    date_time = models.CharField(verbose_name="统计时间", max_length=32)

    def __str__(self):
        return self.point_name


class EdgeDriverSsh(models.Model):
    """
    边缘设备控制信息表
    """
    ssh_addr = models.GenericIPAddressField(verbose_name="IP地址")
    status_list = (
        (1, "在线"),
        (2, "离线"),
    )
    driver_status = models.IntegerField(verbose_name="设备状态", choices=status_list, default=2)
    rtmp_server_status = models.IntegerField(verbose_name="流服务器状态", choices=status_list, default=2)
    program_status = models.IntegerField(verbose_name="程序状态", choices=status_list, default=2)
    driver_name = models.OneToOneField(to="EdgeDriver", verbose_name="设备名称", on_delete=models.DO_NOTHING)
