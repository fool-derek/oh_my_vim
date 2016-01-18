#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: gitccd.py
# Author: 陈昌栋
# Mail: ccdaccd@163.com
# Created Time: Sun 17 Jan 2016 07:01:45 PM CST
#########################################################################
from handlers import *
from connect_server import *
import readline

class Parser:
    """
    Gitccd版本控制处理程序基类。
    """
    def __init__(self, handler, sock):
        self.handler = handler
        self.sock = sock

    def parse(self):
        """
        具体操作执行器。
        """
        while True:
            cmd = raw_input("请输入你的命令:").strip()
            if len(cmd) == 0:
                continue
            self.handler.gitccd(cmd.split()[0], self.sock, cmd)

class BasicGitccdParser(Parser):
    """
    Gitccd版本控制处理程序子类。
    """
    def __init__(self, handler, sock):
        Parser.__init__(self, handler, sock)

if __name__ == "__main__":
    sock_connect = SocketConnect()
    sock = sock_connect.GetSocket()
    handler = GitccdOperate()
    parser = BasicGitccdParser(handler, sock)
    parser.parse() #Gitccd版本控制处理程序执行处理程序器
