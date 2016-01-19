#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: server_ftp.py
# Author: 陈昌栋
# Mail: ccdaccd@163.com
# Created Time: Sat 16 Jan 2016 05:15:23 PM CST
#########################################################################
import SocketServer,commands
import time

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
            if user_input[0] == 'clone':
                print '开始传输文件...'
                try:
                    with open(user_input[1],'rb') as f:
                        self.request.sendall(f.read())
                    time.sleep(0.5)
                    self.request.send('FileTransferDone')
                    continue
                except IOError:
                    self.request.sendall('IOError')
                    continue
            elif user_input[0] == 'push':
                print '开始接收文件...'
                with open(user_input[1],'wb') as f:
                    while True:
                        data = self.request.recv(1024)
                        if data == 'FileTransferDone':
                            break
                        elif data == 'IOError':
                            print '%s试图上传一个文件失败!' % self.client_address[0]
                            f.close()
                            file_remove = 'rm -rf ' + user_input[1]
                            commands.getstatusoutput(file_remove)
                            break
                        f.write(data)
                        print '接收文件中...'
                    f.close()
                continue
            cmd_status, cmd_result = commands.getstatusoutput(self.data)
            if len(cmd_result.strip()) != 0:
                if cmd_status != 0:
                    cmd_result = "这个命令不存在！"
                self.request.sendall(cmd_result)
            else:
                self.request.sendall('Done')
if __name__ == "__main__":
    HOST, PORT = "localhost", 9999

    # Create the server, binding to localhost on port 9999
    server = SocketServer.TCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
