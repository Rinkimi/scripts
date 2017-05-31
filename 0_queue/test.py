from subprocess import Popen, PIPE

ip = ' 10.77.30.66 '
ip_up = []

def cameras_check(ip_global):
    key = ' -i c:/keys/key.ppk '
    user = ' -l smihaylov '
    with open('cameras.txt') as fi:
        l = fi.read().splitlines()
        for i in l:
            command = ' ping -c 1 -W 5 ' + i
            s = 'plink.exe -batch -ssh' + ip_global + key + user + command
            proc = Popen(s, stdout=PIPE, stderr=PIPE)
            r = proc.communicate()
            res = r[0].decode('utf-8').rsplit(' received,', 1)[0].split(', ', 1)[1]
            if res == '1':
                ip_up.append(i)
    print(ip_up)


cameras_check(ip)

for i in cam:
    command = ' ping -c 1 -W 5 ' + i[0]
    s = 'plink.exe -batch -ssh' + ip + key + user + command
    proc = Popen(s, stdout=PIPE, stderr=PIPE)
    r = proc.communicate()
    res = r[0].decode('utf-8').rsplit(' received,', 1)[0].split(', ', 1)[1]
    if res == '1':
        self.ip_up.append(i[0])
    proc.kill()
self.cameras(self.ip0_global, self.ip_up)