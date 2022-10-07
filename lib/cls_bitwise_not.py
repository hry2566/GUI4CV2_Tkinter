import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class Bitwise_Not(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        # self.__proc_flag = False

        if len(param) == 1:
            pass
        else:
            pass

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__bitwise_not()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
        pass

    def __bitwise_not(self):
        img_copy = self.origin_img.copy()
        img = cv2.bitwise_not(img_copy)
        return img

    def get_data(self):
        param = []
        print('Proc : WhiteBalance')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/202103100903164c4.jpg')
    param = []
    app = Bitwise_Not(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Bitwise_Not.jpg', dst_img)
