import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class Trim(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False

        if len(param) == 4:
            self.__x1 = param[0]
            self.__y1 = param[1]
            self.__x2 = param[2]
            self.__y2 = param[3]
        else:
            self.__x1 = 0
            self.__y1 = 0
            self.__x2 = self.origin_img.shape[1]
            self.__y2 = self.origin_img.shape[0]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__trim()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=0, to=self.origin_img.shape[1],
                                label="x1", orient="horizontal", command=self.__onScale)
        self.__scale1.pack(side="top")

        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=0, to=self.origin_img.shape[0],
                                label="y1", orient="horizontal", command=self.__onScale)
        self.__scale2.pack(side="top")

        self.__scale3 = tk.Scale(self.settings_frame)
        self.__scale3.configure(from_=0, to=self.origin_img.shape[1],
                                label="x2", orient="horizontal", command=self.__onScale)
        self.__scale3.pack(side="top")

        self.__scale4 = tk.Scale(self.settings_frame)
        self.__scale4.configure(from_=0, to=self.origin_img.shape[0],
                                label="y2", orient="horizontal", command=self.__onScale)
        self.__scale4.pack(side="top")

        self.__scale1.set(self.__x1)
        self.__scale2.set(self.__y1)
        self.__scale3.set(self.__x2)
        self.__scale4.set(self.__y2)
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__x1 = self.__scale1.get()
        self.__y1 = self.__scale2.get()
        self.__x2 = self.__scale3.get()
        self.__y2 = self.__scale4.get()

        self.__scale3.configure(from_=self.__scale1.get()+2)
        self.__scale4.configure(from_=self.__scale2.get()+2)
        self.__scale1.configure(to=self.__scale3.get()-2)
        self.__scale2.configure(to=self.__scale4.get()-2)

        self.dst_img = self.__trim()
        self.Draw()
        self.__proc_flag = False
        pass

    def __trim(self):
        img_copy = self.origin_img.copy()
        img = img_copy[self.__y1: self.__y2, self.__x1: self.__x2]
        return img

    def get_data(self):
        param = []
        param.append(self.__x1)
        param.append(self.__y1)
        param.append(self.__x2)
        param.append(self.__y2)
        print('Proc : Trim')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    # param = [0, 0, 0, 0]
    app = Trim(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Trim.jpg', dst_img)
