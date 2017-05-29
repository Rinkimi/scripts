import csv
import subprocess


def csv_check(x):
    global net
    with open('c:/Ubnt/list.csv', newline='') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            if row['Метка по КС'] == x and row['Тип канала'] == 'Основной':
                net = row['net Z1']
    return net


ramka = input('Введите номер рамки: ')
csv_check(ramka)
p = 'netsh interface ipv4 set address name="Network" static ' + net +'124 255.255.255.192 ' + net +'65'
#subprocess.call(p)
print(p)
