# coding: gbk
# must run in CMD, pycharm has a bug when input interrupted
import socket, threading, sys
client=socket.socket()
client.connect(('freechess.org',5000))
running=True
def blockData(chan):
    '''
    :param socket._socketobject chan:
    :return:
    '''
    global running
    while True:
        data=chan.recv(1)
        if data:
            sys.stdout.write(data)
            sys.stdout.flush()
        else:
            print '<connection closed, press enter to exit'
            running=False
            break
b=threading.Thread(target=blockData,args=(client,))
b.setDaemon(True)
b.start()
while running:
    ui=raw_input('')
    client.send(ui+'\n')