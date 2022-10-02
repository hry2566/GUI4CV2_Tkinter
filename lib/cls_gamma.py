import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow


class Gamma(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False

        if len(param) == 1:
            self.__gamma = param[0]
        else:
            self.__gamma = 1

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__gamma_correction()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale = tk.Scale(self.settings_frame)
        self.__scale.configure(from_=0, to=2,
                               label="gamma", orient="horizontal", resolution=0.1, command=self.__onScale)
        self.__scale.pack(side="top")

        self.__scale.set(self.__gamma)
        pass

    def __init_events(self):
        pass

    def __onScale(self, events):
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
        print('Proc : Gamma')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/test.jpg')
    param = []
    param = [1]
    app = Gamma(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./laplacian.jpg', dst_img)
