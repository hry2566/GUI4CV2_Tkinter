import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class Gamma(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__gamma = 1
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 1:
            self.__gamma = param[0]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()
            self.run()
        else:
            self.dst_img = self.__gamma_correction()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale = Parts_Scale(self.settings_frame)
        self.__scale.configure(label='gamma', side='top',
                               resolution=0.1, from_=0, to=2)
        self.__scale.set(self.__gamma)
        pass

    def __init_events(self):
        self.__scale.bind(changed=self.__onScale)
        pass

    def __onScale(self):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__gamma = self.__scale.get()
        self.dst_img = self.__gamma_correction()
        self.Draw()
        self.__proc_flag = False
        pass

    def __gamma_correction(self):
        img_copy = self.origin_img.copy()
        table = (np.arange(256) / 255) ** self.__gamma * 255
        table = np.clip(table, 0, 255).astype(np.uint8)
        img = cv2.LUT(img_copy, table)
        return img

    def get_data(self):
        param = []
        param.append(self.__gamma)
        if self.__gui:
            print('Proc : Gamma')
            print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/I.jpg')
    # img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [0.5]
    app = Gamma(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Gamma.jpg', dst_img)
