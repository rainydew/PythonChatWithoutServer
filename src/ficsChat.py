# coding: gbk
# must run in CMD, pycharm has a bug when input interrupted
import socket, threading, sys, re, time, base64
client=socket.socket()
print '连接服务器中，请稍候'
try:
    client.connect(('freechess.org',5000))
except:
    print '服务器连接超时'
    sys.exit(-1)
chatting=False

def startwith(instr,totalstr):
    totalstr=totalstr.replace('\r','')
    return totalstr[:len(instr)]==instr

def blockData(chan):
    '''
    :param socket._socketobject chan:
    :return:
    '''
    global chatting
    buffer=''
    while True:
        data=chan.recv(1)
        if data:
            buffer+=data
            if startwith('login:', buffer):
                chan.send('guest\n')
                buffer=''
            elif buffer[-1]=='\n':
                if startwith('Press return to enter the server as ',buffer):
                    chan.send('\n')
                    print '您的昵称是：'+re.findall('"Guest(.*)"',buffer)[0]
                    print '输入对方的昵称+消息(中间以空格隔开)，即可发送聊天信息，输入quit则退出登录'
                    chatting=True
                elif startwith('Thank you for using the Free Internet Chess server ',buffer):
                    print '您已经退出登录'
                elif '(told ' in buffer:
                    print buffer[:-1].replace('\r','').replace('told','消息已发送给').replace('fics% ','')
                elif 'is not logged in.' in buffer:
                    print buffer[:-1].replace('\r','').replace('is not logged in','不在线').replace('fics% ','')
                elif '(U) tells you: ' in buffer:
                    try:
                        buffer=buffer.replace('\r','')  # 万一用户乱输入，可能杯具。我们之前压缩过中文，解压一下
                        i=buffer.index('(U) tells you:')
                        left=buffer[:i]+' 对你说: '
                        right=base64.b64decode(buffer[i+15:])
                        print left+right
                    except:
                        print buffer.replace('\r','').replace('(U) tells you:', ' 对你说:')
                buffer=''
        else:
            print '连接关闭成功'
            chatting=False
            break
b=threading.Thread(target=blockData,args=(client,))
b.setDaemon(True)
b.start()
s=0
while s<150 and not chatting:
    time.sleep(0.1)
    s=s+1
if not chatting:
    print '服务器响应超时'
    sys.exit(-1)

while chatting:
    ui=raw_input('')
    if ui=='quit':
        client.send('quit\n')
        s=0
        while chatting and s<50:
            time.sleep(0.1)
            s=s+1
        sys.exit(0)
    elif chatting:
        try:
            assert len(ui.split(' '))>=2
            assert len(ui.split(' ')[0])==4
            assert len(ui)>5
        except:
            print '输入的信息格式不正确，请重新输入'
        else:
            try:
                ui=ui[:5]+base64.b64encode(ui[5:])  # 使用base64压缩
                assert len(ui)<60
            except:
                print '输入信息超长，请重新输入'
            else:
                client.send(('tell Guest%s\n'%ui))  # fics不支持中文，我们必须编码为utf-8字节码格式