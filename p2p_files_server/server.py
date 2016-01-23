#!/usr/bin/env python
# -*- coding: utf-8 -*-
#########################################################################
# File Name: server.py
# Author: 陈昌栋
# Mail: ccdaccd@163.com
# Created Time: Thu 21 Jan 2016 12:21:36 PM CST
#########################################################################
from xmlrpclib import ServerProxy, Fault
from os.path import join, abspath, isfile
from SimpleXMLRPCServer import SimpleXMLRPCServer
from urlparse import urlparse
from os import listdir
import sys

SimpleXMLRPCServer.allow_reuse_address = 1

MAX_HISTORY_LENGTH = 6

UNHANDLED = 100
ACCESS_DENIED = 200
FINISH_LIST_FILES = 300

class UnhandledQuery(Fault):
    """
    表示无法处理的查询的异常。
    """
    def __init__(self, message = "Couldn't handle the query"):
        Fault.__init__(self, UNHANDLED, message)

class FinishListFiles(Fault):
    """
    表示当前主机文件已经查询完成的查询的标志。
    """
    def __init__(self, message = "Finish list all access files!"):
        Fault.__init__(self, FINISH_LIST_FILES, message)

class AccessDenied(Fault):
    """
    在用户试图访问未被授权访问的资源时引发的异常。
    """
    def __init__(self, message = "Access denied"):
        Fault.__init__(self, ACCESS_DENIED, message)

def inside(dir, name):
    """
    检查给定的目录中是否有给定的文件名。
    """
    dir = abspath(dir)
    name = abspath(name)
    return name.startswith(join(dir, ''))
def getPort(url):
    """
    从URL中提取端口号。
    """
    name = urlparse(url)[1]
    parts = name.split(':')
    return int(parts[-1])

class Node:
    """
    P2P网络中的节点。
    """
    def __init__(self, url, dirname, secret):
        self.url = url
        self.dirname = dirname
        self.secret = secret
        self.konwn = set()
    def query(self, query, history = []):
        """
        查询文件，可能会向其他已知节点请求帮助。将文件作为字符串返回。
        """
        try:
            return self._query_handle(query)
        except UnhandledQuery:
            history = history + [self.url]
            if len(history) >= MAX_HISTORY_LENGTH:raise
            return self._query_broadcast(query, history)

    def listfiles(self, file_list_list = [], history = []):
        """
        列出可以查询的文件，可能会向其他已知节点请求帮助。
        """
        try:
            file_list_list = file_list_list + self._list_handle()
            raise FinishListFiles
        except FinishListFiles:
            history = history + [self.url]
            if len(history) >= MAX_HISTORY_LENGTH:
                return [file_list_list, history]
            #  print file_list_list
            return self._list_broadcast(file_list_list, history)

    def hello(self, other):
        """
        用于将节点介绍给其他节点。
        """
        self.konwn.add(other)
        #  print self.konwn
        return 0

    def fetch(self, query, secret):
        """
        用于让节点找到文件并且下载。
        """
        if secret != self.secret:
            raise AccessDenied
        result = self.query(query)
        f = open(join(self.dirname, query), 'w')
        f.write(result)
        f.close()
        return 0

    def list_file(self, secret):
        """
        用于让节点找到文件并且下载。
        """
        if secret != self.secret:
            raise AccessDenied
        all_files_data= self.listfiles()
        #  print all_files_data
        for file_name in all_files_data[0]:
            print file_name
        return 0

    def _start(self):
        """
        内部使用,以启动XML_RPC服务器。
        """

        s = SimpleXMLRPCServer(("", getPort(self.url)), logRequests = False)
        s.register_instance(self)
        s.serve_forever()

    def _query_handle(self, query):
        """
        内部使用,用于处理请求。
        """
        dir = self.dirname
        name = join(dir, query)
        if not isfile(name):
            raise UnhandledQuery
        if not inside(dir, name):
            raise AccessDenied
        return open(name).read()

    def _query_broadcast(self, query, history):
        """
        内部使用，用于将查询广播到所有已知节点。
        """
        for other in self.konwn.copy():
            if other in history:
                continue
            try:
                s = ServerProxy(other)
                return s.query(query, history)
            except Fault, f:
                if f.faultCode == UNHANDLED:
                    pass
                else:
                    self.konwn.remove(other)
            except:
                self.konwn.remove()
        raise UnhandledQuery

    def _list_handle(self):
        """
        内部使用,用于处理列出本地文件请求。
        """
        files = listdir(self.dirname)
        if files:
            files_list = ['-----------' + self.url + '-----------'] + files
            #  print '_list_handle runing...'
            return files_list
        else:
            return None

    def _list_broadcast(self, file_list_list, history):
        """
        内部使用，用于将列出文件广播到所有已知节点。
        """
        for other in self.konwn.copy():
            if other in history:
                continue
            try:
                s = ServerProxy(other)
                returned_files_data = s.listfiles(file_list_list, history)
                file_list_list = returned_files_data[0]
                history = returned_files_data[1]
                #  print history
            except Fault, f:
                if f.faultCode == FINISH_LIST_FILES:
                    pass
                else:
                    self.konwn.remove(other)
            except:
                self.konwn.remove()
        return [file_list_list, history]
def main():
    url, directory, secret = sys.argv[1:]
    n = Node(url, directory, secret)
    n._start()
if __name__ == '__main__':
    main()
