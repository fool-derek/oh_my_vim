#!/usr/bin/env python
#-*- encoding: utf-8 -*-
"""
local area network chatting program
"""

import os
import wx
import socket
import threading
#import SocketServer 
#import time

FILE_PORT = 7777
BROADCAST_PORT = 8888
CHAT_PORT = 9999

#get hostname and host ip address
hostname = socket.gethostname()
hostip = socket.gethostbyname(hostname)

#get local broadcast address
list = hostip.split('.')
list[-1] = '255'
broadcast = ".".join(list)

#broadcast = "255.255.255.255"

#print local information
print "host name: ", hostname
print "host ip address: ", hostip
print "broadcast address: ", broadcast

#directory usrdir used to store user information
userdir = {"lilong" : hostip, "NONE" : "192.168.1.1"}

#gui class
class MainWindow(wx.Frame):
    def __init__(self, parent, id, title):
        wx.Frame.__init__(self, parent, id, title, size = (800, 600))# , style=wx.SYSTEM_MENU|wx.MINIMIZE_BOX|wx.CLOSE_BOX|wx.CAPTION)
        #panel = wx.Panel(self, -1)
        self.SetBackgroundColour(wx.Color(255, 255, 255))
        self.chat = None
        self.msgList = []
        self.userList = []
        self.statusBar = self.CreateStatusBar()
        self.StatusBar.SetStatusText("Local area network chatting room")
        
        #listbox list all the local user     
        self.listBox = wx.ListBox(self, -1,  \
                             choices = userdir.keys(), style = wx.LB_DEFAULT)
        self.msgTextCtrl = wx.TextCtrl(self, -1,\
                                  style = wx.TE_MULTILINE | wx.TE_READONLY)
        self.editTextCtrl = wx.TextCtrl(self, -1,\
                                   style = wx.TE_MULTILINE | wx.TE_PROCESS_ENTER)
        
        self.nullLabel1 = wx.StaticText(self, -1)
        #self.nullLabel2 = wx.StaticText(self, -1)
        self.msgButton = wx.Button(self, -1, "No Message Received")
        self.sendButton = wx.Button(self, -1, "Send")
        self.closeButton = wx.Button(self, -1, "Close")
        self.fileButton = wx.Button(self, -1, "Send File")
        self.refreshButton = wx.Button(self, -1, "Refresh")
        self.recordButton = wx.Button(self, -1, "Records")
        
        #button layout
        hsizer2 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer2.Add(self.recordButton, proportion = 0, flag = wx.RIGHT)
        hsizer2.Add(self.fileButton, proportion = 0, flag = wx.RIGHT)
        #hsizer2.Add(self.nullLabel2, proportion = 1, flag = wx.RIGHT)
        #button layout
        hsizer1 = wx.BoxSizer(wx.HORIZONTAL)
        hsizer1.Add(self.nullLabel1, proportion = 1, flag = wx.EXPAND | wx.BOTTOM)
        hsizer1.Add(self.refreshButton, proportion = 0, flag = wx.EXPAND | wx.RIGHT | wx.BOTTOM)
        #hsizer.Add(self.recordButton, proportion = 0, flag = wx.RIGHT | wx.BOTTOM)
        hsizer1.Add(self.sendButton, proportion = 0, flag = wx.RIGHT | wx.BOTTOM)
        hsizer1.Add(self.closeButton, proportion = 0, flag = wx.RIGHT | wx.BOTTOM)
        
        #text control layout
        vsizer1 = wx.BoxSizer(wx.VERTICAL)
        vsizer1.Add(self.msgTextCtrl, 1, wx.EXPAND)
        vsizer1.Add(hsizer2, 0, wx.EXPAND)
        vsizer1.Add(self.editTextCtrl, 1, wx.EXPAND)
        vsizer1.Add(hsizer1, 0, wx.EXPAND)
        
        #list and button layout
        vsizer2 = wx.BoxSizer(wx.VERTICAL)
        vsizer2.Add(self.listBox, 1, wx.EXPAND)
        vsizer2.Add(self.msgButton, 0, wx.EXPAND)
        
        #all widgets layout
        sizer = wx.BoxSizer(wx.HORIZONTAL)
        sizer.Add(vsizer2, 1, wx.EXPAND)
        sizer.Add(vsizer1, 2, wx.EXPAND)
        
        #add layout
        self.SetSizer(sizer)
        self.SetAutoLayout(1)
        sizer.Fit(self)
        
        #bind
        self.Bind(wx.EVT_LISTBOX, self.OnListBox, self.listBox)
        self.Bind(wx.EVT_LISTBOX_DCLICK, self.DListBox, self.listBox)
        
        #button action
        self.Bind(wx.EVT_BUTTON, self.MsgRecvd, self.msgButton)
        self.Bind(wx.EVT_BUTTON, self.OnRefresh, self.refreshButton)
        self.Bind(wx.EVT_BUTTON, self.OnSend, self.sendButton)
        self.Bind(wx.EVT_BUTTON, self.OnClose, self.closeButton)
        self.Bind(wx.EVT_BUTTON, self.OnFile, self.fileButton)
        
        #text changed and save chatting records
        self.Bind(wx.EVT_TEXT, self.SaveRecord, self.msgTextCtrl)
        #press enter and send the message
        self.Bind(wx.EVT_TEXT_ENTER, self.OnSend, self.editTextCtrl)
        
        self.Show()
        
    #received message
    def MsgRecvd(self, event):
        if len(self.msgList):
            print "This is message received: ", self.msgList[0]
            if os.name == 'nt':
                self.msgList[0] = self.msgList[0].decode('gbk')
            elif os.name == 'posix':
                self.msgList[0] = self.msgList[0].decode('gb2312')
            else:
                print "unknown OS"
                pass
            self.msgTextCtrl.AppendText(self.msgList[0])
            del self.msgList[0]
        if len(self.userList):
            print type(self.userList[0])
            string = str(self.userList[0])
            print string
            id = self.listBox.FindString(string)
            print id
            self.listBox.Select(id)
            del self.userList[0]
        if not len(self.userList):
            self.msgButton.SetLabel("No Message Received")
        
    
    #send file
    def OnFile(self, event):
        sendfile = fileClient("sendFile")
        sendfile.setDaemon(True)
        sendfile.start()
        #time.sleep(1)
