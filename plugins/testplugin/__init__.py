#!/usr/bin/env python 3.10.2
# -*-coding:utf-8 -*-
#创建日期: 2022/05/13 22:10:28 
#创建者: SixWalnut
#文件描述: 测试插件描述文件

#准备好后可以导入模块了
#self lib

#package lib

#sys lib
import sys
sys.path.append("../..")
import message as Messages
import log

def OnEnable():
    print("Enable! test1!")

def OnLoad():
    #Messages.sendMessage(1,"1632556087","aaaa")
    print("Load! test1!")

def GetMsg(Message):
    log.info("插件1获取到消息:{}".format(Message.Msg),"Plugin")

def CommandRegister():
    return ["test1"]

def CommandExecuter(command,args):
    print("这里不带参数！")

def Exit():
    print("Exited! test1")
