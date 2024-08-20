"""濃淡補正(ShadingMedianBlur)"""
import tkinter as tk

import cv2
import numpy as np

from lib.gui.cls_edit_window import EditWindow, even2odd
from lib.parts.parts_scale import Parts_Scale


class ShadingMedianBlur(EditWindow):
    """濃淡補正(ShadingMedianBlur)クラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__kernel = 1
        self.__noise_cut = 0
        self.__select_menu = 0
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 3:
            self.__kernel = param[0]
            self.__noise_cut = param[1]
            self.__select_menu = param[2]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()

        self.dst_img = self.__shading_median_blur()

        if gui:
            self.draw()
            self.run()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = Parts_Scale(self.settings_frame)
        self.__scale1.configure(label='kernel_x', side='top', from_=1, to=100)
        self.__scale2 = Parts_Scale(self.settings_frame)
        self.__scale2.configure(label='remove noise',
                                side='top', from_=0, to=128)
        self.__tkvar = tk.StringVar(value=None)
        __values = ['明', '暗', '明＋暗']
        self.optionmenu1 = tk.OptionMenu(
            self.settings_frame, self.__tkvar, 'None', *__values, command=self.__on_select)
        self.optionmenu1.pack(side='top', fill='x')

        self.__scale1.set(self.__kernel)
        self.__scale2.set(self.__noise_cut)

        if self.__select_menu == 0:
            self.__tkvar.set(None)
        elif self.__select_menu == 1:
            self.__tkvar.set('明')
        elif self.__select_menu == 2:
            self.__tkvar.set('暗')
        elif self.__select_menu == 3:
            self.__tkvar.set('明＋暗')

    def __init_events(self):
        self.__scale1.bind(changed=self.__on_scale)
        self.__scale2.bind(changed=self.__on_scale)

    def __on_scale(self):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.__kernel = self.__scale1.get()
        self.__noise_cut = self.__scale2.get()
        self.dst_img = self.__shading_median_blur()
        self.draw()
        self.__proc_flag = False

    def __on_select(self, event):
        if self.__tkvar.get() == 'None':
            self.__select_menu = 0
        elif self.__tkvar.get() == '明':
            self.__select_menu = 1
        elif self.__tkvar.get() == '暗':
            self.__select_menu = 2
        elif self.__tkvar.get() == '明＋暗':
            self.__select_menu = 3

        self.dst_img = self.__shading_median_blur()
        self.draw()

    def __shading_median_blur(self):
        img_copy = self.origin_img.copy()
        image = cv2.cvtColor(img_copy, cv2.COLOR_BGR2GRAY)
        height, width = image.shape[:2]

        kernel = even2odd(self.__kernel)
        blur = cv2.medianBlur(image, ksize=kernel)
        img = image / blur
        img = np.clip(img * 128, 0, 255).astype(np.uint8)

        if not self.__select_menu == 0:
            for index in range(height):
                val = img[index:index + 1, 0:width][0]
                if self.__select_menu == 1:  # 明
                    val = np.where((val < 128 + self.__noise_cut), 0, 255)
                elif self.__select_menu == 2:  # 暗
                    val = np.where((val > 128 - self.__noise_cut), 255, 0)
                elif self.__select_menu == 3:  # 明暗
                    val = np.where((val > 128 - self.__noise_cut) &
                                   (val < 128 + self.__noise_cut), int(255 / 2), 255)
                img[index:index + 1, 0:width][0] = val

        img = cv2.cvtColor(img, cv2.COLOR_GRAY2BGR)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__kernel)
        param.append(self.__noise_cut)
        param.append(self.__select_menu)
        if self.__gui:
            print('Proc : Shading_MedianBlur')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     img = cv2.imread('./0000_img/shading.png')
#     # img = cv2.imread('./0000_img/10.png')
#     param = []
#     param = [18, 38, 2]
#     app = ShadingMedianBlur(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./Shading_MedianBlur.jpg', dst_img)
