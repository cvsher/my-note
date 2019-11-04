### 简介
ELK即Elasticsearch、Logstash、Kibana 三个组件的组合，每个组件有各自的功能。
 * 日志聚合：在现在微服务化的趋势下，一个应用通常会划分成相互独立的多个模块，而且每个模块也有可能进行多节点冗余部署，这样的场景下要查询服务的日志文件就需要登录到不同的服务器上各自去查看日志，操作繁琐且不容易找到想要的日志，这样的情况下就可以使用ELK进行日志聚合和分析查询。
#### Elasticsearch
Elasticsearch 是一个搜索和分析引擎，可实现数据的实时全文搜索、支持水平扩展，高可用，并提供API接口，可以处理大规模日志数据搜索，比如Nginx、Tomcat、系统日志等功能[官方地址](https://www.elastic.co/cn/)，纯java语言开发，基于Apache Lucene搜索引擎库构建
#### Logstash
Logstash 是用于日志的收集、转换、并输出到ES，其中有丰富的插件用于集成诸如Filebeat、Flume、Kafka、Log4J等各种外部数据源，还能输出到各种目标存储器中，可通过插件实现日志收集，支持日志过滤，支持普通log、自定义json格式的日志解析
#### Kibana
Kibana 是基于ES的分析与可视化平台，我们可以通过Kibana在ES中搜索、查看各类索引并制作出各种图表

### ELK安装部署
#### Elasticsearch 安装
[官方文档](https://www.elastic.co/guide/en/elasticsearch/reference/current/install-elasticsearch.html)
##### 1、下载Elasticsearch安装包
 * 访问后面地址下载Elasticsearch安装包，并上传到服务器中。```https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-7.4.2-linux-x86_64.tar.gz```

##### 2、解压安装包
 * ```tar -zvxf elasticsearch-7.4.2-linux-x86_64.tar.gz```

##### 3、修改配置文件```elasticsearch.yml```
```
# 修改data存放的路径
path.data: /data/es-data
# 修改logs日志的路径
path.logs: /var/log/elasticsearch/
# 需要设置绑定的ip，否则只能本机访问es
network.host: 10.17.162.115
discovery.seed_hosts: ["10.17.162.115"]
```

##### 4、启停Elasticsearch
 * ```./bin/elasticsearch -d -p pid``` 在后台运行Elasticsearch，并将进行id记录到pid文件中
 * ```kill `cat pid` ``` 根据pid文件记录的进程id杀掉进程，以关闭Elasticsearch

##### 5、访问```http://10.17.162.115:9200/``` 访问界面

#### Kibana 安装
[官方文档](https://www.elastic.co/guide/en/kibana/current/install.html)
##### 1、下载Kibana安装包
 * 访问后面地址下载Kibana安装包，并上传到服务器中。```https://artifacts.elastic.co/downloads/kibana/kibana-7.4.2-linux-x86_64.tar.gz```

##### 2、解压安装包
 * ```tar -zvxf kibana-7.4.2-linux-x86_64.tar.gz```

##### 3、修改配置文件```config/kibana.yml```
```
# Specifies the address to which the Kibana server will bind. IP addresses and host names are both valid values.
# The default is 'localhost', which usually means remote machines will not be able to connect.
# To allow connections from remote users, set this parameter to a non-loopback address.
server.host: "0.0.0.0"

# The URLs of the Elasticsearch instances to use for all your queries.
elasticsearch.hosts: ["http://10.17.162.115:9200"]

# Specifies the address to which the Kibana server will bind. IP addresses and host names are both valid values.
# The default is 'localhost', which usually means remote machines will not be able to connect.
# To allow connections from remote users, set this parameter to a non-loopback address.
# 设置绑定ip，否则只有本机可以访问
server.host: "10.17.162.115"
```

##### 4、启停Kibana
 * ```bin/kibana ``` 启动kibana

##### 5、访问```http://10.17.162.115:5601 ``` 访问界面

#### Logstash 安装
[官方文档](https://www.elastic.co/guide/en/logstash/current/installing-logstash.html)
##### 1、下载Logstash安装包
 * 访问后面地址下载Logstash安装包，并上传到服务器中。```https://artifacts.elastic.co/downloads/logstash/logstash-7.4.2.tar.gz```

##### 2、解压安装包
 * ```tar -zvxf logstash-7.4.2.tar.gz```

##### 3、创建配置文件logstash.conf
logstash默认提供多种插件用于处理输入输出，常用的[输入插件](https://www.elastic.co/guide/en/logstash/current/input-plugins.html)有tcp、http、kafka、file、log4j等；常用[输出插件](https://www.elastic.co/guide/en/logstash/current/output-plugins.html)有file、zabbix、Elasticsearch等
如下实例配置文件配置logstash从tcp端口接收日志输入，并输出到Elasticsearch中
```
# 输入 以tcp_input为例
input {      
    tcp {
       port => 9876
       mode => "server"  #值是["server","client"]其中之一,默认是server 
       ssl_enable => false
   }
}
# 输出 以ES为例
output {
    elasticsearch { 
        hosts => ["10.17.162.115:9200"] 
    }
}

```
##### 4、启停Logstash
 * ```bin/logstash -f logstash.conf ``` 启动logstash
