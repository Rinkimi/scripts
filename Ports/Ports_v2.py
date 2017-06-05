import sqlite3
from subprocess import Popen
from tkinter import *
from tkinter import ttk


class App(Frame):
    def __init__(self, parent, *args, **kwargs):
        Frame.__init__(self, parent, *args, **kwargs)
        self.root = parent
        self.entry = StringVar()
        self.name_v = StringVar()
        self.ip_v = StringVar()
        self.ip_v2 = StringVar()
        self.ramka_q = StringVar()
        self.gui()
        root.bind("<Return>", lambda event: self.get_entry(event))
        root.protocol('WM_DELETE_WINDOW', self.b_b)

    def sql(self, data):
        conn = sqlite3.connect('C:/bases/Ip_base1.db')
        cur = conn.cursor()
        cur.execute('SELECT Queue, Name, Controller1, Controller2 FROM CCK WHERE number = ' + data)
        result = cur.fetchone()
        conn.close()
        if result is None:
            self.error_messg()
        else:
            self.ip0 = result[2]
            self.ip1 = result[3]
            if self.ip1 == '':
                self.control1.config(state='active')
                self.control1.bind("<Button-1>", lambda event: self.connect(self.ip0))
                self.control2.config(state='disable')
            else:
                self.control1.config(state='active')
                self.control1.bind("<Button-1>", lambda event: self.connect(self.ip0))
                self.control2.config(state='active')
                self.control2.bind("<Button-1>", lambda event: self.connect(self.ip1))
            self.name_v.set(result[1])
            self.ip_v.set(result[2])
            self.ip_v2.set(result[3])
            self.ramka_q.set(result[0])

    def error_messg(self):
        top = Toplevel()
        label = Label(top, text='Такой рамки не существет!')
        label.grid(row=0, column=0, sticky=(W, E, S, N))
        self.name.delete(0, 'end')
        exit_but = Button(top, text='OK', command=top.destroy)
        exit_but.grid(row=1,column=0,sticky=(W ,E ,S ,N))

    def connect(self, ip):
        try:
            self.p0.kill()
            self.p1.kill()
        finally:
            key = 'C:/Keys/ssk.ppk'
            plink = 'plink.exe -L 5938:' + ip + ':5938 -ssh 10.69.71.178 -l ssk_operator -i ' + key
            team = 'C:/Program Files (x86)/TeamViewer/TeamViewer.exe -i 127.0.0.1 --Password 111111'
            self.p0 = Popen(plink)
            self.p1 = Popen(team)

    def get_entry(self, event):
        data = str(self.entry.get())
        if data == '': return
        self.sql(data)
        self.update()
        self.frame.update()

    def b_b(self):
        try:
            self.p1.kill()
            self.p0.kill()
        finally:
            root.destroy()

    def gui(self):
        content = ttk.Frame(root, padding=(3, 3, 12, 12))
        self.frame = ttk.Frame(content, borderwidth=5, relief="sunken", width=200, height=100)
        namelbl = ttk.Label(content, text="Введите номер рамки:")
        self.name = ttk.Entry(content, textvariable=self.entry)
        conn = ttk.Button(content, text='Connect')
        self.control1 = ttk.Button(content, text='Контроллер 1', state='disable')
        self.control2 = ttk.Button(content, text='Контроллер 2', state='disable')
        ramka_name_lb = ttk.Label(self.frame, text='Имя рамки:')
        ramka_name_val = ttk.Label(self.frame, textvariable=self.name_v)
        ramka_q_lb = ttk.Label(self.frame, text='Очередь:')
        ramka_q_val = ttk.Label(self.frame, textvariable=self.ramka_q)
        ramka_ip_lb = ttk.Label(self.frame, text='IP адрес: ')
        ramka_ip_val1 = ttk.Label(self.frame, textvariable=self.ip_v)
        ramka_ip_val2 = ttk.Label(self.frame, textvariable=self.ip_v2)
        conn.bind("<Button-1>", lambda event: self.get_entry(event))

        content.grid(column=0, row=0, sticky=(N, S, E, W))
        self.frame.grid(column=0, row=0, columnspan=3, rowspan=2, sticky=(N, S, E, W))
        namelbl.grid(column=3, row=0, columnspan=2, sticky=(N, W, E, S))
        self.name.grid(column=3, row=1, columnspan=2, sticky=(N, E, W), pady=5)
        conn.grid(column=3, row=2, columnspan=2, sticky=(N, E, W, S))
        self.control1.grid(row=2, column=0)
        self.control2.grid(row=2, column=1)
        ramka_name_lb.grid(row=0, column=0, sticky=W)
        ramka_name_val.grid(row=0, column=2, sticky=E)
        ramka_q_lb.grid(row=1, column=0, sticky=W)
        ramka_q_val.grid(row=1, column=2, sticky=E)
        ramka_ip_lb.grid(row=2, column=0, sticky=W)
        ramka_ip_val1.grid(row=2, column=2, sticky=E)
        ramka_ip_val2.grid(row=3, column=2, sticky=E)

        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        content.columnconfigure(0, weight=3)
        content.columnconfigure(1, weight=3)
        content.columnconfigure(2, weight=3)
        content.columnconfigure(3, weight=1)
        content.columnconfigure(4, weight=1)
        content.rowconfigure(1, weight=1)


if __name__ == '__main__':
    root = Tk()
    root.title('Ports')
    App(root)
    root.mainloop()
