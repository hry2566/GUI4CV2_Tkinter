import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class EqualizeHist(EditWindow):
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

        self.dst_img = self.__equalize_hist()

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

    def __equalize_hist(self):
        img_copy = self.origin_img.copy()
        # b1, g1, r1 = cv2.split(img_copy)
        # b2 = cv2.equalizeHist(b1)
        # g2 = cv2.equalizeHist(g1)
        # r2 = cv2.equalizeHist(r1)
        # img = cv2.merge((b2, g2, r2))

        # h1, s1, v1 = cv2.split(cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV))
        # v2 = cv2.equalizeHist(v1)
        # img = cv2.cvtColor(cv2.merge((h1, s1, v2)), cv2.COLOR_HSV2BGR)

        cl = 1
        gsize = 1
        b1, g1, r1 = cv2.split(img_copy)
        clahe = cv2.createCLAHE(clipLimit=cl, tileGridSize=(gsize, gsize))
        b2 = clahe.apply(b1)
        g2 = clahe.apply(g1)
        r2 = clahe.apply(r1)
        img = cv2.merge((b2, g2, r2))

        # cl = 1
        # gsize = 1
        # h1, s1, v1 = cv2.split(cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV))
        # clahe = cv2.createCLAHE(clipLimit=cl, tileGridSize=(gsize, gsize))
        # h2 = clahe.apply(h1)
        # s2 = clahe.apply(s1)
        # v2 = clahe.apply(v1)
        # img = cv2.cvtColor(cv2.merge((h2, s2, v2)), cv2.COLOR_HSV2BGR)

        return img

    def get_data(self):
        param = []
        print('Proc : WhiteBalance')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/202103100903164c4.jpg')
    param = []
    app = EqualizeHist(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./EqualizeHist.jpg', dst_img)
