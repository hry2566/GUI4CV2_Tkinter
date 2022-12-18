import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class ReverseBrightness(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__gui=gui

        if gui:
            super().__init__(img, master)

        if len(param) == 1:
            pass
        else:
            pass

        if gui:
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__reverse_brightness()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()
        pass

    def __init_events(self):
        pass

    def __onClick(self, event):
        self.Draw()
        pass

    def __onScale(self, events):
        pass

    def __reverse_brightness(self):
        img_copy = self.origin_img.copy()
        h1, s1, v1 = cv2.split(cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV))
        v1 = 255 - v1
        img = cv2.cvtColor(cv2.merge((h1, s1, v1)), cv2.COLOR_HSV2BGR)

        return img

    def get_data(self):
        param = []
        if self.__gui:
            print('Proc : ReverseBrightness')
            print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/test.jpg')
    param = [False, False, True]
    app = ReverseBrightness(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./ReverseBrightness.jpg', dst_img)