#        try:
#            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#            sock.connect((userdir[self.chat], FILE_PORT))
#            dirname = ''
#            filedlg = wx.FileDialog(self, "choose a file", dirname, "", "*.*", wx.OPEN)
#            if filedlg.ShowModal() == wx.ID_OK and filedlg.GetFilename():
#                print "hellO"
#                filename = filedlg.GetFilename()
#                dirname = filedlg.GetDirectory()
#                print "FILENAME:", filename
#                if filename:
#                    path = os.path.join(dirname, filename)
#                    sock.send(filename)
#                    ack = sock.recv(12)
#                    print ack
#                    filedes = open(path, "rb")
#                    while True:
#                        data = filedes.read(8192)
#                        #print data
#                        if not data:
#                            break
#                        while len(data) > 0:
#                            sent = sock.send(data)
#                            #print sent
#                            data = data[sent:]
#                        ack = sock.recv(12)
#                        if ack == "ACK":
#                            self.showMsg("the file send successfully")
##                            d = wx.MessageDialog(self, "The file send successfully", style = wx.OK)
##                            #create a message dialog
##                            d.ShowModal()   #show dialog
##                            d.Destroy()
#                        print ack
#        except socket.error:
#            d = wx.MessageDialog(self, "Create socket error", style = wx.OK)
#                            #create a message dialog
#            d.ShowModal()   #show dialog
#            d.Destroy()
#        finally:
#            sock.close()
    
    def SaveRecord(self, event):
        #write the chatting records to the local file
        print "MAIN WINDOW save"
    
    def OnListBox(self, event):
        user = event.GetString()
        #print "user = %s" % user
        #self.Title = "Double click chat to %s" % user 
        self.StatusBar.SetStatusText("Double click chat to %s" % user)
    
    #double click user name and chat to him/her
    def DListBox(self, event):
        user = event.GetString()
        self.chat = user
        self.Title = "Chat with %s" % user
        self.msgTextCtrl.SetValue("")
        self.editTextCtrl.SetValue("")
        
    #refresh user list
    def OnRefresh(self, event):
        pass
    
    #send message
    def OnSend(self, event):
        data = self.editTextCtrl.GetValue()
        if data:
            if self.chat:
                print "I am OnSend", data
                self.senddata = [hostname, hostip, data]
                self.ipaddr = (userdir[self.chat], CHAT_PORT)
                print "MAIN WINDOW OnSend"
                print type(self.ipaddr)
                print "MAIN WINDOW ", self.ipaddr
                #msgdata display in the msgTextCtrl widget
                import time
                now = time.localtime()
                hour, min, sec = (now.tm_hour, now.tm_min, now.tm_sec)
                if hour < 10:
                    hour = "0" + str(hour)
                if min < 10:
                    min = "0" + str(min)
                if sec < 10:
                    sec = "0" + str(sec)
                ltime = "%s:%s:%s" % (hour, min, sec)
                msgdata = socket.gethostname() + "  " + ltime + "\n\t" + data + "\n"
                self.editTextCtrl.SetValue("")
                self.msgTextCtrl.AppendText(msgdata)
                #senddata send to user
                #senddata = [hostname, hostip, data]
                print "MAIN WINDOW", userdir[self.chat]
                print "MAIN WINDOW", type(userdir[self.chat])
                print self.senddata
                sendMsg(self.senddata, self.ipaddr)
                print "MAIN WINDOW after send"
            else:
                d = wx.MessageDialog(self, "Please choose a user you want to chat with", style = wx.OK)
                        #create a message dialog
                d.ShowModal()   #show dialog
                d.Destroy()
    
    #send error
    def SendError(self, errdata):
        d = wx.MessageDialog(self, errdata, style = wx.OK)
                        #create a message dialog
        d.ShowModal()   #show dialog
        d.Destroy()
    
    #receive message
    def RecvMsg(self, user, data):
        #self.msgTextCtrl.AppendText("I am Lilong")
        print "MAIN WINDOW win.RecvMsg"
        print "MAIN WINDOW", data, user
        import time
        now = time.localtime()
        hour, min, sec = (now.tm_hour, now.tm_min, now.tm_sec)
        if hour < 10:
            hour = "0" + str(hour)
        if min < 10:
            min = "0" + str(min)
        if sec < 10:
            sec = "0" + str(sec)
        ltime = "%s:%s:%s" % (hour, min, sec)
        msgdata = user + "  " + ltime + "\n\t" + data + "\n"
        print "this is msgdata:", msgdata
        #print type(data)
        self.msgList.append(msgdata)
        self.userList.append(user)
