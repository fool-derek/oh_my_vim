#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: handlers.py
# Author: 陈昌栋
# Mail: ccdaccd@163.com
# Created Time: Mon 18 Jan 2016 04:15:43 PM CST
#########################################################################
import commands
import time
class Handler:
    """
    处理从Parser调用的方法的对象。
    """
    def callback(self, prefix, name, *args):
        method = getattr(self, prefix + name, None)
        #  print method
        if callable(method):
            return method(*args)
        else:
            method = getattr(self, prefix + 'default', None)
            return method(*args)
    def gitccd(self, name, *args):
        self.callback('gitccd_server_', name, *args)

class GitccdServerOperate(Handler):
    """
    用于Gitccd的具体操作处理
    """
    def __init__(self):
        pass

    def gitccd_server_default(self, sock, cmd):
        cmd_status, cmd_result = commands.getstatusoutput(cmd)
        if len(cmd_result.strip()) != 0:
            if cmd_status != 0:
                cmd_result = "这个命令不存在！"
            sock.sendall(cmd_result)
        else:
            sock.sendall('Done')

    def gitccd_server_clone(self, sock, cmd):
        print '开始传输文件...'
        user_input = cmd.split()
        try:
            with open(user_input[1],'rb') as f:
                sock.sendall(f.read())
            time.sleep(0.5)
            sock.send('FileTransferDone')
            f.close()
        except IOError:
            sock.sendall('IOError')

    def gitccd_server_push(self, sock, cmd):
        print '开始接收文件...'
        user_input = cmd.split()
        with open(user_input[1],'wb') as f:
            while True:
                data = sock.recv(1024)
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
