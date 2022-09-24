import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow, even2odd


class Morphology(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__proc_flag = False
        self.__type_list = [cv2.MORPH_OPEN,
                            cv2.MORPH_CLOSE,
                            cv2.MORPH_GRADIENT]

        if len(param) == 3:
            self.__type_index = param[0]
            self.__kernel_x = param[1]
            self.__kernel_y = param[2]
        else:
            self.__type_index = 0
            self.__kernel_x = 1
            self.__kernel_y = 1

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__morphology()

        if gui:
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__tkvar = tk.StringVar(value='OPEN')
        __values = ['OPEN', 'CLOSE', 'GRADIENT']
        self.optionmenu2 = tk.OptionMenu(
            self.settings_frame, self.__tkvar, *__values, command=self.__onSelect)
        self.optionmenu2.pack(fill='x', side='top')

        self.scale1 = tk.Scale(self.settings_frame)
        self.scale1.configure(from_=0, to=30,
                              label='kernel_x', orient='horizontal', command=self.__onScale)
        self.scale1.pack(side='top')

        self.scale2 = tk.Scale(self.settings_frame)
        self.scale2.configure(from_=0, to=30,
                              label='kernel_y', orient='horizontal', command=self.__onScale)
        self.scale2.pack(side='top')

        self.scale1.set(self.__kernel_x)
        self.scale2.set(self.__kernel_y)
        pass

    def __init_events(self):
        pass

    def __onSelect(self, event):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        if self.__tkvar.get() == 'OPEN':
            self.__type_index = 0
        elif self.__tkvar.get() == 'CLOSE':
            self.__type_index = 1
        elif self.__tkvar.get() == 'GRADIENT':
            self.__type_index = 2

        self.dst_img = self.__morphology()
        self.Draw()
        self.__proc_flag = False

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__kernel_x = self.scale1.get()
        self.__kernel_y = self.scale2.get()
        self.dst_img = self.__morphology()
        self.Draw()
        self.__proc_flag = False
        pass

    def __morphology(self):
        img_copy = self.origin_img.copy()

        kernel = np.ones((self.__kernel_x, self.__kernel_y), np.uint8)
        # kernel = cv2.getStructuringElement(
        #     cv2.MORPH_RECT, (self.kernel_x, self.kernel_y))
        # kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (self.kernel_x, self.kernel_y))
        # kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (self.kernel_x, self.kernel_y))

        self.type = self.__type_list[self.__type_index]
        img = cv2.morphologyEx(img_copy, self.type, kernel)
        return img

    def get_data(self):
        param = []
        param.append(self.__type_index)
        param.append(self.__kernel_x)
        param.append(self.__kernel_y)
        print('Proc : Morphology')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/opencv_logo.jpg')
    param = []
    param = [0, 1, 1]
    app = Morphology(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Morphology.jpg', dst_img)