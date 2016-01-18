#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: connect_server.py
# Author: 陈昌栋
# Mail: ccdaccd@163.com
# Created Time: Mon 18 Jan 2016 10:13:39 AM CST
#########################################################################
import socket

class SocketConnect:
    """
    与远程主机建立Socket连接.
    """
    def __init__(self, host = 'localhost', port = 9999):
        self.host = host
        self.port = port
        self.__Socket()
        self.__Connect()

    def __Socket(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def __Connect(self):
        self.s.connect((self.host, self.port))

    def GetSocket(self):
        return self.s
