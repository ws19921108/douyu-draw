# 这个抓取弹幕后保存为text文档，然后词云分析,此部分是抓取弹幕内容
__author__ = '布咯咯_rieuse'
__time__ = '2017.6.2'
__github__ = 'https://github.com/rieuse'

import multiprocessing
import re
import socket
import time

import requests
from bs4 import BeautifulSoup

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
host = socket.gethostbyname("openbarrage.douyutv.com")
port = 8601
client.connect((host, port))

danmu = re.compile(b'txt@=(.+?)/cid@')


def sendmsg(msgstr):
    msg = msgstr.encode('utf-8')
    data_length = len(msg) + 8
    code = 689
    msgHead = int.to_bytes(data_length, 4, 'little') \
              + int.to_bytes(data_length, 4, 'little') + int.to_bytes(code, 4, 'little')
    client.send(msgHead)
    sent = 0
    while sent < len(msg):
        tn = client.send(msg[sent:])
        sent = sent + tn

'''username@=rieuse/password@=douyu/'''


def start(roomid):
    msg = 'type@=loginreq/roomid@={}/\0'.format(roomid)
    sendmsg(msg)
    msg_more = 'type@=joingroup/rid@={}/gid@=-9999/\0'.format(roomid)
    sendmsg(msg_more)

    print('---------------欢迎连接到{}的直播间---------------'.format(get_name(roomid)))
    while True:
        data = client.recv(1024)
        danmu_more = danmu.findall(data)
        if not data:
            break
        else:
            for i in range(0, len(danmu_more)):
                with open('danmu_1txt', 'a') as fo:
                    try:
                        print(danmu_more[0].decode(encoding='utf-8'))
                        txt = danmu_more[0].decode(encoding='utf-8') + '\n'
                        fo.writelines(txt)
                    except:
                        print('出错了')


def keeplive():
    while True:
        msg = 'type@=keeplive/tick@=' + str(int(time.time())) + '/\0'
        sendmsg(msg)
        time.sleep(10)


def get_name(roomid):
    r = requests.get("http://www.douyu.com/" + roomid)
    soup = BeautifulSoup(r.text, 'lxml')
    return soup.find('a', {'class', 'zb-name'}).string


if __name__ == '__main__':
    room_id = input('请输入房间ID： ')
    p1 = multiprocessing.Process(target=start, args=(room_id,))
    p2 = multiprocessing.Process(target=keeplive)
    p1.start()
    p2.start()