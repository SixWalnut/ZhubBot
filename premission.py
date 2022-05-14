#!/usr/bin/env python 3.10.2
# -*-coding:utf-8 -*-
#创建日期: 2022/05/14 14:29:47 
#创建者: SixWalnut
#文件描述: 权限操纵文件 会主动修改premission.json文件

#准备好后可以导入模块了
#self lib
import config
import var
import log
#package lib

#sys lib
import json

# 权限文件加载
def PremessionFileLoad():
    file = open("premission.json","w+")
    text = file.read()
    file.close()
    if text != "":
        var.Premession = json.loads(text)
    else:
        var.Premession[config.master] = 100

# 从内存更新到权限文件
def PremessionFileUpLoad():
    file = open("premission.json","w+")
    file.truncate(0)
    file.write(json.dumps(var.Premession))
    file.close()

# 设置SetQQ的权限，如果设置者User的权限等级小于SetQQ或者设置的等级SetLevel大于等于设置者则设置会失败
def SetPremession(SetQQ,SetLevel,User="Base"):
    if User == "Base":
        var.Premession[SetQQ] = SetLevel
        log.info("{}的权限已被设置为{}级".format(SetQQ,SetLevel),"Premission")
        # 在设置权限后更新文件
        PremessionFileUpLoad()
    else:
        try:
            var.Premession[SetQQ]
        except:
            var.Premession[SetQQ] = 1
        try:
            var.Premession[User]
        except:
            var.Premession[User] = 1
        try:
            if SetLevel >= var.Premession[User] or var.Premession[User] <= var.Premession[SetQQ]:
                log.warn("{}的权限不足，设置失败".format(User),"Premission")
                return False
            else:
                var.Premession[SetQQ] = SetLevel
                log.info("{}的权限已被设置为{}级,操作者{}的权限等级为{}".format(SetQQ,SetLevel,User,Premission[User]),"Premission")
                PremessionFileUpLoad()
                return True
        except:
            log.warn("{}的权限不足，设置失败".format(User),"Premission")

# 获取该QQ的权限等级
def GetPremission(QQ):
    return var.Premession[QQ]

# 比较两个账号的权限等级 返回权限等级高的账号，相等则返回"Same"
def ComparePremission(QQ1,QQ2):
    if var.Premession[QQ1] > var.Premession[QQ2]:
        return QQ1
    elif var.Premession[QQ1] < var.Premession[QQ2]:
        return QQ2
    elif var.Premession[QQ1] == var.Premession[QQ2]:
        return "Same"

if __name__ == "__main__":
    PremessionFileLoad()
    PremessionFileUpLoad()
    SetPremession("4684136847",10)
    SetPremession("4684136847",100,"47")
    SetPremession("4684136847",99,"52894798")
    PremessionFileUpLoad()