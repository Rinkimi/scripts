import sqlite3
import easygui
import subprocess


def name(x):
    conn = sqlite3.connect('Ip_base.db')
    cur = conn.cursor()
    cur.execute('SELECT Name, Controller1, Controller2 FROM CCK WHERE number = ' + x)
    result = cur.fetchone()
    conn.close()
    return result


def ip_check(x):
    global ip, n
    ip0 = x[1]
    ip1 = x[2]
    n = x[0]
    if ip1 is not '':
        res = easygui.choicebox(msg='Выбор контроллера', choices=[ip0, ip1])
        ip = res
    else:
        ip = ip0
    return ip, n


def work(x):
    while True:
        if x:
            r = name(x)
            if r is None:
                break
            ip_check(r)
            s = 'plink.exe -L 5938:{}:5938 -ssh 10.69.71.178 -l ssk_operator -i ssk.ppk -l ssk_operator'.split(' ')
            team = 'C:/Program Files (x86)/TeamViewer/TeamViewer.exe -i 127.0.0.1 --Password 111111'
            s[2] = s[2].format(ip)
            p0 = subprocess.Popen(s)
            p1 = subprocess.Popen(team)
            easygui.msgbox('Вы подключились к рамке ' + n + '.\nIP-адрес Контроллера автоурагана - ' + ip,
                           ok_button='Отключить')
            p0.kill()
            p1.kill()
            break
        else:
            easygui.msgbox('Такой рамки нет')
            break


while True:
    cck = easygui.enterbox(msg='Номер рамки', title='Выбор рамки')
    if cck is None:
        break
    work(cck)
