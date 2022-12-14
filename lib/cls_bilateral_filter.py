"""ぼかし(BilateralFilter)"""
import tkinter as tk

import cv2

from lib.gui.cls_edit_window import EditWindow


class BilateralFilter(EditWindow):
    """ぼかし(BilateralFilter)クラス"""

    def __init__(self, img, param, master=None, gui=False):
        self.origin_img = img
        self.__d = 0
        self.__sigma_color = 0
        self.__sigma_space = 0
        self.__proc_flag = False
        self.__gui = gui

        if len(param) == 3:
            self.__d = param[0]
            self.__sigma_color = param[1]
            self.__sigma_space = param[2]

        if gui:
            super().__init__(img, master)
            self.__init_gui()
            self.__init_events()
            self.run()
        else:
            self.dst_img = self.__bilateral_filter()

    def __init_gui(self):
        self.none_label.destroy()

        self.__scale1 = tk.Scale(self.settings_frame)
        self.__scale1.configure(from_=-128, to=128,
                                label="d", orient="horizontal", command=self.__on_scale)
        self.__scale1.pack(side="top")
        self.__scale2 = tk.Scale(self.settings_frame)
        self.__scale2.configure(from_=0, to=50,
                                label="sigma_color", orient="horizontal", command=self.__on_scale)
        self.__scale2.pack(side="top")
        self.__scale3 = tk.Scale(self.settings_frame)
        self.__scale3.configure(from_=0, to=50,
                                label="sigma_space", orient="horizontal", command=self.__on_scale)
        self.__scale3.pack(side="top")

        self.__scale1.set(self.__d)
        self.__scale2.set(self.__sigma_color)
        self.__scale3.set(self.__sigma_space)

    def __init_events(self):
        pass

    def __on_scale(self, events):
        if self.__proc_flag:
            return
        self.__proc_flag = True
        self.__d = self.__scale1.get()
        self.__sigma_color = self.__scale2.get()
        self.__sigma_space = self.__scale3.get()
        self.dst_img = self.__bilateral_filter()
        self.draw()
        self.__proc_flag = False

    def __bilateral_filter(self):
        img_copy = self.origin_img.copy()

        img = cv2.bilateralFilter(img_copy,
                                  d=self.__d,
                                  sigmaColor=self.__sigma_color,
                                  sigmaSpace=self.__sigma_space)
        return img

    def dummy(self):
        """パブリックダミー関数"""

    def get_data(self):
        """パラメータ取得"""
        param = []
        param.append(self.__d)
        param.append(self.__sigma_color)
        param.append(self.__sigma_space)
        if self.__gui:
            print('Proc : BilateralFilter')
            print(f'param = {param}')
        return param, self.dst_img


# if __name__ == "__main__":
#     # img = cv2.imread('./0000_img/opencv_logo.jpg')
#     img = cv2.imread('./0000_img/I.jpg')
#     param = []
#     param = [60, 30, 30]
#     app = BilateralFilter(img, param, gui=True)
#     param, dst_img = app.get_data()
#     cv2.imwrite('./BilateralFilter.jpg', dst_img)
