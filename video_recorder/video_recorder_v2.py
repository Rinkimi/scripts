import sqlite3
from datetime import datetime
import os
import subprocess
from threading import Thread
import queue
import sys


#############################################################
#ГЛОБАЛЬНЫЙ ПЕРЕМЕННЫЕ
PATH = "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"    #Путь до vlc. Обратите внимание на обратные слеши, ЭТО ВАЖНО!
DIR = "c:/video/"                                       #Путь куда будут сохраняться видео записи
T = '120'                                                #Время записи в секундах
th = 10                                                  #Количество запускаемых потоков
#############################################################


def proverka(x):
    for i in range(x):
        if x > 20:
            print('Общее число рамок не может превышать 20!')
            break
        else:
            ramka = input('Введите номер рамки: ')
            sql(ramka)
            ramkas.append(params1)
            ramkas.append(params2)
    q_put(ramkas)


def q_put(x):
    for i in x:
        q.put(i)


def worker():
    while True:
        if q.empty():
            sys.exit()
        item = q.get()
        proc = subprocess.run(item)
        q.task_done()


def sql(num):
    conn = sqlite3.connect('c:/bases/Ip_base1.db')
    cur = conn.cursor()
    cur.execute('SELECT Name, Controller1, Rows FROM CCK WHERE number = ' + num)
    result = cur.fetchone()
    conn.close()
    ip_cameras(result)


def ip_cameras(data):
    n = {2: "68", 3: "69", 4: "70", 5: "71", 6: "72"}
    ip = data[1].split('.')
    ip[3] = '67'
    ip0 = '.'.join(ip)
    ip[3] = n[data[2]]
    ip1 = '.'.join(ip)
    name = data[0].replace(' ', '')
    vlc(ip0, ip1, name)


def vlc(ip1, ip2, name):
    global params1, params2
    name1 = str('/' + name + '-ov1')
    name2 = str('/' +name + '-ov2')
    vid_dir = str(DIR + name)
    if not os.path.isdir(vid_dir):
        os.makedirs(vid_dir)
    filename1 = str('--sout file/mp4:' + vid_dir + name1 + '(' + str(date) + ').ts ')
    filename2 = str('--sout file/mp4:' + vid_dir + name2 + '(' + str(date) + ').ts ')
    stream1 = str('rtsp://admin:admin12345@' + ip1 + ':554/Streaming/Channels/2 ')
    stream2 = str('rtsp://admin:admin12345@' + ip2 + ':554/Streaming/Channels/2 ')
    params1 = str(PATH + ' --qt-start-minimized ' + str(stream1) + str(filename1) + '--run-time=' + T + ' vlc://quit')
    params2 = str(PATH + ' --qt-start-minimized ' + str(stream2) + str(filename2) + '--run-time=' + T + ' vlc://quit')


q = queue.Queue()
ramkas = []
date = datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S")
nums = int(input('Введите количество рамок (10 максимум): '))
proverka(nums)
for i in range(th):
    i = Thread(target=worker).start()
q.join()