#!/usr/bin/python3
import tkinter as tk


class LabellingNoiseBaseApp:
    def __init__(self, master=None):
        # build ui
        frame1 = tk.Frame(master)
        frame1.configure(height=200, width=200)
        labelframe1 = tk.LabelFrame(frame1)
        labelframe1.configure(height=200, text='width', width=200)
        frame2 = tk.Frame(labelframe1)
        frame2.configure(height=200, width=200)
        label1 = tk.Label(frame2)
        label1.configure(text='min')
        label1.pack(expand=True, fill="x", side="left")
        label2 = tk.Label(frame2)
        label2.configure(text='   ')
        label2.pack(expand=True, fill="x", side="left")
        label3 = tk.Label(frame2)
        label3.configure(text='max')
        label3.pack(expand=True, fill="x", side="left")
        frame2.pack(fill="x", padx=5, side="top")
        frame3 = tk.Frame(labelframe1)
        frame3.configure(height=200, width=200)
        self.spin_width_min = tk.Spinbox(frame3, name="spin_width_min")
        self.width_min = tk.IntVar()
        self.spin_width_min.configure(
            from_=0,
            increment=1,
            justify="right",
            textvariable=self.width_min,
            to=10000,
            width=8)
        self.spin_width_min.pack(expand=True, fill="x", side="left")
        label4 = tk.Label(frame3)
        label4.configure(text='   -   ')
        label4.pack(expand=True, fill="x", side="left")
        self.spin_width_max = tk.Spinbox(frame3, name="spin_width_max")
        self.width_max = tk.IntVar()
        self.spin_width_max.configure(
            from_=0,
            increment=1,
            justify="right",
            textvariable=self.width_max,
            to=10000,
            width=8)
        self.spin_width_max.pack(expand=True, fill="x", side="left")
        frame3.pack(fill="x", padx=5, pady=5, side="top")
        labelframe1.pack(fill="x", padx=5, pady=5, side="top")
        labelframe2 = tk.LabelFrame(frame1)
        labelframe2.configure(height=200, text='height', width=200)
        frame4 = tk.Frame(labelframe2)
        frame4.configure(height=200, width=200)
        label5 = tk.Label(frame4)
        label5.configure(text='min')
        label5.pack(expand=True, fill="x", side="left")
        label6 = tk.Label(frame4)
        label6.configure(text='   ')
        label6.pack(expand=True, fill="x", side="left")
        label7 = tk.Label(frame4)
        label7.configure(text='max')
        label7.pack(expand=True, fill="x", side="left")
        frame4.pack(fill="x", padx=5, side="top")
        frame8 = tk.Frame(labelframe2)
        frame8.configure(height=200, width=200)
        self.spin_height_min = tk.Spinbox(frame8, name="spin_height_min")
        self.height_min = tk.IntVar()
        self.spin_height_min.configure(
            from_=0,
            increment=1,
            justify="right",
            textvariable=self.height_min,
            to=10000,
            width=8)
        self.spin_height_min.pack(expand=True, fill="x", side="left")
        label13 = tk.Label(frame8)
        label13.configure(text='   -   ')
        label13.pack(expand=True, fill="x", side="left")
        self.spin_height_max = tk.Spinbox(frame8, name="spin_height_max")
        self.height_max = tk.IntVar()
        self.spin_height_max.configure(
            from_=0,
            increment=1,
            justify="right",
            textvariable=self.height_max,
            to=10000,
            width=8)
        self.spin_height_max.pack(expand=True, fill="x", side="left")
        frame8.pack(fill="x", padx=5, pady=5, side="top")
        labelframe2.pack(fill="x", padx=5, pady=5, side="top")
        labelframe3 = tk.LabelFrame(frame1)
        labelframe3.configure(height=200, text='area', width=200)
        frame6 = tk.Frame(labelframe3)
        frame6.configure(height=200, width=200)
        label9 = tk.Label(frame6)
        label9.configure(text='min')
        label9.pack(expand=True, fill="x", side="left")
        label10 = tk.Label(frame6)
        label10.configure(text='   ')
        label10.pack(expand=True, fill="x", side="left")
        label11 = tk.Label(frame6)
        label11.configure(text='max')
        label11.pack(expand=True, fill="x", side="left")
        frame6.pack(fill="x", padx=5, side="top")
        frame9 = tk.Frame(labelframe3)
        frame9.configure(height=200, width=200)
        self.spin_area_min = tk.Spinbox(frame9, name="spin_area_min")
        self.area_min = tk.IntVar()
        self.spin_area_min.configure(
            from_=0,
            increment=1,
            justify="right",
            textvariable=self.area_min,
            to=10000,
            width=8)
        self.spin_area_min.pack(expand=True, fill="x", side="left")
        label14 = tk.Label(frame9)
        label14.configure(text='   -   ')
        label14.pack(expand=True, fill="x", side="left")
        self.spin_area_max = tk.Spinbox(frame9, name="spin_area_max")
        self.area_max = tk.IntVar()
        self.spin_area_max.configure(
            from_=0,
            increment=1,
            justify="right",
            textvariable=self.area_max,
            to=10000,
            width=8)
        self.spin_area_max.pack(expand=True, fill="x", side="left")
        frame9.pack(fill="x", padx=5, pady=5, side="top")
        labelframe3.pack(fill="x", padx=5, pady=5, side="top")
        frame1.pack(expand=True, fill="both", side="top")

        # Main widget
        self.mainwindow = frame1

    def run(self):
        self.mainwindow.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = LabellingNoiseBaseApp(root)
    app.run()
