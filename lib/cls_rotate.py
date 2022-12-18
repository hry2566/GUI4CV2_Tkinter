import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class Rotate(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__ang = 0
        self.__scale = 1.0
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 2:
            self.__ang = param[0]
            self.__scale = param[1]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__rotate()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = Parts_Scale(self.settings_frame)
        self.__scale1.configure(label='angle', side='top', from_=0, to=359)
        self.__scale2 = Parts_Scale(self.settings_frame)
        self.__scale2.configure(label='scale', side='top',
                                resolution=0.1, from_=0.1, to=2.0)

        self.__scale1.set(self.__ang)
        self.__scale2.set(self.__scale)

    def __init_events(self):
        self.__scale1.bind(changed=self.__onScale)
        self.__scale2.bind(changed=self.__onScale)

    def __onScale(self):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__ang = self.__scale1.get()
        self.__scale = self.__scale2.get()
        self.dst_img = self.__rotate()
        self.Draw()
        self.__proc_flag = False
        pass

    def __rotate(self):
        img_copy = self.origin_img.copy()

        # 高さを定義
        height = img_copy.shape[0]
        # 幅を定義
        width = img_copy.shape[1]
        # 回転の中心を指定
        center = (int(width/2), int(height/2))
        # getRotationMatrix2D関数を使用
        trans = cv2.getRotationMatrix2D(center, self.__ang, self.__scale)
        # アフィン変換
        img = cv2.warpAffine(img_copy, trans, (width, height))

        return img

    def get_data(self):
        param = []
        param.append(self.__ang)
        param.append(self.__scale)
        if self.__gui:
            print('Proc : Rotate')
            print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [90, 1]
    app = Rotate(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./rotate.jpg', dst_img)
