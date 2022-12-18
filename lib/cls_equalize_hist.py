import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class EqualizeHist(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__h_flag = True
        self.__s_flag = True
        self.__v_flag = True
        self.__gui = gui

        if len(param) == 3:
            self.__h_flag = param[0]
            self.__s_flag = param[1]
            self.__v_flag = param[2]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__equalize_hist()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__h_bool = tk.BooleanVar()
        self.__s_bool = tk.BooleanVar()
        self.__v_bool = tk.BooleanVar()

        self.__h_bool.set(self.__h_flag)
        self.__s_bool.set(self.__s_flag)
        self.__v_bool.set(self.__v_flag)

        self.checkbutton1 = tk.Checkbutton(
            self.settings_frame, variable=self.__h_bool, command=self.__onClick)
        self.checkbutton1.configure(text="H",)
        self.checkbutton1.pack(side="top")
        self.checkbutton2 = tk.Checkbutton(
            self.settings_frame, variable=self.__s_bool, command=self.__onClick)
        self.checkbutton2.configure(text="S")
        self.checkbutton2.pack(side="top")
        self.checkbutton3 = tk.Checkbutton(
            self.settings_frame, variable=self.__v_bool, command=self.__onClick)
        self.checkbutton3.configure(text="V")
        self.checkbutton3.pack(side="top")

    def __init_events(self):
        pass

    def __onClick(self):
        self.__h_flag = self.__h_bool.get()
        self.__s_flag = self.__s_bool.get()
        self.__v_flag = self.__v_bool.get()

        self.dst_img = self.__equalize_hist()
        self.Draw()
        pass

    def __onScale(self, events):
        pass

    def __equalize_hist(self):
        img_copy = self.origin_img.copy()

        cl = 1
        gsize = 1
        h1, s1, v1 = cv2.split(cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV))
        clahe = cv2.createCLAHE(clipLimit=cl, tileGridSize=(gsize, gsize))

        if self.__h_flag:
            h1 = clahe.apply(h1)
        if self.__s_flag:
            s1 = clahe.apply(s1)
        if self.__v_flag:
            v1 = clahe.apply(v1)

        img = cv2.cvtColor(cv2.merge((h1, s1, v1)), cv2.COLOR_HSV2BGR)

        return img

    def get_data(self):
        param = []
        param.append(self.__h_flag)
        param.append(self.__s_flag)
        param.append(self.__v_flag)
        if self.__gui:
            print('Proc : EqualizeHist')
            print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/I.jpg')
    # param = []
    param = [False, False, True]
    app = EqualizeHist(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./EqualizeHist.jpg', dst_img)
