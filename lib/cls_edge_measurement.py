from decimal import ROUND_HALF_UP, Decimal
import random
import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class EdgeMeasurement(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__origin_bk = img
        self.__drag_flag = False
        self.__start_x = 0
        self.__start_y = 0
        self.__finish_x = 0
        self.__finish_y = 0
        self.__line_array = []
        self.__gui = gui
        self.direction_mode = 0
        self.__gui = gui

        if len(param) == 6:
            self.__start_x = param[0]
            self.__start_y = param[1]
            self.__finish_x = param[2]
            self.__finish_y = param[3]
            self.direction_mode = param[4]
            self.__line_array = param[5]
            pass
        else:
            pass

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__edge_location_measurement()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.var = tk.IntVar()
        self.var.set(self.direction_mode)

        self.frame3 = tk.Frame(self.settings_frame)
        self.frame3.configure(height=200, width=200)
        self.labelframe4 = tk.LabelFrame(self.frame3)
        self.labelframe4.configure(
            height=200, text='edge direction', width=200)
        self.radio_horizontal = tk.Radiobutton(
            self.labelframe4, value=0, variable=self.var)
        self.radio_horizontal.configure(
            text='horizontal', command=self.__onClick_radio)
        self.radio_horizontal.pack(anchor="w", side="top")
        self.redio_virtical = tk.Radiobutton(
            self.labelframe4, value=1, variable=self.var)
        self.redio_virtical.configure(
            text='virtical', command=self.__onClick_radio)
        self.redio_virtical.pack(anchor="w", side="top")
        self.labelframe4.pack(
            expand="true",
            fill="both",
            padx=5,
            pady=5,
            side="left")
        self.labelframe5 = tk.LabelFrame(self.frame3)
        self.labelframe5.configure(
            height=200, text='seach direction', width=200)
        self.redio_left2right = tk.Radiobutton(self.labelframe5)
        self.redio_left2right.configure(text='left to right')
        self.redio_left2right.pack(anchor="w", side="top")
        self.radio_right2left = tk.Radiobutton(self.labelframe5)
        self.radio_right2left.configure(text='right to left')
        self.radio_right2left.pack(anchor="w", side="top")
        self.radio_top2bottom = tk.Radiobutton(self.labelframe5)
        self.radio_top2bottom.configure(text='top to bottom')
        self.radio_top2bottom.pack(anchor="w", side="top")
        self.radio_bottom2top = tk.Radiobutton(self.labelframe5)
        self.radio_bottom2top.configure(text='bottom to top')
        self.radio_bottom2top.pack(anchor="w", side="top")
        self.labelframe5.pack(
            expand="true",
            fill="both",
            padx=5,
            pady=5,
            side="left")
        self.frame3.pack(fill="x", side="top")
        self.labelframe2 = tk.LabelFrame(self.settings_frame)
        self.labelframe2.configure(height=200, text='area', width=200)
        self.frame1 = tk.Frame(self.labelframe2)
        self.frame1.configure(height=200, width=200)
        self.label1 = tk.Label(self.frame1)
        self.label1.configure(text='x1')
        self.label1.pack(padx=5, side="top")
        self.label2 = tk.Label(self.frame1)
        self.label2.configure(text='y1')
        self.label2.pack(padx=5, side="top")
        self.label3 = tk.Label(self.frame1)
        self.label3.configure(text='x2')
        self.label3.pack(padx=5, side="top")
        self.label4 = tk.Label(self.frame1)
        self.label4.configure(text='y2')
        self.label4.pack(padx=5, side="top")
        self.frame1.pack(side="left")
        self.frame2 = tk.Frame(self.labelframe2)
        self.frame2.configure(height=200, width=200)
        self.area_x1 = tk.Entry(self.frame2)
        self.area_x1.pack(fill="x", padx=5, side="top")
        self.area_y1 = tk.Entry(self.frame2)
        self.area_y1.pack(fill="x", padx=5, side="top")
        self.area_x2 = tk.Entry(self.frame2)
        self.area_x2.pack(fill="x", padx=5, side="top")
        self.area_y2 = tk.Entry(self.frame2)
        self.area_y2.pack(fill="x", padx=5, side="top")
        self.frame2.pack(expand="true", fill="x", side="left")
        self.labelframe2.pack(fill="x", padx=5, pady=5, side="top")
        self.labelframe3 = tk.LabelFrame(self.settings_frame)
        self.labelframe3.configure(height=200, text='resoult', width=200)
        self.resoult_list = tk.Listbox(self.labelframe3)
        self.resoult_list.configure(width=40)
        self.resoult_list.pack(
            expand="true",
            fill="both",
            padx=5,
            pady=5,
            side="top")
        self.labelframe3.pack(fill="x", padx=5, pady=5, side="top")

        self.direction_mode = self.var.get()
        pass

    def __init_events(self):
        self.canvas1.bind("<ButtonPress-1>", self.__OnMouseDown)
        self.canvas1.bind("<ButtonRelease-1>", self.__OnMouseUp)
        self.canvas1.bind('<B1-Motion>', self.__OnMouseMove)
        pass

    def __onScale(self, events):
        pass

    def __onClick_radio(self):
        self.direction_mode = self.var.get()
        self.dst_img = self.__edge_location_measurement()
        self.Draw()
        pass

    def __OnMouseDown(self, event):
        self.__drag_flag = True
        self.__start_x, self.__start_y = self.__GetMousePos(event)
        pass

    def __OnMouseUp(self, event):
        self.__drag_flag = False

        x, y = self.__GetMousePos(event)
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
        self.__finish_x = x
        self.__finish_y = y

        self.area_x1.delete(0, tk.END)
        self.area_x1.insert(0, self.__start_x)
        self.area_y1.delete(0, tk.END)
        self.area_y1.insert(0, self.__start_y)
        self.area_x2.delete(0, tk.END)
        self.area_x2.insert(0, self.__finish_x)
        self.area_y2.delete(0, tk.END)
        self.area_y2.insert(0, self.__finish_y)

        self.dst_img = self.__edge_location_measurement()
        self.Draw()

    def __OnMouseMove(self, event):
        if self.__drag_flag:
            x, y = self.__GetMousePos(event)
            self.dst_img = self.__origin_bk.copy()
            cv2.rectangle(self.dst_img,
                          pt1=(self.__start_x, self.__start_y),
                          pt2=(x, y),
                          color=(255, 0, 0),
                          thickness=1,
                          lineType=cv2.LINE_4,
                          shift=0)
            self.Draw()
        pass

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

    def __edge_location_measurement(self):
        img_copy = self.origin_img.copy()
        img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

        if self.direction_mode == 0:
            kernel = np.array([[0, 0, 0],
                               [1, -2, 1],
                               [0, 0, 0]])
        else:
            kernel = np.array([[0, 1, 0],
                               [0, -2, 0],
                               [0, 1, 0]])

        img_copy = cv2.filter2D(img_copy, -1, kernel, delta=128)

        _, img = cv2.threshold(
            img_copy, 0, 255, cv2.THRESH_BINARY_INV + cv2.THRESH_OTSU)

        whole_area = img.size
        white_area = cv2.countNonZero(img)
        black_area = whole_area-white_area

        if white_area > black_area:
            _, img = cv2.threshold(img_copy, 0, 255, cv2.THRESH_OTSU)

        mask_x1 = self.__start_x
        mask_y1 = self.__start_y
        mask_x2 = self.__finish_x
        mask_y2 = self.__finish_y

        mask = np.zeros(img_copy.shape, dtype="uint8")
        mask = cv2.rectangle(mask,
                             pt1=(mask_x1, mask_y1),
                             pt2=(mask_x2, mask_y2),
                             color=(255, 255, 255),
                             thickness=-1)

        mask = cv2.bitwise_and(img, mask)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if self.__gui:
            self.resoult_list.delete(0, self.resoult_list.size())
        self.__line_array = []

        img_copy = self.origin_img.copy()
        for cont in contours:
            vx, vy, x0, y0 = cv2.fitLine(cont, cv2.DIST_L2, 0, 0.01, 0.01)

            if self.direction_mode == 0:
                vx = round(vx[0])
                vy = round(vy[0])
                y1 = mask_y1
                y2 = mask_y2
                x1 = int(y1*vx+x0)
                x2 = int(y2*vx+x0)
            else:
                vx = round(vx[0])
                vy = round(vy[0])
                x1 = mask_x1
                x2 = mask_x2
                y1 = int(x1*vy+y0)
                y2 = int(x2*vy+y0)

            if mask_x1 <= x1 and mask_x2 >= x2 and mask_y1 <= y1 and mask_y2 >= y2:
                img_copy = cv2.line(img_copy,
                                    pt1=(x1, y1),
                                    pt2=(x2, y2),
                                    color=(0, 0, 255),
                                    thickness=1)
                add_flag = self.__add_list([x1, y1, x2, y2])
                if add_flag:
                    self.__line_array.append([x1, y1, x2, y2])
                    pass

        img_copy = cv2.rectangle(img_copy,
                                 pt1=(mask_x1, mask_y1),
                                 pt2=(mask_x2, mask_y2),
                                 color=(255, 0, 0),
                                 thickness=1)
        img = img_copy
        return img

    def __add_list(self, data):
        add_data = f'x1={data[0]} y1={data[1]} x2={data[2]} y2={data[3]}'

        if self.__gui:
            for index in range(self.resoult_list.size()):
                if add_data == self.resoult_list.get(index):
                    return False

            self.resoult_list.insert(0, add_data)
        return True

    def get_data(self):
        param = []
        param.append(self.__start_x)
        param.append(self.__start_y)
        param.append(self.__finish_x)
        param.append(self.__finish_y)
        param.append(self.direction_mode)
        param.append(self.__line_array)
        if self.__gui:
            print('Proc : EdgeMeasurement')
            print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/edge2.png')
    # img = cv2.imread('./edge6_1.png')
    # img = cv2.imread('./edge6_2.png')
    # img = cv2.imread('./0000_img/edge1.png')
    param = []
    app = EdgeMeasurement(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./EdgeMeasurement.jpg', dst_img)
