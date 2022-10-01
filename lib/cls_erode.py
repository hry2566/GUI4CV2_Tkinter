import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class Erode(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False

        if len(param) == 2:
            self.__kernel_x = param[0]
            self.__kernel_y = param[1]
        else:
            self.__kernel_x = 1
            self.__kernel_y = 1

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__erode()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=1, to=50,
                                label="kernel x", orient="horizontal", command=self.__onScale)
        self.__scale1.pack(side="top")

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=1, to=50,
                                label="kernel y", orient="horizontal", command=self.__onScale)
        self.__scale2.pack(side="top")

        self.__scale1.set(self.__kernel_x)
        self.__scale2.set(self.__kernel_y)
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
        self.dst_img = self.__erode()
        self.Draw()
        self.__proc_flag = False
        pass

    def __erode(self):
        img_copy = self.origin_img.copy()

        kernel = np.ones((self.__kernel_x, self.__kernel_y), np.uint8)
        img = cv2.erode(img_copy, kernel, iterations=1)
        return img

    def get_data(self):
        param = []
        param.append(self.__kernel_x)
        param.append(self.__kernel_y)
        print('Proc : Enode')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [3, 3]
    app = Erode(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./erode.jpg', dst_img)
