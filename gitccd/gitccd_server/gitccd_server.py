#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: server_ftp.py
# Author: 陈昌栋
# Mail: ccdaccd@163.com
# Created Time: Sat 16 Jan 2016 05:15:23 PM CST
#########################################################################
import SocketServer
from handlers import *
class MyTCPHandler(SocketServer.BaseRequestHandler):
    """
    SocketServer处理方法类定义，handler函数中定义了处理方法。
    """
    def handle(self):
        while True:
            self.data = self.request.recv(1024).strip()
            print "{} wrote:".format(self.client_address[0]) #, self.numbers
            if not self.data:
                print "客户端%s已断开！" % self.client_address[0]
                break
            user_input = self.data.split()
            handler = GitccdServerOperate()
            handler.gitccd(user_input[0], self.request, self.data)


if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
