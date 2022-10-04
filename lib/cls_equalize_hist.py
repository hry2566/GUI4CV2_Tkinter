import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class EqualizeHist(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        # self.__proc_flag = False

        if gui:
            super().__init__(img, master)
            self.__h_bool = tk.BooleanVar()
            self.__s_bool = tk.BooleanVar()
            self.__v_bool = tk.BooleanVar()

        if len(param) == 3:
            self.__h_bool.set(param[0])
            self.__s_bool.set(param[1])
            self.__v_bool.set(param[2])
            pass
        else:
            self.__h_bool.set(True)
            self.__s_bool.set(True)
            self.__v_bool.set(True)
            pass

        if gui:
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__equalize_hist()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.checkbutton1 = tk.Checkbutton(
            self.settings_frame, variable=self.__h_bool)
        self.checkbutton1.configure(text="H",)
        self.checkbutton1.pack(side="top")
        self.checkbutton2 = tk.Checkbutton(
            self.settings_frame, variable=self.__s_bool)
        self.checkbutton2.configure(text="S")
        self.checkbutton2.pack(side="top")
        self.checkbutton3 = tk.Checkbutton(
            self.settings_frame, variable=self.__v_bool)
        self.checkbutton3.configure(text="V")
        self.checkbutton3.pack(side="top")

        self.checkbutton1.update()
        pass

    def __init_events(self):
        self.checkbutton1.bind('<ButtonRelease>', self.__onClick)
        self.checkbutton2.bind('<ButtonRelease>', self.__onClick)
        self.checkbutton3.bind('<ButtonRelease>', self.__onClick)
        pass

    def __onClick(self, event):
        self.dst_img = self.__equalize_hist()
        self.Draw()
        pass

    def __onScale(self, events):
        pass

    def __equalize_hist(self):
        img_copy = self.origin_img.copy()
        # b1, g1, r1 = cv2.split(img_copy)
        # b2 = cv2.equalizeHist(b1)
        # g2 = cv2.equalizeHist(g1)
        # r2 = cv2.equalizeHist(r1)
        # img = cv2.merge((b2, g2, r2))

        # h1, s1, v1 = cv2.split(cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV))
        # # h2 = cv2.equalizeHist(h1)
        # # s2 = cv2.equalizeHist(s1)
        # v2 = cv2.equalizeHist(v1)
        # img = cv2.cvtColor(cv2.merge((h1, s1, v2)), cv2.COLOR_HSV2BGR)

        # cl = 1
        # gsize = 1
        # b1, g1, r1 = cv2.split(img_copy)
        # clahe = cv2.createCLAHE(clipLimit=cl, tileGridSize=(gsize, gsize))
        # b2 = clahe.apply(b1)
        # g2 = clahe.apply(g1)
        # r2 = clahe.apply(r1)
        # img = cv2.merge((b2, g2, r2))

        cl = 1
        gsize = 1
        h1, s1, v1 = cv2.split(cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV))
        clahe = cv2.createCLAHE(clipLimit=cl, tileGridSize=(gsize, gsize))

        if self.__h_bool.get():
            h1 = clahe.apply(h1)
        if self.__s_bool.get():
            s1 = clahe.apply(s1)
        if self.__v_bool.get():
            v1 = clahe.apply(v1)

        img = cv2.cvtColor(cv2.merge((h1, s1, v1)), cv2.COLOR_HSV2BGR)

        return img

    def get_data(self):
        param = []
        param.append(self.__h_bool.get())
        param.append(self.__s_bool.get())
        param.append(self.__v_bool.get())
        print('Proc : WhiteBalance')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/test.jpg')
    param = [False, False, True]
    app = EqualizeHist(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./EqualizeHist.jpg', dst_img)
