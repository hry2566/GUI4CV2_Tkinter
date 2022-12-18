import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow
from lib.parts.parts_scale import Parts_Scale


class Shading_Approximate(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__kernel_x = 15
        self.__kernel_y = 15
        self.__noise_cut = 0
        self.__select_menu = 0
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 4:
            self.__kernel_x = param[0]
            self.__kernel_y = param[1]
            self.__noise_cut = param[2]
            self.__select_menu = param[3]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__shading_approximate()

        if gui:
            self.Draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = Parts_Scale(self.settings_frame)
        self.__scale1.configure(label='kernel_x', side='top', from_=0, to=15)

        self.__scale2 = Parts_Scale(self.settings_frame)
        self.__scale2.configure(label='kernel_y', side='top', from_=0, to=15)

        self.__scale3 = Parts_Scale(self.settings_frame)
        self.__scale3.configure(label='remove noise',
                                side='top', from_=0, to=128)

        # self.__scale1 = tk.Scale(self.settings_frame)
        # self.__scale1.configure(from_=0, to=15,
        #                         label='kernel x', orient='horizontal', command=self.__onScale)
        # self.__scale1.pack(side='top')

        # self.__scale2 = tk.Scale(self.settings_frame)
        # self.__scale2.configure(from_=0, to=15,
        #                         label='kernel y', orient='horizontal', command=self.__onScale)
        # self.__scale2.pack(side='top')

        # self.__scale3 = tk.Scale(self.settings_frame)
        # self.__scale3.configure(from_=0, to=128,
        #                         label='remove noise', orient='horizontal', command=self.__onScale)
        # self.__scale3.pack(side='top')

        self.__tkvar = tk.StringVar(value=None)
        __values = ['明', '暗', '明＋暗']
        self.optionmenu1 = tk.OptionMenu(
            self.settings_frame, self.__tkvar, 'None', *__values, command=self.__onSelect)
        self.optionmenu1.pack(side='top', fill='x')

        self.__scale1.set(self.__kernel_x)
        self.__scale2.set(self.__kernel_y)
        self.__scale3.set(self.__noise_cut)

        if self.__select_menu == 0:
            self.__tkvar.set(None)
        elif self.__select_menu == 1:
            self.__tkvar.set('明')
        elif self.__select_menu == 2:
            self.__tkvar.set('暗')
        elif self.__select_menu == 3:
            self.__tkvar.set('明＋暗')
        pass

    def __init_events(self):
        self.__scale1.bind(changed=self.__onScale)
        self.__scale2.bind(changed=self.__onScale)
        self.__scale3.bind(changed=self.__onScale)

    def __onScale(self):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__kernel_x = self.__scale1.get()
        self.__kernel_y = self.__scale2.get()
        self.__noise_cut = self.__scale3.get()
        self.dst_img = self.__shading_approximate()
        self.Draw()
        self.__proc_flag = False

    def __onSelect(self, event):

        if self.__tkvar.get() == 'None':
            self.__select_menu = 0
        elif self.__tkvar.get() == '明':
            self.__select_menu = 1
        elif self.__tkvar.get() == '暗':
            self.__select_menu = 2
        elif self.__tkvar.get() == '明＋暗':
            self.__select_menu = 3

        self.dst_img = self.__shading_approximate()
        self.Draw()

    def __shading_approximate(self):
        img_copy = self.origin_img.copy()
        img = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        height, width = img.shape[:2]
        x1 = np.arange(width)
        x2 = np.arange(height)

        for index in range(height):
            y1 = img[index:index+1, 0:width][0]
            res = np.polyfit(x1, y1, self.__kernel_x)
            y2 = np.poly1d(res)(x1)
            dev = np.round(y1-y2)
            img[index:index+1, 0:width][0] = dev+int(255/2)

        for index in range(width):
            y1 = img[0:height, index:index+1].T[0]
            res = np.polyfit(x2, y1, self.__kernel_y)
            y2 = np.poly1d(res)(x2)
            dev = np.round(y1-y2)
            img[0:height, index:index+1].T[0] = dev+int(255/2)

        if not self.__select_menu == 0:
            for index in range(height):
                v = img[index:index+1, 0:width][0]
                if self.__select_menu == 1:  # 明
                    v = np.where((v < 128+self.__noise_cut),  0, 255)
                elif self.__select_menu == 2:  # 暗
                    v = np.where((v > 128-self.__noise_cut),  255, 0)
                elif self.__select_menu == 3:  # 明暗
                    v = np.where((v > 128-self.__noise_cut) &
                                 (v < 128+self.__noise_cut),  int(255/2), 255)
                img[index:index+1, 0:width][0] = v

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img

    def get_data(self):
        param = []
        param.append(self.__kernel_x)
        param.append(self.__kernel_y)
        param.append(self.__noise_cut)
        param.append(self.__select_menu)
        if self.__gui:
            print('Proc : Shading_Approximate')
            print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/shading.png')
    # img = cv2.imread('./0000_img/I.jpg')
    # img = cv2.imread('./0000_img/10.png')
    param = []
    param = [11, 15, 60, 2]
    app = Shading_Approximate(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Shading_Approximate.jpg', dst_img)
