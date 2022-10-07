import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class Fillter2D(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False

        if len(param) == 1:
            self.__kernel = param[0]
        else:
            self.__kernel = 0

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__fillter2d()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=0, to=10,
                                label="kernel", orient="horizontal", resolution=0.1, command=self.__onScale)
        self.__scale1.pack(side="top")
        self.__scale1.set(self.__kernel)

        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__kernel = self.__scale1.get()
        self.dst_img = self.__fillter2d()
        self.Draw()
        self.__proc_flag = False
        pass

    def __fillter2d(self):
        img_copy = self.origin_img.copy()

        kernel = np.array([[-self.__kernel, -self.__kernel, -self.__kernel],
                           [-self.__kernel, 1+8*self.__kernel, -self.__kernel],
                           [-self.__kernel, -self.__kernel, -self.__kernel]])
        img = cv2.filter2D(img_copy, ddepth=-1, kernel=kernel)
        return img

    def get_data(self):
        param = []
        param.append(self.__kernel)
        print('Proc : Fillter2D')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    # param = [15]
    app = Fillter2D(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./fillter2d.jpg', dst_img)
