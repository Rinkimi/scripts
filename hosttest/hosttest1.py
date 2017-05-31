import os
import csv


def ping(x):
    for item in x:
        ip = str(item).strip('[]')
        response = os.system("ping -n 1 " + ip + " > NUL")
        print(response)
        if response == 0:
            up.append(item)
        else:
            down.append(item)
    write(up)
    write0(down)


def write(ip):
    with open('up.csv', 'w') as fo:
        a = csv.writer(fo)
        a.writerows(ip)


def write0(ip):
    with open('down.csv', 'w', newline='') as fo:
        a = csv.writer(fo)
        a.writerows(ip)


def hput(x):
    ip=[]
    with open(x) as fi:
        reader = csv.reader(fi)
        ip = list(reader)
        for item in ip:
            ping(item)


up = []
down = []
hosts = hput('list.csv')
print('Hosts: ', up, ' is up!')
print('Hosts: ', down, ' is down!')
