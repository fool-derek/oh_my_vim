#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: cl_ftp.py
# Author: 陈昌栋
# Mail: ccdaccd@163.com
# Created Time: Sat 16 Jan 2016 05:34:02 PM CST
#########################################################################
import socket
import commands
import readline
import time

HOST = 'localhost' #远程端主机IP地址
PORT = 9999

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((HOST, PORT))
while True:
    cmd = raw_input("请输入你的命令:").strip()
    if len(cmd) == 0:
        continue
    if cmd.split()[0] == 'get':
        #  print cmd.split()[1:]
        for filename in cmd.split()[1:]:
            getfile_cmd = cmd.split()[0] + ' ' + filename
            s.sendall(getfile_cmd)
            print "开始下载文件..."
            with open(filename,'wb') as f:
                while True:
                    data = s.recv(1024)
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
            continue
    elif cmd.split()[0] == 'push':
        for filename in cmd.split()[1:]:
            getfile_cmd = cmd.split()[0] + ' ' + filename
            s.sendall(getfile_cmd)
            print "开始上传文件..."
            try:
                with open(filename,'rb') as f:
                    s.sendall(f.read())
                time.sleep(0.5)
                s.send('FileTransferDone')
                continue
            except IOError:
                s.sendall('IOError')
                print '%s这个文件不存在或者文件读写错误!' % filename
                continue
    else:
        s.sendall(cmd)
        print s.recv(1024)
s.close()
