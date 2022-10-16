import os
import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class CustomFillter(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False

        if len(param) == 4:
            self.__kernel_x = param[0]
            self.__kernel_y = param[1]
            self.__k = param[2]
            self.__noise_cut = param[3]
        else:
            self.__kernel_x = 2
            self.__kernel_y = 2
            self.__k = 1
            self.__noise_cut = 0

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__custom_fillter()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=2, to=10,
                                label="kernel x", orient="horizontal", command=self.__onScale)
        self.__scale1.pack(side="top")

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=2, to=10,
                                label="kernel y", orient="horizontal", command=self.__onScale)
        self.__scale2.pack(side="top")

        self.__scale3 = tk.Scale(self.settings_frame)
        self.__scale3.configure(from_=0.1, to=2,
                                label="k", orient="horizontal", resolution=0.1, command=self.__onScale)
        self.__scale3.pack(side="top")

        self.__scale4 = tk.Scale(self.settings_frame)
        self.__scale4.configure(from_=0, to=255,
                                label='remove noise', orient='horizontal', command=self.__onScale)
        self.__scale4.pack(side='top')

        self.__scale1.set(self.__kernel_x)
        self.__scale2.set(self.__kernel_y)
        self.__scale3.set(self.__k)
        self.__scale4.set(self.__noise_cut)
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__kernel_x = self.__scale1.get()
        self.__kernel_y = self.__scale2.get()
        self.__k = self.__scale3.get()
        self.__noise_cut = self.__scale4.get()
        self.dst_img = self.__custom_fillter()
        self.Draw()
        self.__proc_flag = False
        pass

    def __custom_fillter(self):
        img_copy = self.origin_img.copy()
        img = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        height, width = img.shape[:2]
        kernel_x = self.__kernel_x
        kernel_y = self.__kernel_y

        if kernel_x % 2 == 0:
            posx1 = int(kernel_x/2-1)
            posx2 = int(kernel_x/2+1)-1
        else:
            posx1 = int(kernel_x/2)+1-1
            posx2 = posx1
        if kernel_y % 2 == 0:
            posy1 = int(kernel_y/2-1)
            posy2 = int(kernel_y/2+1)-1
        else:
            posy1 = int(kernel_y/2)+1-1
            posy2 = posy1

        kernel = np.zeros((kernel_y, kernel_x))
        kernel[0][posx1] = -self.__k
        kernel[-1][posx2] = self.__k
        kernel[posy1][0] = -self.__k
        kernel[posy2][-1] = self.__k

        img = cv2.filter2D(img, -1, kernel, delta=128)

        if self.__noise_cut > 0:
            for index in range(height):
                y1 = img[index:index+1, 0:width][0]
                y1 = np.where(y1 < self.__noise_cut, 255, int(255/2))
                img[index:index+1, 0:width][0] = y1

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)

        return img

    def get_data(self):
        param = []
        param.append(self.__kernel_x)
        param.append(self.__kernel_y)
        param.append(self.__k)
        param.append(self.__noise_cut)
        print('Proc : CustomFillter')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    # img = cv2.imread('./0000_img/opencv_logo.jpg')
    img = cv2.imread('./0000_img/2.png')
    # img = cv2.imread('./0000_img/test.jpg')
    # img = cv2.imread('./0000_img/1.png')
    param = []
    param = [10, 2, 0.9, 29]
    app = CustomFillter(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./CustomFillter.jpg', dst_img)
