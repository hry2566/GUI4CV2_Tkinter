import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow, even2odd


class Shading_Color_MedianBlur(EditWindow):
    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__kernel = 1
        self.__noise_cut = 0
        self.__select_menu = 0
        self.__proc_flag = False

        if len(param) == 3:
            self.__kernel = param[0]
            self.__noise_cut = param[1]
            self.__select_menu = param[2]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()
            self.run()
        else:
            self.dst_img = self.__shading_color_median_blur()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=1, to=100,
                                label='kernel x', orient='horizontal', command=self.__onScale)
        self.__scale1.pack(side='top')

        self.__scale3 = tk.Scale(self.settings_frame)
        self.__scale3.configure(from_=0, to=128,
                                label='remove noise', orient='horizontal', command=self.__onScale)
        self.__scale3.pack(side='top')

        self.__tkvar = tk.StringVar(value=None)
        __values = ['明', '暗', '明＋暗']
        self.optionmenu1 = tk.OptionMenu(
            self.settings_frame, self.__tkvar, 'None', *__values, command=self.__onSelect)
        self.optionmenu1.pack(side='top', fill='x')

        self.__scale1.set(self.__kernel)
        self.__scale3.set(self.__noise_cut)

        if self.__select_menu == 0:
            self.__tkvar.set(None)
        elif self.__select_menu == 1:
            self.__tkvar.set('明')
        elif self.__select_menu == 2:
            self.__tkvar.set('暗')
        elif self.__select_menu == 3:
            self.__tkvar.set('明＋暗')

    def __init_events(self):
        pass

    def __onScale(self, events):
        if self.__proc_flag:
            return
        else:
            self.__proc_flag = True

        self.__kernel = self.__scale1.get()
        self.__noise_cut = self.__scale3.get()
        self.dst_img = self.__shading_color_median_blur()
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

        self.dst_img = self.__shading_color_median_blur()
        self.Draw()

    def __shading_color_median_blur(self):
        img_copy = self.origin_img.copy()

        image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2HSV)
        h1, s1, v1 = cv2.split(image)
        height, width = image.shape[:2]

        kernel = even2odd(self.__kernel)
        blur = cv2.medianBlur(v1, ksize=kernel)
        v2 = v1/blur
        v2 = np.clip(v2*128, 0, 255).astype(np.uint8)

        if not self.__select_menu == 0:
            for index in range(height):
                v = v2[index:index+1, 0:width][0]
                if self.__select_menu == 1:  # 明
                    v = np.where((v < 128+self.__noise_cut),  0, 255)
                elif self.__select_menu == 2:  # 暗
                    v = np.where((v > 128-self.__noise_cut),  255, 0)
                elif self.__select_menu == 3:  # 明暗
                    v = np.where((v > 128-self.__noise_cut) &
                                 (v < 128+self.__noise_cut),  int(255/2), 255)
                v2[index:index+1, 0:width][0] = v

        img = cv2.cvtColor(cv2.merge((h1, s1, v2)), cv2.COLOR_HSV2BGR)
        return img

    def get_data(self):
        param = []
        param.append(self.__kernel)
        param.append(self.__noise_cut)
        param.append(self.__select_menu)
        print('Proc : Shading_Color_MedianBlur')
        print(f'param = {param}')
        return param, self.dst_img


if __name__ == "__main__":
    img = cv2.imread('./0000_img/shading.png')
    # img = cv2.imread('./0000_img/10.png')
    param = []
    param = [18, 38, 2]
    app = Shading_Color_MedianBlur(img, param, gui=True)
    param, dst_img = app.get_data()
    cv2.imwrite('./Shading_MedianBlur.jpg', dst_img)