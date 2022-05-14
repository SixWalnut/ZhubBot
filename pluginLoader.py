#!/usr/bin/env python 3.10.2
# -*-coding:utf-8 -*-
#创建日期: 2022/05/13 21:39:50 
#创建者: SixWalnut
#文件描述: 插件加载文件

#准备好后可以导入模块了
#self lib
import log
import message
import var
#package lib

#sys lib
import sys
import os
sys.path.append("./plugins")
PluginList=[]

# 检索plugins文件夹，获取其中所有文件夹名
def ScanPluginList():
    PluginNameList = []
    for parent,PluginNameList,filenames in os.walk("./plugins"):
        break
    log.info("找到{}个加载项".format(len(PluginNameList)),"Plugin")
    return PluginNameList

# 将传入的文件夹名列表视为模块并导入他们 随后将它们放入插件列表
def PluginLoad(PluginNameList):
    for PluginName in PluginNameList:
        log.info("正在加载{}...".format(PluginName),"Plugin")
        # 捕获导入错误
        try:
            Plugin = __import__(PluginName)
            Plugin.OnLoad()
            PluginList.append(Plugin)
        except:
            log.error("载入插件{}失败！".format(PluginName),"Plugin")
    log.info("已加载{}个加载项".format(len(PluginList)),"Plugin")
    
# 初始化插件列表中的所有插件
def PluginInit():
    for Plugin in PluginList:
        try:
            Plugin.OnEnable()
        except:
            log.error("插件{}启用失败！".format(Plugin.__name__),"Plugin")

# 向所有插件推送消息
def MessagePush(Message):
    for Plugin in PluginList:
        Plugin.GetMsg(Message)

# 停用所有插件
def PluginExit():
    for Plugin in PluginList:
        Plugin.Exit()

# 为插件注册命令
def PluginCommandRegister():
    for Plugin in PluginList:
        #尝试为每一个插件注册命令
        try:
            PluginCommandList = Plugin.CommandRegister()
        except:
            log.error("为{}注册命令时发生错误,可能是由于它没有正确配置__init__.py中的CommandRegister函数".format(Plugin.__name__),"Plugin")
        else:
            # 查看返回是否是空结果
            if PluginCommandList == []:
                continue
            # 检查返回是否合法
            elif str(type(PluginCommandList)) !="<class 'list'>":
                log.error("为{}注册命令时发生错误,原因是__init__.py中的CommandRegister函数返回值不是一个列表".format(Plugin.__name__),"Plugin")
            else:
                #为列表里的每个命令注册这个插件
                for command in PluginCommandList:
                    # 检查这条命令是否合法 不合法则跳过
                    if " " in command:
                        log.error("为{}注册命令时发生错误,原因是尝试注册了一个包含空格的命令{}".format(Plugin.__name__,command),"Plugin")
                        continue
                    # 检查这命令是否已经存在
                    try:
                        var.PluginCommandList[command]
                    # 不存在时赋值
                    except:
                        var.PluginCommandList[command] = [Plugin]
                        log.info("已为{}注册了一个命令{}".format(Plugin.__name__,command),"Plugin")
                    # 存在时添加到末尾
                    else:
                        var.PluginCommandList[command].append(Plugin)
                        log.info("已为{}注册了一个命令{},该命令已被其他插件注册过,使用时将会分别执行".format(Plugin.__name__,command),"Plugin")

# 传入命令信息
def PluginCommandExecuter(commandWithArgs):
    # 寻找命令参数起点
    commandLocate = commandWithArgs.find(" ")
    # 截取一级命令
    if commandLocate == -1:
        command = commandWithArgs
    else:
        command = commandWithArgs[:commandLocate]
    # 获取命令参数
    args = commandWithArgs[commandLocate+1:].split(" ") if commandLocate != -1 else None
    # 检查命令是否已注册
    try:
        var.PluginCommandList[command]
    except:
        return False
    else:
        for Plugin in var.PluginCommandList[command]:
            Plugin.CommandExecuter(command,args)
        return True

# 插件初始化过程封装
def LoadPluginInit():
    PluginNameList = ScanPluginList()
    PluginLoad(PluginNameList)
    PluginInit()

# 测试函数
def main():
    PluginNameList = ScanPluginList()
    PluginLoad(PluginNameList)
    PluginInit()
    MessagePush(message.FakeMessage("987645986",1,"伪造测试消息","123456789"))
    PluginExit()

if __name__ == "__main__":
    main()