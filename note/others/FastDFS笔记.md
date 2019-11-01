### 介绍
FastDFS是一个轻量级高性能分布式文件系统，主要功能是文件存储，同步和访问(上传下载文件)，主要适用于小文件存储需求(4k-500M)。
FastDFS主要有两个角色：
 * tracker：追踪服务器，主要负责调度以及负载均衡工作。
 * storage：存储服务器，即文件存储节点，主要负责存储文件，直接利用OS的件系统进行文件管理，storage可以进行分组/卷(group/volume)，同一组内服务器文件相互同步完全相同，因此一各组的最大存储空间受组中存储服务器最小存储空间限制；可以通过增加组/卷(group/volume)的方式来横向扩展FastDFS的存储空间。【简单来说一个FastDFS集群可以有一个或多个组/卷，集群存储容量为多有组容量的总和，一个组/卷可以有一个或多个storage存储服务器，组/卷的存储空间为组中storage存储服务器中容量最小的一台决定】

### FastDFS安装部署
本安装部署步骤在centos7环境上
[官方文档](https://github.com/happyfish100/fastdfs/wiki)
#### 1、安装编译环境
```
sudo yum install git gcc gcc-c++ make automake autoconf libtool pcre pcre-devel zlib zlib-devel
```
#### 2、创建安装目录：
 * ```mkdir -p /apps/svr/FastDFS```

#### 3、安装libfastcommon 公共依赖
 * 下载依赖包： ```https://github.com/happyfish100/libfastcommon/archive/V1.0.35.tar.gz```，并将安装包上传到服务器/apps/svr/FastDFS目录
 * 解压依赖包： ```tar -zvxf libfastcommon-1.0.35.tar.gz```
 * 编译安装(**root用户**)： ```cd libfastcommon-1.0.35; ./make.sh && sudo ./make.sh install```

#### 4、安装FastDFS：
 * 下载安装包： ```https://github.com/happyfish100/fastdfs/archive/V5.11.tar.gz```，并将安装包上传到服务器/apps/svr/FastDFS目录
 * 解压安装包： ```tar -zvxf fastdfs-5.11.tar.gz```
 * 编译安装(**root用户**)： ```cd fastdfs-5.11; ./make.sh && sudo ./make.sh install```

#### 5、创建数据目录：
 * ```mkdir -p /apps/fastdfs-data/tracker; mkdir -p /apps/fastdfs-data/storage```

#### 6、配置tracter：
 * 复制配置文件： ``` sudo cp /etc/fdfs/tracker.conf.sample /etc/fdfs/tracker.conf```
 * 修改文件： ``` sudo vi /etc/fdfs/tracker.conf```
```
# 修改数据以及日志基础路径，绑定端口等沿用默认值
# the base path to store data and log files
base_path=/apps/fastdfs-data/tracker
```

#### 7、配置storage：
 * 复制配置文件： ```sudo cp /etc/fdfs/storage.conf.sample /etc/fdfs/storage.conf```
 * 修改配置文件： ```sudo vi /etc/fdfs/storage.conf```
```
# the base path to store data and log files
base_path=/apps/fastdfs-data/storage
# store_path#, based 0, if store_path0 not exists, it's value is base_path
# the paths must be exist
store_path0=/apps/fastdfs-data/storage
# tracker_server can ocur more than once, and tracker_server format is
#  "host:port", host can be hostname or ip address
tracker_server=10.17.162.114:22122
```

#### 8、tracker启停命令：
```
sudo /etc/init.d/fdfs_trackerd start #启动tracker服务
sudo /etc/init.d/fdfs_trackerd restart #重启动tracker服务
sudo /etc/init.d/fdfs_trackerd stop #停止tracker服务
sudo chkconfig fdfs_trackerd on #自启动tracker服务
```

#### 9、storage启停命令：
```
sudo /etc/init.d/fdfs_storaged start #启动storage服务
sudo /etc/init.d/fdfs_storaged restart #重动storage服务
sudo /etc/init.d/fdfs_storaged stop #停止动storage服务
sudo chkconfig fdfs_storaged on #自启动storage服务
```

#### 10、查看是否启动成功
```
ps -ef | grep tracker | grep -v grep
ps -ef | grep storage | grep -v grep
```

#### 11、测试功能
 * 修改配置： ```sudo cp /etc/fdfs/client.conf.sample /etc/fdfs/client.conf```
```
# the base path to store log files
base_path=/apps/fastdfs-data

# tracker_server can ocur more than once, and tracker_server format is
#  "host:port", host can be hostname or ip address
tracker_server=10.17.162.114:22122
```
 * 测试上传文件： ```fdfs_upload_file /etc/fdfs/client.conf /apps/fastdfs-data/tracker/logs/trackerd.log ```
上传成功会返回上传后的文件路径，如下:
```
# 测试上传文件
[apps@myxl50356 ~]$ fdfs_upload_file /etc/fdfs/client.conf /apps/fastdfs-data/tracker/logs/trackerd.log
# 上传完后返回文件标识
group1/M00/00/00/ChGicl270nqAAenIAAAFVMk9l44187.log
# 查看上传后的文件
[apps@myxl50356 ~]$ ls /apps/fastdfs-data/storage/data/00/00/
ChGicl270nqAAenIAAAFVMk9l44187.log
```
