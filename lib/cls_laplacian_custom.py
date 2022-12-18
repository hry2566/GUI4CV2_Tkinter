import os
import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class Laplacian_Custom(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__k = 1
        self.__noise_cut = 0
        self.__select_menu = 0
        self.direction_mode = 0
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 4:
            self.__k = param[0]
            self.__noise_cut = param[1]
            self.__select_menu = param[2]
            self.direction_mode = param[3]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.Laplacian_Custom()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.var = tk.IntVar()
        self.var.set(self.direction_mode)

        self.radio_horizontal = tk.Radiobutton(
            self.settings_frame, value=0, variable=self.var)
        self.radio_horizontal.configure(
            text='horizontal', command=self.__onClick_radio)
        self.radio_horizontal.pack(anchor="w", side="top")
        self.redio_virtical = tk.Radiobutton(
            self.settings_frame, value=1, variable=self.var)
        self.redio_virtical.configure(
            text='virtical', command=self.__onClick_radio)
        self.redio_virtical.pack(anchor="w", side="top")

        self.__scale3 = Parts_Scale(self.settings_frame)
        self.__scale3.configure(label='k', side='top',
                                resolution=0.1, from_=0.1, to=2)
        self.__scale4 = Parts_Scale(self.settings_frame)
        self.__scale4.configure(label='remove noise',
                                side='top', from_=0, to=128)

        self.__tkvar = tk.StringVar(value=None)
        __values = ['明', '暗', '明＋暗']
        self.optionmenu1 = tk.OptionMenu(
            self.settings_frame, self.__tkvar, 'None', *__values, command=self.__onSelect)
        self.optionmenu1.pack(side='top', fill='x')

        self.direction_mode = self.var.get()
        self.__scale3.set(self.__k)
        self.__scale4.set(self.__noise_cut)

        if self.__select_menu == 0:
            self.__tkvar.set(None)
        elif self.__select_menu == 1:
            self.__tkvar.set('明')
        elif self.__select_menu == 2:
            self.__tkvar.set('暗')
        elif self.__select_menu == 3:
            self.__tkvar.set('明＋暗')
        pass

    def __init_events(self):
        self.__scale3.bind(changed=self.__onScale)
        self.__scale4.bind(changed=self.__onScale)

    def __onScale(self):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__k = self.__scale3.get()
        self.__noise_cut = self.__scale4.get()
        self.dst_img = self.Laplacian_Custom()
        self.Draw()
        self.__proc_flag = False
        pass

    def __onClick_radio(self):
        self.direction_mode = self.var.get()
        self.dst_img = self.Laplacian_Custom()
        self.Draw()

    def __onSelect(self, event):
        if self.__tkvar.get() == 'None':
            self.__select_menu = 0
        elif self.__tkvar.get() == '明':
            self.__select_menu = 1
        elif self.__tkvar.get() == '暗':
            self.__select_menu = 2
        elif self.__tkvar.get() == '明＋暗':
            self.__select_menu = 3

        self.dst_img = self.Laplacian_Custom()
        self.Draw()

    def Laplacian_Custom(self):
        img_copy = self.origin_img.copy()
        img = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        height, width = img.shape[:2]

        if self.direction_mode == 0:
            kernel = np.array([[0, 0, 0],
                               [self.__k, -(self.__k*2), self.__k],
                               [0, 0, 0]
                               ])
        else:
            kernel = np.array([[0, self.__k, 0],
                               [0, -(self.__k*2), 0],
                               [0, self.__k, 0]
                               ])

        img = cv2.filter2D(img, -1, kernel, delta=128)

        if not self.__select_menu == 0:
            for index in range(height):
                v = img[index:index+1, 0:width][0]
                if self.__select_menu == 1:  # 明
                    v = np.where((v < 128+self.__noise_cut),  0, 255)
                elif self.__select_menu == 2:  # 暗
                    v = np.where((v > 128-self.__noise_cut),  255, 0)
                elif self.__select_menu == 3:  # 明暗
                    v = np.where((v > 128-self.__noise_cut) &
                                 (v < 128+self.__noise_cut),  int(255/2), 255)
                img[index:index+1, 0:width][0] = v

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        return img

    def get_data(self):
        param = []
        param.append(self.__k)
        param.append(self.__noise_cut)
        param.append(self.__select_menu)
        param.append(self.direction_mode)
        if self.__gui:
            print('Proc : Laplacian_Custom')
            print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/edge2.png')
    param = []
    param = [4, 5, 0.9, 105, 2]
    app = Laplacian_Custom(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Laplacian_Custom.jpg', dst_img)
