from django.test import TestCase

# Create your tests here.

import paramiko
import sys

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect('192.168.2.53', username='ncp', password='123123', timeout=5)
except Exception as e:
    print(e)
    sys.exit()

# cmd = 'ps -ef | grep python3'
# cmd = 'cd /opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/jetson_pro;ls -l'
# cmd = """sh -c 'cd home;ls -l'"""
# cmd_run = 'cd /opt/nvidia/deepstream/deepstream-5.1/sources/deepstream_python_apps/apps/jetson_pro;nohup /bin/sh start.sh 2>&1 &'
cmd_run = 'ps -ef | grep node'
# cmd_ping = 'ping -c 2 192.168.2.29'
#
# print("------------------------")
# _, stdout, stderr = ssh.exec_command(cmd_ping)
#
# data = stdout.read().decode("utf-8")
# data = data.split('\n')
# for i in data:
#     if " 0 received" in i:
#         print("driver is not found")
#         sys.exit()
_, stdout, stderr = ssh.exec_command(cmd_run, 4096)
# while True:
#     line = stdout.readline()
#     if not line:
#         break
#     print(line)
# stdin, stdout, stderr = ssh.exec_command(cmd)
data = stdout.readlines()
if stderr.read():
    print(stderr.read())
if data:
    print(data)
    for i in data:
        if "node app.js" in i:
            print(i)
        if "python3 enrty.py" in i:
            print(i)
        continue

ssh.close()
sys.exit()
