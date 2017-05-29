from paramiko import SSHClient
from scp import SCPClient
import paramiko
import time


host = '192.168.1.2'
user = 'ubnt'
secret = '12345678'
port = 22
localpath = 'C:/scripts/Ubnt/car/system.cfg'
#localpath1 = 'C:/scripts/Ubnt/default.cfg'
remotepath = '/tmp/'
ssh = SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
try:
    ssh.connect(hostname=host, username=user, password=secret, port=port)
    with SCPClient(ssh.get_transport()) as scp:
        scp.put(localpath, remote_path=remotepath)
#        scp.get(remote_path='/etc/default.cfg', local_path=localpath1)
        stdin, stdout, stderr = ssh.exec_command('cfgmtd -w -f /tmp/system.cfg')
        time.sleep(5)
        ssh.exec_command('reboot')
        data = stdout.read() + stderr.read()
except paramiko.SSHException:
    print("Connection Failed")
    quit()
print(data)