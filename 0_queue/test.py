from subprocess import Popen, PIPE

ip = ' 10.77.41.66 '
key = ' -i key.ppk '
user = ' -l smihaylov '
command = ' service its_ts status'
s = 'plink.exe -batch -ssh' + ip + key + user + command
proc = Popen(s, stderr=PIPE, stdout=PIPE)
res = proc.communicate()
print(res)