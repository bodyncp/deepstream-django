# Generated by Django 2.0 on 2021-10-09 00:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='EdgeDriver',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('dname', models.CharField(max_length=32, unique=True, verbose_name='设备名称')),
                ('driver_pull', models.CharField(blank=True, default='ws://<input_ip>:8000/live/test', max_length=64, null=True, verbose_name='网页拉流地址')),
                ('bearing_point', models.CharField(max_length=64, verbose_name='承载点位')),
            ],
        ),
        migrations.CreateModel(
            name='EdgeDriverSsh',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ssh_addr', models.GenericIPAddressField(verbose_name='IP地址')),
                ('driver_status', models.IntegerField(choices=[(1, '在线'), (2, '离线')], default=2, verbose_name='设备状态')),
                ('rtmp_server_status', models.IntegerField(choices=[(1, '在线'), (2, '离线')], default=2, verbose_name='流服务器状态')),
                ('program_status', models.IntegerField(choices=[(1, '在线'), (2, '离线')], default=2, verbose_name='程序状态')),
                ('driver_name', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to='vision.EdgeDriver', verbose_name='设备名称')),
            ],
        ),
        migrations.CreateModel(
            name='PersonPostInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('point_name', models.CharField(max_length=32, verbose_name='统计点位名称')),
                ('point_in', models.CharField(max_length=32, verbose_name='进入流量')),
                ('point_out', models.CharField(max_length=32, verbose_name='出去流量')),
                ('date_time', models.CharField(max_length=32, verbose_name='统计时间')),
            ],
        ),
        migrations.CreateModel(
            name='PointInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pname', models.CharField(max_length=32, unique=True, verbose_name='点位名称')),
                ('pull_address', models.CharField(max_length=128, unique=True, verbose_name='拉流地址')),
                ('driver', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='vision.EdgeDriver', verbose_name='承载AI设备')),
            ],
        ),
        migrations.CreateModel(
            name='UserInfoExtent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=32, unique=True, verbose_name='用户名')),
                ('password', models.CharField(max_length=64, verbose_name='密码')),
                ('email', models.CharField(blank=True, default='xx@189.cn', max_length=32, null=True, verbose_name='邮箱')),
                ('phone', models.CharField(blank=True, max_length=32, null=True, unique=True, verbose_name='联系方式')),
                ('level', models.IntegerField(blank=True, choices=[(1, 'T1'), (2, 'T2'), (3, 'T3')], null=True, verbose_name='级别')),
                ('roles', models.ManyToManyField(blank=True, default=2, to='rbac.Role', verbose_name='拥有的所有角色')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