#        self.msgButton.SetLabel("Message from %s") % self.userList[-1]
        #self.msgTextCtrl.SetValue(data)
#        print "MAIN WINDOW after setValue"
    
    #show message dialog
    def showMsg(self, data):
        dlg = wx.MessageDialog(self, data, style = wx.OK)
        dlg.ShowModal()
        dlg.Destroy()
    
    #close window
    def OnClose(self, event):
        recv.kill()
        server.kill()
        client.kill()
        self.Close(True)

class fileClient(threading.Thread):
    def __init__(self, threadName):
        threading.Thread.__init__(self, name = threadName)
    def run(self):
#        try:
#            fileSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#            fileSock.connect((userdir[win.chat], FILE_PORT))
#            
#        except socket.error:
#            pass
#        finally:
#            fileSock.close()
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((userdir[win.chat], FILE_PORT))
            dirname = ''
            filedlg = wx.FileDialog(win, "choose a file", dirname, "", "*.*", wx.OPEN)
            if filedlg.ShowModal() == wx.ID_OK and filedlg.GetFilename():
                #print "hello"
                filename = filedlg.GetFilename()
                dirname = filedlg.GetDirectory()
                print "IN fileClient FILENAME:", filename
                if filename:
                    path = os.path.join(dirname, filename)
                    sock.send(filename)
                    ack = sock.recv(12)
                    print "ACK from SERVER", ack
                    filedes = open(path, "rb")
                    pieces = 1
                    while True:
                        data = filedes.read(8192)
                        print "\nRead the %d piece" % pieces
                        pieces += 1
                        print "I AM IN FILECLIENT\n\n\n\n\n\n"
                        #print data
                        if not data:
                            break
                        while len(data) > 0:
                            sent = sock.send(data)
                            #print sent
                            data = data[sent:]
                    print "have exited from WHILE"
                    ack = sock.recv(12)
                    if ack == "ACK":
                        win.showMsg("the file send successfully")
#                            d = wx.MessageDialog(self, "The file send successfully", style = wx.OK)
#                            #create a message dialog
#                            d.ShowModal()   #show dialog
#                            d.Destroy()
                        print ack
        except socket.error:
            d = wx.MessageDialog(win, "Create socket error", style = wx.OK)
                            #create a message dialog
            d.ShowModal()   #show dialog
            d.Destroy()
        finally:
            sock.close()

#thread receive file 
class fileServer(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name = threadname)
    def run(self):
        print "file receive run"
        self.tcpsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.tcpsock.bind((hostip, FILE_PORT))
        self.tcpsock.listen(1)
        #receive file name
        while True:
            clientsock, clientaddr = self.tcpsock.accept()
            filename = clientsock.recv(1024)
            if filename:
#                d = wx.MessageDialog(win, "receive file", style = wx.OK)
#                        #create a message dialog
#                d.ShowModal()   #show dialog
#                d.Destroy()
                print "show Msg"
                win.showMsg("receive file")
                print "filename:", filename
                clientsock.send("ack")
                filedes = open(filename, "wb")
                print "open successfully"
                while True:
                    recvdata = clientsock.recv(8192)
                    print "RECVDATA \n\n\n%s" % recvdata
                    if not recvdata:
                        break
                    filedes.write(recvdata)
                    #print "write successfully"
                    if len(recvdata) < 8192:
                        break
                clientsock.send("ACK")
                filedes.flush
                filedes.close()

