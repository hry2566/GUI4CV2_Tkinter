import os
import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow, even2odd


class Median_Blur(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False

        if len(param) == 1:
            self.__kernel = param[0]
        else:
            self.__kernel = 1

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__median_blur()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale = tk.Scale(self.settings_frame)
        self.__scale.configure(from_=1, to=30,
                               label="kernel", orient="horizontal", command=self.__onScale)
        self.__scale.pack(side="top")

        self.__scale.set(self.__kernel)
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__kernel = self.__scale.get()
        self.dst_img = self.__median_blur()
        self.Draw()
        self.__proc_flag = False
        pass

    def __median_blur(self):
        img_copy = self.origin_img.copy()

        self.__kernel = even2odd(self.__kernel)
        img = cv2.medianBlur(img_copy, self.__kernel)
        return img

    def get_data(self):
        param = []
        param.append(self.__kernel)
        print('Proc : Median Blur')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [5]
    app = Median_Blur(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Median_Blur.jpg', dst_img)