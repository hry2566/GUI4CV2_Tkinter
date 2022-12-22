"""モルフォロジー"""
import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class Morphology(EditWindow):
    """モルフォロジークラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__type_index = 0
        self.__kernel_x = 1
        self.__kernel_y = 1
        self.__proc_flag = False
        self.__type_list = [cv2.MORPH_OPEN,
                            cv2.MORPH_CLOSE,
                            cv2.MORPH_GRADIENT]
        self.__values = ['OPEN', 'CLOSE', 'GRADIENT']
        self.__gui = gui

        if len(param) == 3:
            self.__type_index = param[0]
            self.__kernel_x = param[1]
            self.__kernel_y = param[2]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__morphology()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__tkvar = tk.StringVar(value='OPEN')
        self.__values = ['OPEN', 'CLOSE', 'GRADIENT']
        self.__optionmenu2 = tk.OptionMenu(
            self.settings_frame, self.__tkvar, *self.__values, command=self.__on_select)
        self.__optionmenu2.pack(fill='x', side='top')

        self.__scale1 = Parts_Scale(self.settings_frame)
        self.__scale1.configure(label='kernel_x', side='top', from_=1, to=30)
        self.__scale2 = Parts_Scale(self.settings_frame)
        self.__scale2.configure(label='kernel_y', side='top', from_=1, to=30)

        self.__tkvar.set(self.__values[self.__type_index])
        self.__scale1.set(self.__kernel_x)
        self.__scale2.set(self.__kernel_y)

    def __init_events(self):
        self.__scale1.bind(changed=self.__on_scale)
        self.__scale2.bind(changed=self.__on_scale)

    def __on_select(self, event):
        if self.__proc_flag:
            return
        self.__proc_flag = True

        if self.__tkvar.get() == 'OPEN':
            self.__type_index = 0
        elif self.__tkvar.get() == 'CLOSE':
            self.__type_index = 1
        elif self.__tkvar.get() == 'GRADIENT':
            self.__type_index = 2

        self.dst_img = self.__morphology()
        self.draw()
        self.__proc_flag = False

    def __on_scale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.__kernel_x = self.__scale1.get()
        self.__kernel_y = self.__scale2.get()
        self.dst_img = self.__morphology()
        self.draw()
        self.__proc_flag = False

    def __morphology(self):
        img_copy = self.origin_img.copy()
        kernel = np.ones((self.__kernel_x, self.__kernel_y), np.uint8)
        self.type = self.__type_list[self.__type_index]
        img = cv2.morphologyEx(img_copy, self.type, kernel)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__type_index)
        param.append(self.__kernel_x)
        param.append(self.__kernel_y)
        if self.__gui:
            print('Proc : Morphology')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/opencv_logo.jpg')
#     param = []
#     param = [2, 4, 4]
#     app = Morphology(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./Morphology.jpg', dst_img)
