# deepstream-django-check_web
# 本项目结合多方源码实现基于web的实时目标检测系统，系统采用python3.6+deepstream5.1+django2.0实现目标检测人流、车流计数任务，实现内容如下：
1. 分时段计数统计
2. 数据可视化展示
3.截图抓拍、平台显示
4. 数据下载
5. 设备状态查看
6. 用户权限管理

## 设计思路
采用jetson设备边缘部署方式，以每一个边缘设备为节点进行数据采集和监控处理，如图所示:
![image](https://user-images.githubusercontent.com/40747806/135811095-ab259816-7da2-49ea-b38f-843762691041.png)

## 如何使用
### 1. 安装
1、后台需要按照requirements.txt文件下载对应安装包，执行pip install -r ./requirements.txt，如果网速太慢可添加国内源下载，如：pip install -r ./requriements.txt -i https://mirrors.aliyun.com/pypi/simple

2、边缘端需下载deepstream>=5.0(因本项目全部采用python3.6开发，因此需deepstream升级至5.0或更高版本，下载deepstream需注意与其对应的jetpack版本！)

3、作者在jetson设备桌面配置了一键启动脚本，拿到jetson端源码后可直接双击运行

### 2. 启动
1、先启动后台django程序，注释掉django rbac中间件，然后查看rbac文件夹下的文档说明.py文件进行配置，保证能够创建用户并进入系统，然后配置属于自己的初始化数据例如：用户、权限等内容，能够正常使用后再开启rbac中间件，配置jetson设备信息以及需要接入的前端摄像头的、rtsp地址或者其他流媒体地址（！一定是先创建jetson设备，然后再创建前端拉流信息等后续内容！）。

2、在settings文件同级目录下创建local_settings文件，配置路由、校验秘钥等信息用于jetson设备和django通信，配置设备监控信息，用于平台侧检测边缘端设备工作情况。

3、后台能够正常运行后，双击前端jetson设备的桌面一键启动按钮，先启动server服务，然后启动project服务，能够看见弹出框并且正常运行即可。

4、观察后台检测到的前端平台运行情况及视频监控流媒体调用情况，若均正常，启动完毕

### 功能截图
![screenshot-127 0 0 1_8000-2021 10 04-15_07_03](https://user-images.githubusercontent.com/40747806/135811154-7f8d59e9-669d-4311-ac43-7db687a3efb3.png)

![screenshot-127 0 0 1_8000-2021 10 04-15_07_21](https://user-images.githubusercontent.com/40747806/135811268-f0e5a311-eadb-431f-8414-878c9e7313d7.png)

![screenshot-127 0 0 1_8000-2021 10 04-15_07_47](https://user-images.githubusercontent.com/40747806/135811126-f041fb71-dca3-413e-9fe9-1b4f55f3c33b.png)

### 如需帮助
可联系作者获取sqlite3.db，直接进入系统使用
如需使用mysql等数据库或不会操作，可联系作者邮箱：18981275647@189.cn

### 感谢
https://github.com/WuPeiqi
