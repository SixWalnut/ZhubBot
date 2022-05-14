# ZhubBot自述文件
---
## 关于
写在最前:项目名称无指代性，请勿对号入座！
随缘更新

---
## 安装运行
运行前，你需要:
Python 3.8.10或以上
[QQminiBot](https://minibot.cc/) 点击跳转

### 第一步 安装QQminiBot
安装方法[见此](https://doc.minibot.cc/web/#/1/4)

### 第二步 安装HttpAPI与PicHttp
[HttpAPI指路](https://forum.minibot.cc/forum.php?mod=viewthread&tid=34)
[PicHttp指路](https://forum.minibot.cc/forum.php?mod=viewthread&tid=175)
[插件安装方法](https://doc.minibot.cc/web/#/1/23)

### 第三步 配置HttpAPI
运行QQmini
选择"拓展"
找到你刚刚安装的"HttpAPI" 右键→设置窗口
在"消息推送"一栏中 填入你要推送到的地址与端口 举个例子 我要推送到本地的11451这个端口，那这里就填写```http://127.0.0.1:11451/``` 
如果你不知道我在说什么 那就和我填一样的
随后，在下方的本地服务设置→开关服务中，关掉这个服务
因为发送使用PicHttp而非HttpAPI 而PicHttp的接收端口是被作者写死在PicHttp里的1044。

### 第四步 部署本项目
打包下载
使用文本编辑器打开```config.py```
在第22行ListenPort,将它改成你在第三步中填写的端口，例中填写的是```http://127.0.0.1:11451/```,所以这一行为
```
ListenPort = 11451
```
在第26行中写入最高管理者的QQ号 例如
```
master= "1145141919180"
```
在第28行填入默认机器人的QQ号 不知道啥是默认机器人就写MiniBot上登录的机器人的QQ号 例如
```
defaultBot = "9527"
```

### 第五步 启动
以Windows为例，在项目目录下新建一个文本文档,重命名为run.bat 右键→编辑，在里面输入
```
python main.py
pause
```
保存后双击运行

不出意外的话 项目就部署完了

---
# 插件开发
等待编辑
