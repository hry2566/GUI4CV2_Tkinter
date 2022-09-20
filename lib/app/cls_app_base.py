#!/usr/bin/python3
import tkinter as tk
import tkinter.ttk as ttk


class App_Base:
    def __init__(self, master=None):
        # build ui
        self.toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        self.toplevel1.configure(height=200, width=200)
        self.frame1 = tk.Frame(self.toplevel1)
        self.frame1.configure(height=200, padx=5, pady=5, width=200)
        __values = ['a']
        self.tkvar = tk.StringVar()
        self.optionmenu1 = tk.OptionMenu(
            self.frame1, self.tkvar, *__values, command=None)
        self.optionmenu1.pack(fill="x", side="top")
        self.frame3 = tk.Frame(self.frame1)
        self.frame3.configure(height=200, width=200)
        self.add_btn = tk.Button(self.frame3)
        self.add_btn.configure(text="Add")
        self.add_btn.pack(expand="true", fill="x", side="left")
        self.del_btn = tk.Button(self.frame3)
        self.del_btn.configure(text="Del")
        self.del_btn.pack(expand="true", fill="x", side="left")
        self.frame3.pack(fill="x", side="top")
        self.task_list = tk.Listbox(self.frame1)
        self.task_list.pack(expand="true", fill="both", side="top")
        self.set_param_btn = ttk.Button(self.frame1)
        self.set_param_btn.configure(text="Set Param")
        self.set_param_btn.pack(fill="x", side="top")
        self.create_code_btn = tk.Button(self.frame1)
        self.create_code_btn.configure(text="Create Python Code")
        self.create_code_btn.pack(fill="x", side="top")
        self.frame1.pack(fill="y", side="left")
        self.dummy_frame = tk.Frame(self.toplevel1)
        self.dummy_frame.configure(height=200, padx=5, pady=5, width=200)
        self.dummy_frame.pack(expand="true", fill="both", side="left")

        # Main widget
        self.appwindow = self.toplevel1

    def run(self):
        self.appwindow.mainloop()


if __name__ == "__main__":
    app = App_Base()
    app.run()
