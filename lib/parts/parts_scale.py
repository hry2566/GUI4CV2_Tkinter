import tkinter as tk
from functools import partial


class Parts_Scale():
    def __init__(self, master):
        self.__val = tk.StringVar()
        self.__max = 100
        self.__min = 0
        self.__changed_proc = None
        self.master = master

        self.__lblframe = tk.LabelFrame(master)
        self.__lblframe.configure(text='scale')
        self.__frame = tk.Frame(self.__lblframe)
        self.__frame.configure(height=200, width=200)
        self.__leftbtn = tk.Button(self.__frame)
        self.__leftbtn.configure(text='<', width=1)
        self.__leftbtn.pack(side="left")
        self.__scale = tk.Scale(self.__frame)
        self.__scale.configure(orient="horizontal", showvalue="false")
        self.__scale.pack(expand="true", fill="x", side="left")
        self.__rightbtn = tk.Button(self.__frame)
        self.__rightbtn.configure(text='>')
        self.__rightbtn.pack(side="left")
        self.__entry = tk.Entry(self.__frame)
        self.__entry.configure(width=6, justify="right")
        self.__entry.pack(padx=5, side="left")
        self.__frame.pack(side="top", fill='x', padx=5, pady=5)
        self.__lblframe.pack(side="top",  fill='x', padx=5)
        self.__init_gui()
        self.__init_events()

    def __init_gui(self):
        self.__scale.configure(variable=self.__val)
        self.set(0)

    def __init_events(self):
        self.__scale.configure(command=self.__onScale)
        self.__entry.bind('<Return>', self.__onKey)
        self.__leftbtn.bind('<1>', self.__onClick_left)
        self.__rightbtn.bind('<1>', self.__onClick_right)

    def __onClick_right(self, event):
        val = int(self.__val.get())+1
        if val > self.__max:
            val = self.__max
        self.set(val)

    def __onClick_left(self, event):
        val = int(self.__val.get())-1
        if val < self.__min:
            val = self.__min
        self.set(val)

    def __onKey(self, event):
        self.set(self.__entry.get())

    def __onScale(self, event):
        self.__entry.delete(0, tk.END)
        self.__entry.insert(0, self.__val.get())
        self.__callback()

    def __callback(self):
        if self.__changed_proc == None:
            return
        self.__handler(self.__changed_proc)

    def __handler(self, func, *args):
        return func(*args)

    def set(self, val):
        self.__val.set(val)
        self.__entry.delete(0, tk.END)
        self.__entry.insert(0, self.__val.get())
        self.__callback()

    def configure(self, padx=None, pady=None, label=None, side=None, from_=None, to=None, resolution=None):
        self.__lblframe.configure(text=label)
        self.__lblframe.pack(side=side, padx=padx, pady=pady)
        self.__scale.configure(from_=from_, to=to, resolution=resolution)

        if not to == None:
            self.__max = to
        if not from_ == None:
            self.__min = from_

    def get(self):
        if self.__scale['resolution'] == 1.0:
            return int(self.__val.get())
        else:
            return float(self.__val.get())

    def bind(self, changed=None):
        self.__changed_proc = changed
