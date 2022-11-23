import tkinter as tk
import numpy as np
import cv2

from lib.gui.cls_edit_window import EditWindow


class InRange(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__origin_bk = img
        self.__proc_flag = False
        self.__r_h_1 = 0
        self.__g_s_1 = 0
        self.__b_v_1 = 0
        self.__r_h_2 = 255
        self.__g_s_2 = 255
        self.__b_v_2 = 255
        self.__hsv_flag = False
        self.__start_x = 0
        self.__start_y = 0
        self.__drag_flag = False
        self.__add_flag = False
        self.__select_img = []
        self.__master = master

        if len(param) == 7:
            self.__r_h_1 = param[0]
            self.__g_s_1 = param[1]
            self.__b_v_1 = param[2]
            self.__r_h_2 = param[3]
            self.__g_s_2 = param[4]
            self.__b_v_2 = param[5]
            self.__hsv_flag = param[6]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()
            self.run()
        else:
            self.dst_img = self.__inrange()

    def __init_gui(self):
        self.none_label.destroy()

        self.__hsv_bool = tk.BooleanVar()
        self.__hsv_bool.set(self.__hsv_flag)

        self.checkbutton1 = tk.Checkbutton(
            self.settings_frame, variable=self.__hsv_bool)
        self.checkbutton1.configure(text="HSV", command=self.__onClick)
        self.checkbutton1.pack(anchor="w", side="top")

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=0, to=255,
                                label='r(v)_1', orient="horizontal", command=self.__onScale)
        self.__scale1.pack(side="top")

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=0, to=255,
                                label='g(s)_1', orient="horizontal", command=self.__onScale)
        self.__scale2.pack(side="top")

        self.__scale3 = tk.Scale(self.settings_frame)
        self.__scale3.configure(from_=0, to=255,
                                label='b(h)_1', orient="horizontal", command=self.__onScale)
        self.__scale3.pack(side="top")

        self.__scale4 = tk.Scale(self.settings_frame)
        self.__scale4.configure(from_=0, to=255,
                                label='r(v)_2', orient="horizontal", command=self.__onScale)
        self.__scale4.pack(side="top")

        self.__scale5 = tk.Scale(self.settings_frame)
        self.__scale5.configure(from_=0, to=255,
                                label='g(s)_2', orient="horizontal", command=self.__onScale)
        self.__scale5.pack(side="top")

        self.__scale6 = tk.Scale(self.settings_frame)
        self.__scale6.configure(from_=0, to=255,
                                label='b(h)_2', orient="horizontal", command=self.__onScale)
        self.__scale6.pack(side="top")

        self.__scale1.set(self.__r_h_1)
        self.__scale2.set(self.__g_s_1)
        self.__scale3.set(self.__b_v_1)
        self.__scale4.set(self.__r_h_2)
        self.__scale5.set(self.__g_s_2)
        self.__scale6.set(self.__b_v_2)

        self.reset_label = tk.Label(self.settings_frame)
        self.reset_label.configure(text="select reset")
        self.reset_label.pack(side="top", fill='x')

        self.add_reset_btn = tk.Button(self.settings_frame)
        self.add_reset_btn.configure(text="reset", command=self.__select_reset)
        self.add_reset_btn.pack(side="top", fill='x')

    def __onClick(self):
        self.__hsv_flag = self.__hsv_bool.get()
        self.dst_img = self.__inrange()
        self.Draw()

    def __init_events(self):
        self.canvas1.bind("<ButtonPress-1>", self.__OnMouseDown)
        self.canvas1.bind("<ButtonRelease-1>", self.__OnMouseUp)
        self.canvas1.bind('<B1-Motion>', self.__OnMouseMove)

        if self.__master == None:
            self.mainwindow.bind("<KeyPress>", self.__keydown_event)
            self.mainwindow.bind("<KeyRelease>", self.__keyup_event)
        else:
            master = self.settings_frame.master.master.master
            master.bind("<KeyPress>", self.__keydown_event)
            master.bind("<KeyRelease>", self.__keyup_event)
        pass

    def __keydown_event(self, event):
        if event.keysym == 'Control_L':
            self.__add_flag = True

    def __keyup_event(self, event):
        pass

    def __select_reset(self):
        self.__select_img = []

    def __GetMousePos(self, pos):
        view_scale = self.GetViewScale()
        canvas_width = int(self.canvas1.winfo_width()*view_scale)
        canvas_height = int(self.canvas1.winfo_height()*view_scale)

        img_width = self.origin_img.shape[1]
        img_height = self.origin_img.shape[0]

        scale_x = img_width/canvas_width
        scale_y = img_height/canvas_height
        pos_x, pos_y = self.GetImgPos()

        if scale_x < scale_y:
            scale = scale_y
            dev = int((canvas_width-img_width/scale)/2)
            x = int((pos.x-dev)*scale)-int(pos_x*scale)
            y = int(pos.y*scale)-int(pos_y*scale)
        else:
            scale = scale_x
            dev = int((canvas_height-img_height/scale)/2)
            x = int(pos.x*scale)-int(pos_x*scale)
            y = int((pos.y-dev)*scale)-int(pos_y*scale)

        return x, y

    def __OnMouseDown(self, event):
        if not self.__add_flag:
            return

        self.__drag_flag = True
        self.__start_x, self.__start_y = self.__GetMousePos(event)

    def __OnMouseUp(self, event):
        if not self.__add_flag:
            return

        self.__add_flag = False
        self.__drag_flag = False
        self.origin_img = self.__origin_bk.copy()
        x, y = self.__GetMousePos(event)

        if x == self.__start_x and y == self.__start_y:
            return

        if self.__start_x > x:
            dummy1 = self.__start_x
            dummy2 = x
            self.__start_x = dummy2
            x = dummy1

        if self.__start_y > y:
            dummy1 = self.__start_y
            dummy2 = y
            self.__start_y = dummy2
            y = dummy1

        img1 = self.origin_img[self.__start_y:y, self.__start_x:x]
        self.__select_img.append(img1)

        total_b_h = []
        total_g_s = []
        total_r_v = []
        for img in self.__select_img:
            if self.__hsv_flag:
                img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV_FULL)

            b_h, g_s, r_v = cv2.split(img)
            total_b_h.extend(b_h[0].tolist())
            total_g_s.extend(g_s[0].tolist())
            total_r_v.extend(r_v[0].tolist())

        self.__proc_flag = True
        self.__scale1.set(min(total_r_v))
        self.__scale2.set(min(total_g_s))
        self.__scale3.set(min(total_b_h))
        self.__scale4.set(max(total_r_v))
        self.__scale5.set(max(total_g_s))
        self.__scale6.set(max(total_b_h))
        self.__proc_flag = False

        self.Draw()

    def __OnMouseMove(self, event):
        if not self.__add_flag:
            return

        if self.__drag_flag:
            x, y = self.__GetMousePos(event)
            self.origin_img = self.__origin_bk.copy()
            cv2.rectangle(self.origin_img,
                          pt1=(self.__start_x, self.__start_y),
                          pt2=(x, y),
                          color=(0, 0, 0),
                          thickness=1,
                          lineType=cv2.LINE_4,
                          shift=0)

            self.Draw()

    def __onScale(self, event):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__r_h_1 = self.__scale1.get()
        self.__g_s_1 = self.__scale2.get()
        self.__b_v_1 = self.__scale3.get()
        self.__r_h_2 = self.__scale4.get()
        self.__g_s_2 = self.__scale5.get()
        self.__b_v_2 = self.__scale6.get()
        self.dst_img = self.__inrange()
        self.Draw()
        self.__proc_flag = False
        pass

    def __inrange(self):
        img_copy = self.origin_img.copy()

        if self.__hsv_flag:
            img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV_FULL)

        img = cv2.inRange(img_copy,
                          (self.__b_v_1, self.__g_s_1, self.__r_h_1),
                          (self.__b_v_2, self.__g_s_2, self.__r_h_2))
        return img

    def get_data(self):
        param = []
        param.append(self.__r_h_1)
        param.append(self.__g_s_1)
        param.append(self.__b_v_1)
        param.append(self.__r_h_2)
        param.append(self.__g_s_2)
        param.append(self.__b_v_2)
        param.append(self.__hsv_flag)
        img = cv2.cvtColor(self.dst_img, cv2.COLOR_GRAY2BGR)
        print('Proc : inRange')
        print(f'param = {param}')
        return param, img


if __name__ == "__main__":
    # img = cv2.imread('./0000_img/I.jpg')
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [150, 188, 45, 255, 255, 109, True]
    app = InRange(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./inrange.jpg', dst_img)
