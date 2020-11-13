# TOSA的mirai讲座

**docs**中是讲义

**miraiOK**是本地配置好的一个版本的mirai

**graia**中是python部分的代码

### 使用docker-compose部署Bot

推荐使用常见Linux发行版。

1. 安装docker和docker-compose，并设置国内源（略，教程较多）

2. 构建镜像`docker-compose build`

3. 首次运行容器`docker-compose up`

4. 看见报错后按Ctrl-C停止

5. 修改`./miraiOK/config/Console/AutoLogin.yml`和`./miraiOK/config/MiraiApiHttp/setting.yml`，并将`./miraiOK/config/MiraiApiHttp/setting.yml`复制到`.graia/`下。`.graia/`下的`setting.yml`应当根据后续的报错修改。

6. 运行容器`docker-compose up` （或后台运行`docker-compose up -d`）

样例`.graia/setting.yml`:

```
host: mirai
port: 8080
authKey: INITKEYWhaxxxx
qq: 353364xxxx
cacheSize: 4096
enableWebsocket: false
report:
  enable: false
  groupMessage:
    report: true
  friendMessage:
    report: true
  tempMessage:
    report: true
  eventMessage:
    report: true
  destinations: []
  extraHeaders: {}

heartbeat:
  enable: false
  delay: 1000
  period: 15000
  destinations: []
  extraBody: {}
  extraHeaders: {}

```
