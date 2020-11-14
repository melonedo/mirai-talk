# windows下配置mirai

前置条件：java和python（似乎需要3.7以上）

## 使用mirua安装（似乎会失败）

1. 使用mirua启动器。先下载[mirua](https://github.com/zkonge/mirua)的windows版本，下载后修改后缀为 **.exe** ，新建一个文件夹mirua并放入。运行一次mirua时，会自动在 **mirua/** 下载mirai本体。

2. 安装插件[mirai-api-http](https://github.com/project-mirai/mirai-api-http/releases) 和[mirai-console-addition](https://github.com/Pai2Chen/mirai-console-addition/releases)。mirai-app-http的新版本似乎有兼容问题，此处使用[mirai-api-http-v1.8.2](https://github.com/project-mirai/mirai-api-http/releases/download/v1.8.2/mirai-api-http-v1.8.2.jar)。mirai-console-addition使用[mirai-console-addition-1.2-beta](https://github.com/Pai2Chen/mirai-console-addition/releases/download/v1.2-beta/console-addition-1.2-beta.jar)。下载后放入 **mirua/plugins/** 。

3. 再次启动mirua，配置自动登录。在界面中输入`/autologin qq号 密码`，按回车确认（输错密码就再输一次）。此时已配置好自动登录。

4. 正式启动mirua，此时会看到大量的信息。

## 使用miraiOK安装

1. 下载[GitHub - LXY1226/MiraiOK: 另一个Mirai一键包](https://github.com/LXY1226/MiraiOK)的amd64版本，放到 **miraiOK/** 目录下。运行一次，会自动下载mirai本体。

2. 再次运行以生成对应目录，输入`exit`回车退出mirai。从[GitHub - Anillc/miraiok-resource: miraiok-resource](https://github.com/Anillc/miraiok-resource)下载mirai-api-http，放到 **miraiOK/plugins/** 。

3. 自动登录。编辑 **miraiOK/config/Console/AutoLogin.yml** ，将plainPasswords下面的123456改为qq号，example改为密码。

4. 启动miraiOK。

## 安装python框架graia

使用指令

`pip install graia-application-mirai graia-broadcast PyYAML --update`

## 收工

接下来可以看graia的[教程](https://graiaproject.github.io/Application/#/)了。
