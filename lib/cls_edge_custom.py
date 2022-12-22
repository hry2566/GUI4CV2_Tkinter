"""エッジ位置計測(カスタム)"""
import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class EdgeCustom(EditWindow):
    """エッジ位置計測(カスタム)クラス"""

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
        else:
            pass

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__edge_custom()

        if gui:
            self.draw()
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
            text='horizontal', command=self.__on_click_radio)
        self.radio_horizontal.pack(anchor="w", side="top")
        self.redio_virtical = tk.Radiobutton(
            self.labelframe4, value=1, variable=self.var)
        self.redio_virtical.configure(
            text='virtical', command=self.__on_click_radio)
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

    def __init_events(self):
        self.canvas1.bind("<ButtonPress-1>", self.__on_mouse_down)
        self.canvas1.bind("<ButtonRelease-1>", self.__on_mouse_up)
        self.canvas1.bind('<B1-Motion>', self.__on_mouse_move)

    def __on_click_radio(self):
        self.direction_mode = self.var.get()
        self.dst_img = self.__edge_custom()
        self.draw()

    # def __onScale(self, events):
    #     pass

    def __on_mouse_down(self, event):
        self.__drag_flag = True
        self.__start_x, self.__start_y = self.__get_mouse_pos(event)

    def __on_mouse_up(self, event):
        self.__drag_flag = False

        pos_x, pos_y = self.__get_mouse_pos(event)
        if self.__start_x > pos_x:
            dummy1 = self.__start_x
            dummy2 = pos_x
            self.__start_x = dummy2
            pos_x = dummy1

        if self.__start_y > pos_y:
            dummy1 = self.__start_y
            dummy2 = pos_y
            self.__start_y = dummy2
            pos_y = dummy1
        self.__finish_x = pos_x
        self.__finish_y = pos_y

        self.area_x1.delete(0, tk.END)
        self.area_x1.insert(0, self.__start_x)
        self.area_y1.delete(0, tk.END)
        self.area_y1.insert(0, self.__start_y)
        self.area_x2.delete(0, tk.END)
        self.area_x2.insert(0, self.__finish_x)
        self.area_y2.delete(0, tk.END)
        self.area_y2.insert(0, self.__finish_y)

        self.dst_img = self.__edge_custom()
        self.draw()

    def __on_mouse_move(self, event):
        if self.__drag_flag:
            pos_x, pos_y = self.__get_mouse_pos(event)
            self.dst_img = self.__origin_bk.copy()
            cv2.rectangle(self.dst_img,
                          pt1=(self.__start_x, self.__start_y),
                          pt2=(pos_x, pos_y),
                          color=(255, 0, 0),
                          thickness=1,
                          lineType=cv2.LINE_4,
                          shift=0)
            self.draw()

    def __get_mouse_pos(self, pos):
        view_scale = self.get_view_scale()
        canvas_width = int(self.canvas1.winfo_width()*view_scale)
        canvas_height = int(self.canvas1.winfo_height()*view_scale)

        img_width = self.origin_img.shape[1]
        img_height = self.origin_img.shape[0]

        scale_x = img_width/canvas_width
        scale_y = img_height/canvas_height
        pos_x, pos_y = self.get_img_pos()

        if scale_x < scale_y:
            scale = scale_y
            dev = int((canvas_width-img_width/scale)/2)
            pos_x = int((pos.x-dev)*scale)-int(pos_x*scale)
            pos_y = int(pos.y*scale)-int(pos_y*scale)
        else:
            scale = scale_x
            dev = int((canvas_height-img_height/scale)/2)
            pos_x = int(pos.x*scale)-int(pos_x*scale)
            pos_y = int((pos.y-dev)*scale)-int(pos_y*scale)

        return pos_x, pos_y

    def __edge_custom(self):
        img_copy = self.origin_img.copy()
        img_copy = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)

        whole_area = img_copy.size
        white_area = cv2.countNonZero(img_copy)
        black_area = whole_area-white_area

        if white_area > black_area:
            img_copy = 255-img_copy

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

        mask = cv2.bitwise_and(img_copy, mask)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        if self.__gui:
            self.resoult_list.delete(0, self.resoult_list.size())
        self.__line_array = []

        img_copy = self.origin_img.copy()
        for cont in contours:
            vec_x, vec_y, x_0, y_0 = cv2.fitLine(
                cont, cv2.DIST_L2, 10, 0.01, 0.01)

            if self.direction_mode == 0:
                vec_x = round(vec_x[0])
                vec_y = round(vec_y[0])
                y_1 = mask_y1
                y_2 = mask_y2
                x_1 = int(y_1*vec_x+x_0)
                x_2 = int(y_2*vec_x+x_0)
            else:
                vec_x = round(vec_x[0])
                vec_y = round(vec_y[0])
                x_1 = mask_x1
                x_2 = mask_x2
                y_1 = int(x_1*vec_y+y_0)
                y_2 = int(x_2*vec_y+y_0)

            if mask_x1 <= x_1 and mask_x2 >= x_2 and mask_y1 <= y_1 and mask_y2 >= y_2:
                img_copy = cv2.line(img_copy,
                                    pt1=(x_1, y_1),
                                    pt2=(x_2, y_2),
                                    color=(0, 0, 255),
                                    thickness=1)
                add_flag = self.__add_list([x_1, y_1, x_2, y_2])
                if add_flag:
                    self.__line_array.append([x_1, y_1, x_2, y_2])

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

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__start_x)
        param.append(self.__start_y)
        param.append(self.__finish_x)
        param.append(self.__finish_y)
        param.append(self.direction_mode)
        param.append(self.__line_array)
        if self.__gui:
            print('Proc : EdgeCustom')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     # img = cv2.imread('./0000_img/edge2.png')
#     # img = cv2.imread('./edge6_1.png')
#     # img = cv2.imread('./edge6_2.png')
#     img = cv2.imread('./horizontal.png')
#     param = []
#     app = EdgeCustom(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./EdgeCustom.jpg', dst_img)
