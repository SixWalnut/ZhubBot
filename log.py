#!/usr/bin/env python 3.10.2
# -*-coding:utf-8 -*-
#创建日期: 2022/05/07 22:37:34 
#创建者: SixWalnut
#文件描述: 日志记录模块

#准备好后可以导入模块了
#self lib
#none
#package lib
#none
#sys lib
import time
import os

# 路径检查 如果不存在日志路径则创建
def checkFile():
    try:
        date = time.strftime("%Y-%m-%d",time.localtime())
        open("./Logging/"+date+".log","a+").close()
    except:
        os.makedirs("./Logging")
        warn("日志文件夹不存在！正在创建...")

# 定义info类型的日志
def info(text,event="Base"):
    # 检查路径
    checkFile()
    # 转化传入参数为字符串型
    text = str(text)
    # 获取指定格式时间
    date = time.strftime("%Y-%m-%d",time.localtime())
    # 开启日志文件
    logfile = open("./Logging/"+date+".log","a+")
    # 拼接日志内容
    text = time.strftime("[%H:%M:%S]",time.localtime()) + "[INFO]" + "[" +event + "]" + text +"\n"
    # 输出到控制台
    print(text,end="")
    # 尝试写入
    try:
        logfile.write(text)
    except Exception as err:
        #写入错误 关闭日志文件
        logfile.close()
        return err
    # 否则关闭日志文件
    else:
        logfile.close()
        return True

# 定义warn类型的日志 如info类似
def warn(text,event="Base"):
    checkFile()
    text = str(text)
    date = time.strftime("%Y-%m-%d",time.localtime())
    logfile = open("./Logging/"+date+".log","a+")
    text = time.strftime("[%H:%M:%S]",time.localtime()) + "[-WARN-]" + "[" +event + "]" + text +"\n"
    print(text,end="")
    try:
        logfile.write(text)
    except Exception as err:
        logfile.close()
        return err
    else:
        logfile.close()
        return True

# 定义error类型的日志 如info类似
def error(text,event="Base"):
    checkFile()
    text = str(text)
    date = time.strftime("%Y-%m-%d",time.localtime())
    logfile = open("./Logging/"+date+".log","a+")
    text = time.strftime("[%H:%M:%S]",time.localtime()) + "------------[{}ERROR]------------\n".format(event) + text  +"\n"
    print(text,end="")
    try:
        logfile.write(text)
    except Exception as err:
        logfile.close()
        return err
    else:
        logfile.close()
        return True

def main():
    info("这是一条INFO消息!")
    warn("这是一条WARN消息!")
    error("这是一条ERROR消息！不！")

if __name__ == "__main__":
    main()