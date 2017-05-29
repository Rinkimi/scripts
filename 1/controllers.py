import csv
import subprocess
import easygui


def myjoin(a,b):
    if b:
        return ' '.join((a,b))
    else:
        return a


def list2dict(a):
    ret = {}
    for rec in a:
        t = {}
        for key in rec.keys():
            if rec[key]:
                t[key] = rec[key]
        if t['Метка по КС'] in ret.keys():
            continue
        ret[t['Метка по КС']] = {}
        ret[t['Метка по КС']].update(t)
    return ret


def ask(ramk, res, val='Контроллер Ураган 1'):
    ret = None
    ramka = str(ramk)
    if ramka in res.keys():
        if val in res[ramka].keys():
            print(res[ramka][val])
        else:
            print('No value')
    else:
        print('no ramka')
    try:
        ret = res[ramka][val]
    except:
        ret = None
    return ret


def ask1(ramk, res, val='Очередь'):
    ret = None
    ramka = str(ramk)
    if ramka in res.keys():
        if val in res[ramka].keys():
            print(res[ramka][val])
        else:
            print('No value')
    else:
        print('no ramka')
    try:
        ret=res[ramka][val]
    except:
        ret = None
    return ret


def work(data):
    while True:
        s = 'plink.exe -L 5938:{}:5938 -ssh 10.69.71.178 -l ssk_operator -i ssk.ppk -l ssk_operator'.split(' ')
        team = 'C:/Program Files (x86)/TeamViewer/TeamViewer.exe -i 127.0.0.1 --Password 111111'
        ramka = easygui.enterbox(msg='Номер рамки', title='Выбор рамки')
        if ramka is None:
            break
        if ramka in data.keys():
            ip0 = ask(ramka,data)
            queue = ask1(ramka,data)
            ip1 = ask(ramka,data,'Контроллер Ураган 2')
            if ip1 is not None:
                res = easygui.choicebox(msg='Выбор контроллера',choices=[ip0, ip1])
                ip = res
            else:
                ip = ip0
            s[2] = s[2].format(ip)
            proc = subprocess.Popen(s)
            proc1 = subprocess.Popen(team)
            ans = easygui.msgbox('Вы подключились к рамке ' + queue + ' очереди. Контроллер автоурагана - ' + ip, ok_button='Отключить')
            print(s)
            proc.kill()
            proc1.kill()
        else:
            ans = easygui.msgbox('Такой рамки нет')
            break
            

def load_data(infile):
    data = []
    with open(infile) as f:
        testreader = csv.reader(f, delimiter=';')
        head = next(testreader)
        subheader = next(testreader)
        header = list(map(myjoin, head, subheader))
        flag = True
        while flag:
            try:
                q = next(testreader)
                data.append(dict(zip(header, q)))
            except:
                flag = False
                break
    res = list2dict(data)
    return res


r = load_data('list1.csv')
work(r)
