import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class WhiteBalance(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__gui = gui

        if len(param) == 1:
            pass
        else:
            pass

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__white_balance()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()
        pass

    def __init_events(self):
        pass

    def __onScale(self):
        pass

    def __white_balance(self):
        img_copy = self.origin_img.copy()
        image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2LAB)
        avg_a = np.average(image[:, :, 1])
        avg_b = np.average(image[:, :, 2])
        image[:, :, 1] = image[:, :, 1] - (
            (avg_a - 128) * (image[:, :, 0] / 255.0) * 1.1
        )
        image[:, :, 2] = image[:, :, 2] - (
            (avg_b - 128) * (image[:, :, 0] / 255.0) * 1.1
        )
        img = cv2.cvtColor(image, cv2.COLOR_LAB2BGR)
        return img

    def get_data(self):
        param = []
        if self.__gui:
            print('Proc : WhiteBalance')
            print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/202103100903164c4.jpg')
    param = []
    app = WhiteBalance(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./WhiteBalance.jpg', dst_img)
