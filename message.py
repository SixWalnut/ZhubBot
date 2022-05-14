#!/usr/bin/env python 3.10.2
# -*-coding:utf-8 -*-
#创建日期: 2022/05/12 18:33:13 
#创建者: SixWalnut
#文件描述: 消息相关方法定义模块

#准备好后可以导入模块了
#self lib
import log
import config
import var
import config
#package lib

#sys lib
import json
import requests

# 消息类
class Message():
    # 初始化
    def __init__(self,origianMessage):
        # 原始消息字符串
        self.origianMessage = origianMessage
        self.decode = json.loads(origianMessage)                #  转换为字典对象
        self.MsgId = self.decode["MsgId"]                       #  设置消息属性
        self.MsgSn = self.decode["MsgSn"]
        self.FromQQ = self.decode["FromQQ"]
        self.Event = self.decode["Event"]
        self.GetMessageBot = self.decode["Robot"]
        self.From = self.decode["From"]
        self.Type = self.decode["Type"]
        self.To = self.decode["To"]
        self.Msg = self.decode["Msg"]
        self.addToBoard()                                       #  将消息添加到消息板上
    
    # 回复方法 用于对消息快速回复
    def reply(self,Msg):
        # 过滤url中特殊意义字符
        MSg = Msg.replace("+","%2b")
        MSg = Msg.replace("&","%26")
        # 判断消息类型是群组还是私聊
        # 群组
        if self.Event in [1]: 
            type_ = "1"
            r= requests.get("http://"+config.PostIP+":"+config.PostPort+"/?robot="+self.GetMessageBot+"&type="+ type_+"&qq="+ self.FromQQ +"&data=" + Msg)
        # 私聊
        elif self.Event in [2,3,4,5,6]:
            type_ = str(self.Event)
            r= requests.get("http://"+config.PostIP+":"+config.PostPort+"/?robot="+self.GetMessageBot+"&type="+ type_+"&guid="+ self.From +"&data=" + Msg)
        # 二者都不是
        else:
            raise Exception("不能回复的消息类型:{}".format(self.Event))
        return r
        # 可以看出群组和私聊用于get的链接有些不同，群组为guid 私聊为qq

    # 将消息添加到消息板
    def addToBoard(self):
        var.MessageBoard.append(self)

# 伪造消息类
class FakeMessage(Message):
    #初始化 需要传入接收的bot, 消息类型, 消息内容, 发信者
    def __init__(self,bot,Event,Msg,getFrom):
        self.bot = bot
        self.Event = Event
        self.Msg = Msg
        self.MsgId = ""
        self.MsgSn = ""
        self.FromQQ = ""
        self.GetMessageBot = bot
        self.From = ""
        self.Type = 0
        self.Msg = Msg
        if Event in [1]:
            self.FromQQ = getFrom
        elif Event in [2,3,4,5,6]:
            self.From = getFrom

    def addToBoard(self):
        var.MessageBoard.append(self)

# 发送消息方法 需要传入消息类型 发送到的账号(QQ号或群号) 消息内容 Bot为用于发送的机器人，不填则默认config
def sendMessage(SendType, SendTo, Msg, Bot= config.defaultBot):
    if SendType in [1]:
        return requests.get("http://"+config.PostIP+":"+config.PostPort+"/?robot="+Bot+"&type="+ str(SendType)+"&qq="+ SendTo +"&data=" + Msg)
    elif SendType in [2,3,4,5,6]:
        return requests.get("http://"+config.PostIP+":"+config.PostPort+"/?robot="+Bot+"&type="+ str(SendType)+"&guid="+ SendTo +"&data=" + Msg)

def main():
    testmsg='{"MsgId":"207910","MsgSn":"1856224566","FromQQ":"1145141919180","Event":2,"Robot":"987654321","From":"123456789","Type":0,"To":"11223345","Msg":"测试消息"}'
    Message(testmsg).reply("asdasd")
    newfake = FakeMessage("987645986",1,"伪造测试消息","123456789")
    newfake.addToBoard()
    newfake.reply("dkuyashgdiloasuy")
    for i in var.MessageBoard:
        print(i.Msg)

if __name__ == "__main__":
    main()