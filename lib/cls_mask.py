import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class Mask(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__mask_array = []
        self.__rect_index = 0
        self.__circle_index = 0
        self.__selected_index = -1
        self.return_img = img
        self.__proc_flag = False

        if len(param) == 1:
            self.__mask_array = param[0]
            pass
        else:
            pass

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__mask()

        if gui:
            self.__draw_mask_list()
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()
        self.radio_var = tk.IntVar()

        self.frame8 = tk.Frame(self.settings_frame)
        self.frame8.configure(height=200, width=200)
        self.frame2 = tk.Frame(self.frame8)
        self.frame2.configure(height=200, width=200)
        self.del_btn = tk.Button(self.frame2)
        self.del_btn.configure(text='Del')
        self.del_btn.pack(fill="x", padx=5, side="top")
        self.frame1 = tk.Frame(self.frame2)
        self.frame1.configure(height=200, width=200)
        self.add_rect_btn = tk.Button(self.frame1)
        self.add_rect_btn.configure(text='Add Rect')
        self.add_rect_btn.pack(expand="true", fill="x", side="left")
        self.add_circle_btn = tk.Button(self.frame1)
        self.add_circle_btn.configure(text='Add Circle')
        self.add_circle_btn.pack(expand="true", fill="x", side="left")
        self.frame1.pack(fill="x", padx=5, side="top")
        self.label1 = tk.Label(self.frame2)
        self.label1.configure(text='mask list')
        self.label1.pack(anchor="w", padx=5, side="top")
        self.mask_list = tk.Listbox(self.frame2)
        self.mask_list.pack(expand="true", fill="both", padx=5, side="top")
        self.frame2.pack(expand="true", fill="both", padx=5, side="left")
        self.frame9 = tk.Frame(self.frame8)
        self.frame9.configure(height=200, width=200)
        self.rect_frame = tk.LabelFrame(self.frame9)
        self.rect_frame.configure(height=200, text='rect', width=200)
        self.frame10 = tk.Frame(self.rect_frame)
        self.frame10.configure(height=200, width=200)
        self.scale_x1 = tk.Scale(self.frame10)
        self.scale_x1.configure(label='x1', orient="horizontal")
        self.scale_x1.pack(fill="x", side="left")
        self.entry_x1 = tk.Entry(self.frame10)
        self.entry_x1.configure(width=6)
        self.entry_x1.pack(side="bottom")
        self.frame10.pack(side="top")
        self.frame11 = tk.Frame(self.rect_frame)
        self.frame11.configure(height=200, width=200)
        self.scale_y1 = tk.Scale(self.frame11)
        self.scale_y1.configure(label='y1', orient="horizontal")
        self.scale_y1.pack(fill="x", side="left")
        self.entry_y1 = tk.Entry(self.frame11)
        self.entry_y1.configure(width=6)
        self.entry_y1.pack(side="bottom")
        self.frame11.pack(side="top")
        self.frame12 = tk.Frame(self.rect_frame)
        self.frame12.configure(height=200, width=200)
        self.scale_x2 = tk.Scale(self.frame12)
        self.scale_x2.configure(label='x2', orient="horizontal")
        self.scale_x2.pack(fill="x", side="left")
        self.entry_x2 = tk.Entry(self.frame12)
        self.entry_x2.configure(width=6)
        self.entry_x2.pack(side="bottom")
        self.frame12.pack(side="top")
        self.frame13 = tk.Frame(self.rect_frame)
        self.frame13.configure(height=200, width=200)
        self.scale_y2 = tk.Scale(self.frame13)
        self.scale_y2.configure(label='y2', orient="horizontal")
        self.scale_y2.pack(fill="x", side="left")
        self.entry_y2 = tk.Entry(self.frame13)
        self.entry_y2.configure(width=6)
        self.entry_y2.pack(side="bottom")
        self.frame13.pack(side="top")
        self.rect_frame.pack(expand="true", fill="both", side="top")
        self.circle_frame = tk.LabelFrame(self.frame9)
        self.circle_frame.configure(height=200, text='circle', width=200)
        self.frame14 = tk.Frame(self.circle_frame)
        self.frame14.configure(height=200, width=200)
        self.scale_x = tk.Scale(self.frame14)
        self.scale_x.configure(label='x', orient="horizontal")
        self.scale_x.pack(fill="x", side="left")
        self.entry_x = tk.Entry(self.frame14)
        self.entry_x.configure(width=6)
        self.entry_x.pack(side="bottom")
        self.frame14.pack(side="top")
        self.frame15 = tk.Frame(self.circle_frame)
        self.frame15.configure(height=200, width=200)
        self.scale_y = tk.Scale(self.frame15)
        self.scale_y.configure(label='y', orient="horizontal")
        self.scale_y.pack(fill="x", side="left")
        self.entry_y = tk.Entry(self.frame15)
        self.entry_y.configure(width=6)
        self.entry_y.pack(side="bottom")
        self.frame15.pack(side="top")
        self.frame16 = tk.Frame(self.circle_frame)
        self.frame16.configure(height=200, width=200)
        self.scale_radius = tk.Scale(self.frame16)
        self.scale_radius.configure(label='radius', orient="horizontal")
        self.scale_radius.pack(fill="x", side="left")
        self.entry_radius = tk.Entry(self.frame16)
        self.entry_radius.configure(width=6)
        self.entry_radius.pack(side="bottom")
        self.frame16.pack(side="top")
        self.circle_frame.pack(expand="true", fill="both", side="top")
        self.com_frame = tk.LabelFrame(self.frame9)
        self.com_frame.configure(height=200, text='com', width=200)
        self.and_radio_btn = tk.Radiobutton(self.com_frame)
        self.and_radio_btn.configure(text='AND')
        self.and_radio_btn.pack(expand="true", fill="x", side="left")
        self.or_radio_btn = tk.Radiobutton(self.com_frame)
        self.or_radio_btn.configure(text='OR')
        self.or_radio_btn.pack(expand="true", fill="x", side="left")
        self.com_frame.pack(expand="true", fill="both", side="top")
        self.frame9.pack(side="top")
        self.frame8.pack(expand="true", fill="y", side="top")

        self.and_radio_btn.configure(value=1, variable=self.radio_var)
        self.or_radio_btn.configure(value=0, variable=self.radio_var)
        self.param_frame_show(0)

    def __init_events(self):
        self.add_rect_btn.bind('<1>', self.__onClick_add_rect)
        self.add_circle_btn.bind('<1>', self.__onClick_add_circle)
        self.mask_list.bind("<<ListboxSelect>>", self.__onSelectListBox_Events)
        self.and_radio_btn.configure(command=self.__onCkick_radio)
        self.or_radio_btn.configure(command=self.__onCkick_radio)
        self.scale_x1.configure(command=self.__onScale_rect)
        self.scale_y1.configure(command=self.__onScale_rect)
        self.scale_x2.configure(command=self.__onScale_rect)
        self.scale_y2.configure(command=self.__onScale_rect)
        self.entry_x1.bind('<Return>', self.__onEnter_rect)
        self.entry_y1.bind('<Return>', self.__onEnter_rect)
        self.entry_x2.bind('<Return>', self.__onEnter_rect)
        self.entry_y2.bind('<Return>', self.__onEnter_rect)
        self.del_btn.bind('<1>', self.__onClick_del)
        self.scale_x.configure(command=self.__onScale_circle)
        self.scale_y.configure(command=self.__onScale_circle)
        self.scale_radius.configure(command=self.__onScale_circle)

    def param_frame_show(self, mode):
        if mode == 0:
            self.rect_frame.pack_forget()
            self.circle_frame.pack_forget()
            self.com_frame.pack_forget()
            self.frame9.pack_forget()
        elif mode == 1:
            self.param_frame_show(0)
            self.frame9.pack(side="top")
            self.rect_frame.pack(expand="true", fill="both", side="top")
            self.com_frame.pack(expand="true", fill="both", side="top")
        elif mode == 2:
            self.param_frame_show(0)
            self.frame9.pack(side="top")
            self.circle_frame.pack(expand="true", fill="both", side="top")
            self.com_frame.pack(expand="true", fill="both", side="top")

    def __onClick_del(self, event):
        index = self.__selected_index
        if index == -1:
            return
        self.__mask_array.pop(index)
        if len(self.__mask_array) == 0:
            self.param_frame_show(0)
        self.__selected_index = -1
        self.__draw_mask_list()
        self.__redraw()

    def __onEnter_rect(self, event):
        x1, y1, x2, y2 = self.__get_entry_rect()
        self.__set_scale_rect([x1, y1, x2, y2])
        self.__onScale_rect(None)

    def __get_entry_rect(self):
        x1 = self.entry_x1.get()
        y1 = self.entry_y1.get()
        x2 = self.entry_x2.get()
        y2 = self.entry_y2.get()
        return x1, y1, x2, y2

    def __set_scale_rect(self, param):
        self.scale_x1.set(param[0])
        self.scale_y1.set(param[1])
        self.scale_x2.set(param[2])
        self.scale_y2.set(param[3])

    def __get_scale_circle(self):
        x = self.scale_x.get()
        y = self.scale_y.get()
        radius = self.scale_radius.get()
        return x, y, radius

    def __onScale_circle(self, event):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        index = self.__selected_index
        x, y, radius = self.__get_scale_circle()
        self.__mask_array[index][2] = x
        self.__mask_array[index][3] = y
        self.__mask_array[index][4] = radius
        self.entry_x.delete("0", "end")
        self.entry_x.insert("0", x)
        self.entry_y.delete("0", "end")
        self.entry_y.insert("0", y)
        self.entry_radius.delete("0", "end")
        self.entry_radius.insert("0", radius)
        self.__redraw()
        self.__proc_flag = False

    def __onScale_rect(self, event):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        index = self.__selected_index
        x1 = self.scale_x1.get()
        y1 = self.scale_y1.get()
        x2 = self.scale_x2.get()
        y2 = self.scale_y2.get()
        self.__mask_array[index][2] = x1
        self.__mask_array[index][3] = y1
        self.__mask_array[index][4] = x2
        self.__mask_array[index][5] = y2
        self.entry_x1.delete("0", "end")
        self.entry_x1.insert("0", x1)
        self.entry_y1.delete("0", "end")
        self.entry_y1.insert("0", y1)
        self.entry_x2.delete("0", "end")
        self.entry_x2.insert("0", x2)
        self.entry_y2.delete("0", "end")
        self.entry_y2.insert("0", y2)
        self.__redraw()
        self.__proc_flag = False

    def __onCkick_radio(self):
        index = self.__selected_index
        col = 0
        if self.__mask_array[index][0] == 'rect':
            col = 6
        elif self.__mask_array[index][0] == 'circle':
            col = 5
        if self.radio_var.get():
            self.__mask_array[index][col] = True    # AND
        else:
            self.__mask_array[index][col] = False   # OR
        self.__redraw()

    def __onSelectListBox_Events(self, event):
        if self.mask_list.curselection() == ():
            return

        self.__selected_index = self.mask_list.curselection()[0]
        index = self.__selected_index
        if self.__mask_array[index][0] == 'rect':
            self.param_frame_show(1)
            x1 = self.__mask_array[index][2]
            y1 = self.__mask_array[index][3]
            x2 = self.__mask_array[index][4]
            y2 = self.__mask_array[index][5]
            height, width, _ = self.origin_img.shape
            self.scale_x1.configure(from_=0, to=width)
            self.scale_y1.configure(from_=0, to=height)
            self.scale_x2.configure(from_=x1, to=width)
            self.scale_y2.configure(from_=y1, to=height)
            self.__set_scale_rect([x1, y1, x2, y2])
            if not self.__mask_array[index][6]:
                self.radio_var.set(0)
            else:
                self.radio_var.set(1)
        elif self.__mask_array[index][0] == 'circle':
            self.param_frame_show(2)
            x = self.__mask_array[index][2]
            y = self.__mask_array[index][3]
            radius = self.__mask_array[index][4]
            height, width, _ = self.origin_img.shape
            self.scale_x.configure(from_=0, to=width)
            self.scale_y.configure(from_=0, to=height)
            self.scale_radius.configure(from_=0, to=width)
            self.scale_x.set(x)
            self.scale_y.set(y)
            self.scale_radius.set(radius)
            if not self.__mask_array[index][5]:
                self.radio_var.set(0)
            else:
                self.radio_var.set(1)
            pass
        self.__redraw()

    def __add_circle(self):
        height, width, _ = self.origin_img.shape
        x = int(width/2)
        y = int(height/2)
        radius = int(width/3)
        params = ['circle',                         # mode          0
                  f'circle{self.__circle_index}',   # name          1
                  x, y, radius,                     # rect          2-4
                  False,                            # AND/OR        5
                  False]                            # select_flag   6
        self.__circle_index += 1
        self.__add_mask(params, 2)

    def __add_rect(self):
        height, width, _ = self.origin_img.shape
        x1 = 0
        y1 = 0
        x2 = int(width/2)
        y2 = int(height/2)
        params = ['rect',                       # mode          0
                  f'rect{self.__rect_index}',   # name          1
                  x1, y1, x2, y2,               # rect          2-5
                  False,                        # AND/OR        6
                  False]                        # select_flag   7
        self.__rect_index += 1
        self.__add_mask(params, 1)

    def __add_mask(self, params, mode):
        mask = []
        for param in params:
            mask.append(param)

        self.__mask_array.append(mask)
        self.__rect_index += 1
        self.__draw_mask_list()
        self.mask_list.select_set(len(self.__mask_array)-1)
        self.param_frame_show(mode)
        self.__onSelectListBox_Events(None)
        self.__redraw()

    def __onClick_add_circle(self, event):
        # self.mainwindow.after(1, self.__add_circle)
        self.settings_frame.after(1, self.__add_circle)

    def __onClick_add_rect(self, event):
        # self.mainwindow.after(1, self.__add_rect)
        self.settings_frame.after(1, self.__add_rect)

    def __draw_mask_list(self):
        self.mask_list.delete(0, tk.END)
        for mask in self.__mask_array:
            self.mask_list.insert(tk.END, mask[1])

    def __redraw(self):
        self.dst_img = self.__mask()
        self.Draw()

    def __mask(self):
        img_copy = self.origin_img.copy()
        height, width, _ = img_copy.shape
        for mask in self.__mask_array:
            mask_img = np.zeros((height, width, 3), np.uint8)
            color = (255, 255, 255)
            col = 0
            if mask[0] == 'rect':
                mask_img = cv2.rectangle(mask_img,
                                         (mask[2], mask[3]),
                                         (mask[4], mask[5]),
                                         color, -1)
                col = 6
            elif mask[0] == 'circle':
                mask_img = cv2.circle(mask_img,
                                      (mask[2], mask[3]),
                                      mask[4],
                                      color, -1)
                col = 5
            if not mask[col]:
                mask_img = cv2.bitwise_not(mask_img)
            img_copy = cv2.bitwise_and(img_copy, mask_img)
        self.return_img = img_copy.copy()
        index = self.__selected_index
        if index == -1:
            return img_copy
        if self.__mask_array[index][0] == 'rect':
            x1 = self.__mask_array[index][2]
            y1 = self.__mask_array[index][3]
            x2 = self.__mask_array[index][4]
            y2 = self.__mask_array[index][5]
            img_copy = cv2.rectangle(img_copy,
                                     (x1, y1),
                                     (x2, y2),
                                     (0, 0, 255), 5)
        elif self.__mask_array[index][0] == 'circle':
            x = self.__mask_array[index][2]
            y = self.__mask_array[index][3]
            radius = self.__mask_array[index][4]
            img_copy = cv2.circle(img_copy,
                                  (x, y),
                                  radius,
                                  (0, 0, 255), 5)
        return img_copy

    def get_data(self):
        param = []
        param = [self.__mask_array]
        print('Proc : Mask')
        print(f'param = {param}')
        return param, self.return_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/ECU/ECUlow_base.jpg')
    param = []
    param = [[['circle', 'circle0', 1280, 957, 787, True, False],
              ['circle', 'circle1', 1287, 955, 137, False, False]]]
    app = Mask(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Mask.jpg', dst_img)
