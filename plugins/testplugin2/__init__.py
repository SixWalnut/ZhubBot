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
import log
import message as Messages

def OnEnable():
    print("Enable! test2!")

def OnLoad():
    print("Load! test2!")

def GetMsg(Message):
    log.info("插件2获取到消息:{}".format(Message.Msg),"Plugin")

def CommandRegister():
    return ["test2"]

def CommandExecuter(command,args):
    print("这是附带的参数！{}".format(args))

def Exit():
    print("Exited! test2")
