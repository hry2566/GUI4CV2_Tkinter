#!/usr/bin/python3
import tkinter as tk


class PartsSwitchButtonBaseApp:
    def __init__(self, master=None):
        # build ui
        # toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
        toplevel1 = tk.Tk() if master is None else master
        toplevel1.configure(height=200, width=200)
        frame1 = tk.Frame(toplevel1)
        frame1.configure(height=200, width=200)
        self.lbl = tk.Label(frame1, name="lbl")
        self.lbl.configure(text='camra')
        self.lbl.pack(side="left")
        self.scale_button = tk.Scale(frame1, name="scale_button")
        self.scale_button.configure(
            activebackground="#008040",
            background="#008040",
            from_=0,
            orient="horizontal",
            showvalue=False,
            sliderrelief="flat",
            to=1)
        self.scale_button.pack(expand=True, fill="x", side="left")
        self.lbl_state = tk.Label(frame1, name="lbl_state")
        self.lbl_state.configure(state="normal", text='OFF')
        self.lbl_state.pack(side="left")
        frame1.pack(fill="x", side="top")

        # Main widget
        self.mainwindow = toplevel1

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    app = PartsSlideButtonBaseApp()
    app.run()
