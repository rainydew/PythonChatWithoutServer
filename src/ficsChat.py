# coding: gbk
# must run in CMD, pycharm has a bug when input interrupted
import socket, threading, sys, re, time, base64
client=socket.socket()
print '���ӷ������У����Ժ�'
try:
    client.connect(('freechess.org',5000))
except:
    print '���������ӳ�ʱ'
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
                    print '�����ǳ��ǣ�'+re.findall('"Guest(.*)"',buffer)[0]
                    print '����Է����ǳ�+��Ϣ(�м��Կո����)�����ɷ���������Ϣ������quit���˳���¼'
                    chatting=True
                elif startwith('Thank you for using the Free Internet Chess server ',buffer):
                    print '���Ѿ��˳���¼'
                elif '(told ' in buffer:
                    print buffer[:-1].replace('\r','').replace('told','��Ϣ�ѷ��͸�').replace('fics% ','')
                elif 'is not logged in.' in buffer:
                    print buffer[:-1].replace('\r','').replace('is not logged in','������').replace('fics% ','')
                elif '(U) tells you: ' in buffer:
                    try:
                        buffer=buffer.replace('\r','')  # ��һ�û������룬���ܱ��ߡ�����֮ǰѹ�������ģ���ѹһ��
                        i=buffer.index('(U) tells you:')
                        left=buffer[:i]+' ����˵: '
                        right=base64.b64decode(buffer[i+15:])
                        print left+right
                    except:
                        print buffer.replace('\r','').replace('(U) tells you:', ' ����˵:')
                buffer=''
        else:
            print '���ӹرճɹ�'
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
    print '��������Ӧ��ʱ'
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
            print '�������Ϣ��ʽ����ȷ������������'
        else:
            try:
                ui=ui[:5]+base64.b64encode(ui[5:])  # ʹ��base64ѹ��
                assert len(ui)<60
            except:
                print '������Ϣ����������������'
            else:
                client.send(('tell Guest%s\n'%ui))  # fics��֧�����ģ����Ǳ������Ϊutf-8�ֽ����ʽ