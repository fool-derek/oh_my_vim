#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: handlers.py
# Author: 陈昌栋
# Mail: ccdaccd@163.com
# Created Time: Sun 17 Jan 2016 06:38:24 PM CST
#########################################################################
import commands
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
        self.callback('gitccd_', name, *args)

class GitccdOperate(Handler):
    """
    用于Gitccd的具体操作处理
    """
    def __init__(self):
        pass

    def gitccd_default(self, sock, cmd):
        sock.sendall(cmd)
        print sock.recv(1024)

    def gitccd_clone(self, sock, cmd):
        #  print "clone操作已经被触发！"
        for filename in cmd.split()[1:]:
            getfile_cmd = cmd.split()[0] + ' ' + filename
            sock.sendall(getfile_cmd)
            print "开始下载文件" + filename
            with open(filename,'wb') as f:
                while True:
                    data = sock.recv(1024)
                    if data == 'FileTransferDone':
                        break
                    if data == 'IOError':
                        print '%s这个文件不存在或者文件读写错误!' % filename
                        f.close()
                        file_remove = 'rm -rf ' + cmd.split()[1]
                        commands.getstatusoutput(file_remove)
                        break
                    f.write(data)
                    print '下载文件中...'
                f.close()