#thread recv the broadcast information
class broadServer(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name = threadname)
        self.flag = True
        self.addr = None
    def run(self):
        self.udpsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.udpsock.bind((hostip, BROADCAST_PORT))

        #receive information from local area network
        while self.flag:
            data, address = self.udpsock.recvfrom(1024)
            self.addr = address
            if not data:
                break
            key, value = data.split(':')
            #add new user to userdir
            if value == hostip:
                continue
            if key not in userdir.keys():
                userdir[key] = value
            print "BROAD SERVER", userdir
            data = hostname + ":" + hostip
            self.udpsock.sendto(data, address)
        self.udpsock.close()
        print "BROAD SERVER exit from broadServer"
    
    def kill(self):
        self.flag = False
        #threading.Thread.join(self, 0)
        print "exit from %s" % self.getName()
        self.udpsock.close()

#this thread broadcast its ip to local area network
#and receive others' ip
class broadClient(threading.Thread):
    def __init__(self, threadname):
        threading.Thread.__init__(self, name = threadname)
        self.flag = True
    def run(self):
        self.clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.clientsock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

        #local information send to the local area network
        data = hostname + ":" + hostip
        self.clientsock.sendto(data, (broadcast, BROADCAST_PORT))

        #receive messages the local area network returns
        while self.flag:
            newdata = self.clientsock.recvfrom(1024)
            print "BROAD CLIENT CONFIRM  ", newdata
            print newdata[0]
            
            key = newdata[0].split(":")[0]
            value = newdata[0].split(":")[1]
            userdir[key] = value
            print userdir
            
        self.clientsock.close()
        print "exit from while and broadClient"
    
    def kill(self):
        self.flag = False
        #threading.Thread.join(self, 0)
        print "exit from %s" % self.getName()
        self.clientsock.close()

#funtion send message to the given ip address
def sendMsg(data, ipaddr):
    clientsock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print "sendMsg"
    print "SEND MSG  ", data
    print "SEND MSG  ", ipaddr
    data = data[-1]
    print "I am data:", data
    print type(data)
    import os
    if os.name == 'nt':
        print "windows nt"
        data = data.encode('gbk')
    elif os.name == 'posix':
        print "posix OS"
        #unicode(data, 'gb2312')
        data = data.encode('gb2312')
    else:
        print "unkown operation system"
    print "sendMsg  " + data
    data = "%s" % data
    #data = str(data)
    print type(data)
    clientsock.sendto(data, ipaddr)
    #clientsock.sendto("I am lilong", (("202.114.95.110", CHAT_PORT)))
    
    #ack check whether the message send successfully or not
    try:
        ack = clientsock.recvfrom(16)
        if ack[0] != "ACK":
            print "The message \"%s\" haven't sent successfully" % data
        else:
            print "send successfully"
    except socket.error:
        errdata =  "The message \"%s\" haven't sent successfully" % data
        print errdata
        win.SendError(errdata)
    finally:
        clientsock.close()

#thread receive message
class recvMsg(threading.Thread):
    def __init__(self, threadName):
        self.flag = True
        threading.Thread.__init__(self, name = threadName)
        self.serversock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.serversock.bind((socket.gethostbyname(socket.gethostname()), CHAT_PORT))
        
    def run(self):
        #server socket bind to localhost:9999 and always receive messages
        while self.flag:
            recvdata, address= self.serversock.recvfrom(1024)
            #print userdir
            username = [name for name in userdir.keys() if userdir[name] == address[0]]
            #name = [name for name in userdir.keys() if userdir[name] == address]
            print "RECVDATA IS ", recvdata, address, username
            print type(recvdata)
            print "recvMsg receive message successfully"
            win.RecvMsg(username[-1], recvdata)
            print "Done"
            if recvdata:
                self.serversock.sendto("ACK", address)
            label = "Received Message From %s" % win.userList[0]
            win.msgButton.SetLabel(label)
    
    def kill(self):
        self.flag = False
        #threading.Thread.join(self, 0)
        print "exit from %s" % self.getName()
        self.serversock.close()

#-------------------------------------------------------------------
#the program starts here
import sys
print "ENCODING", sys.getdefaultencoding()
recv = recvMsg("receiveMessage")
recvfile = fileServer("recvFile")
server = broadServer("broadServer")
client = broadClient("broadClient")
#sendfile = fileClient("sendFile")

#set daemon and the son Thread exit after the main Thread exit
server.setDaemon(True)
recvfile.setDaemon(True)
client.setDaemon(True)
recv.setDaemon(True)
#sendfile.setDaemon(True)

#thread start
server.start()
recvfile.start()
client.start()
recv.start()
#sendfile.start()

#loop and the thread recv alsays alive
app = wx.PySimpleApp()
win = MainWindow(None, wx.ID_ANY, "chatting room")
#test
#win.msgTextCtrl.SetValue("I am Lilong")
app.MainLoop()

print "window exit"
print "all exit"
