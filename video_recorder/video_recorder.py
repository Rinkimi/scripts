import csv
from datetime import datetime
import subprocess
from threading import Thread
import queue
import sys
import os


#############################################################
#Сюда прописать директорию куда будут сохраняться видео файлы
#И директорию где живет vlc
PATH = "C:/Program Files (x86)/VideoLAN/VLC/vlc.exe"
DIR = "c:/video/"
#############################################################


def proverka(x):
    for i in range(x):
        if x > 10:
            print('Общее число рамок не может превышать 10!')
            break
        else:
            ramka = input('Введите номер рамки: ')
            func(ramka)
            l.append(params1)
            l.append(params2)

def func(x):
    with open('C:/Users/stanislav.mihaylov/Documents/list1.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row['Метка по КС'] == x and row['Очередь'] in ('I', 'II') and row['Тип канала'] == 'Основной':
                print('Рамка: ', row['Идентификатор канала'])
                u = str(row['net Z1'])
                v = int(row['Полосность'])
                p = str(row['Метка по КС'])
                ip(v, u, p)

def ip(o, u, p):
    n = {2: "68", 3: "69", 4: "70", 5: "71", 6: "72"}
    ln = n[o]
    ip1 = u + "67"
    ip2 = u + ln
    name = p
    vlc(ip1, ip2, name)

def vlc(ip1, ip2, name):
    global params1, params2
    name1 = str('/' + name + '-ov1')
    name2 = str('/' +name + '-ov2')
    vid_dir = str(DIR + name)
    if not os.path.isdir(vid_dir):
        os.makedirs(vid_dir)
    filename1 = str('--sout file/mp4:' + vid_dir + name1 + '(' + str(date) + ').ts ')
    filename2 = str('--sout file/mp4:' + vid_dir + name2 + '(' + str(date) + ').ts ')
    stream1 = str('rtsp://admin:admin12345@' + ip1 + ':554/Streaming/Channels/3 ')
    stream2 = str('rtsp://admin:admin12345@' + ip2 + ':554/Streaming/Channels/3 ')
    params1 = str(PATH + ' --qt-start-minimized ' + str(stream1) + str(filename1) + '--run-time=30 vlc://quit')
    params2 = str(PATH + ' --qt-start-minimized ' + str(stream2) + str(filename2) + '--run-time=30 vlc://quit')

def put(n):
    for item in n:
        q.put(item)

def worker():
    while True:
        if q.empty():
            sys.exit()
        item = q.get()
        proc = subprocess.run(item)
        q.task_done()


q = queue.Queue()
l = []
date = datetime.strftime(datetime.now(), "%Y-%m-%d_%H-%M-%S")
nums = int(input('Введите количество рамок (10 максимум): '))
proverka(nums)
put(l)
t1 = Thread(target=worker).start()
t2 = Thread(target=worker).start()
t3 = Thread(target=worker).start()
t4 = Thread(target=worker).start()
q.join()
