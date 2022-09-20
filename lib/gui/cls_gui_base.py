#!/usr/bin/python3
import tkinter as tk


class GuiBase:
    def __init__(self, master=None):
        self.master = master
        # build ui
        if master == None:
            toplevel1 = tk.Tk() if master is None else tk.Toplevel(master)
            toplevel1.configure(height=200, width=200)
            self.image_edit_frame = tk.Frame(toplevel1)
        else:
            self.image_edit_frame = tk.Frame(master)

        self.image_edit_frame.configure(height=200, padx=5, pady=5, width=200)
        self.settings_frame = tk.LabelFrame(self.image_edit_frame)
        self.settings_frame.configure(height=200, text="settings", width=200)
        self.none_label = tk.Label(self.settings_frame)
        self.none_label.configure(text="none label")
        self.none_label.pack(side="top")
        self.settings_frame.pack(fill="y", side="left")
        image_view_frame = tk.LabelFrame(self.image_edit_frame)
        image_view_frame.configure(
            height=200, text="image view", width=200)
        self.canvas1 = tk.Canvas(image_view_frame)
        self.canvas1.pack(expand="true", fill="both", side="top")
        frame5 = tk.Frame(image_view_frame)
        frame5.configure(height=200, width=200)
        self.image_switch_btn = tk.Button(frame5)
        self.image_switch_btn.configure(text="button1")
        self.image_switch_btn.pack(side="right")
        self.image_reset_btn = tk.Button(frame5)
        self.image_reset_btn.configure(text="button2")
        self.image_reset_btn.pack(side="right")
        frame5.pack(fill="x", side="top")
        image_view_frame.pack(expand="true", fill="both", side="left")
        self.image_edit_frame.pack(expand="true", fill="both", side="top")

        if master == None:
            # Main widget
            self.mainwindow = toplevel1

    def run(self):
        if self.master == None:
            self.mainwindow.mainloop()
        pass


if __name__ == "__main__":
    app = GuiBase()
    app.run()
