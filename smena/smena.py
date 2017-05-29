import os
import sqlite3
import subprocess
import tkinter as tk
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class App(tk.Frame):
    def __init__(self, parent, *args, **kwargs):
            tk.Frame.__init__(self, parent, *args, **kwargs)
            self.root = parent
            self.entry = tk.StringVar()
            self.name_v = tk.StringVar()
            self.ip_v = tk.StringVar()
            self.ip_v2 = tk.StringVar()
            self.inode_status = tk.Label()
            self.apc_status = tk.Label()
            self.ip0_global = ''
            self.ip1_global = ''
            self.apc = ''
            self.inode = ''
            self.tems = 'C:/Program Files (x86)/SICK/TEMS Manager/Ectn.Tems.TemsManager.exe'
            self.gui()

    def base(self, data):
        params = "SELECT cont, cont2, iNode, APC, name FROM queue WHERE num = " + data
        conn = sqlite3.connect('queue.db')
        cur = conn.cursor()
        cur.execute(params)
        res = cur.fetchone()
        conn.close()
        if res is None:
            self.create_error_window()
            return
        else:
            ip0 = res[0]
            ip1 = res[1]
            self.ip0_global = ip0
            self.ip1_global = ip1
            if ip1 is not '0':
                self.ip_v2.set(ip1)
                self.ip_v.set(ip0)
                self.but_check_2()
            else:
                self.ip_v.set(ip0)
                self.ip_v2.set('')
                self.but_check_1()
            inode = res[2]
            apc = res[3]
            name = res[4]
            self.inode = 'http://' + inode
            self.apc = 'http://' + apc
            self.name_v.set(name)
            self.check(inode, apc)

    def but_check_1(self):
        self.ssh1_but.config(state='active')
        self.ssh2_but.config(state='disable')
        self.trafic1.config(state='active')
        self.trafic2.config(state='disable')
        self.trafic1_xml.config(state='active')
        self.trafic2_xml.config(state='disable')
        self.trafic1_ftp.config(state='active')
        self.trafic2_ftp.config(state='disable')
        self.camera1.config(state='active')
        self.ssh1_but.bind("<Button-1>", lambda event: self.ssh_connect(event, self.ip0_global))
        self.trafic1.bind("<Button-1>", lambda event: self.traffic_spot(event, self.ip0_global))
        self.trafic1_xml.bind("<Button-1>", lambda event: self.traffic_spot_xml(event, self.ip0_global))
        self.trafic1_ftp.bind("<Button-1>", lambda event: self.traffic_spot_ftp(event, self.ip0_global))
        self.camera1.bind("<Button-1>", lambda event: self.cameras(self.ip0_global))
        self.lazori1.config(state='active')
        self.lazori2.config(state='disable')
        self.lazori1.bind("<Button-1>", lambda  event: self.lazors(self.ip0_global))

    def but_check_2(self):
        self.ssh1_but.config(state='active')
        self.ssh2_but.config(state='active')
        self.trafic1.config(state='active')
        self.trafic2.config(state='active')
        self.trafic1_xml.config(state='active')
        self.trafic2_xml.config(state='active')
        self.trafic1_ftp.config(state='active')
        self.trafic2_ftp.config(state='active')
        self.camera1.config(state='active')
        self.ssh1_but.bind("<Button-1>", lambda event: self.ssh_connect(event, self.ip0_global))
        self.ssh2_but.bind("<Button-1>", lambda event: self.ssh_connect(event, self.ip1_global))
        self.trafic1.bind("<Button-1>", lambda event: self.traffic_spot(event, self.ip0_global))
        self.trafic2.bind("<Button-1>", lambda event: self.traffic_spot(event, self.ip1_global))
        self.trafic1_xml.bind("<Button-1>", lambda event: self.traffic_spot_xml(event, self.ip0_global))
        self.trafic2_xml.bind("<Button-1>", lambda event: self.traffic_spot_xml(event, self.ip1_global))
        self.trafic1_ftp.bind("<Button-1>", lambda event: self.traffic_spot_ftp(event, self.ip0_global))
        self.trafic2_ftp.bind("<Button-1>", lambda event: self.traffic_spot_ftp(event, self.ip1_global))
        self.camera1.bind("<Button-1>", lambda event: self.cameras(self.ip0_global))
        self.lazori1.config(state='active')
        self.lazori2.config(state='active')
        self.lazori1.bind("<Button-1>", lambda event: self.lazors(self.ip0_global))
        self.lazori2.bind("<Button-1>", lambda event: self.lazors(self.ip1_global))

    def create_error_window(self):
        self.w = tk.Toplevel()
        error = tk.Label(self.w, text='Такой рамки не существует!').grid(row=0, column=0, columnspan=3, rowspan=2)
        self.ip_v.set('')
        self.ip_v2.set('')
        self.name_v.set('')
        okay = tk.Button(self.w, text="OK", command=self.w.destroy).grid(row=3)

    def get_entry(self):
        data = str(self.entry.get())
        if data == '': return
        self.base(data)
        self.update()
        self.driver = webdriver.Firefox()

    def check(self, ip0, ip1):
        res = os.system("ping -n 1 " + ip0 + ' > NUL')
        res1 = os.system("ping -n 1 " + ip1 + ' > NUL')
        if res == 0:
            self.inode_status.config(text='OK')
            self.inode_status.config(bg='green')
            self.inode_status.config(fg='white')
            self.inode_but.config(state='active')
        else:
            self.inode_status.config(text='BAD')
            self.inode_status.config(bg='red')
            self.inode_status.config(fg='black')
        if res1 == 0:
            self.apc_status.config(text='OK')
            self.apc_status.config(bg='green')
            self.apc_status.config(fg='white')
            self.apc_but.config(state='active')
        else:
            self.apc_status.config(text='BAD')
            self.apc_status.config(bg='red')
            self.apc_status.config(fg='black')

    def inode_url_open(self):
        driver = webdriver.Firefox()
        self.driver.get(self.inode)

    def apc_url_open(self):
        self.driver.get(self.inode)

    def ssh_connect(self, event, ip):
        ssh_conn = 'putty.exe -ssh -i op_smena.ppk op_smena@' + ip
        ssh = subprocess.Popen(ssh_conn, shell=True)

    def traffic_spot(self, event, ip):
        addr = 'http://' + ip + ':8088'
        self.driver.get(addr)
        email_field = self.driver.find_element_by_name("username")
        email_field.send_keys("operator")
        password_field = self.driver.find_element_by_name("password")
        password_field.send_keys("operator")
        password_field.send_keys(Keys.RETURN)

    def traffic_spot_xml(self, event, ip):
        addr = 'http://' + ip + ':2077'
        self.driver.get(addr)

    def traffic_spot_ftp(self, event, ip):
        addr = 'http://' + ip + ':8888'
        self.driver.get(addr)

    def gui(self):
        self.q_label = tk.Label(text="Номер рамки")
        self.q_entry = tk.Entry(textvariable=self.entry)
        self.q_but = tk.Button(text="OK", command=self.get_entry)
        self.inode_lable = tk.Label(text='Статус iNode')
        self.inode_but = tk.Button(text='Открыть', state='disable', command=self.inode_url_open)
        self.apc_label = tk.Label(text='Статус APC')
        self.apc_but = tk.Button(text='Открыть', state='disable', command=self.apc_url_open)
        self.name = tk.Label(text='Название рамки: ')
        self.ip = tk.Label(text='IP рамки: ')
        self.inode_status.grid(row=2, column=1, columnspan=2)
        self.apc_status.grid(row=3, column=1, columnspan=2)
        self.name_val = tk.Label(textvariable=self.name_v, fg='blue')
        self.ip1_val = tk.Label(textvariable=self.ip_v, fg='blue')
        self.ip2_val = tk.Label(textvariable=self.ip_v2, fg='blue')
        self.ssh1_but = tk.Button(text='SSH controller1', state='disable')
        self.trafic1 = tk.Button(text='Trafickspot c1', state='disable')
        self.trafic1_xml = tk.Button(text='Trafick_xml c1', state='disable')
        self.trafic1_ftp = tk.Button(text='Trafick_ftp c1', state='disable')
        self.ssh2_but = tk.Button(text='SSH controller2', state='disable')
        self.trafic2 = tk.Button(text='Trafickspot c2', state='disable')
        self.trafic2_xml = tk.Button(text='Trafick_xml c2', state='disable')
        self.trafic2_ftp = tk.Button(text='Trafick_ftp c2', state='disable')
        self.camera1 = tk.Button(text='Камеры контроллер 1', state='disable')
        self.lazori1 = tk.Button(text='Комплекс классификации 1', state='disable')
        self.lazori2 = tk.Button(text='Комплекс классификации 2', state='disable')
        self.quit_but = tk.Button(text='quit', command=self.b_b)

        #GRIDS MOFO!!!!!!!!!

        self.q_label.grid(column=0, row=1, sticky=tk.W)
        self.q_entry.grid(column=1, row=1, columnspan=3)
        self.q_but.grid(column=4, row=1)
        self.inode_lable.grid(row=2, column=0, sticky=tk.W)
        self.inode_but.grid(row=2, column=4)
        self.apc_label.grid(row=3, column=0, sticky=tk.W)
        self.apc_but.grid(row=3, column=4)
        self.name.grid(row=4, column=0, sticky=tk.W)
        self.ip.grid(row=4, column=3, sticky=tk.W)
        self.inode_status.grid(row=2, column=1, columnspan=2)
        self.apc_status.grid(row=3, column=1, columnspan=2)
        self.name_val.grid(row=4, column=1)
        self.ip1_val.grid(row=4, column=4)
        self.ip2_val.grid(row=5, column=4)
        self.ssh1_but.grid(row=6, column=0, sticky='w, e')
        self.trafic1.grid(row=6, column=1, sticky=tk.W)
        self.trafic1_xml.grid(row=6, column=3, sticky=tk.E)
        self.trafic1_ftp.grid(row=6, column=4, sticky=tk.E)
        self.ssh2_but.grid(row=7, column=0, sticky='w, e')
        self.trafic2.grid(row=7, column=1, sticky=tk.W)
        self.trafic2_xml.grid(row=7, column=3, sticky=tk.E)
        self.trafic2_ftp.grid(row=7, column=4, sticky=tk.E)
        self.camera1.grid(row=8, column=0, columnspan=5, sticky='w, e')
        self.lazori1.grid(row=9, column=0, columnspan=3, sticky='w, e')
        self.lazori2.grid(row=9, column=3, columnspan=2, sticky='w, e')
        self.quit_but.grid(row=10, column=0, columnspan=5, rowspan=2, sticky='w ,e, n, s')

    def b_b(self):
        try:
            self.p1.kill()
            self.p2.kill()
            self.driver.quit()
        finally:
            self.quit()

    def cameras(self, ip0):
        ip = []
        self.w1 = tk.Toplevel()
        exit_but = tk.Button(self.w1, text='Close', command=self.new_w_close).grid(row=2, column=0, columnspan=4)
        with open('cameras.txt') as f:
            l = f.read().splitlines()
            for i in l:
                but = tk.Button(self.w1)
                but["text"] = str(i)
                but.bind("<Button-1>", lambda event, but=but, i=i, ip0=ip0: self.on_click(event, but, i, ip0))
                but.grid(row=0, column=l.index(i))

    def new_w_close(self):
        self.p0.terminate()
        self.w1.destroy()

    def on_click(self, event, button, ip, ip0):
        s = 'plink.exe -L 9000:' + ip + ':80 -L 9901:' + ip + ':9901 -ssh ' + ip0 + ' -l op_smena -i op_smena.ppk'
        self.p0 = subprocess.Popen(s)
        addr = 'http://127.0.0.1:9000'
        self.driver.get(addr)
        but = tk.Button(self.w1, text='Disconnect', command=self.disconn).grid(row=2, column=0, sticky='w, e')

    def disconn(self):
        self.p0.terminate()

    def lazors(self, ip):
        try:
            self.p1.kill()
            self.p2.kill()
        finally:
            s = 'plink.exe -L 59801:192.168.10.200:59801 -ssh ' + ip + ' -l op_smena -i op_smena.ppk'
            self.p1 = subprocess.Popen(s)
            self.p2 = subprocess.Popen(self.tems)


if __name__ == '__main__':
    root = tk.Tk()
    root.title('0 Queue testing')
    App(root)
    root.mainloop()
