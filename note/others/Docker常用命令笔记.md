### 根据Dockerfile构建镜像
docker build -t \<tag-name\> .
> tag-name表示镜像名称，如docker build -t oujh/eureka-server .；.表示Dockerfile在当前目录下

### 查看目前在运行的容器
docker ps

### 查看本地镜像列表
docker images

### 运行容器
docker run -p <主机(宿主)端口>:<容器端口> -d \<tag-name\>
> 如：docker run -p 8761:8761 -d oujh/eureka-server

### 进入容器并打开bash界面，可以执行命令
docker exec -it <容器id> /bin/bash

### 实时刷新容器启动日志
docker logs -f <容器id>

### spring cloud项目Dockerfile简单示例
```
FROM centos:7
LABEL maintainer=oujh@test.com
RUN yum install -y net-tools vim java-1.8.0-openjdk

COPY /target/application-0.0.1.jar ./application-0.0.1.jar
ENTRYPOINT ["java", "-jar",  "application-0.0.1.jar"]
```
启动命令
```
# bootstrap.yml文件中不配置注册中心地址，启动时动态指定注册中心
docker run -p 8080:8080 -d -it oujh/application-service --eureka.client.service-url.defaultZone=http://172.17.0.2:8761/eureka
```