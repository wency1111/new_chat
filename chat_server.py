"""
socket fork 练习
群聊聊天室
功能 ： 类似qq群功能
【1】 有人进入聊天室需要输入姓名，姓名不能重复
【2】 有人进入聊天室时，其他人会收到通知：xxx 进入了聊天室
【3】 一个人发消息，其他人会收到：xxx ： xxxxxxxxxxx
【4】 有人退出聊天室，则其他人也会收到通知:xxx退出了聊天室
【5】 扩展功能：服务器可以向所有用户发送公告:管理员消息： xxxxxxxxx
"""
"""
1.技术点的确认
    *转发模型：客户端－－》服务端－－》转发给其他客户端
    *网络模型：UDP通信
    *保存用户信息 [(name,addr),(...)]  {name:addr}
    *收发关系处理：采用多进程分别进行收发操作
2.结构设计
    *采用什么样的封装结构：函数
    *编写一个功能，测试一个功能
    *注意注释和结构的设计
3.分析功能模块，制定具体编写流程
    *搭建网络连接
    *进入聊天室
        客户端：*输入姓名
               *将姓名发送给服务器
               *接收返回的结果
               *如果不允许则重复输入姓名
        
        服务端：*接受姓名
               *判断姓名是否存在
               *将结果给客户端
               *如果允许进入聊天室增加用户信息
               *通知其他用户
    *聊天
        客户端：*创建新的进程
               *一个进程循环发送消息
               *一个进程循环接收消息
        服务端：*接收请求，判断请求类型
               *将消息转发给其他用户
    
    *退出聊天室
        客户端：*输入quit或者ctrl+c退出
               *将请求发送给服务端
               *结束进程
               *接收端接收EXIT退出进程
        客户端：*接收消息
               *将退出消息告诉其他人
               *
               *
    
    *管理员消息
4.协议
    *如果允许进入聊天室，服务端发送OK给客户端
    *如果不允许进入聊天室，服务端发送 不允许原因
    *请求类别：
        L-->进入聊天室
        C-->聊天信息
        Q-->退出聊天室
    *用户存储结构：{name:addr...}
    
作业：1.整理客户端收发消息的显示情况
     2.回顾思路
"""
from socket import *
import os,sys

#服务器地址
ADDR=("0.0.0.0",8888)
#存储用户信息
user = {}
def do_login(s,name,addr):
    if name in user or "管理员" in name:
        s.sendto("该用户已存在".encode(),addr)
        return

    s.sendto(b'OK',addr)
    #通知其他人
    msg="欢迎%s进入聊天室"%name
    for i in user:
        s.sendto(msg.encode(),user[i])
    #将用户加入
    user[name]=addr

#聊天
def do_chat(s,name,text):
    msg="%s : %s"%(name,text)
    for i in user:
        if i !=name:
            s.sendto(msg.encode(),user[i])

#退出程序
def do_quit(s,name):
    msg="%s退出了聊天室"%name
    for i in user:
        if i !=name:
            s.sendto(msg.encode(),user[i])
        else:
            s.sendto(b'EXIT',user[i])
    #将用户删除
    del user[name]

#接受各种客户端请求
def do_request(s):
    while True:
        data,addr=s.recvfrom(1024)
        msg=data.decode().split(" ")
        #区分请求类型
        if msg[0]=="L":
            do_login(s,msg[1],addr)
            print(data.decode())
        elif msg[0]=="C":
            text=" ".join(msg[2:])
            do_chat(s,msg[1],text)
            print("%s : %s"%(msg[1],text))

        elif msg[0]=="Q":
            do_quit(s,msg[1])

#创建网络连接
def main():
    #套接字
    s=socket(AF_INET,SOCK_DGRAM)
    s.bind(ADDR)

    pid=os.fork()
    if pid<0:
        return
    #发送管理员消息
    elif pid==0:
        while True:
            msg=input("管理员消息：")
            msg="C 管理员消息"+msg
            s.sendto(msg.encode(),ADDR)
    else:
        #请求处理
        do_request(s)#处理客户端请求


if __name__=="__main__":
    main()












