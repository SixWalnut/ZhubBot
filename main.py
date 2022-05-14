#!/usr/bin/env python 3.10.2
# -*-coding:utf-8 -*-
#创建日期: 2022/05/13 22:00:58 
#创建者: SixWalnut
#文件描述: 项目主进程

#准备好后可以导入模块了
#self lib
import log
import config
import Listener
import pluginLoader
import var
import message
import premission
#package lib

#sys lib
import copy
import threading
import time
import requests

# 消息广播器，向所有插件广播消息板上的消息
def messagePusher():
    while(True):
        if var.exitFlag == True:
            log.info("正在关闭消息推送器...")
            exit(0)
        if var.MessageBoard != []:
            # 设置临时消息板 当临时消息板上的消息广播完后 去掉消息板的上已经被广播的消息以保证线程安全
            tempMessageboard = copy.deepcopy(var.MessageBoard)
            for message in tempMessageboard:
                pluginLoader.MessagePush(message)
            var.MessageBoard = var.MessageBoard[len(tempMessageboard):]

# 命令执行器
def commandExecuter():
    while(True):
        # 获取输入命令
        command = input("")
        
        # 命令stop
        if command == "stop":
            # 设置全局退出标志
            var.exitFlag = True
            # 向消息接收服务器发出停止指令
            requests.get("http://"+"127.0.0.1"+":"+str(config.ListenPort)+"/")
            # 执行插件退出
            log.info("停用插件","Plugin")
            pluginLoader.PluginExit()
            # 本进程退出
            exit(0)
        
        # 命令list
        elif command == "list":
            for msg in var.MessageBoard:
                print(msg.Msg)
        
        else:
            if pluginLoader.PluginCommandExecuter(command) == False:
                print("未知指令")

def main():
    startTime = time.time()
    # 记录日志
    log.info("启动中...")
    log.info("加载配置文件")
    log.info("推送地址:{},推送端口:{},默认机器人:{},需要监听的端口:{}".format(config.PostIP,config.PostPort,config.defaultBot,config.ListenPort))

    # 加载用户权限
    log.info("加载用户权限...")
    premission.PremessionFileLoad()
    premission.PremessionFileUpLoad()

    # 加载插件
    log.info("加载插件...")
    pluginLoader.LoadPluginInit()

    # 注册命令
    log.info("注册命令中...")
    pluginLoader.PluginCommandRegister()

    # 启动消息接收服务器线程
    log.info("启动服务器...")
    serverThread = threading.Thread(target=Listener.server)
    serverThread.start()

    # 启动消息广播线程
    log.info("启动消息推送器...")
    pushThread = threading.Thread(target=messagePusher)
    pushThread.start()

    # 启动命令处理器线程 并作为主线程
    log.info("加载命令处理器")
    commandThread = threading.Thread(target=commandExecuter)
    log.info("加载完成!耗时{:.2f}s".format(time.time()-startTime))
    commandThread.start()
    commandThread.join()

if __name__ == "__main__":
    main()