# ZhubBot自述文件
---
##项目已废弃！
依赖框架已跑路！
存在关键性错误 可能导致血压升高
新版正在开发中...
---
## 关于
- 写在最前:项目名称无指代性，请勿对号入座！
- 随缘更新

---
## 安装运行
- 运行前，你需要:
- Python 3.8.10或以上
- [QQminiBot](https://minibot.cc/) 点击跳转

### 第一步 安装QQminiBot
- 安装方法[见此](https://doc.minibot.cc/web/#/1/4)

### 第二步 安装HttpAPI与PicHttp
- [HttpAPI指路](https://forum.minibot.cc/forum.php?mod=viewthread&tid=34)
- [PicHttp指路](https://forum.minibot.cc/forum.php?mod=viewthread&tid=175)
- [插件安装方法](https://doc.minibot.cc/web/#/1/23)

### 第三步 配置HttpAPI
- 运行QQmini
- 选择"拓展"
- 找到你刚刚安装的"HttpAPI" 右键→设置窗口
- 在"消息推送"一栏中 填入你要推送到的地址与端口 举个例子 我要推送到本地的11451这个端口，那这里就填写```http://127.0.0.1:11451/``` 
- 如果你不知道我在说什么 那就和我填一样的
- 随后，在下方的本地服务设置→开关服务中，关掉这个服务
- 因为发送使用PicHttp而非HttpAPI 而PicHttp的接收端口是被作者写死在PicHttp里的1044。

### 第四步 部署本项目
- 打包下载
- 使用文本编辑器打开```config.py```
- 在第22行ListenPort,将它改成你在第三步中填写的端口，例中填写的是```http://127.0.0.1:11451/```,所以这一行为
```
ListenPort = 11451
```
- 在第26行中写入最高管理者的QQ号 例如
```
master= "1145141919180"
```
- 在第28行填入默认机器人的QQ号 不知道啥是默认机器人就写MiniBot上登录的机器人的QQ号 例如
```
defaultBot = "9527"
```

### 第五步 启动
- 以Windows为例，在项目目录下新建一个文本文档,重命名为run.bat 右键→编辑，在里面输入
```
python main.py
pause
```
- 保存后双击运行

- 不出意外的话 项目就部署完了

---
# 插件开发

### 1.项目运行过程
 - (1)项目启动后，首先会加载配置文件与用户权限。
 -  (2)随后，项目会执行位于```pluginLoader.py```下的```PluginLoad()```，以导入```plugins```下的所有模块，随后执行插件自定的导入函数与初始化函数。
 -  (3)再之后，项目会为所有插件注册命令(如果有)。
-  (4)接着，项目会分裂出消息接收线程，消息广播线程，与命令处理线程。消息接收线程接收到由上级HttpAPI推送的消息后，借由此消息生成一个message对象(在```message.py```中定义),随后将这个对象传 - 递到消息板上(由```var.py```定义)，消息广播线程会监听消息板，当板上存在消息时，获取存在的消息对象，将这个消息对象推送给所有插件，执行每个插件的消息处理函数，随后从消息板上删除这个消息。而命令处理器用于处理在控制台输入的命令。
 - (5)当收到```stop```命令时，```exitFlag```(```var.py```中定义)变为True，由命令处理线程向消息 - 接收线程get一个停止请求,接着执行插件自定的关闭函数，随后命令处理线程与消息接收线程退出，而消息推送器监听```exitFlag```的值，当其为True时执行退出。
 
### 2.插件开发细则
ZhubBot将位于plugins下的所有模块视为插件，并要求其```__init___.py```下有规定的函数，他们分别是
``` Python
def OnEnable(Null):
    pass
    # 插件导入函数
  
def OnLoad(Null):
    pass
    #插件初始化函数
  
def CommandRegister(Null):
   commandList = ["command1", "command2",......,"command114514"]
   return commandList
   #命令注册函数
 
def CommandExecuter(commands, args):
    #python3.10
    match command:
        case "command1":
            pass #  命令语句
        case "command2":
            pass #  命令语句
         ...
         case _:
            log.error("未知错误！程序执行到了不可到达的地方！", "Plugin")

def GetMsg(Message):
    pass #  消息处理函数
    # 这里传入的MEssage是一个消息对象，详细定义位于message.py
 
def Exit(Null):
    pass #  退出时需要执行的函数，一般为保存文件等
```
### 3.自带模块介绍
### 此部分存在关键性错误！
 - 调用自带模块需要在项目首行添加
```python
import sys
sys.path.append(:../..")
```
 - 或者，你也可以直接复制你要调用模块的py文件到你的模块文件夹。

1. ```config.py```
 - 为项目自带的配置文件,不推荐使用插件更改这里的设置或将配置保存在这里，建议保存在插件模块内

2. ```Listener.py```
 - 定义了消息接收线程，不建议调用

3. ```log.py```
 - 定义了日志，主要用于打印以及保存日志。分为info、warn与error，传参相同，以info为例
```python
log.info("这是一条测试日志消息","Plugin")
```
 - 第一个参数表示需要输出的消息，第二个参数表示日志发出者，是可选参数，可以为插件名，默认Base。
 - log模块会输出日志到```./Logging/```下，以日期命名。

4. ```main.py```
 - 项目主文件，不建议调用

5. ```message.py```
 - 定义了消息类与一些(个)常用的消息方法
 - Message类:
 - 传参:未经过json解码的获取到的原始消息
属性:
```python
self.origianMessage #  未经过json解码的获取到的原始消息
self.decode         #  经过json解码后得到的字典
self.MsgID          #  这条消息的MsgID
self.MsgSn          #  这条消息的MsgSn
self.FromQQ         #  这条消息的发信者QQ账号(群聊消息时指发消息的人，私聊时也指发消息的人)
self.Event          #  这条消息的事件类型，常见的类型有1为私聊消息，2，3，4，5，6为群聊消息
self.GeetMessageBot #  收到这条消息的机器人的QQ号
self.From           #  从哪里收到这条消息(私聊为发消息的人的QQ号，群聊为群号)
self.Type           #  未知含义，总是0
self.To             #  发送到的目标
self.Msg            #  消息内容
```
 - 方法:
```python
def reply(self,Msg)       #  用于快速对这条消息进行回复，回复内容为Msg
```

FakeMessage类:
 - 伪造一条消息
 - 是Message的子类，除非执行self.addToBoard()否则不会将自己广播到消息板
 - 传参:```bot, Event, Msg, getFrom```
 - 他们分别为假装获取到这条消息的机器人; 事件类型; 伪造的消息内容; 发信者(QQ号或群号); 
 - 无新增属性与新增方法

函数:
 - sendMessage函数
 - 传参:```SendType, SendTo, Msg, Bot= config.defaultBot ```他们分别为发送的类型(1为私聊,2，3，4，5，6为群聊); 发送到的QQ号或群号; 发送的消息内容，以及可选参数 发送的机器人，默认为config.py中设置的默认机器人

6. ```PluginLoader.py```
 - 定义了插件加载与运行相关的函数，不可导入，会触发循环导入错误。

7. ```premission.py```
 - 定义了权限相关的函数
```PremessionFileLoad()```
 - 从文件加载权限信息，一般用不到，加载到的信息储存在```var.Premission中```
```PremessionFileUpLoad()```
 - 从内存更新权限到文件
 - 推荐在修改权限后使用以保存修改，如果修改权限后不执行此函数则修改只对这次项目关闭前有效。
```SetPremession(SetQQ,SetLevel,User="Base")```
 - 设置一个用户的权限等级
 - 传参:```SetQQ,SetLevel,User="Base"``` 分别表示被设置的QQ; 要设置到的权限等级; 可选参数，默认为base(服务器), 传入非默认值时表示发起这次设置的人的QQ，除config.py中设置的master账号初始权限等级为100之外，其他所有用户默认权限等级均为1。
```GetPremission(QQ)```
 - 获取一个用户的权限等级，返回一个整数表示用户的权限等级
```ComparePremission(QQ1,QQ2)```
 - 比较QQ1与QQ2两个账号权限等级的打小,返回值为权限等级高的QQ号，若相同则返回"Same"。

8. ```var.py```
 - 用于定义项目全局变量,不建议修改或导入
---
