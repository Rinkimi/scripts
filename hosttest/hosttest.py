import os
import socket
import csv


def ping(x):
    for item in x:
        response = os.system("ping -n 1 " + item + " > NUL")
        if response == 0:
            up.append(item)
        else:
            down.append(item)
    return up, down


def lookup(x):
    for i in x:
        ip_list = []
        ais = socket.getaddrinfo(i, 0, 0, 0, 0)
        for result in ais:
            ip_list.append(result[-1][0])
        ip_list = list(set(ip_list))
        res[i] = ip_list
    for key, val in res.items():
        if key in res.keys():
            ping(val)


def hput(x):
    with open(x) as fi:
        h = fi.read().splitlines()
    return h


res = {}
up = []
down = []
hosts = hput('list.csv')
lookup(hosts)
print('Hosts: ', up, ' is up!')
print('Hosts: ', down, ' is down!')
