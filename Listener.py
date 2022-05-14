#!/usr/bin/env python 3.10.2
# -*-coding:utf-8 -*-
#创建日期: 2022/05/07 23:11:47 
#创建者: SixWalnut
#文件描述: 端口监听模块

#准备好后可以导入模块了
#self lib
import config
import log
import message
import var
#package lib
#none
#sys lib
import socket
import requests
import json
import threading
import multiprocessing

# 消息初步处理器 被处理好的消息会被转换为消息对象
def client(new_socket):
    request=  new_socket.recv(1024) 
    response  = "HTTP/1.1 200 OK\r\n"           #创建头
    response  += "\r\n"                         #创建分隔行
    response  += "{\"Code\":0}"                 #创建返回
    new_socket.send(response.encode("utf-8"))   #将返回编码为utf-8格式并发送
    new_socket.close()                          #关闭链接字
    request = str(request,'utf-8')              #处理请求：转换变量为字符串
    body_locate = request.rfind("\r\n\r\n")     #寻找分割行位置
    body = request[(body_locate+4):]            #获取body信息
    body.replace("\\","")
    msg_locate = body.find("\"Msg\":\"")        #定位消息位置
    if msg_locate != -1:                        #处理非法字符
        json_end = body[-2:]                    #获取末尾内容
        json_head_locate = msg_locate + 7       #定位原始消息
        json_head =body[:json_head_locate]      #头部内容
        Msg_orig =body[json_head_locate:-2]     #获取原始消息
        Msg = Msg_orig.replace('"','\"')        #处理非法字符
        body = json_head + Msg + json_end       #拼接处理后的内容
    if body == "":
        exit(0)
    log.info(body,"GetMessage")         #输出日志内容
    msg = message.Message(body)         #转换为消息对象

def server():
    #创建套接字
    tcp_server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #绑定套接字
    tcp_server_socket.bind(("", config.ListenPort))
    #监听端口
    tcp_server_socket.listen(128)
    while(True):
        if var.exitFlag == True:
            log.info("正在关闭服务器...")
            exit(0)
        new_socket, client_addr = tcp_server_socket.accept()
        #创建一个新服务进程，传入复制链接参数传入子进程
        clientThread = threading.Thread(target=client, args=(new_socket,))
        #开始进程
        clientThread.start()
        #关闭父进程链接