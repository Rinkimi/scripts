from tkinter import *
import time
from tkinter import ttk
import sqlite3
import os
from subprocess import Popen, PIPE
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


class App(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.ip0 = StringVar()
        self.ip1 = StringVar()
        self.inode = ''
        self.apc = ''
        self.name = StringVar()
        self.tems = 'C:/Program Files (x86)/SICK/TEMS Manager/Ectn.Tems.TemsManager.exe'
        self.driver = webdriver.Firefox()
        self.gui()
        root.protocol('WM_DELETE_WINDOW', self.exit_event)

    def exit_event(self):
        try:
            self.p1.kill()
            self.p2.kill()
            self.driver.quit()
        finally:
            print('Good bye!')
            root.destroy()

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

    def check(self, ip0, ip1):
        res = os.system("ping -n 1 " + ip0 + ' > NUL')
        res1 = os.system("ping -n 1 " + ip1 + ' > NUL')
        if res == 0:
            self.inode_status.config(text='OK')
            self.inode_status.config(background='green')
            self.inode_status.config(foreground='white')
            self.inode_but.config(state='active')
            self.inode = ip0
            self.inode_but.bind("<Button-1>", self.inode_url_open)
        else:
            self.inode_status.config(text='BAD')
            self.inode_status.config(background='red')
            self.inode_status.config(foreground='black')
        if res1 == 0:
            self.apc_status.config(text='OK')
            self.apc_status.config(background='green')
            self.apc_status.config(foreground='white')
            self.apc_but.config(state='active')
            self.apc = ip1
            self.apc_but.bind("<Button-1>", self.apc_url_open)
        else:
            self.apc_status.config(text='BAD')
            self.apc_status.config(background='red')
            self.apc_status.config(foreground='black')

    def inode_url_open(self, event):
        adr = 'http://' + self.inode
        self.driver.get(adr)

    def apc_url_open(self, event):
        adr = 'http://' + self.apc
        self.driver.get(adr)

    def exit_button(self):
        try:
            self.p1.kill()
            self.p2.kill()
        finally:
            print('Done!')

    def OnDouble(self, event):
        widget = event.widget
        selection = widget.curselection()
        value = widget.get(selection[0])
        self.sql(value[1])

    def sql(self, num):
        params = "SELECT cont, cont2, iNode, APC, name FROM queue WHERE num = " + str(num)
        conn = sqlite3.connect('c:/bases/queue.db')
        cur = conn.cursor()
        cur.execute(params)
        res = cur.fetchone()
        conn.close()
        self.name.set(res[4])
        if res[1] is '0':
            self.ip0.set(res[0])
            self.ip0_global = res[0]
            self.check(res[2], res[3])
            self.buttons()
        else:
            self.ip1.set(res[1])
            self.ip0.set(res[0])
            self.ip0_global = res[0]
            self.ip1_global = res[1]
            self.check(res[2], res[3])
            self.buttons2()

    def buttons(self):
        self.trafic1.config(state='active')
        self.trafic2.config(state='disable')
        self.trafic1_xml.config(state='active')
        self.trafic2_xml.config(state='disable')
        self.trafic1_ftp.config(state='active')
        self.trafic2_ftp.config(state='disable')
        self.ssh0.config(state='active')
        self.ssh1.config(state='disable')
        self.tems0.config(state='active')
        self.tems1.config(state='disable')
        self.camera.config(state='active')
        self.ssh0.bind("<Button-1>", lambda event: self.ssh_connect(event, self.ip0_global))
        self.tems0.bind("<Button-1>", lambda event: self.lazors(event, self.ip0_global))
        self.trafic1.bind("<Button-1>", lambda event: self.traffic_spot(event, self.ip0_global))
        self.trafic1_xml.bind("<Button-1>", lambda event: self.traffic_spot_xml(event, self.ip0_global))
        self.trafic1_ftp.bind("<Button-1>", lambda event: self.traffic_spot_ftp(event, self.ip0_global))
        self.camera.bind("<Button-1>", lambda event: self.cameras_check(self.ip0_global))

    def buttons2(self):
        self.trafic1.config(state='active')
        self.trafic2.config(state='active')
        self.trafic1_xml.config(state='active')
        self.trafic2_xml.config(state='active')
        self.trafic1_ftp.config(state='active')
        self.trafic2_ftp.config(state='active')
        self.ssh0.config(state='active')
        self.ssh1.config(state='active')
        self.tems0.config(state='active')
        self.tems1.config(state='active')
        self.camera.config(state='active')
        self.ssh0.bind("<Button-1>", lambda event: self.ssh_connect(event, self.ip0_global))
        self.tems0.bind("<Button-1>", lambda event: self.lazors(event, self.ip0_global))
        self.ssh1.bind("<Button-1>", lambda event: self.ssh_connect(event, self.ip1_global))
        self.tems1.bind("<Button-1>", lambda event: self.lazors(event, self.ip1_global))
        self.trafic1.bind("<Button-1>", lambda event: self.traffic_spot(event, self.ip0_global))
        self.trafic2.bind("<Button-1>", lambda event: self.traffic_spot(event, self.ip1_global))
        self.trafic1_xml.bind("<Button-1>", lambda event: self.traffic_spot_xml(event, self.ip0_global))
        self.trafic2_xml.bind("<Button-1>", lambda event: self.traffic_spot_xml(event, self.ip1_global))
        self.trafic1_ftp.bind("<Button-1>", lambda event: self.traffic_spot_ftp(event, self.ip0_global))
        self.trafic2_ftp.bind("<Button-1>", lambda event: self.traffic_spot_ftp(event, self.ip1_global))
        self.camera.bind("<Button-1>", lambda event: self.cameras_check(self.ip0_global))

    def ssh_connect(self, event, ip):
        key = 'c:/Keys/key.ppk'
        ssh_conn = 'putty.exe -ssh -i ' + key + ' smihaylov@' + ip
        self.ssh_conn = Popen(ssh_conn, shell=True)

    def lazors(self, event, ip):
        try:
            self.p1.kill()
            self.p2.kill()
        finally:
            key = 'c:/Keys/key.ppk'
            s = 'plink.exe -L 59801:192.168.10.200:59801 -ssh ' + ip + ' -l smihaylov -i ' + key
            self.p1 = Popen(s)
            self.p2 = Popen(self.tems)

    def listfill(self):
        params = "SELECT name, num FROM queue"
        conn = sqlite3.connect('c:/bases/queue.db')
        cur = conn.cursor()
        cur.execute(params)
        res = cur.fetchall()
        for i in res:
            self.listbox.insert(END, i)
        conn.close()

    def gui(self):
        content = ttk.Frame(root, padding=(3, 3, 12, 12))
        self.frame = ttk.Frame(content, borderwidth=5, relief="groove", width=200, height=100)
        name_lb = ttk.Label(self.frame, text='Название рамки:')
        self.name_val = ttk.Label(self.frame, textvariable=self.name, foreground='blue')
        ip_lb = ttk.Label(self.frame, text='IP адрес:', width=33)
        self.ip_val1 = ttk.Label(self.frame, textvariable=self.ip0, foreground='blue')
        self.ip_val2 = ttk.Label(self.frame, textvariable=self.ip1, foreground='blue')
        tfframe = ttk.Labelframe(content, text='Trafficspot', borderwidth=5, width=200, height=100)
        self.trafic1 = ttk.Button(tfframe, text='Trafickspot c1', state='disable', width=13)
        self.trafic1_xml = ttk.Button(tfframe, text='Trafick_xml c1', state='disable', width=13)
        self.trafic1_ftp = ttk.Button(tfframe, text='Trafick_ftp c1', state='disable', width=13)
        self.trafic2 = ttk.Button(tfframe, text='Trafickspot c2', state='disable', width=13)
        self.trafic2_xml = ttk.Button(tfframe, text='Trafick_xml c2', state='disable', width=13)
        self.trafic2_ftp = ttk.Button(tfframe, text='Trafick_ftp c2', state='disable', width=13)
        inodeframe = ttk.Labelframe(content, text='Status', borderwidth=5, width=200, height=50)
        inode_lb = ttk.Label(inodeframe, text='iNode', width=10)
        self.inode_status = ttk.Label(inodeframe, width=20)
        self.inode_but = ttk.Button(inodeframe, text='Open', state='disable')
        apc_lb = ttk.Label(inodeframe, text='APC', width=10)
        self.apc_status = ttk.Label(inodeframe, width=20)
        self.apc_but = ttk.Button(inodeframe, text='Open', state='disable')
        sshframe = ttk.Labelframe(content, text='SSH', borderwidth=5, width=200, height=50)
        self.ssh0 = ttk.Button(sshframe, text='SSH controller 1', state='disable', width=20)
        self.ssh1 = ttk.Button(sshframe, text='SSH controller 2', state='disable', width=20)
        temsframe = ttk.Labelframe(content, text='TEMS', borderwidth=5, width=200, height=50)
        self.tems0 = ttk.Button(temsframe, text='TEMS controller 1', state='disable', width=20)
        self.tems1 = ttk.Button(temsframe, text='TEMS controller 2', state='disable', width=20)
        camerasframe = ttk.Labelframe(content, text='Cameras', borderwidth=5, width=200, height=50)
        self.camera = ttk.Button(camerasframe, text='Камеры', state='disable', width=20)
        self.off_button = ttk.Button(content, text='Disconnect', command=self.exit_button)
        self.listbox = Listbox(content, relief="groove", selectmode=SINGLE)
        self.listfill()
        self.listbox.bind("<Double-Button-1>", self.OnDouble)

        content.grid(column=0, row=0, sticky=(N, S, E, W))
        self.frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        name_lb.grid(row=0, column=0, sticky=W)
        self.name_val.grid(row=0, column=1, sticky=E)
        ip_lb.grid(row=2, column=0, sticky=W)
        self.ip_val1.grid(row=2, column=1, sticky=E)
        self.ip_val2.grid(row=3, column=1, sticky=E)
        tfframe.grid(row=3, column=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        self.trafic1.grid(row=0, column=0)
        self.trafic1_xml.grid(row=0, column=1)
        self.trafic1_ftp.grid(row=0, column=2)
        self.trafic2.grid(row=1, column=0)
        self.trafic2_xml.grid(row=1, column=1)
        self.trafic2_ftp.grid(row=1, column=2)
        inodeframe.grid(row=5, column=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        inode_lb.grid(row=0, column=0, sticky=W)
        self.inode_status.grid(row=0, column=1)
        self.inode_but.grid(row=0, column=2, sticky=E)
        apc_lb.grid(row=1, column=0, sticky=W)
        self.apc_status.grid(row=1, column=1)
        self.apc_but.grid(row=1, column=2, sticky=E)
        sshframe.grid(row=7, column=0, columnspan=3, sticky=(N, S, E, W))
        self.ssh0.grid(row=0, column=0, sticky=(W, E))
        self.ssh1.grid(row=0, column=1, sticky=(W, E))
        temsframe.grid(row=8, column=0, columnspan=3, sticky=(N, S, E, W))
        self.tems0.grid(row=0, column=0, sticky=(W, E))
        self.tems1.grid(row=0, column=1, sticky=(W, E))
        camerasframe.grid(row=9, column=0, columnspan=3, sticky=(N, S, E, W))
        self.camera.grid(row=0, column=0, sticky=(W, E))
        self.off_button.grid(row=10, column=0, columnspan=4, sticky=(W, E))
        self.listbox.grid(row=0, column=3, rowspan=10, sticky=(N, S, E, W))

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=3)
        content.columnconfigure(2, weight=3)
        content.columnconfigure(3, weight=1)
        content.columnconfigure(4, weight=1)
        content.rowconfigure(1, weight=1)

    def cameras_check(self, ip):
        key = ' -i c:/keys/key.ppk '
        user = ' -l smihaylov '
        self.ip_up = []
        params = "SELECT Camera FROM cameras"
        conn = sqlite3.connect('c:/bases/queue.db')
        cur = conn.cursor()
        cur.execute(params)
        cam = cur.fetchall()
        conn.close()
        for i in cam:
            command = ' ping -c 1 -W 5 ' + i[0]
            s = 'plink.exe -batch -ssh ' + ip + key + user + command
            proc = Popen(s, stdout=PIPE, stderr=PIPE)
            r = proc.communicate()
            res = r[0].decode('utf-8')
            res = r[0].decode('utf-8').rsplit(' received,', 1)[0].split(', ', 1)[1]
            if res == '1':
                self.ip_up.append(i)
            proc.kill()
        self.cameras(self.ip0_global, self.ip_up)

    def cameras(self, ip0, ip):
        self.w1 = Toplevel()
        exit_but = ttk.Button(self.w1, text='Close', command=self.new_w_close)
        exit_but.grid(row=2, column=0, columnspan=4)
        for i in ip:
            but = ttk.Button(self.w1)
            but["text"] = str(i[0])
            but.bind("<Button-1>", lambda event, but=but, i=i, ip0=ip0: self.on_click(event, but, i[0], ip0))
            but.grid(row=0, column=ip.index(i))

    def new_w_close(self):
        try:
            self.p0.kill()
        finally:
            self.w1.destroy()
            print("Okay!")

    def on_click(self, event, button, ip, ip0):
        try:
            self.p0.terminate()
        finally:
            key = 'c:/Keys/key.ppk'
            s = 'plink.exe -L 9000:' + ip + ':80 -L 9901:' + ip + ':9901 -ssh ' + ip0 + ' -l smihaylov -i ' + key
            self.p0 = Popen(s)
            time.sleep(3)
            addr = 'http://127.0.0.1:9000'
            self.driver.get(addr)

if __name__ == '__main__':
    root = Tk()
    root.title('Ports')
    App(root)
    root.mainloop()
